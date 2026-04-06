# Release

OSCaR is published as a coordinated GitHub + Hugging Face release:

- GitHub code repo: `nguyennm1024/OSCaR`
- Hugging Face dataset: `ali-vosoughi/oscar-dataset`
- Hugging Face model namespace: `ali-vosoughi`

## Prepare The Staged Bundle

From the bundle root:

```bash
uv venv --python 3.10 .venv
source .venv/bin/activate
uv pip install -e ./release_repos/github/OSCaR[release]
python ./release_repos/github/OSCaR/scripts/release/prepare_hf_release.py \
  --bundle-root /path/to/llava_statechange_hf_release_bundle \
  --namespace ali-vosoughi
```

That command generates:

- dataset card at `release_repos/huggingface/datasets/llava-statechange-dataset/README.md`
- normalized metadata tables under `metadata/`
- model cards in each staged model directory
- `release_repos/huggingface/models/upload_manifest.json`

## Publish To Hugging Face

Authenticate with a token through the environment only:

```bash
export HF_TOKEN=...
python ./release_repos/github/OSCaR/scripts/release/publish_hf_release.py \
  --bundle-root /path/to/llava_statechange_hf_release_bundle \
  --namespace ali-vosoughi
```

Notes:

- adapter and projector repos are uploaded when their local staging folders exist
- merged-model repos are skipped unless the corresponding merged model folders are present
- the token is never written to tracked files

## Resumable Dataset Upload

The dataset is large enough that it should be uploaded from `tmux` with the
resumable uploader instead of one monolithic pass.

From the bundle root:

```bash
export HF_TOKEN=...
./upload_oscar_dataset_tmux.sh |& tee upload_oscar_dataset.log
```

If the session is interrupted, rerun the same command. Progress is tracked in:

```text
/path/to/llava_statechange_hf_release_bundle/.hf_dataset_upload_state.json
```

The uploader commits:

- root `README.md`
- `splits/`
- `manifests/`
- `metadata/`
- `eval/`
- annotation folders
- `data/object-state-data/` in participant-prefix batches such as `P01`, `P02`, `P22`

## Publish The GitHub Repo

The project page is served from `docs/` on `main`. After pushing the branch,
enable GitHub Pages in the repository settings with:

- Source: `Deploy from a branch`
- Branch: `main`
- Folder: `/docs`
