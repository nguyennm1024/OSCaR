# Setup Guide

This guide describes the environment expected by the current OSCaR codebase,
which is based on the local LLaVA-derived training and inference stack used for
state-change captioning experiments.

## Recommended Environment

- Linux
- Python 3.10
- CUDA-capable GPU for training or larger-scale inference
- Conda or another isolated Python environment manager

## Create an Environment

```bash
conda create -n oscar python=3.10 -y
conda activate oscar
pip install --upgrade pip setuptools wheel
```

## Core Dependencies

These match the versions used in the current internal training code:

```bash
pip install \
  torch==2.0.1 torchvision==0.15.2 \
  transformers==4.31.0 "tokenizers>=0.12.1,<0.14" \
  sentencepiece==0.1.99 shortuuid \
  accelerate==0.21.0 peft==0.4.0 bitsandbytes==0.41.0 \
  "pydantic>=1,<2" "markdown2[all]" numpy scikit-learn==1.2.2 \
  gradio==3.35.2 gradio_client==0.2.9 \
  requests httpx==0.24.0 uvicorn fastapi \
  einops==0.6.1 einops-exts==0.0.4 timm==0.6.13
```

## Training Extras

```bash
pip install deepspeed==0.9.5 ninja wandb
```

Optional:

```bash
pip install flash-attn --no-build-isolation
```

## Recommended Environment Variables

Avoid hardcoded local paths in scripts. Prefer environment variables such as:

```bash
export HF_HOME="$HOME/.cache/huggingface"
export TRANSFORMERS_CACHE="$HF_HOME/transformers"
export WANDB_MODE=dryrun
```

If your workflow needs API-backed prompt generation, load credentials from the
environment rather than committing them to source files.

## Expected Public Release Layout

The full public release is split across three surfaces:

- GitHub code repo: training, inference, evaluation, and data-prep code
- Hugging Face dataset repo: manifests, split metadata, and redistributable
  dataset assets
- Hugging Face model repo(s): projectors, adapters, and optionally merged model
  weights

## Current Status

The public repo scaffolding is in place. Code import and cleanup are being
prepared next, including:

- removal of private or machine-specific paths
- removal of secrets from helper scripts
- cleanup of release-only versus internal-only artifacts
