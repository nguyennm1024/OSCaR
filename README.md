# OSCaR: Object State Captioning and State Change Representation

OSCaR is a benchmark and code release for studying object state captioning and
state change representation in egocentric video.

This repository is being prepared as the public codebase for:

- training and fine-tuning
- inference and evaluation
- data preparation utilities
- reproducibility documentation

The corresponding dataset and model weights are being organized as separate
Hugging Face releases so the public code repository stays focused and usable.

## Paper

- NAACL 2024 paper: [OSCaR: Object State Captioning and State Change Representation](https://arxiv.org/abs/2402.17128)

## Release Plan

The public release is split into three parts:

1. GitHub code repository
2. Hugging Face dataset repository
3. Hugging Face model repository or repositories

This repository is the code component of that release.

## Repository Goals

- provide reproducible training and inference scripts
- document the dataset and split structure used in experiments
- make evaluation and state-change generation workflows easier to run
- keep large assets out of GitHub and in the appropriate Hugging Face repos

## Setup

Environment guidance lives in [docs/setup.md](docs/setup.md).

Release structure guidance lives in [docs/release-layout.md](docs/release-layout.md).

Contribution guidance lives in [CONTRIBUTING.md](CONTRIBUTING.md).

## Current Status

The repository has started public-release hardening. The next steps are:

- import the cleaned training, inference, and evaluation code
- remove private or cluster-specific assumptions from scripts
- remove secrets and internal-only helper artifacts
- document reproducible paths for model and dataset release

## Citation

If OSCaR is useful in your work, please cite:

```bibtex
@inproceedings{nguyen2024oscar,
  title={OSCaR: Object State Captioning and State Change Representation},
  author={Nguyen, Nguyen and Bi, Jing and Vosoughi, Ali and Tian, Yapeng and Fazli, Pooyan and Xu, Chenliang},
  booktitle={North American Chapter of the Association for Computational Linguistics (NAACL)},
  year={2024}
}
```
