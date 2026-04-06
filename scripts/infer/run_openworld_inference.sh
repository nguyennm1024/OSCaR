#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)

args=(
  --data-mapping "${DATA_MAPPING:?Set DATA_MAPPING to the open-world CSV mapping file.}"
  --path-prefix "${PATH_PREFIX:-}"
  --model-path "${MODEL_PATH:?Set MODEL_PATH to the adapter or merged model path.}"
  --output-root "${OUTPUT_ROOT:-$REPO_ROOT/outputs/openworld}"
)

if [[ -n "${MODEL_BASE:-}" ]]; then
  args+=(--model-base "$MODEL_BASE")
fi

python -m llava.serve.openworld_inference "${args[@]}" "$@"
