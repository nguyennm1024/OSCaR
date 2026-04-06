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

## 4. Environment Variables

```bash
export HF_HOME="$HOME/.cache/huggingface"
export TRANSFORMERS_CACHE="$HF_HOME/transformers"
export WANDB_MODE=dryrun
```

If you plan to use the optional QA-generation helper:

```bash
export OPENAI_API_KEY=...
```

## 5. Verify The Install

```bash
python -c "import llava; print('ok')"
python -m llava.serve.cli --help
python scripts/eval/eval_text_gen.py --help
```

## Notes

- Training and larger inference runs require a CUDA-capable GPU.
- The code repo does not bundle dataset payloads or model weights.
- Download the OSCaR dataset assets and model repos from Hugging Face, then
  point the scripts to those local paths.
