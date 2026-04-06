# Inference

OSCaR publishes benchmark and open-world inference paths for the released
adapter checkpoints. Merged full-model checkpoints are optional local outputs
that you can build yourself, but they are not part of the public release.

## Released Weights

- Released OSCaR weights are LoRA adapters plus projector checkpoints.
- Released adapter repos require `--model-base`.
- Merged local exports do not require `--model-base`, but those are not hosted
  as part of the current OSCaR release.

## Quickstart With The Released 13B Adapter

```bash
huggingface-cli download ali-vosoughi/oscar-llava-v1.5-13b-oscar-adapter --local-dir ../oscar-llava-v1.5-13b-oscar-adapter
python -m llava.serve.cli \
  --model-path ../oscar-llava-v1.5-13b-oscar-adapter \
  --model-base lmsys/vicuna-13b-v1.5 \
  --image-file /path/to/image.jpg
```

## Benchmark Inference

The released benchmark split lives at:

- `../oscar-dataset/splits/data_mapping_final_EK_test.csv`

and its `image_path` values resolve correctly when:

- `PATH_PREFIX=../oscar-dataset/data`

```bash
DATASET_ROOT=../oscar-dataset \
PATH_PREFIX="$DATASET_ROOT/data" \
DATA_MAPPING="$DATASET_ROOT/splits/data_mapping_final_EK_test.csv" \
MODEL_PATH=../oscar-llava-v1.5-13b-oscar-adapter \
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
MODEL_PATH=../oscar-llava-v1.5-13b-oscar-adapter \
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
  --model-path ../oscar-llava-v1.5-13b-oscar-adapter \
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
  --model-path ../oscar-llava-v1.5-13b-oscar-adapter \
  --model-base lmsys/vicuna-13b-v1.5
```
