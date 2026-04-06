# Release Layout

OSCaR is being prepared as a multi-repository public release.

## GitHub Code Repository

This repository is intended to contain:

- training scripts
- inference scripts
- evaluation scripts
- data preparation utilities
- reproducibility documentation

This repository should not store large checkpoints or raw datasets.

## Hugging Face Dataset Repository

The dataset release should contain:

- dataset manifests
- split metadata
- dataset card documentation
- redistributable image assets, if licensing permits

## Hugging Face Model Repository

Model releases should contain only the publishable artifacts for each variant,
for example:

- `adapter_model.bin`
- `adapter_config.json`
- `config.json`
- `non_lora_trainables.bin`
- projector checkpoints such as `mm_projector.bin`

DeepSpeed resume state and nested training checkpoints should be excluded from
public model repos.
