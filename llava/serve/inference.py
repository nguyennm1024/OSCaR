import argparse
import os
from pathlib import Path

import pandas as pd
import requests
import torch
from PIL import Image
from io import BytesIO

from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from llava.model.builder import load_pretrained_model
from llava.utils import disable_torch_init
from llava.mm_utils import process_images, tokenizer_image_token, get_model_name_from_path


def load_image(image_file):
    if image_file.startswith('http://') or image_file.startswith('https://'):
        response = requests.get(image_file)
        image = Image.open(BytesIO(response.content)).convert('RGB')
    else:
        image = Image.open(image_file).convert('RGB')
    return image

def resolve_image_path(image_path, args):
    if image_path.startswith("http://") or image_path.startswith("https://"):
        return image_path
    if os.path.isabs(image_path):
        return image_path
    if "storage" in image_path and args.legacy_ego4d_root:
        return os.path.join(args.legacy_ego4d_root, image_path)
    if "storage" not in image_path and args.legacy_epic_root:
        return os.path.join(args.legacy_epic_root, image_path)
    if args.path_prefix:
        return os.path.join(args.path_prefix, image_path)
    return image_path


def output_relative_path(image_path):
    path_parts = Path(image_path).parts
    anchors = ("object-state-data", "ego4d-video", "openworld-indomain", "openworld-outdomain")
    for anchor in anchors:
        if anchor in path_parts:
            anchor_index = path_parts.index(anchor)
            return Path(*path_parts[anchor_index:]).with_suffix(".txt")
    return Path(Path(image_path).name).with_suffix(".txt")


def process_and_save(image_path, model_name, args, model, tokenizer, image_processor, model_config, device, object_name):
    image = load_image(image_path)
    image_tensor = process_images([image], image_processor, model_config)
    image_tensor = image_tensor.to(device, dtype=torch.float16)
    if 'state_change' in image_path:
        inp = "Describe the state change and progress of the <object> through these frames".replace('<object>', object_name)
    else:
        inp = "Describe state of the <object> in this image in a detailed way".replace('<object>', object_name)
    print(f"Processing: {image_path}")

    if model_config.mm_use_im_start_end:
        inp = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN + '\n' + inp
    else:
        inp = DEFAULT_IMAGE_TOKEN + '\n' + inp

    input_ids = tokenizer_image_token(inp, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).to(device)

    with torch.inference_mode():
        output_ids = model.generate(
            input_ids,
            images=image_tensor,
            do_sample=True if args.temperature > 0 else False,
            temperature=args.temperature,
            max_new_tokens=args.max_new_tokens)
        

    outputs = tokenizer.decode(output_ids[0, input_ids.shape[1]:]).strip()

    model_name_part = model_name.split(os.sep)[-1]
    output_path = Path(args.output_root) / model_name_part / output_relative_path(image_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as file:
        file.write(outputs)


def main(args):
    # Model
    disable_torch_init()

    model_name = get_model_name_from_path(args.model_path)
    if len(model_name) < 3:
        model_name = args.model_path.split('/')[1]
    
    tokenizer, model, image_processor, context_len = load_pretrained_model(args.model_path, args.model_base, model_name, args.load_8bit, args.load_4bit, device=args.device)
    

    data = pd.read_csv(args.data_mapping)
    file_paths = data["image_path"].tolist()
    object_names = data["object"].tolist()
    for i, image_path in enumerate(file_paths):
        resolved_path = resolve_image_path(image_path, args)
        process_and_save(resolved_path, model_name, args, model, tokenizer, image_processor, model.config, args.device, object_names[i])


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="facebook/opt-350m")
    parser.add_argument("--model-base", type=str, default=None)
    parser.add_argument("--data-mapping", type=str, required=True)
    parser.add_argument("--path-prefix", type=str, default="")
    parser.add_argument("--legacy-ego4d-root", type=str, default="")
    parser.add_argument("--legacy-epic-root", type=str, default="")
    parser.add_argument("--output-root", type=str, default="outputs/benchmark")
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--load-8bit", action="store_true")
    parser.add_argument("--load-4bit", action="store_true")
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    main(args)
