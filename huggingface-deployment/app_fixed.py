import torch
import torch.nn as nn
import torch.nn.functional as F
import gradio as gr
from PIL import Image
import numpy as np
import torchvision.models as models
import json

# Model architecture matching trained weights exactly
class DenseLayer(nn.Module):
    def __init__(self, in_channels, growth):
        super().__init__()
        # State dict has direct .0 access, NO 'layers' wrapper
        # trunk_a.0.db.convs.0.0.weight (not .layers.0)
        self.convs = nn.ModuleList([nn.Conv2d(in_channels, growth, 3, 1, 1)])
        self.lrelu = nn.LeakyReLU(0.2, inplace=True)
    
    def forward(self, x):
        return self.lrelu(self.convs[0](x))

class RRDB(nn.Module):
    def __init__(self, nc=64, growth=32):
        super().__init__()
        self.db = nn.Module()
        self.db.convs = nn.ModuleList([
            DenseLayer(nc + i * growth, growth) for i in range(5)
        ])
        self.conv = nn.Conv2d(5 * growth, nc, 1, 1, 0)
        self.lrelu = nn.LeakyReLU(0.2, inplace=True)
    
    def forward(self, x):
        feats = [x]
        for layer in self.db.convs:
            feats.append(layer(torch.cat(feats, 1)))
        res = self.conv(torch.cat(feats[1:], 1))
        return self.lrelu(res * 0.2 + x)

class RFB_Branch(nn.Module):
    def __init__(self, in_c):
        super().__init__()
        inter_c = in_c // 4  # For 64ch: 16, for 512ch: 128
        
        # Branch 1: Simple 1×1 conv
        self.b1 = nn.Sequential(
            nn.Conv2d(in_c, inter_c, 1, 1, 0),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(inter_c, inter_c, 1, 1, 0)  # b1.2
        )
        
        # Branch 2: 1×1 → 1×5 asymmetric conv (state dict shows [16,16,1,5])
        self.b2 = nn.Sequential(
            nn.Conv2d(in_c, inter_c, 1, 1, 0),  # b2.0
            nn.LeakyReLU(0.2, inplace=True),     # b2.1
            nn.Conv2d(inter_c, inter_c, (1, 5), 1, (0, 2)),  # b2.2
            nn.LeakyReLU(0.2, inplace=True),     # b2.3
            nn.Conv2d(inter_c, inter_c, 1, 1, 0)  # b2.4
        )
        
        # Branch 3: 1×1 → 1×7 asymmetric conv (state dict shows [16,16,1,7])
        self.b3 = nn.Sequential(
            nn.Conv2d(in_c, inter_c, 1, 1, 0),  # b3.0
            nn.LeakyReLU(0.2, inplace=True),     # b3.1
            nn.Conv2d(inter_c, inter_c, (1, 7), 1, (0, 3)),  # b3.2
            nn.LeakyReLU(0.2, inplace=True),     # b3.3
            nn.Conv2d(inter_c, inter_c, 1, 1, 0)  # b3.4
        )
        
        # Branch 4: 1×1 → 3×3 → 3×3 conv
        self.b4 = nn.Sequential(
            nn.Conv2d(in_c, inter_c, 1, 1, 0),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(inter_c, inter_c, 3, 1, 1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(inter_c, inter_c, 3, 1, 1)
        )
        
        # Channel fusion (4 branches × inter_c = in_c)
        self.cl = nn.Conv2d(in_c, in_c, 1, 1, 0)
        
        # Shortcut
        self.sc = nn.Conv2d(in_c, in_c, 1, 1, 0)
    
    def forward(self, x):
        b1 = self.b1(x)
        b2 = self.b2(x)
        b3 = self.b3(x)
        b4 = self.b4(x)
        fused = torch.cat([b1, b2, b3, b4], 1)
        return F.leaky_relu(self.cl(fused) + self.sc(x), 0.2, inplace=True)

class RFB_Modified(nn.Module):
    def __init__(self, nc=64):
        super().__init__()
        growth = 32
        
        # Dense block
        self.db = nn.Module()
        self.db.convs = nn.ModuleList([
            DenseLayer(nc + i * growth, growth) for i in range(5)
        ])
        
        # RFB processing (state dict shows trunk_rfb.*.conv expects 160 input channels)
        self.rfb = RFB_Branch(5 * growth)  # 5 × 32 = 160 channels
        
        # Fusion back to nc channels (160 → 64)
        self.conv = nn.Conv2d(5 * growth, nc, 1, 1, 0)
    
    def forward(self, x):
        # Dense connections
        feats = [x]
        for layer in self.db.convs:
            feats.append(layer(torch.cat(feats, 1)))
        
        # Only dense outputs (no original x)
        db_out = torch.cat(feats[1:], 1)  # 5 × 32 = 160 channels
        
        # RFB processing on dense outputs
        rfb_out = self.rfb(db_out)
        
        # Fuse back to nc with residual
        return F.leaky_relu(self.conv(rfb_out) + x, 0.2, inplace=True)

class RFBESRGANGenerator(nn.Module):
    def __init__(self, growth=32, num_rrdb=16, num_rfb=8, nc=64, upscale=4):
        super().__init__()
        
        # Initial convolution (cl is activation, not conv layer)
        self.c1 = nn.Conv2d(3, nc, 3, 1, 1)
        # Note: 'cl.weight' in state dict is separate from c1
        self.cl = nn.Conv2d(nc, nc, 1, 1, 0)
        
        # Trunk A - RRDB blocks
        self.trunk_a = nn.ModuleList([RRDB(nc, growth) for _ in range(num_rrdb)])
        
        # Trunk RFB - RFB-Modified blocks
        self.trunk_rfb = nn.ModuleList([RFB_Modified(nc) for _ in range(num_rfb)])
        
        # RFB fusion - state dict shows 64 input channels (not 512!)
        self.rfb_fuse = RFB_Branch(nc)  # 64 channels
        
        # Upsampling - state dict shows u1: [256, 64], u2: [256, 256], u3: [256, 256]
        self.u1 = nn.Conv2d(nc, 256, 3, 1, 1)  # 64 → 256
        self.u2 = nn.Conv2d(256, 256, 3, 1, 1)  # 256 → 256
        self.u3 = nn.Conv2d(256, 256, 3, 1, 1)  # 256 → 256
        
        # Final output convolution (256 → 3 RGB after PixelShuffle)
        self.c2 = nn.Conv2d(16, 3, 3, 1, 1)  # After 4× PixelShuffle: 256/16 = 16
    
    def forward(self, x):
        # Initial features
        feat = F.leaky_relu(self.cl(self.c1(x)), 0.2, inplace=True)
        
        # RRDB trunk
        trunk_a_out = feat
        for rrdb in self.trunk_a:
            trunk_a_out = rrdb(trunk_a_out)
        
        # RFB trunk - only last output matters
        rfb_out = feat
        for rfb_mod in self.trunk_rfb:
            rfb_out = rfb_mod(rfb_out)
        
        # RFB fusion (NOT concatenating all 8 outputs - just final one!)
        fused = self.rfb_fuse(rfb_out)
        
        # Add trunk_a residual
        combined = F.leaky_relu(fused + trunk_a_out, 0.2, inplace=True)
        
        # Upsampling
        up = F.leaky_relu(self.u1(combined), 0.2, inplace=True)
        up = F.leaky_relu(self.u2(up), 0.2, inplace=True)
        up = F.leaky_relu(self.u3(up), 0.2, inplace=True)
        
        # PixelShuffle 4× upscaling (256 → 16 channels)
        up = F.pixel_shuffle(up, 4)
        
        # Final RGB output
        return torch.tanh(self.c2(up))

# ResNet-18 Classifier (unchanged)
class ResNetClassifier(nn.Module):
    def __init__(self, num_classes=43):
        super().__init__()
        resnet = models.resnet18(pretrained=False)
        self.features = nn.Sequential(*list(resnet.children())[:-1])
        self.fc = nn.Linear(512, num_classes)
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)

# Device setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Load models
try:
    sr_model = RFBESRGANGenerator().to(device)
    sr_model.load_state_dict(torch.load('sr_model.pth', map_location=device))
    sr_model.eval()
    print("✓ SR model loaded successfully")
except Exception as e:
    print(f"Error loading SR model: {e}")
    raise

try:
    classifier = ResNetClassifier(num_classes=43).to(device)
    classifier.load_state_dict(torch.load('classifier.pth', map_location=device))
    classifier.eval()
    print("✓ Classifier loaded successfully")
except Exception as e:
    print(f"Error loading classifier: {e}")
    raise

# Load class labels
with open('label_indices.json', 'r') as f:
    label_data = json.load(f)
    class_names = [label_data[str(i)] for i in range(43)]

# Inference function
def enhance_and_classify(image):
    """Process image through SR and classification"""
    try:
        # Preprocess
        img = image.convert('RGB')
        img = img.resize((30, 30), Image.Resampling.BILINEAR)
        img_tensor = torch.from_numpy(np.array(img)).float().permute(2, 0, 1).unsqueeze(0) / 127.5 - 1.0
        img_tensor = img_tensor.to(device)
        
        # Super-resolution
        with torch.no_grad():
            sr_output = sr_model(img_tensor)
        
        # Convert to displayable image
        sr_img = (sr_output.squeeze().permute(1, 2, 0).cpu().numpy() + 1.0) * 127.5
        sr_img = np.clip(sr_img, 0, 255).astype(np.uint8)
        
        # Classification
        sr_tensor = sr_output.repeat(1, 1, 1, 1) if sr_output.size(2) < 224 else sr_output
        sr_tensor = F.interpolate(sr_tensor, size=(224, 224), mode='bilinear', align_corners=False)
        
        with torch.no_grad():
            logits = classifier(sr_tensor)
            probs = torch.sigmoid(logits).squeeze().cpu().numpy()
        
        # Top 5 predictions
        top5_idx = np.argsort(probs)[-5:][::-1]
        predictions = {class_names[i]: float(probs[i]) for i in top5_idx}
        
        return Image.fromarray(sr_img), predictions
    
    except Exception as e:
        return None, {f"Error": str(e)}

# Gradio interface
demo = gr.Interface(
    fn=enhance_and_classify,
    inputs=gr.Image(type="pil", label="Upload Low-Resolution Image (30×30 recommended)"),
    outputs=[
        gr.Image(type="pil", label="Super-Resolved Image (120×120)"),
        gr.Label(num_top_classes=5, label="Top 5 Land Cover Predictions")
    ],
    title="🌍 BigEarthNet SR + Classification",
    description="Upload a satellite image to enhance resolution (4× super-resolution) and classify land cover types.",
    examples=[["example1.png"], ["example2.png"]] if False else None
)

if __name__ == "__main__":
    demo.launch()
