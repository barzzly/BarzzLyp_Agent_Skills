---
name: image-super-resolution
description: "Use when upscaling or enhancing image resolution with AI."
version: 1.0.0
author: BarzzLyp Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Image, Upscaling, Super-Resolution, Real-ESRGAN, Spandrel, PyTorch, Media]
---

# Image Super-Resolution & Upscaling

Autonomous image upscaling, super-resolution, and restoration workflows for Linux/macOS environments with or without dedicated GPUs.

## Quick Start (Single Command)

Run the included runner script via `uv` (handles dependencies, model fetching, and dual-format output):

```bash
uv run --with torch --with torchvision --with spandrel --with pillow \
  ~/.hermes/skills/media/image-super-resolution/scripts/upscale.py \
  --input /path/to/input.jpg \
  --output-dir ~/Pictures/Images \
  --model realesr-general-x4v3
```

## Step-by-Step Procedure

1. **Inspect Input Dimensions and Type**:
   ```bash
   identify /path/to/input.jpg 2>/dev/null || file /path/to/input.jpg
   ```
   Determine whether the image is digital art/wallpaper, anime, or real photo to select the model architecture.

2. **Select Model Architecture**:
   - **Digital Art / Wallpapers / General**: `realesr-general-x4v3` (Compact SRVGGNet, 4.7MB). Best balance of sharp detail, brushwork preservation, and CPU speed (processes 1280x731 to 5K in ~14s on CPU).
   - **Photographs / Complex Photorealism**: `RealESRGAN_x4plus` (RRDBNet, 64MB). Deeper reconstruction but computationally heavier.
   - **Flat Anime / Cartoons**: `realesr-animevideov3` (Compact). Sharp lines, but avoid on painterly art because aggressive denoise smears textures.

3. **Execute Native PyTorch CPU / GPU Inference**:
   Use `spandrel` to load weights without framework bloat (`basicsr` / `torchvision` legacy wrappers):
   ```bash
   uv run --with torch --with torchvision --with spandrel --with pillow python -c "
   import torch
   from PIL import Image
   from torchvision.transforms.functional import to_tensor, to_pil_image
   from spandrel import ModelLoader

   loader = ModelLoader()
   model = loader.load_from_file('~/.local/share/models/realesr-general-x4v3.pth').eval()

   img = Image.open('/path/to/input.jpg').convert('RGB')
   tensor = to_tensor(img).unsqueeze(0)

   with torch.no_grad():
       out = model(tensor)

   out_img = to_pil_image(out.squeeze(0).clamp(0, 1))
   out_img.save('~/Pictures/Images/output_5k.png')
   out_img.save('~/Pictures/Images/output_5k.jpg', quality=98, optimize=True)
   "
   ```

4. **Deliver and Verify Deliverables**:
   - Save full uncompressed output (`.png`) and lightweight high-grade (`.jpg` q=98) in `~/Pictures/Images/` (never loose in home root).
   - For chat/Telegram delivery, use `MEDIA:/path/to/output.jpg` to stay under API upload and inline image size caps.

## Pitfalls & Lessons

- **Never use `realesrgan-ncnn-vulkan` on headless servers without hardware Vulkan GPUs**: On CPU, ncnn falls back to Mesa llvmpipe software emulation, which single-threads shader dispatch and takes >60s for a 200x200 crop. Native PyTorch uses AVX-512 / oneDNN vector instructions directly and runs 10x-30x faster.
- **Do not use anime-specific models on painterly or textured digital art**: Models like `realesr-animevideov3` apply heavy noise filtering that erases canvas grain, brushstrokes, and fine silhouette boundaries into plastic gradients. Use `realesr-general-x4v3`.
- **Dual-save outputs for platform delivery**: Pure 4K/5K PNG files frequently exceed 12-25MB and trigger HTTP 413 or API upload failures on chat proxies. Generate a lossless PNG for the user's filesystem and a quality=98 JPEG for chat preview transmission.
- **Do not send uncompressed 4K/5K images to vision inspection endpoints**: Multimodal inspection APIs (such as `vision_analyze`) often sit behind reverse proxies with strict body payload limits (e.g. Nginx 413 Request Entity Too Large). Always downscale or compress to a high-quality JPEG under 5MB before feeding into vision tools for QA.

## Supporting Files

- `scripts/upscale.py` — Deterministic CLI upscaler with automated model caching and dual-format output.
- `references/architecture-selection.md` — Detailed parameter and performance breakdown across SR models.
