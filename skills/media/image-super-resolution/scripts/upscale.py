#!/usr/bin/env python3
import argparse
import os
import sys
import urllib.request
from pathlib import Path

MODEL_URLS = {
    "realesr-general-x4v3": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth",
    "RealESRGAN_x4plus": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
    "realesrgan-x4plus-anime": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth",
}

def ensure_model(model_name: str, cache_dir: Path) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    model_path = cache_dir / f"{model_name}.pth"
    if not model_path.exists():
        if model_name not in MODEL_URLS:
            raise ValueError(f"Unknown model: {model_name}. Available: {list(MODEL_URLS.keys())}")
        url = MODEL_URLS[model_name]
        print(f"Downloading model {model_name} from {url}...")
        urllib.request.urlretrieve(url, model_path)
    return model_path

def main():
    parser = argparse.ArgumentParser(description="Deterministic AI image super-resolution upscaler.")
    parser.add_argument("--input", "-i", required=True, help="Path to input image")
    parser.add_argument("--output-dir", "-o", default=str(Path.home() / "Pictures" / "Images"), help="Output directory")
    parser.add_argument("--model", "-m", default="realesr-general-x4v3", choices=list(MODEL_URLS.keys()), help="Model name")
    parser.add_argument("--threads", "-t", type=int, default=4, help="PyTorch CPU threads")
    args = parser.parse_args()

    import torch
    from PIL import Image
    from torchvision.transforms.functional import to_tensor, to_pil_image
    from spandrel import ModelLoader

    torch.set_num_threads(args.threads)
    model_cache = Path.home() / ".local" / "share" / "models"
    model_path = ensure_model(args.model, model_cache)

    loader = ModelLoader()
    model = loader.load_from_file(str(model_path)).eval()

    in_path = Path(args.input).resolve()
    if not in_path.exists():
        sys.exit(f"Input file not found: {in_path}")

    img = Image.open(in_path).convert("RGB")
    tensor = to_tensor(img).unsqueeze(0)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda":
        model = model.cuda()
        tensor = tensor.cuda()

    print(f"Upscaling {in_path.name} ({img.width}x{img.height}) using {args.model} on {device}...")
    with torch.no_grad():
        out_tensor = model(tensor)

    out_img = to_pil_image(out_tensor.squeeze(0).clamp(0, 1).cpu())
    out_dir = Path(args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base_stem = f"{in_path.stem}_upscaled_{out_img.width}x{out_img.height}"
    png_path = out_dir / f"{base_stem}.png"
    jpg_path = out_dir / f"{base_stem}.jpg"

    out_img.save(png_path)
    out_img.save(jpg_path, quality=98, optimize=True)

    print(f"Generated: {png_path} ({png_path.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"Generated: {jpg_path} ({jpg_path.stat().st_size / 1024 / 1024:.1f} MB)")

if __name__ == "__main__":
    main()
