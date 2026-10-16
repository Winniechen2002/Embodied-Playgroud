#!/usr/bin/env python3
"""Build a STREAM3D-ready scene folder from an arbitrary (custom) capture.

The runner (`python -m streaming.runner`) expects ONE directory per object:

    <root>/
      <render_split>/            # data.render_split, default: render_spiral_100
        images/                  # data.image_dir_name  — N RGB frames, stem must end in an int
        masks/                   # data.mask_dir_name   — <stem>.png foreground masks
        da3/                     # data.da3_dir_name
          camera_poses.txt       # N lines, 12 or 16 floats, world-to-camera, row-major
          results_output/
            frame_0.npz ... frame_{N-1}.npz   # keys: depth (HxW), intrinsics (3x3)

Pairing rules enforced by the loader (streaming/data/data_gso.py,
streaming/utils/streaming_da3.py, streaming/data/chunks.py):

  * images are sorted by ``int(stem.split("_")[-1])``  -> that order defines frame index i
  * ``frame_*.npz`` are sorted the same way and paired with images BY POSITION
  * camera_poses.txt line i is paired with frame i BY POSITION
  * masks are looked up BY STEM (``<image stem>.png``); an RGB (no alpha) mask is silently
    treated as full-frame foreground, so use RGBA-alpha or single-channel L/P masks
  * len(images) == len(npz) == len(pose lines), otherwise the run aborts

This script copies a contiguous or strided subset of a source capture into that layout and
re-numbers nothing: original file names are preserved because they already sort correctly.

Example (DTU scan24, first 20 views = 3 chunks at chunk_size=8 / overlap=2):

    python3 prepare_custom_case.py \
        --src-images  /data/DTU/DTU/scan24/image_masked \
        --src-masks   /data/DTU/DTU/scan24/mask \
        --src-da3     /data/DTU/DTU/scan24/da3_masked \
        --out         /data/_t451_custom/DTU_scan24 \
        --num-views 20
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import numpy as np
from PIL import Image

IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg")


def sort_key(path: Path):
    stem = path.stem
    try:
        return (0, int(stem.split("_")[-1]), stem)
    except ValueError:
        return (1, 0, stem)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--src-images", type=Path, required=True)
    parser.add_argument("--src-masks", type=Path, required=True)
    parser.add_argument("--src-da3", type=Path, required=True, help="dir holding camera_poses.txt + results_output/")
    parser.add_argument("--out", type=Path, required=True, help="object dir to create")
    parser.add_argument("--render-split", default="render_spiral_100")
    parser.add_argument("--num-views", type=int, default=20)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stride", type=int, default=1)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--keep-mask-mode",
        action="store_true",
        help="copy masks verbatim instead of converting them to single-channel L "
        "(an RGB mask is silently read as full-frame foreground by chunks.py)",
    )
    return parser.parse_args()


def write_mask(src: Path, dst: Path, *, keep_mode: bool, size_wh: tuple[int, int]) -> None:
    if keep_mode:
        shutil.copy2(src, dst)
        return
    image = Image.open(src)
    if image.mode == "RGBA":
        array = np.asarray(image)[..., 3]
    else:
        array = np.asarray(image.convert("L"))
    mask = Image.fromarray(((array > 127) * 255).astype(np.uint8), mode="L")
    if mask.size != size_wh:
        mask = mask.resize(size_wh, Image.NEAREST)
    mask.save(dst)


def main() -> None:
    args = parse_args()

    images = sorted(
        [p for p in args.src_images.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES],
        key=sort_key,
    )
    npzs = sorted((args.src_da3 / "results_output").glob("frame_*.npz"), key=sort_key)
    pose_lines = [
        line.strip()
        for line in (args.src_da3 / "camera_poses.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    if not (len(images) == len(npzs) == len(pose_lines)):
        raise SystemExit(
            f"source is inconsistent: {len(images)} images, {len(npzs)} npz, {len(pose_lines)} pose lines"
        )

    selected = list(range(args.start, len(images), args.stride))[: args.num_views]
    if len(selected) < args.num_views:
        raise SystemExit(f"only {len(selected)} views available with start/stride, wanted {args.num_views}")

    render_root = args.out / args.render_split
    if render_root.exists():
        if not args.overwrite:
            raise SystemExit(f"{render_root} exists; pass --overwrite")
        shutil.rmtree(render_root)

    image_dir = render_root / "images"
    mask_dir = render_root / "masks"
    results_dir = render_root / "da3" / "results_output"
    for directory in (image_dir, mask_dir, results_dir):
        directory.mkdir(parents=True)

    for index in selected:
        image_path = images[index]
        shutil.copy2(image_path, image_dir / image_path.name)

        mask_path = None
        for suffix in IMAGE_SUFFIXES:
            candidate = args.src_masks / f"{image_path.stem}{suffix}"
            if candidate.exists():
                mask_path = candidate
                break
        if mask_path is None:
            raise SystemExit(f"no mask found for image stem {image_path.stem} in {args.src_masks}")
        write_mask(
            mask_path,
            mask_dir / f"{image_path.stem}.png",
            keep_mode=args.keep_mask_mode,
            size_wh=Image.open(image_path).size,
        )

        shutil.copy2(npzs[index], results_dir / npzs[index].name)

    (render_root / "da3" / "camera_poses.txt").write_text(
        "\n".join(pose_lines[index] for index in selected) + "\n", encoding="utf-8"
    )

    print(f"wrote {len(selected)} views to {render_root}")
    print(f"  images : {len(list(image_dir.iterdir()))}")
    print(f"  masks  : {len(list(mask_dir.iterdir()))}")
    print(f"  da3    : {len(list(results_dir.iterdir()))} npz + camera_poses.txt")


if __name__ == "__main__":
    main()
