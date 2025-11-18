---
title: BigEarthNet SR-AL Classifier
emoji: 🛰️
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.8.0
app_file: app.py
pinned: false
license: mit
---

# BigEarthNet Super-Resolution + Active Learning Classifier

This application enhances satellite images using Super-Resolution and classifies them into 43 land cover types.

## Features

- **Super-Resolution**: 4× upscaling (30×30 → 120×120) using RFB-ESRGAN
- **Multi-label Classification**: 43 BigEarthNet V2 land cover classes
- **Active Learning**: Trained efficiently using DBSS + SSAS strategies

## Models

- **SR Generator**: RFB-ESRGAN with 6 RRDB + 6 RFB blocks
- **Classifier**: ResNet-18 backbone with multi-label head

## Usage

1. Upload a satellite image (RGB)
2. View the enhanced SR image
3. See top 5 predicted land cover classes

## Dataset

Trained on [BigEarthNet V2](http://bigearth.net/) - Sentinel-2 satellite imagery dataset.

## Citation

If you use this model, please cite:
```
@inproceedings{bigearthnet,
  title={BigEarthNet: A Large-Scale Benchmark Archive for Remote Sensing Image Understanding},
  author={Sumbul, Gencer and Charfuelan, Marcela and Demir, Begum and Markl, Volker},
  booktitle={IEEE International Geoscience and Remote Sensing Symposium},
  year={2019}
}
```

## License

MIT License
