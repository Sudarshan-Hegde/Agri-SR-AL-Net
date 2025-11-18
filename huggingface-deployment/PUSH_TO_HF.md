# How to Push to HuggingFace Space

## Method 1: Web Interface (Recommended)

1. Go to: https://huggingface.co/spaces/HegdeSudarshan/BigEarthNetModels
2. Click **Files** tab
3. Click on **app.py** 
4. Click **Edit** (pencil icon)
5. Copy content from local `app.py` and paste
6. Commit message: "Fix model architecture"
7. Click **Commit changes to main**

---

## Method 2: Git Command Line

### Step 1: Get HuggingFace Token
1. Go to https://huggingface.co/settings/tokens
2. Click **New token**
3. Name: `git-push`
4. Type: **Write**
5. Click **Generate** and copy token

### Step 2: Clone Repository
```powershell
cd c:\Users\sudar\OneDrive\Desktop\majorProject\Agri-SR-AL-Net

# Clone with authentication (replace YOUR_TOKEN)
git clone https://HegdeSudarshan:YOUR_TOKEN@huggingface.co/spaces/HegdeSudarshan/BigEarthNetModels
```

### Step 3: Copy Files
```powershell
# Copy your fixed files
Copy-Item huggingface-deployment\app.py BigEarthNetModels\app.py -Force
Copy-Item huggingface-deployment\requirements.txt BigEarthNetModels\requirements.txt -Force
Copy-Item huggingface-deployment\README.md BigEarthNetModels\README.md -Force
```

### Step 4: Commit and Push
```powershell
cd BigEarthNetModels

git add app.py requirements.txt README.md
git commit -m "Fix model architecture to match trained weights"
git push origin main
```

---

## Method 3: Upload Model Files (First Time Only)

If you haven't uploaded your model files yet:

### Via Web:
1. Go to Space → **Files**
2. Click **Add file** → **Upload files**
3. Upload:
   - `sr_model.pth` (from Kaggle)
   - `classifier.pth` (from Kaggle)
   - `label_indices.json` (from Kaggle)
4. Commit message: "Add trained models"
5. Click **Commit**

### Via Git LFS (for large files):
```powershell
cd BigEarthNetModels

# Install Git LFS if not already
git lfs install

# Track large files
git lfs track "*.pth"
git add .gitattributes

# Copy models from Kaggle download location
# (Replace paths with your actual download location)
Copy-Item "C:\Users\sudar\Downloads\sr_model.pth" . -Force
Copy-Item "C:\Users\sudar\Downloads\classifier.pth" . -Force
Copy-Item "C:\Users\sudar\Downloads\label_indices.json" . -Force

# Commit and push
git add *.pth label_indices.json
git commit -m "Add trained model weights"
git push origin main
```

---

## Quick Command Reference

### Check Space Status
Visit: https://huggingface.co/spaces/HegdeSudarshan/BigEarthNetModels

### View Build Logs
Click **Logs** tab in your Space to see if it's building correctly

### Test Your Space
After successful build, click **App** tab and try uploading an image

---

## Troubleshooting

### "Authentication failed"
- Use personal access token instead of password
- Format: `https://USERNAME:TOKEN@huggingface.co/spaces/...`

### "File too large" (> 100MB)
- Use Git LFS: `git lfs track "*.pth"`
- Or upload via web interface

### Build fails
- Check **Logs** tab for errors
- Verify `requirements.txt` has correct versions
- Check model file sizes match expectations

### Space stays in "Building" forever
- Refresh page
- Check logs for errors
- May need to restart: Settings → **Factory Rebuild**

---

## Current Files Needed

Make sure these files exist in your Space:

✅ **app.py** (Fixed architecture - MUST UPDATE)
✅ **requirements.txt**
✅ **README.md**
⬜ **sr_model.pth** (Download from Kaggle first)
⬜ **classifier.pth** (Download from Kaggle first)
⬜ **label_indices.json** (Download from Kaggle first)

---

## Next Steps After Push

1. ✅ Push fixed `app.py`
2. ⬜ Wait for build (~2-3 min)
3. ⬜ Check logs for errors
4. ⬜ Upload model files if not done
5. ⬜ Test with sample image
6. ⬜ Update backend API URL if needed
