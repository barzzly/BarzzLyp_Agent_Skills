# Super-Resolution Model Architecture Selection

| Model | Architecture | Size | Ideal Content | CPU Performance | Artifact Profile |
|---|---|---|---|---|---|
| `realesr-general-x4v3` | SRVGGNetCompact (16 conv layers) | ~4.7 MB | Digital art, concept art, wallpapers, illustrations | **Very fast** (~10-15s for 720p to 5K) | Maintains brush strokes, avoids plastic posterization |
| `RealESRGAN_x4plus` | RRDBNet (23 dense blocks) | ~64 MB | Complex photos, intricate architectural masonry | **Heavy** (~2-3 mins on CPU, requires tiling) | Sharper fine edge reconstruction, higher hallucination risk |
| `realesrgan-x4plus-anime` | RRDBNet-6B (6 dense blocks) | ~18 MB | Cel-shaded 2D anime, manga scans | **Moderate** (~30-45s on CPU) | High line contrast, smooth color fills |
| `realesr-animevideov3` | CompactSRVGG (small channel width) | ~1.2 MB | Low-bitrate video frames, flat web icons | **Ultra fast** (~2s on CPU) | Strong denoise, smears fine texture into flat patches |

## Performance Decision Matrix

1. **Headless Linux VPS / CPU-only inference**:
   - Prefer `SRVGGNetCompact` models (`realesr-general-x4v3`).
   - Run via PyTorch native CPU (`spandrel` + AVX-512 / OpenMP with 4-8 threads).
   - Avoid `realesrgan-ncnn-vulkan` on CPU due to software Mesa llvmpipe emulation overhead.

2. **Memory & Tiling Strategy**:
   - For images up to 1080p, `realesr-general-x4v3` fits in standard RAM in a single forward pass without tiling artifacts.
   - For `RealESRGAN_x4plus` or inputs >1080p on memory-constrained systems, process tiles with a 32px overlap padding to prevent visible seam borders.
