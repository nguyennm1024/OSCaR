#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)

args=(
  --data-mapping "${DATA_MAPPING:?Set DATA_MAPPING to the benchmark CSV or equivalent mapping file.}"
  --path-prefix "${PATH_PREFIX:-}"
  --legacy-ego4d-root "${LEGACY_EGO4D_ROOT:-}"
  --legacy-epic-root "${LEGACY_EPIC_ROOT:-}"
  --model-path "${MODEL_PATH:?Set MODEL_PATH to the adapter or merged model path.}"
  --output-root "${OUTPUT_ROOT:-$REPO_ROOT/outputs/benchmark}"
)

if [[ -n "${MODEL_BASE:-}" ]]; then
  args+=(--model-base "$MODEL_BASE")
fi

python -m llava.serve.inference "${args[@]}" "$@"
