#!/usr/bin/env bash
# =============================================================================
# run_custom_case.sh — run the full Stream3D pipeline on a custom scene folder
# built by prepare_custom_case.py.
#
# Usage:
#   bash custom_case/run_custom_case.sh <gpu> <object_dir> <output_dir> [chunk_indices]
#
# Example (DTU scan24, 20 views -> chunks 0,1,2 at chunk_size=8 / overlap=2):
#   bash custom_case/run_custom_case.sh 1 /data/_t451_custom/DTU_scan24 /data/_t451_out "[0,1,2]"
# =============================================================================
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-/usr/bin/python3}"
CKPT="${CKPT:-checkpoints/hf/pipeline.yaml}"
RENDER_SPLIT="${RENDER_SPLIT:-render_spiral_100}"

GPU="${1:?usage: run_custom_case.sh <gpu> <object_dir> <output_dir> [chunk_indices]}"
OBJ="${2:?need object_dir}"
OUT="${3:?need output_dir}"
CHUNKS="${4:-[-1]}"

cd "$REPO"
exec env CUDA_VISIBLE_DEVICES="$GPU" PYTHONPATH="$REPO/_compat" \
  HF_HUB_OFFLINE=1 HYDRA_FULL_ERROR=1 ATTN_BACKEND=sdpa \
  "$PYTHON" -m streaming.runner backend=sam3d \
  data.roots=[$OBJ] data.render_split=$RENDER_SPLIT \
  data.image_dir_name=images data.mask_dir_name=masks data.da3_dir_name=da3 \
  camera_pose_source=da3 \
  streaming.topk=8 streaming.stage2_selection.topk=8 \
  ++streaming.selection_strategy=va_div ++streaming.selection_div_lambda=0.1 \
  pipeline.ss_weight_source=mass_relative pipeline.stage2_weighting.weight_source=mass_relative \
  pipeline.ss_jam_kappa=8 pipeline.stage2_weighting.jam_kappa=8 \
  pipeline.ss_uniform_blend=0 pipeline.stage2_weighting.uniform_blend=0 \
  pipeline.decode_formats=[gaussian,mesh] pipeline.with_texture_baking=false \
  output_root="$OUT" model_config_path="$CKPT" \
  chunk_size=8 chunk_overlap=2 chunk_indices=$CHUNKS seed=0 \
  hydra.run.dir=/tmp/stream3d_custom_case hydra.output_subdir=.hydra
