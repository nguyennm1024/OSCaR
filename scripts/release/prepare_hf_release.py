#!/usr/bin/env python3
"""Prepare Hugging Face dataset/model staging folders for the OSCaR release."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable


MODEL_RELEASES = {
    "llava-v1.5-7b-lora-oscar-adapter": {
        "repo_name": "oscar-llava-v1.5-7b-oscar-adapter",
        "title": "OSCaR LLaVA v1.5 7B Adapter",
        "artifact_type": "adapter",
        "base_model": "lmsys/vicuna-7b-v1.5",
        "training_data": "OSCaR-only fine-tuning manifest (`llava_data.json`)",
        "load_snippet": "python -m llava.serve.cli --model-path ali-vosoughi/oscar-llava-v1.5-7b-oscar-adapter --model-base lmsys/vicuna-7b-v1.5 --image-file /path/to/image.jpg",
    },
    "llava-v1.5-13b-lora-oscar-adapter": {
        "repo_name": "oscar-llava-v1.5-13b-oscar-adapter",
        "title": "OSCaR LLaVA v1.5 13B Adapter",
        "artifact_type": "adapter",
        "base_model": "lmsys/vicuna-13b-v1.5",
        "training_data": "OSCaR-only fine-tuning manifest (`llava_data.json`)",
        "load_snippet": "python -m llava.serve.cli --model-path ali-vosoughi/oscar-llava-v1.5-13b-oscar-adapter --model-base lmsys/vicuna-13b-v1.5 --image-file /path/to/image.jpg",
    },
    "llava-v1.5-13b-lora-mixed-adapter": {
        "repo_name": "oscar-llava-v1.5-13b-mixed-adapter",
        "title": "OSCaR LLaVA v1.5 13B Mixed Adapter",
        "artifact_type": "adapter",
        "base_model": "lmsys/vicuna-13b-v1.5",
        "training_data": "OSCaR plus the upstream LLaVA v1.5 mixed visual-instruction manifest (`llava_final.json`)",
        "load_snippet": "python -m llava.serve.cli --model-path ali-vosoughi/oscar-llava-v1.5-13b-mixed-adapter --model-base lmsys/vicuna-13b-v1.5 --image-file /path/to/image.jpg",
    },
    "llava-v1.5-7b-pretrain-projector": {
        "repo_name": "oscar-llava-v1.5-7b-projector",
        "title": "OSCaR LLaVA v1.5 7B Projector",
        "artifact_type": "projector",
        "base_model": "openai/clip-vit-large-patch14-336",
        "training_data": "projector pretraining assets used before OSCaR LoRA fine-tuning",
        "load_snippet": "bash scripts/train/pretrain_v1_5_13b_projector.sh",
    },
    "llava-v1.5-13b-pretrain-projector": {
        "repo_name": "oscar-llava-v1.5-13b-projector",
        "title": "OSCaR LLaVA v1.5 13B Projector",
        "artifact_type": "projector",
        "base_model": "openai/clip-vit-large-patch14-336",
        "training_data": "projector pretraining assets used before OSCaR LoRA fine-tuning",
        "load_snippet": "bash scripts/train/pretrain_v1_5_13b_projector.sh",
    },
}

MERGED_RELEASES = {
    "oscar-llava-v1.5-7b-oscar": "Merged full-model export built from the OSCaR-only 7B adapter.",
    "oscar-llava-v1.5-13b-oscar": "Merged full-model export built from the OSCaR-only 13B adapter.",
    "oscar-llava-v1.5-13b-mixed": "Merged full-model export built from the mixed-data 13B adapter.",
}


def infer_source(clip_id: str) -> str:
    if re.match(r"^P\d{2}_", clip_id):
        return "epic-kitchens"
    if re.match(r"^[0-9a-f]{8}-", clip_id):
        return "ego4d"
    return "unknown"


def read_json(path: Path):
    with path.open() as handle:
        return json.load(handle)


def read_csv_rows(path: Path) -> list[dict]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def clip_id_from_image_path(image_path: str) -> str | None:
    parts = Path(image_path).parts
    if len(parts) >= 2 and parts[0] == "object-state-data":
        return parts[1]
    return None


def render_dataset_card(summary: dict, namespace: str, dataset_repo: str) -> str:
    return f"""---
pretty_name: OSCaR
language:
- en
license: other
task_categories:
- image-to-text
task_ids:
- image-captioning
size_categories:
- 10K<n<100K
---

# OSCaR

OSCaR is the public dataset release for the NAACL 2024 paper
_Object State Captioning and State Change Representation_.

This release packages the preserved OSCaR image assets, fine-tuning manifests,
benchmark split metadata, and state-caption sidecars used around the LLaVA-based
training and evaluation workflow published in the
[OSCaR GitHub repository](https://github.com/nguyennm1024/OSCaR).

## Release Summary

- Paper-reported scale: **14,084** annotated segments across EPIC-KITCHENS and Ego4D.
- Public raw asset tree in this release: **{summary['raw_clip_dirs']:,}** clip directories under `data/object-state-data`.
- Full preserved image-caption mapping: **{summary['full_mapping_rows']:,}** rows across **{summary['full_mapping_clip_dirs']:,}** clips.
- LLaVA fine-tuning manifest: **{summary['llava_entries']:,}** image-level conversations across **{summary['llava_clip_dirs']:,}** clips.
- Human-verified EPIC benchmark split: **{summary['ek_test_rows']:,}** rows / **{summary['ek_test_clips']:,}** clips / 4 caption slots.
- Sidecar annotations included: **{summary['state_change_json_count']:,}** state-change JSON files, **{summary['qa_json_count']:,}** QA JSON files, **{summary['conversation_json_count']:,}** conversation JSON files.
- Open-world evaluation metadata included: **{summary['openworld_records']:,}** Ego4D records and **{summary['openworld_epic_records']:,}** EPIC-KITCHENS records.

## What Is Included

- `data/object-state-data/`: preserved OSCaR frame directories and `state_change.jpg` composites.
- `manifests/llava_data.json`: OSCaR fine-tuning manifest used for adapter training.
- `splits/data_mapping_final_EK_test.csv`: held-out human-verified EPIC benchmark split.
- `metadata/data_mapping_final.csv`: full preserved image-to-caption mapping.
- `metadata/video-object.csv`: narration-to-object/action table.
- `metadata/ego4d_data.csv`: preserved Ego4D action/object metadata.
- `annotations/state-change-json/`: state caption JSON sidecars.
- `annotations/question-answers-clean/`: optional QA sidecars.
- `annotations/conversation-clean/`: optional conversation sidecars.
- `eval/openworld.json` and `eval/openworld-epic.json`: open-world evaluation prompts/metadata.

## Directory Layout

```text
oscar-dataset/
  data/object-state-data/
  manifests/llava_data.json
  splits/data_mapping_final_EK_test.csv
  metadata/data_mapping_final.csv
  metadata/segment_index.csv
  metadata/release_summary.json
  annotations/state-change-json/
  annotations/question-answers-clean/
  annotations/conversation-clean/
  eval/openworld.json
  eval/openworld-epic.json
```

## Important Notes

- The paper reports 14,084 annotated segments, but the preserved public asset tree
  in this release contains {summary['raw_clip_dirs']:,} clip directories. The
  released metadata keeps both the paper-scale claim and the preserved local
  archive counts explicit.
- `metadata/segment_index.csv` is the normalized release table generated from the
  preserved asset tree, the full mapping CSV, the fine-tuning manifest, and the
  benchmark split.
- Some open-world evaluation JSON records still reference original local EPIC or
  Ego4D frame roots. Those records are included for provenance and regeneration,
  not as a promise that every referenced raw frame path is redistributed here.

## Usage With OSCaR Code

The public code release expects a workspace like:

```text
workspace/
  OSCaR/
  oscar-dataset/
```

Then run, for example:

```bash
DATASET_ROOT=../oscar-dataset \\
bash scripts/train/finetune_v1_5_13b_oscar_lora.sh
```

## Provenance

- Source corpora: EPIC-KITCHENS and Ego4D, as described in the paper.
- Public code: `nguyennm1024/OSCaR`
- Public model namespace: `{namespace}`
- Dataset repo: `{namespace}/{dataset_repo}`

## Citation

```bibtex
@inproceedings{{nguyen2024oscar,
  title={{OSCaR: Object State Captioning and State Change Representation}},
  author={{Nguyen, Nguyen and Bi, Jing and Vosoughi, Ali and Tian, Yapeng and Fazli, Pooyan and Xu, Chenliang}},
  booktitle={{North American Chapter of the Association for Computational Linguistics (NAACL)}},
  year={{2024}}
}}
```
"""


def render_model_card(namespace: str, local_name: str, config: dict) -> str:
    repo_name = config["repo_name"]
    if config["artifact_type"] == "adapter":
        artifact_lines = """- `adapter_model.bin`
- `adapter_config.json`
- `config.json`
- `non_lora_trainables.bin`"""
        use_note = (
            "This is an adapter-only release. Pass `--model-base` with the matching "
            "Vicuna checkpoint when loading it."
        )
    else:
        artifact_lines = """- `config.json`
- `mm_projector.bin`"""
        use_note = (
            "This is a projector-only release. It is intended for the pretraining and "
            "fine-tuning workflow documented in the OSCaR code repository."
        )

    yaml_lines = [
        "---",
        f"library_name: {'peft' if config['artifact_type'] == 'adapter' else 'transformers'}",
        "tags:",
        "- llava",
        "- vision-language",
        "- oscar",
        "- egocentric-video",
        f"base_model: {config['base_model']}",
        "license: other",
        "---",
        "",
    ]
    return "\n".join(yaml_lines) + f"""# {config['title']}

This repository contains the **{config['artifact_type']}** artifact staged for the
OSCaR public release.

## Artifact Type

- Local staging directory: `{local_name}`
- Public repo id: `{namespace}/{repo_name}`
- Training data condition: {config['training_data']}

## Files

{artifact_lines}

## Loading

{use_note}

Example:

```bash
{config['load_snippet']}
```

## Training Configuration

- LLaVA v1.5 stack
- CLIP ViT-L/336 vision tower
- LoRA rank `128`
- LoRA alpha `256`
- learning rate `2e-4`
- 1 epoch
- max sequence length `2048`

## Related Resources

- Code: `https://github.com/nguyennm1024/OSCaR`
- Dataset: `https://huggingface.co/datasets/{namespace}/oscar-dataset`
- Paper: `https://aclanthology.org/2024.findings-naacl.226/`
"""


def build_segment_index(
    raw_root: Path,
    llava_manifest: Iterable[dict],
    full_mapping_rows: list[dict],
    ek_test_rows: list[dict],
) -> list[dict]:
    records: Dict[str, dict] = {}

    for entry in sorted(os.scandir(raw_root), key=lambda item: item.name):
        if not entry.is_dir():
            continue
        records[entry.name] = {
            "clip_id": entry.name,
            "source": infer_source(entry.name),
            "raw_asset_dir": f"data/object-state-data/{entry.name}",
            "in_llava_manifest": 0,
            "llava_entry_count": 0,
            "in_full_mapping": 0,
            "full_mapping_entry_count": 0,
            "in_ek_test_split": 0,
            "ek_test_entry_count": 0,
            "object": "",
            "action_narration": "",
            "state_change_json": "",
            "qa_json": "",
            "conversation_json": "",
        }

    for item in llava_manifest:
        clip_id = clip_id_from_image_path(item.get("image", ""))
        if not clip_id:
            continue
        record = records.setdefault(
            clip_id,
            {
                "clip_id": clip_id,
                "source": infer_source(clip_id),
                "raw_asset_dir": f"data/object-state-data/{clip_id}",
                "in_llava_manifest": 0,
                "llava_entry_count": 0,
                "in_full_mapping": 0,
                "full_mapping_entry_count": 0,
                "in_ek_test_split": 0,
                "ek_test_entry_count": 0,
                "object": "",
                "action_narration": "",
                "state_change_json": "",
                "qa_json": "",
                "conversation_json": "",
            },
        )
        record["in_llava_manifest"] = 1
        record["llava_entry_count"] += 1

    for row in full_mapping_rows:
        clip_id = clip_id_from_image_path(row["image_path"])
        if not clip_id:
            continue
        record = records.setdefault(
            clip_id,
            {
                "clip_id": clip_id,
                "source": infer_source(clip_id),
                "raw_asset_dir": f"data/object-state-data/{clip_id}",
                "in_llava_manifest": 0,
                "llava_entry_count": 0,
                "in_full_mapping": 0,
                "full_mapping_entry_count": 0,
                "in_ek_test_split": 0,
                "ek_test_entry_count": 0,
                "object": "",
                "action_narration": "",
                "state_change_json": "",
                "qa_json": "",
                "conversation_json": "",
            },
        )
        record["in_full_mapping"] = 1
        record["full_mapping_entry_count"] += 1
        record["object"] = record["object"] or row.get("object", "")
        record["action_narration"] = record["action_narration"] or row.get("action_narration", "")
        record["state_change_json"] = record["state_change_json"] or row.get("caption_path", "")
        record["qa_json"] = record["qa_json"] or row.get("qa_path", "")
        record["conversation_json"] = record["conversation_json"] or row.get("conversation_path", "")

    for row in ek_test_rows:
        clip_id = clip_id_from_image_path(row["image_path"])
        if not clip_id:
            continue
        record = records.setdefault(
            clip_id,
            {
                "clip_id": clip_id,
                "source": infer_source(clip_id),
                "raw_asset_dir": f"data/object-state-data/{clip_id}",
                "in_llava_manifest": 0,
                "llava_entry_count": 0,
                "in_full_mapping": 0,
                "full_mapping_entry_count": 0,
                "in_ek_test_split": 0,
                "ek_test_entry_count": 0,
                "object": "",
                "action_narration": "",
                "state_change_json": "",
                "qa_json": "",
                "conversation_json": "",
            },
        )
        record["in_ek_test_split"] = 1
        record["ek_test_entry_count"] += 1
        record["object"] = record["object"] or row.get("object", "")
        record["action_narration"] = record["action_narration"] or row.get("action_narration", "")
        record["state_change_json"] = record["state_change_json"] or row.get("caption_path", "")
        record["qa_json"] = record["qa_json"] or row.get("qa_path", "")
        record["conversation_json"] = record["conversation_json"] or row.get("conversation_path", "")

    return [records[key] for key in sorted(records)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle-root", required=True, type=Path)
    parser.add_argument("--namespace", default="ali-vosoughi")
    parser.add_argument("--dataset-repo", default="oscar-dataset")
    args = parser.parse_args()

    bundle_root = args.bundle_root.resolve()
    dataset_root = bundle_root / "release_repos" / "huggingface" / "datasets" / "llava-statechange-dataset"
    models_root = bundle_root / "release_repos" / "huggingface" / "models"
    metadata_root = dataset_root / "metadata"
    metadata_root.mkdir(parents=True, exist_ok=True)

    llava_manifest = read_json(dataset_root / "manifests" / "llava_data.json")
    full_mapping_rows = read_csv_rows(metadata_root / "data_mapping_final.csv")
    ek_test_rows = read_csv_rows(dataset_root / "splits" / "data_mapping_final_EK_test.csv")

    segment_index = build_segment_index(
        dataset_root / "data" / "object-state-data",
        llava_manifest,
        full_mapping_rows,
        ek_test_rows,
    )

    segment_index_path = metadata_root / "segment_index.csv"
    with segment_index_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(segment_index[0].keys()))
        writer.writeheader()
        writer.writerows(segment_index)

    summary = {
        "paper_segments": 14084,
        "raw_clip_dirs": sum(1 for entry in os.scandir(dataset_root / "data" / "object-state-data") if entry.is_dir()),
        "llava_entries": len(llava_manifest),
        "llava_clip_dirs": len({clip_id_from_image_path(item["image"]) for item in llava_manifest if clip_id_from_image_path(item["image"])}),
        "full_mapping_rows": len(full_mapping_rows),
        "full_mapping_clip_dirs": len({clip_id_from_image_path(row["image_path"]) for row in full_mapping_rows if clip_id_from_image_path(row["image_path"])}),
        "ek_test_rows": len(ek_test_rows),
        "ek_test_clips": len({clip_id_from_image_path(row["image_path"]) for row in ek_test_rows if clip_id_from_image_path(row["image_path"])}),
        "ek_test_caption_keys": dict(Counter(row["caption_key"] for row in ek_test_rows)),
        "state_change_json_count": sum(1 for entry in os.scandir(dataset_root / "annotations" / "state-change-json") if entry.name.endswith(".json")),
        "qa_json_count": sum(1 for entry in os.scandir(dataset_root / "annotations" / "question-answers-clean") if entry.name.endswith(".json")),
        "conversation_json_count": sum(1 for entry in os.scandir(dataset_root / "annotations" / "conversation-clean") if entry.name.endswith(".json")),
        "openworld_records": len(read_json(dataset_root / "eval" / "openworld.json")),
        "openworld_epic_records": len(read_json(dataset_root / "eval" / "openworld-epic.json")),
    }
    with (metadata_root / "release_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    (dataset_root / "README.md").write_text(
        render_dataset_card(summary, args.namespace, args.dataset_repo)
    )

    upload_manifest = {"dataset": f"{args.namespace}/{args.dataset_repo}", "models": []}
    for local_name, config in MODEL_RELEASES.items():
        local_dir = models_root / local_name
        if not local_dir.exists():
            continue
        (local_dir / "README.md").write_text(render_model_card(args.namespace, local_name, config))
        upload_manifest["models"].append(
            {
                "local_dir": local_name,
                "repo_id": f"{args.namespace}/{config['repo_name']}",
                "repo_type": "model",
                "artifact_type": config["artifact_type"],
            }
        )

    for repo_name, description in MERGED_RELEASES.items():
        local_dir = models_root / repo_name
        upload_manifest["models"].append(
            {
                "local_dir": repo_name,
                "repo_id": f"{args.namespace}/{repo_name}",
                "repo_type": "model",
                "artifact_type": "merged",
                "present": local_dir.exists(),
                "description": description,
            }
        )

    with (models_root / "upload_manifest.json").open("w") as handle:
        json.dump(upload_manifest, handle, indent=2, sort_keys=True)

    print(f"Wrote {segment_index_path}")
    print(f"Wrote {(metadata_root / 'release_summary.json')}")
    print(f"Wrote {(dataset_root / 'README.md')}")
    print(f"Wrote {(models_root / 'upload_manifest.json')}")


if __name__ == "__main__":
    main()
