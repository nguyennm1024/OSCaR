# OSCaR: Object State Captioning and State Change Representation

OSCaR is the public code release for the NAACL 2024 paper
[OSCaR: Object State Captioning and State Change Representation](https://arxiv.org/abs/2402.17128).

This repository publishes the LLaVA-derived training, inference, evaluation,
and data-preparation code used for OSCaR, alongside release-grade
documentation for the corresponding Hugging Face dataset and model repos.

## Release Surfaces

- Code: `https://github.com/nguyennm1024/OSCaR`
- Dataset: `https://huggingface.co/datasets/ali-vosoughi/oscar-dataset`
- Models: `https://huggingface.co/ali-vosoughi`
- Project page: `https://nguyennm1024.github.io/OSCaR/`

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

## Authors

- [Nguyen Nguyen](https://nguyennm1024.github.io/)
- [Jing Bi](https://jing.vision/)
- [Ali Vosoughi](https://alivosoughi.com/)
- [Yapeng Tian](http://www.yapengtian.com/)
- [Pooyan Fazli](http://pooyanfazli.com/)
- [Chenliang Xu](http://www.cs.rochester.edu/~cxu22/)

## Acknowledgments

OSCaR builds on the LLaVA codebase and training stack. We thank the LLaVA
team for their strong open-source release and the foundation it provided for
this work.

This project was sponsored by DARPA under Contract `HR00112220003`.
