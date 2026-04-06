#!/usr/bin/env python3
"""Create and upload OSCaR release repositories to Hugging Face."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from huggingface_hub import HfApi


def upload_folder(api: HfApi, repo_id: str, folder_path: Path, repo_type: str, private: bool) -> None:
    api.create_repo(repo_id=repo_id, repo_type=repo_type, private=private, exist_ok=True)
    if hasattr(api, "upload_large_folder"):
        api.upload_large_folder(
            repo_id=repo_id,
            repo_type=repo_type,
            folder_path=str(folder_path),
        )
    else:
        api.upload_folder(
            repo_id=repo_id,
            repo_type=repo_type,
            folder_path=str(folder_path),
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle-root", required=True, type=Path)
    parser.add_argument("--namespace", default="ali-vosoughi")
    parser.add_argument("--dataset-repo", default="oscar-dataset")
    parser.add_argument("--private", action="store_true")
    parser.add_argument("--skip-dataset", action="store_true")
    parser.add_argument("--skip-models", action="store_true")
    parser.add_argument("--fail-on-missing-merged", action="store_true")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    api = HfApi(token=token)

    bundle_root = args.bundle_root.resolve()
    dataset_root = bundle_root / "release_repos" / "huggingface" / "datasets" / "llava-statechange-dataset"
    models_root = bundle_root / "release_repos" / "huggingface" / "models"
    upload_manifest = json.loads((models_root / "upload_manifest.json").read_text())

    if not args.skip_dataset:
        dataset_repo_id = f"{args.namespace}/{args.dataset_repo}"
        print(f"Uploading dataset: {dataset_repo_id}")
        upload_folder(api, dataset_repo_id, dataset_root, "dataset", args.private)

    if not args.skip_models:
        for entry in upload_manifest["models"]:
            local_dir = models_root / entry["local_dir"]
            if not local_dir.exists():
                if entry.get("artifact_type") == "merged" and not args.fail_on_missing_merged:
                    print(f"Skipping missing merged model: {entry['repo_id']}")
                    continue
                raise FileNotFoundError(f"Missing local folder for {entry['repo_id']}: {local_dir}")
            print(f"Uploading model: {entry['repo_id']}")
            upload_folder(api, entry["repo_id"], local_dir, "model", args.private)


if __name__ == "__main__":
    main()
