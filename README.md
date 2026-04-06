# OSCaR: Object State Captioning and State Change Representation

Accepted NAACL 2024 paper: `https://aclanthology.org/2024.findings-naacl.226/`

Project page: `https://nguyennm1024.github.io/OSCaR/`

OSCaR is the public code release for the NAACL 2024 paper
[OSCaR: Object State Captioning and State Change Representation](https://aclanthology.org/2024.findings-naacl.226/).

This repository publishes the LLaVA-derived training, inference, evaluation,
and data-preparation code used for OSCaR, alongside release-grade
documentation for the corresponding Hugging Face dataset and model repos.

## Project Overview

OSCaR studies object state captioning and state change representation for
egocentric video. The public release packages the training and inference code,
the Hugging Face dataset and model repos, and the GitHub Pages project site for
the NAACL 2024 paper release.

Paper-level release facts:

- annotated segments reported in the paper: `14,084`
- human-verified benchmark videos: `500`
- LLaVA fine-tuning entries in the preserved OSCaR manifest: `28,308`
- backbone family: `LLaVA v1.5` with `Vicuna 7B/13B` and `CLIP ViT-L/336`

## Project Links

- Project page: `https://nguyennm1024.github.io/OSCaR/`
- Paper: `https://aclanthology.org/2024.findings-naacl.226/`
- Code: `https://github.com/nguyennm1024/OSCaR`
- Dataset: `https://huggingface.co/datasets/ali-vosoughi/oscar-dataset`

Model repos:

- `https://huggingface.co/ali-vosoughi/oscar-llava-v1.5-7b-oscar-adapter`
- `https://huggingface.co/ali-vosoughi/oscar-llava-v1.5-13b-oscar-adapter`
- `https://huggingface.co/ali-vosoughi/oscar-llava-v1.5-13b-mixed-adapter`
- `https://huggingface.co/ali-vosoughi/oscar-llava-v1.5-7b-projector`
- `https://huggingface.co/ali-vosoughi/oscar-llava-v1.5-13b-projector`

## Authors

- [Nguyen Nguyen](https://nguyennm1024.github.io/)
- [Jing Bi](https://jing.vision/)
- [Ali Vosoughi](https://alivosoughi.com/)
- [Yapeng Tian](http://www.yapengtian.com/)
- [Pooyan Fazli](http://pooyanfazli.com/)
- [Chenliang Xu](http://www.cs.rochester.edu/~cxu22/)

## What This Repo Contains

- projector pretraining code for the LLaVA v1.5 stack
- OSCaR-only LoRA fine-tuning scripts for Vicuna 7B and 13B
- mixed-data 13B LoRA fine-tuning that combines OSCaR with LLaVA v1.5 mix data
- benchmark and open-world inference entrypoints
- text-generation evaluation scripts
- dataset-preparation utilities used around manifests, splits, and output conversion

## Reported Training Configuration

The public scripts reflect the paper and local training artifacts:

- base models: `lmsys/vicuna-7b-v1.5` and `lmsys/vicuna-13b-v1.5`
- vision tower: `openai/clip-vit-large-patch14-336`
- LoRA rank: `128`
- LoRA alpha: `256`
- epochs: `1`
- learning rate: `2e-4`
- batch size per device: `16` for OSCaR-only runs
- max sequence length: `2048`

The 13B mixed-data run also has a public script matching the logged local run:

- per-device batch size: `8`
- gradient accumulation: `2`
- save steps: `300`

## Quickstart

Environment setup is UV-based:

```bash
uv venv --python 3.10 .venv
source .venv/bin/activate
uv pip install -e .[train,inference,eval,release]
```

Detailed setup: [INSTALL.md](INSTALL.md)  
Training guide: [TRAIN.md](TRAIN.md)  
Inference guide: [INFERENCE.md](INFERENCE.md)  
Evaluation guide: [EVAL.md](EVAL.md)  
Release guide: [RELEASE.md](RELEASE.md)

## Repository Layout

- `llava/`: model, training, evaluation, and serving code
- `scripts/train/`: projector pretraining, LoRA fine-tuning, merge, and cluster launcher examples
- `scripts/infer/`: public inference wrappers for benchmark and open-world evaluation
- `scripts/eval/`: benchmark metric scripts
- `scripts/data/`: manifest, split, QA-generation, and output-conversion utilities
- `scripts/release/`: Hugging Face card generation and upload helpers
- `configs/deepspeed/`: public DeepSpeed configs
- `docs/`: release docs and GitHub Pages content

## Notes On Dataset And Weights

This repository is intentionally code-first. Large assets are kept out of GitHub:

- OSCaR dataset assets and manifests live in the Hugging Face dataset repo
- projector checkpoints, adapters, and merged-model release artifacts live in the Hugging Face model repos

The code here expects those assets to be mounted or downloaded locally and then
referenced through CLI arguments or environment variables.

## Public Release Structure

OSCaR is intentionally split across public surfaces:

- this GitHub repository for code, install instructions, and reproducibility docs
- the Hugging Face dataset repo for released OSCaR assets and metadata
- the Hugging Face model repos for projector checkpoints and adapter weights
- the project page for paper-oriented presentation and public links

If you are landing here first, the project page is the shortest path to the
paper, code, dataset, and weights:

- `https://nguyennm1024.github.io/OSCaR/`

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

## Acknowledgments

OSCaR builds on the LLaVA codebase and training stack. We thank the LLaVA
team for their strong open-source release and the foundation it provided for
this work.

This project was sponsored by DARPA under Contract `HR00112220003`.
