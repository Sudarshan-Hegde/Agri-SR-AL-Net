# Hugging Face Spaces Deployment Guide

## Step-by-Step Instructions

### 1. Export Your Trained Models

In Kaggle (after training completes), download your models:

```python
# At the end of your notebook, save models
import torch

# Save SR model (remove DataParallel wrapper if needed)
if hasattr(g, 'module'):
    torch.save(g.module.state_dict(), '/kaggle/working/sr_model.pth')
else:
    torch.save(g.state_dict(), '/kaggle/working/sr_model.pth')

# Save classifier
if hasattr(clf, 'module'):
    torch.save(clf.module.state_dict(), '/kaggle/working/classifier.pth')
else:
    torch.save(clf.state_dict(), '/kaggle/working/classifier.pth')

# Also save the label mapping
import json
with open('/kaggle/working/label_indices.json', 'w') as f:
    json.dump({'original_labels': label_map}, f)

print("Models saved! Download from Kaggle output folder.")
```

Click "Download" button in Kaggle to get:
- `sr_model.pth` (~50MB)
- `classifier.pth` (~45MB)
- `label_indices.json` (~5KB)

### 2. Create Hugging Face Account

1. Go to https://huggingface.co/
2. Click "Sign Up" (free account)
3. Verify your email
4. Optional: Add payment method for GPU access (first $10 free)

### 3. Create a New Space

1. Click your profile → "New Space"
2. Fill in details:
   - **Space name**: `bigearthnet-sr-classifier` (or your choice)
   - **License**: MIT
   - **Select SDK**: Gradio
   - **Hardware**: CPU (free) or T4 GPU (paid, ~$0.60/hr)
   - **Visibility**: Public or Private

3. Click "Create Space"

### 4. Upload Files

**Option A: Using Web Interface**
1. In your new Space, click "Files" tab
2. Click "Add file" → "Upload files"
3. Upload:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `sr_model.pth`
   - `classifier.pth`
   - `label_indices.json`
4. Click "Commit changes"

**Option B: Using Git (Recommended)**
```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/bigearthnet-sr-classifier
cd bigearthnet-sr-classifier

# Copy all files from huggingface-deployment folder
cp /path/to/huggingface-deployment/* .

# Add your model files (downloaded from Kaggle)
cp /path/to/downloads/sr_model.pth .
cp /path/to/downloads/classifier.pth .
cp /path/to/downloads/label_indices.json .

# Git LFS for large files (models)
git lfs install
git lfs track "*.pth"

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

### 5. Wait for Build

- HuggingFace will automatically build your app
- Check "Logs" tab for build progress
- First build takes 2-5 minutes
- Status will change from "Building" → "Running"

### 6. Test Your App

1. Once running, you'll see the Gradio interface
2. Upload a test satellite image
3. Verify SR enhancement and classification work

### 7. Get API Endpoint

Your app automatically has a REST API:

```python
# Python client code
import requests

API_URL = "https://huggingface.co/spaces/YOUR_USERNAME/bigearthnet-sr-classifier"

def query(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    response = requests.post(
        API_URL + "/api/predict",
        files={"data": data}
    )
    return response.json()

result = query("satellite_image.jpg")
print(result)
```

### 8. Integrate with Your Backend

```python
# In your FastAPI backend
from fastapi import APIRouter, UploadFile
import httpx

router = APIRouter()

HF_API_URL = "https://YOUR_USERNAME-bigearthnet-sr-classifier.hf.space/api/predict"

@router.post("/api/analyze-satellite")
async def analyze_satellite(file: UploadFile):
    # Forward to HuggingFace
    async with httpx.AsyncClient(timeout=30.0) as client:
        files = {"data": await file.read()}
        response = await client.post(HF_API_URL, files=files)
    
    return response.json()
```

### 9. Optional: Upgrade to GPU

If CPU is too slow:
1. Go to Space Settings
2. Under "Hardware", select "T4 GPU"
3. Costs ~$0.60/hour (only when running)
4. Set sleep timeout to save costs
5. First $10 is free credit

### 10. Monitor Usage

- Dashboard shows:
  - Number of API calls
  - Response times
  - Error rates
- Logs available in real-time
- Set up webhooks for notifications

## Troubleshooting

### Model Files Too Large
```python
# Use model quantization to reduce size
import torch

# Load model
model = YourModel()
model.load_state_dict(torch.load('large_model.pth'))

# Quantize to int8
model_quantized = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

# Save quantized (much smaller)
torch.save(model_quantized.state_dict(), 'small_model.pth')
```

### Out of Memory
- Switch to T4 GPU
- Reduce batch size in inference
- Use torch.cuda.empty_cache()

### Slow Inference
- Enable GPU
- Use torch.compile() (PyTorch 2.0+)
- Batch multiple requests

## Cost Optimization

**Free Tier Strategy:**
```yaml
# Set in Space settings
hardware: cpu-basic  # Free
sleep_after: 1 hour  # Auto-pause when idle
```

**Paid GPU Strategy:**
```yaml
hardware: t4-small   # $0.60/hr
sleep_after: 5 min   # Quick pause to save money
```

## Alternative: Use Free Colab

If you don't want to pay for GPU on HuggingFace:

```python
# Run in Google Colab (free T4 GPU)
!pip install gradio pyngrok

from pyngrok import ngrok
import gradio as gr

# Your inference code here

# Launch with public URL
public_url = ngrok.connect(7860)
print(f"Public URL: {public_url}")

demo.launch(share=True)
```

Keep the Colab tab open, use the ngrok URL in your backend.

## Next Steps

1. Add example images to showcase
2. Create a demo video
3. Share on social media
4. Add to your portfolio/resume
5. Monitor and improve based on feedback

## Support

- HuggingFace Docs: https://huggingface.co/docs/hub/spaces
- Community Forum: https://discuss.huggingface.co/
- Discord: https://discord.gg/hugging-face
