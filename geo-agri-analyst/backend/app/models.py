import torch
import torch.nn as nn
import torch.nn.functional as F


class SR_Model(nn.Module):
    """
    Super-Resolution Model (RFBESRGANGenerator)
    Takes (B, 3, 16, 16) LR image -> (B, 3, 64, 64) SR image
    4x upscaling factor
    """
    
    def __init__(self, nf=64, growth=32):
        super(SR_Model, self).__init__()
        self.nf = nf
        # Placeholder architecture - replace with your actual RFBESRGANGenerator
        self.conv_first = nn.Conv2d(3, nf, 3, 1, 1)
        self.conv_body = nn.Sequential(
            *[nn.Conv2d(nf, nf, 3, 1, 1) for _ in range(8)]
        )
        self.upconv1 = nn.Conv2d(nf, nf * 4, 3, 1, 1)
        self.upconv2 = nn.Conv2d(nf, nf * 4, 3, 1, 1)
        self.conv_last = nn.Conv2d(nf, 3, 3, 1, 1)
        self.lrelu = nn.LeakyReLU(0.2, True)
    
    def forward(self, x):
        """
        Forward pass
        Args:
            x: Input LR image tensor (B, 3, 16, 16)
        Returns:
            SR image tensor (B, 3, 64, 64)
        """
        # Initial feature extraction
        feat = self.lrelu(self.conv_first(x))
        
        # Body convolutions
        body_feat = feat
        for layer in self.conv_body:
            body_feat = self.lrelu(layer(body_feat))
        
        # Upsampling (16x16 -> 32x32 -> 64x64)
        feat = feat + body_feat
        feat = self.lrelu(F.pixel_shuffle(self.upconv1(feat), 2))  # 2x
        feat = self.lrelu(F.pixel_shuffle(self.upconv2(feat), 2))  # 2x
        
        # Final output
        out = torch.sigmoid(self.conv_last(feat))
        return out


class CLF_Model(nn.Module):
    """
    Classification Model (RobustClassifier)
    Takes (B, 3, 64, 64) SR image -> (B, num_classes) logits
    Classifies land use into 10 classes
    """
    
    def __init__(self, num_classes=10):
        super(CLF_Model, self).__init__()
        self.num_classes = num_classes
        
        # Placeholder ResNet-like architecture - replace with your actual RobustClassifier
        self.conv1 = nn.Conv2d(3, 64, 7, 2, 3)  # 64x64 -> 32x32
        self.bn1 = nn.BatchNorm2d(64)
        
        # Feature extraction layers
        self.layer1 = self._make_layer(64, 64, 2)    # 32x32
        self.layer2 = self._make_layer(64, 128, 2)   # 16x16
        self.layer3 = self._make_layer(128, 256, 2)  # 8x8
        self.layer4 = self._make_layer(256, 512, 2)  # 4x4
        
        # Global average pooling and classifier
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)
        
        # Define land use classes
        self.class_names = [
            "Arable Land",
            "Forest",
            "Grassland", 
            "Urban Area",
            "Water Body",
            "Wetland",
            "Barren Land",
            "Permanent Crops",
            "Pasture",
            "Industrial Area"
        ]
    
    def _make_layer(self, in_channels, out_channels, stride):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, stride, 1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, 1, 1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
    
    def forward(self, x):
        """
        Forward pass
        Args:
            x: Input SR image tensor (B, 3, 64, 64)
        Returns:
            Classification logits (B, num_classes)
        """
        # Initial convolution
        x = F.relu(self.bn1(self.conv1(x)))
        
        # Feature extraction
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        
        # Global pooling and classification
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        
        return x
    
    def get_embeddings(self, x):
        """
        Get feature embeddings before final classification
        Args:
            x: Input SR image tensor (B, 3, 64, 64)
        Returns:
            Feature embeddings (B, 512)
        """
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        return torch.flatten(x, 1)