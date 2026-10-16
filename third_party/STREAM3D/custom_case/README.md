# Running STREAM3D on a custom dataset

This folder is a worked, end-to-end example of running the released pipeline on data that is
**not** GSO30 — here a DTU scene (`scan24`) cut down to 20 views (3 chunks).

## 1. Required folder layout

The runner consumes **one directory per object**. Every path component below is a Hydra
override, shown with its default value:

```
<object_dir>/                          # data.roots=[<object_dir>]
  render_spiral_100/                   # data.render_split
    images/                            # data.image_dir_name
      000000.png  000001.png  ...      # N RGB frames
    masks/                             # data.mask_dir_name
      000000.png  000001.png  ...      # N foreground masks, matched BY STEM
    da3/                               # data.da3_dir_name
      camera_poses.txt                 # N lines
      results_output/
        frame_0.npz  frame_1.npz  ...  # N files, keys: depth, intrinsics
```

## 2. What each item must contain

| Item | Requirement | Enforced in |
|---|---|---|
| `images/*.png\|jpg` | Stem must **end in an integer** (`000007.png`, `frame_7.png`). Sort key is `int(stem.split("_")[-1])`; this defines frame index *i*. | `streaming/data/data_gso.py:59-62` |
| `masks/<stem>.png` | Single-channel `L`/`P` (non-zero = foreground) or `RGBA` (alpha > 0 = foreground). **An `RGB` mask is silently treated as full-frame foreground** — only a warning is logged. A mask covering >99% of the frame falls back to the image alpha channel. | `streaming/data/chunks.py:24-51` |
| `da3/results_output/frame_*.npz` | One per image, **paired by position** after the same integer sort. Keys: `depth` (H×W float) and `intrinsics` (3×3, in the *depth* resolution, not the image resolution). | `streaming/utils/streaming_da3.py:130-176` |
| `da3/camera_poses.txt` | N non-empty lines, 12 (3×4) or 16 (4×4) floats, row-major, **world-to-camera**, paired by position. | `streaming/utils/streaming_da3.py:52-68` |

Counts must match exactly: `len(images) == len(frame_*.npz) == len(pose lines)`, otherwise the
run aborts with a `DA3 output count mismatch` error.

### Camera convention note

With the default `camera_pose_source=da3`, `camera_poses.txt` is consumed as **world-to-camera**.
The alternative `camera_pose_source=dataset_gt` reads a NeRF-style JSON (`dataset_camera_path=...`)
and takes `transform_matrix` per frame — which in the NeRF convention is camera-to-world — into the
same slot, so only use it if your JSON already stores w2c. `dataset_gt` replaces poses and
intrinsics only; **depth still comes from the DA3 npz files either way**.

## 3. Producing the `da3/` folder

`da3/` holds monocular depth + intrinsics + poses from Depth-Anything-3. If you already have
depth and calibrated cameras from another source (COLMAP, a depth sensor, a different MVS
pipeline), you can write the npz/txt files yourself — the pipeline never calls DA3 at run time,
it only reads these files. Each npz needs exactly `depth` and `intrinsics`; intrinsics must be
expressed at the depth map's resolution (the loader does not rescale them under
`camera_pose_source=da3`).

## 4. Chunking

`chunk_size` / `chunk_overlap` define the streaming windows; chunk starts are
`0, step, 2*step, ...` with `step = chunk_size - chunk_overlap`, plus a final window flush to the
end. With the defaults (`chunk_size=8`, `chunk_overlap=2`, step 6), **20 views give exactly
3 chunks**: frames 0–7, 6–13, 12–19. `chunk_indices=[-1]` runs all of them.

## 5. The worked example

The ready-to-run scene is published as a HuggingFace dataset — DTU `scan24`, 20 views (52 MB),
already in the layout above, so you can reconstruct it without preparing anything:

**[huggingface.co/datasets/zhouk777/stream3d-sample](https://huggingface.co/datasets/zhouk777/stream3d-sample)**

```bash
# download into custom_case/data/ (creates data/DTU_scan24/...)
hf download zhouk777/stream3d-sample --repo-type dataset --local-dir custom_case/data

# older huggingface_hub releases ship the same command as:
# huggingface-cli download zhouk777/stream3d-sample --repo-type dataset --local-dir custom_case/data
```

No token is needed — the dataset is public.

```
custom_case/data/DTU_scan24/render_spiral_100/
  images/  000000.png … 000019.png     # RGB 1600×1200, background already blacked out
  masks/   000000.png … 000019.png     # mode L, ≈57% foreground
  da3/     camera_poses.txt            # 20 lines × 16 floats (4×4, world-to-camera)
           results_output/frame_0.npz … frame_19.npz   # depth 378×504 float32 + 3×3 intrinsics
```

```bash
# reconstruct the downloaded scene (GPU 0, all 3 chunks)
bash custom_case/run_custom_case.sh 0 custom_case/data/DTU_scan24 /tmp/custom_out "[0,1,2]"
```

To build the same folder yourself from a raw DTU checkout — or from your own capture:

```bash
python3 custom_case/prepare_custom_case.py \
  --src-images /path/DTU/scan24/image_masked \
  --src-masks  /path/DTU/scan24/mask \
  --src-da3    /path/DTU/scan24/da3_masked \
  --out        custom_case/data/DTU_scan24 \
  --num-views 20
```

Note the intrinsics in the npz files are at the **depth** resolution (504×378), not the image
resolution (1600×1200) — that is what the loader expects under `camera_pose_source=da3`.

Outputs land in `<output_dir>/<object_name>/chunk_XXXX/`:

```
result.glb                # vertex-coloured mesh
result.ply                # 3D Gaussians
result_pose.npz           # object pose
params.npz                # generation parameters
result_metadata.json      # image_names, stage-1 / stage-2 selected views
stage1_sparse/            # sparse-structure debug output
stage1_selected_crops/    # crops fed to stage 1
stage2_selected_crops/    # crops fed to stage 2
```

### Measured on this example

DTU `scan24`, 20 views, one H100, `chunk_size=8` / `chunk_overlap=2`:

| Chunk | Frames | Wall time | Mesh verts | GLB | Gaussian PLY |
|---|---|---|---|---|---|
| `chunk_0000` | 000000–000007 | 106.4 s (incl. model load) | 544,840 | 21.8 MB | 84.2 MB |
| `chunk_0001` | 000006–000013 | 85.7 s | 556,032 | 22.2 MB | 85.0 MB |
| `chunk_0002` | 000012–000019 | 84.0 s | 554,214 | 22.2 MB | 86.0 MB |

Steady state is ≈85 s per 8-view chunk (≈10.6 s/view); the first chunk carries the one-off model load
and warm-up.

### Common failure modes

| Symptom | Cause |
|---|---|
| `DA3 output count mismatch` | `len(images) != len(frame_*.npz)` — the counts must match exactly |
| `Mask file ... is RGB, not RGBA. Using all pixels as mask.` | mask stored as RGB; it is being ignored. Convert to `L` (this script does so by default) |
| Reconstruction ignores the silhouette | same as above, or a mask that is >99% foreground |
| `Need at least 8 images to build chunks` | fewer views than `chunk_size` |
| Geometry inverted / cameras behind the object | `camera_poses.txt` holds camera-to-world; invert it, the loader expects world-to-camera |

## 6. Evaluation

`evaluate.sh` is GSO30-specific: it needs a `render_mvs_25` ground-truth split next to the object.
For a custom capture without that split, the pipeline gives you reconstruction output only —
compare against your own ground truth or evaluate qualitatively.
