# Inference

OSCaR publishes benchmark and open-world inference paths for adapter and merged
model variants.

## Adapter Versus Merged Models

- Adapter repos require `--model-base`
- Merged full-model repos do not require `--model-base`

## Benchmark Inference

```bash
DATA_MAPPING=/path/to/benchmark_mapping.csv \
MODEL_PATH=/path/to/oscar-adapter-or-merged-model \
MODEL_BASE=lmsys/vicuna-13b-v1.5 \
bash scripts/infer/run_benchmark_inference.sh
```

Optional inputs:

- `PATH_PREFIX` for relative image paths
- `LEGACY_EGO4D_ROOT` and `LEGACY_EPIC_ROOT` for older local layouts
- `OUTPUT_ROOT` to override the default output directory

Outputs default to:

```text
outputs/benchmark/<model-name>/...
```

## Open-World Inference

```bash
DATA_MAPPING=/path/to/openworld_mapping.csv \
MODEL_PATH=/path/to/oscar-adapter-or-merged-model \
MODEL_BASE=lmsys/vicuna-13b-v1.5 \
bash scripts/infer/run_openworld_inference.sh
```

Outputs default to:

```text
outputs/openworld/<model-name>/...
```

## CLI Demo

```bash
python -m llava.serve.cli \
  --model-path /path/to/model \
  --model-base lmsys/vicuna-13b-v1.5 \
  --image-file /path/to/image.jpg
```

## Gradio Demo

```bash
bash scripts/infer/launch_gradio_demo.sh
```

Then launch a worker in a second shell:

```bash
python -m llava.serve.model_worker \
  --host 0.0.0.0 \
  --controller http://localhost:10000 \
  --port 40000 \
  --worker http://localhost:40000 \
  --model-path /path/to/model \
  --model-base lmsys/vicuna-13b-v1.5
```
