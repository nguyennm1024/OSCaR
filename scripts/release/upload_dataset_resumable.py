#!/usr/bin/env python3
"""Resumable OSCaR dataset uploader for Hugging Face."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from huggingface_hub import HfApi
from huggingface_hub.errors import HfHubHTTPError


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
    always_upload: bool = False,
) -> None:
    if not always_upload and step_name in state["completed"]:
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
    if not always_upload:
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

    bundle_root = args.bundle_root.resolve()
    dataset_root = bundle_root / "release_repos" / "huggingface" / "datasets" / "llava-statechange-dataset"
    repo_id = f"{args.namespace}/{args.dataset_repo}"
    state_path = args.state_path or (bundle_root / STATE_FILENAME)

    if args.reset_state and state_path.exists():
        state_path.unlink()

    state = load_state(state_path)
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    api = HfApi(token=token) if token else HfApi()

    try:
        whoami = api.whoami()
    except HfHubHTTPError as exc:
        raise RuntimeError(
            "Hugging Face authentication failed. Either export a valid HF_TOKEN in this shell "
            "or run `hf auth login` before rerunning the uploader."
        ) from exc

    print(f"Authenticated as: {whoami['name']}")

    try:
        api.create_repo(repo_id=repo_id, repo_type="dataset", exist_ok=True)
    except HfHubHTTPError as exc:
        raise RuntimeError(
            f"Failed to create or access dataset repo `{repo_id}`. "
            "Verify that your token has write access to this account."
        ) from exc

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
        always_upload=True,
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
            always_upload=True,
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
