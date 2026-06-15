#!/usr/bin/env python3
"""Prepare high-resolution, lossless assets before Fig2Edit reconstruction."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageFilter


def positive_float(value: str) -> float:
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Expected number, got {value!r}") from exc
    if number <= 0:
        raise argparse.ArgumentTypeError("Value must be greater than 0.")
    return number


def main() -> int:
    parser = argparse.ArgumentParser(description="Create lossless high-resolution PNG assets for Fig2Edit.")
    parser.add_argument("source", help="Source image path.")
    parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("--scale", type=positive_float, default=2.0, help="Upscale factor. Default: 2.")
    parser.add_argument("--no-sharpen", action="store_true", help="Disable mild sharpening after upscale.")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    out_dir = Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    image = Image.open(source)
    if image.mode not in {"RGB", "RGBA"}:
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")

    original_path = out_dir / "source_lossless.png"
    image.save(original_path, format="PNG", optimize=False, compress_level=0)

    scaled_size = (round(image.width * args.scale), round(image.height * args.scale))
    highres = image.resize(scaled_size, Image.Resampling.LANCZOS)
    if not args.no_sharpen:
        highres = highres.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110, threshold=3))
    highres_path = out_dir / f"source_highres_{args.scale:g}x.png"
    highres.save(highres_path, format="PNG", optimize=False, compress_level=0)

    meta = {
        "source": str(source),
        "source_size": [image.width, image.height],
        "lossless_png": str(original_path),
        "highres_png": str(highres_path),
        "highres_size": [highres.width, highres.height],
        "scale": args.scale,
        "compression": "PNG compress_level=0; no JPEG conversion",
    }
    meta_path = out_dir / "highres_asset_report.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
