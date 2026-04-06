# Setup Guide

OSCaR uses a UV-based public environment for installation and release tooling.

## Requirements

- Linux
- Python 3.10
- CUDA-capable GPU for training or larger-scale inference
- `uv` installed locally

## Create The Environment

```bash
uv venv --python 3.10 .venv
source .venv/bin/activate
uv pip install -e .[train,inference,eval,release]
```

If `uv` selects the wrong Python interpreter on your machine, point it
explicitly at Python 3.10:

```bash
uv venv --python 3.10 .venv
```

## Recommended Environment Variables

```bash
export HF_HOME="$HOME/.cache/huggingface"
export TRANSFORMERS_CACHE="$HF_HOME/transformers"
export WANDB_MODE=dryrun
```

Optional for the QA-generation helper:

```bash
export OPENAI_API_KEY=...
```

## Release Layout

- GitHub code repo: training, inference, evaluation, and data-prep code
- Hugging Face dataset repo: OSCaR assets, manifests, and split metadata
- Hugging Face model repos: projectors, adapters, and merged model releases

For end-to-end commands, see:

- [INSTALL.md](../INSTALL.md)
- [TRAIN.md](../TRAIN.md)
- [INFERENCE.md](../INFERENCE.md)
- [EVAL.md](../EVAL.md)
