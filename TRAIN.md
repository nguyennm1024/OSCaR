# Training

This repository publishes the exact public scripts corresponding to the OSCaR
training pipeline:

- projector pretraining for LLaVA v1.5 13B
- OSCaR-only LoRA fine-tuning for Vicuna 7B
- OSCaR-only LoRA fine-tuning for Vicuna 13B
- mixed-data 13B LoRA fine-tuning using OSCaR plus LLaVA v1.5 mix data

## Expected Local Layout

Recommended layout after cloning the code repo and downloading data:

```text
workspace/
  OSCaR/
  oscar-dataset/
  oscar-llava-v1.5-13b-projector/
```

The fine-tune scripts default `DATASET_ROOT` to `../oscar-dataset`.
For released projector checkpoints, point `MM_PROJECTOR_PATH` to the downloaded
Hugging Face projector repo.

## Projector Pretraining

```bash
bash scripts/train/pretrain_v1_5_13b_projector.sh
```

Useful overrides:

- `PRETRAIN_DATA_PATH`
- `PRETRAIN_IMAGE_FOLDER`
- `OUTPUT_DIR`
- `MODEL_NAME_OR_PATH`
- `DEEPSPEED_CONFIG`

If you want to start from the released projector checkpoint instead of
re-pretraining it:

```bash
huggingface-cli download ali-vosoughi/oscar-llava-v1.5-13b-projector --local-dir ../oscar-llava-v1.5-13b-projector
export MM_PROJECTOR_PATH=../oscar-llava-v1.5-13b-projector/mm_projector.bin
```

## OSCaR-Only 13B LoRA Fine-Tuning

```bash
DATASET_ROOT=../oscar-dataset \
MM_PROJECTOR_PATH=../oscar-llava-v1.5-13b-projector/mm_projector.bin \
bash scripts/train/finetune_v1_5_13b_oscar_lora.sh
```

This matches the paper/local hyperparameters:

- LoRA rank `128`
- LoRA alpha `256`
- learning rate `2e-4`
- one epoch
- per-device batch size `16`
- max length `2048`

## OSCaR-Only 7B LoRA Fine-Tuning

```bash
DATASET_ROOT=../oscar-dataset \
MM_PROJECTOR_PATH=../oscar-llava-v1.5-7b-projector/mm_projector.bin \
bash scripts/train/finetune_v1_5_7b_oscar_lora.sh
```

Download the released 7B projector with:

```bash
huggingface-cli download ali-vosoughi/oscar-llava-v1.5-7b-projector --local-dir ../oscar-llava-v1.5-7b-projector
```

## Mixed-Data 13B LoRA Fine-Tuning

This corresponds to the logged local run that used `llava_final.json`.

```bash
DATASET_ROOT=../oscar-dataset \
DATA_PATH=../oscar-dataset/manifests/llava_final.json \
MM_PROJECTOR_PATH=../oscar-llava-v1.5-13b-projector/mm_projector.bin \
bash scripts/train/finetune_v1_5_13b_mixed_lora.sh
```

If `llava_final.json` is not published directly, build it from:

- OSCaR manifest
- upstream LLaVA v1.5 mix manifest

using:

```bash
python scripts/data/combine_data.py \
  --input-a ../oscar-dataset/manifests/llava_data.json \
  --input-b /path/to/llava_v1_5_mix665k.json \
  --output ../oscar-dataset/manifests/llava_final.json
```

## Removing Held-Out Benchmark Data

```bash
python scripts/data/remove_test_data.py \
  --data-path ../oscar-dataset/manifests/llava_data.json \
  --test-split ../oscar-dataset/splits/data_mapping_final_EK_test.csv \
  --output ../oscar-dataset/manifests/llava_data.train_only.json
```

## Merge Adapter Weights Into A Full Model

```bash
python scripts/train/merge_lora_weights.py \
  --model-path /path/to/adapter-repo-or-local-checkpoint \
  --model-base lmsys/vicuna-13b-v1.5 \
  --save-model-path /path/to/output-merged-model
```

Use `lmsys/vicuna-7b-v1.5` for the 7B adapter.
