# Release Layout

OSCaR is released across GitHub and Hugging Face.

## GitHub Code Repository

This repository contains:

- training code and launch scripts
- inference and model-serving code
- evaluation code
- data-preparation utilities
- reproducibility documentation

It should not contain:

- raw dataset payloads
- model checkpoints or adapter weights
- generated outputs or local logs

## Hugging Face Dataset Repository

Dataset repo: `ali-vosoughi/oscar-dataset`

Intended contents:

- OSCaR image assets
- training manifests
- benchmark and split metadata
- dataset card and normalized metadata tables

## Hugging Face Model Repositories

Model repos under `ali-vosoughi` are intended to publish:

- projector checkpoints
- adapter-only OSCaR releases
- adapter-only mixed-data releases
- merged full-model exports when redistribution is compatible
