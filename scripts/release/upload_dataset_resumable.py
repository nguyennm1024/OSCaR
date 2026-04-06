#!/usr/bin/env python3
"""Resumable OSCaR dataset uploader for Hugging Face."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from huggingface_hub import HfApi


STATE_FILENAME = ".hf_dataset_upload_state.json"


def load_state(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {"completed": []}


def save_state(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, indent=2, sort_keys=True))


def upload_step(
    *,
    api: HfApi,
    repo_id: str,
    src: Path,
    path_in_repo: str | None,
    step_name: str,
    state: dict,
    state_path: Path,
    allow_patterns: list[str] | None = None,
    ignore_patterns: list[str] | None = None,
) -> None:
    if step_name in state["completed"]:
        print(f"Skipping completed step: {step_name}")
        return

    print(f"Uploading step: {step_name}")
    api.upload_folder(
        repo_id=repo_id,
        repo_type="dataset",
        folder_path=str(src),
        path_in_repo=path_in_repo,
        allow_patterns=allow_patterns,
        ignore_patterns=ignore_patterns,
        commit_message=f"Upload {step_name}",
    )
    state["completed"].append(step_name)
    save_state(state_path, state)
    print(f"Completed step: {step_name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle-root", required=True, type=Path)
    parser.add_argument("--namespace", default="ali-vosoughi")
    parser.add_argument("--dataset-repo", default="oscar-dataset")
    parser.add_argument("--state-path", type=Path)
    parser.add_argument("--reset-state", action="store_true")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if not token:
        raise RuntimeError("Set HF_TOKEN or HUGGING_FACE_HUB_TOKEN before running this script.")

    bundle_root = args.bundle_root.resolve()
    dataset_root = bundle_root / "release_repos" / "huggingface" / "datasets" / "llava-statechange-dataset"
    repo_id = f"{args.namespace}/{args.dataset_repo}"
    state_path = args.state_path or (bundle_root / STATE_FILENAME)

    if args.reset_state and state_path.exists():
        state_path.unlink()

    state = load_state(state_path)
    api = HfApi(token=token)
    api.create_repo(repo_id=repo_id, repo_type="dataset", exist_ok=True)

    ignore_patterns = [".cache/**", "**/.cache/**"]

    upload_step(
        api=api,
        repo_id=repo_id,
        src=dataset_root,
        path_in_repo=None,
        step_name="root-readme",
        state=state,
        state_path=state_path,
        allow_patterns=["README.md"],
        ignore_patterns=ignore_patterns,
    )

    for name, path_in_repo in [
        ("splits", "splits"),
        ("manifests", "manifests"),
        ("metadata", "metadata"),
        ("eval", "eval"),
        ("annotations-state-change-json", "annotations/state-change-json"),
        ("annotations-question-answers-clean", "annotations/question-answers-clean"),
        ("annotations-conversation-clean", "annotations/conversation-clean"),
    ]:
        src = dataset_root / path_in_repo
        upload_step(
            api=api,
            repo_id=repo_id,
            src=src,
            path_in_repo=path_in_repo,
            step_name=name,
            state=state,
            state_path=state_path,
            ignore_patterns=ignore_patterns,
        )

    data_root = dataset_root / "data" / "object-state-data"
    prefixes = sorted(
        {
            directory.name.split("_")[0] if "_" in directory.name else directory.name[:3]
            for directory in data_root.iterdir()
            if directory.is_dir()
        }
    )
    for prefix in prefixes:
        upload_step(
            api=api,
            repo_id=repo_id,
            src=data_root,
            path_in_repo="data/object-state-data",
            step_name=f"data-{prefix}",
            state=state,
            state_path=state_path,
            allow_patterns=[f"{prefix}_*/*"],
            ignore_patterns=ignore_patterns,
        )

    print(f"Dataset upload finished. State file: {state_path}")


if __name__ == "__main__":
    main()
