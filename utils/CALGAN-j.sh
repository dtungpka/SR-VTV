#!/bin/bash
#SBATCH --job-name=VSR-CALGAN
#SBATCH --account=ddt_acc23
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --time=08:30:00
#SBATCH --mem=64gb
#SBATCH --cpus-per-task=16
#SBATCH --mail-type=end          
#SBATCH --mail-type=fail
#SBATCH --mail-type=begin
#SBATCH --mail-user=21010294@st.phenikaa-uni.edu.vn
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

module purge
module load cuda
module load python
source /home/21010294/VSR/VSREnv/bin/activate
module list
python -c "import sys; print(sys.path)"

which python
python --version
python cudacheck.py
squeue --me
cd /home/21010294/VSR/Repositories/CAL_GAN/
pip install .
python basicsr/test.py -opt options/test/CAL_GAN/test_CAL_GAN_Synthetic_test.yml

