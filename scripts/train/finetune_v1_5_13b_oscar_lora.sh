#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
DATASET_ROOT="${DATASET_ROOT:-$REPO_ROOT/../oscar-dataset}"

export WANDB_MODE="${WANDB_MODE:-dryrun}"

deepspeed --master_port "${MASTER_PORT:-29700}" "$REPO_ROOT/llava/train/train_mem.py" \
    --lora_enable True --lora_r 128 --lora_alpha 256 --mm_projector_lr 2e-5 \
    --deepspeed "${DEEPSPEED_CONFIG:-$REPO_ROOT/configs/deepspeed/zero3.json}" \
    --model_name_or_path "${MODEL_NAME_OR_PATH:-lmsys/vicuna-13b-v1.5}" \
    --version v1 \
    --data_path "${DATA_PATH:-$DATASET_ROOT/manifests/llava_data.json}" \
    --image_folder "${IMAGE_FOLDER:-$DATASET_ROOT/data}" \
    --vision_tower openai/clip-vit-large-patch14-336 \
    --pretrain_mm_mlp_adapter "${MM_PROJECTOR_PATH:-$REPO_ROOT/checkpoints/llava-v1.5-13b-pretrain/mm_projector.bin}" \
    --mm_projector_type mlp2x_gelu \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end False \
    --mm_use_im_patch_token False \
    --image_aspect_ratio pad \
    --group_by_modality_length True \
    --bf16 True \
    --output_dir "${OUTPUT_DIR:-$REPO_ROOT/checkpoints/llava-v1.5-13b-lora-oscar}" \
    --num_train_epochs 1 \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 1 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 220 \
    --save_total_limit 1 \
    --learning_rate 2e-4 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --dataloader_num_workers 2 \
    --lazy_preprocess True
