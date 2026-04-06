# Install

OSCaR publishes a UV-based environment story for code use and release tooling.

## 1. Create The Environment

```bash
uv venv --python 3.10 .venv
source .venv/bin/activate
```

## 2. Install The Package

```bash
uv pip install -e .[train,inference,eval,release]
```

## 3. Optional Developer Tools

```bash
uv pip install -e .[dev]
```

## 4. Download Public Assets

Recommended workspace layout:

```text
workspace/
  OSCaR/
  oscar-dataset/
  oscar-llava-v1.5-13b-oscar-adapter/
  oscar-llava-v1.5-13b-projector/
```

Download the released dataset:

```bash
huggingface-cli download ali-vosoughi/oscar-dataset --repo-type dataset --local-dir ../oscar-dataset
```

Download one released adapter:

```bash
huggingface-cli download ali-vosoughi/oscar-llava-v1.5-13b-oscar-adapter --local-dir ../oscar-llava-v1.5-13b-oscar-adapter
```

Download one released projector:

```bash
huggingface-cli download ali-vosoughi/oscar-llava-v1.5-13b-projector --local-dir ../oscar-llava-v1.5-13b-projector
```

## 5. Environment Variables

```bash
export HF_HOME="$HOME/.cache/huggingface"
export TRANSFORMERS_CACHE="$HF_HOME/transformers"
export WANDB_MODE=dryrun
export DATASET_ROOT=../oscar-dataset
export PATH_PREFIX="$DATASET_ROOT/data"
```

If you plan to use the optional QA-generation helper:

```bash
export OPENAI_API_KEY=...
```

## 6. Verify The Install

```bash
python -c "import llava; print('ok')"
python -m llava.serve.cli --help
python scripts/eval/eval_text_gen.py --help
```

## 7. Verify A Released Adapter

```bash
python -m llava.serve.cli \
  --model-path ../oscar-llava-v1.5-13b-oscar-adapter \
  --model-base lmsys/vicuna-13b-v1.5 \
  --image-file /path/to/image.jpg
```

## Notes

- Training and larger inference runs require a CUDA-capable GPU.
- The code repo does not bundle dataset payloads or model weights.
- Download the OSCaR dataset assets and model repos from Hugging Face, then
  point the scripts to those local paths.
- For the published benchmark split, use `PATH_PREFIX="$DATASET_ROOT/data"` so
  image paths like `object-state-data/...` resolve correctly.
