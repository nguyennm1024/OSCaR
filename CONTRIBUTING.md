# Contributing to OSCaR

This repository is being prepared as the public code release for OSCaR:
Object State Captioning and State Change Representation.

## Scope

The code repository is intended for:

- training and fine-tuning code
- inference and evaluation code
- data preparation utilities
- documentation and reproducibility notes

Large assets should not be committed here. Use the Hugging Face model and
dataset repos for:

- model checkpoints
- adapter weights
- raw image/video assets
- large generated outputs

## Before Opening a PR

Please make sure your change:

- does not commit secrets, tokens, or private endpoints
- does not commit dataset payloads or model weights
- updates documentation when behavior or setup changes
- keeps hardcoded machine-specific paths out of committed code

## Development Workflow

1. Create a feature branch from `main`.
2. Keep changes scoped and reviewable.
3. Use descriptive commit messages.
4. Include a short note on training, inference, or data impact in the PR.

## Coding Expectations

- Prefer portable paths and environment variables over cluster-local paths.
- Keep scripts runnable from the repository root unless there is a strong
  reason not to.
- Add comments only where they materially improve readability.
- Preserve reproducibility: document model names, data manifests, and runtime
  assumptions near the code that depends on them.

## Security and Privacy

- Never commit API keys or access tokens.
- Never commit credentials in notebooks, shell scripts, or config files.
- Assume this repository will be public.
