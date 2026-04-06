# Evaluation

OSCaR benchmark evaluation uses text-generation metrics over predicted JSON
files and human-verified ground-truth captions.

## Text-Generation Evaluation

```bash
python scripts/eval/eval_text_gen.py \
  --predicted-folder /path/to/predicted_json_folder \
  --groundtruth-ek /path/to/epic_groundtruth_json \
  --groundtruth-ego4d /path/to/ego4d_groundtruth_json
```

The script reports:

- average BLEU
- average ROUGE-1
- average ROUGE-2
- average ROUGE-L

## Output Conversion

If your inference outputs are still in per-frame `.txt` form, convert them to
the JSON format expected by the evaluator:

```bash
python scripts/data/convert_output_to_json.py \
  --root-folder /path/to/output_root
```

## Open-World Data Preparation

To assemble state-change image strips and a CSV mapping from open-world JSON:

```bash
python scripts/data/concat_state_frame.py \
  --json-file /path/to/openworld.json \
  --output-folder /path/to/openworld-output
```

## Optional QA-Based Utilities

The repository also contains optional QA-generation helpers in
`scripts/data/question_answerings/`. These are not required for training or
core benchmark inference, but they are included because they were part of the
broader local workflow around OSCaR data generation and analysis.
