#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)

MODEL_NAME_OR_PATH="${MODEL_NAME_OR_PATH:-lmsys/vicuna-13b-v1.5}"
PRETRAIN_DATA_PATH="${PRETRAIN_DATA_PATH:-$REPO_ROOT/playground/data/LLaVA-Pretrain/blip_laion_cc_sbu_558k.json}"
PRETRAIN_IMAGE_FOLDER="${PRETRAIN_IMAGE_FOLDER:-$REPO_ROOT/playground/data/LLaVA-Pretrain/images}"
OUTPUT_DIR="${OUTPUT_DIR:-$REPO_ROOT/checkpoints/llava-v1.5-13b-pretrain}"
DEEPSPEED_CONFIG="${DEEPSPEED_CONFIG:-$REPO_ROOT/configs/deepspeed/zero2.json}"

deepspeed "$REPO_ROOT/llava/train/train_mem.py" \
    --deepspeed "$DEEPSPEED_CONFIG" \
    --model_name_or_path "$MODEL_NAME_OR_PATH" \
    --version plain \
    --data_path "$PRETRAIN_DATA_PATH" \
    --image_folder "$PRETRAIN_IMAGE_FOLDER" \
    --vision_tower openai/clip-vit-large-patch14-336 \
    --mm_projector_type mlp2x_gelu \
    --tune_mm_mlp_adapter True \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end False \
    --mm_use_im_patch_token False \
    --bf16 True \
    --output_dir "$OUTPUT_DIR" \
    --num_train_epochs 1 \
    --per_device_train_batch_size 32 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 1 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 24000 \
    --save_total_limit 1 \
    --learning_rate 1e-3 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --dataloader_num_workers 4 \
    --lazy_preprocess True \
    --report_to "${REPORT_TO:-wandb}"
