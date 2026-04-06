#!/usr/bin/env bash
set -euo pipefail

#SBATCH --job-name=finetune_oscar               # Job name
#SBATCH --output=result-%j.out          # Standard output and error log (%j expands to jobId)
#SBATCH --error=result-%j.err           # Error File (%j expands to jobId)
#SBATCH --partition=macula                # Partition (queue) to submit to
#SBATCH --nodes=1                       # Number of nodes
#SBATCH --ntasks=1                      # Number of tasks (processes)
#SBATCH --cpus-per-gpu=10               # CPU cores/threads per gpu
#SBATCH --mem=400GB                      # Memory (in MB)
#SBATCH --time=3-00:00:00                 # Time limit hrs:min:sec
#SBATCH --gres=gpu:a6000:4                 # GPU
#SBATCH --export=ALL                    # Export you current env to the job env

# Your program execution follows
echo "Starting my SLURM job - the job ID is $SLURM_JOB_ID"
echo "Running on host $(hostname)"
echo "Time is $(date)"
echo "Directory is $(pwd)"
echo "SLURM job size detected as $SLURM_JOB_NUM_NODES nodes, $SLURM_NTASKS tasks"

# Example launcher for the public repo.
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)

cd "$REPO_ROOT"

if [[ -n "${UV_ENV_DIR:-}" ]]; then
  source "$UV_ENV_DIR/bin/activate"
elif [[ -d "$REPO_ROOT/.venv" ]]; then
  source "$REPO_ROOT/.venv/bin/activate"
fi

export HF_HOME="${HF_HOME:-$HOME/.cache/huggingface}"
export TRANSFORMERS_CACHE="${TRANSFORMERS_CACHE:-$HF_HOME/transformers}"

bash "$REPO_ROOT/scripts/train/finetune_v1_5_13b_oscar_lora.sh"

echo "Job finished with exit code $? at: $(date)"
