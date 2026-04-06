#!/usr/bin/env bash
set -euo pipefail

python -m llava.serve.controller --host 0.0.0.0 --port "${CONTROLLER_PORT:-10000}" &
python -m llava.serve.gradio_web_server --controller "http://localhost:${CONTROLLER_PORT:-10000}" --model-list-mode reload
