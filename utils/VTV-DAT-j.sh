#!/bin/bash
#SBATCH --job-name=VSR-DATA
#SBATCH --account=ddt_acc23
#SBATCH --partition=normal
#SBATCH --nodes=1
#SBATCH --time=08:30:00
#SBATCH --mem=64gb
#SBATCH --cpus-per-task=16
#SBATCH --mail-type=end          
#SBATCH --mail-user=21010294@st.phenikaa-uni.edu.vn
#SBATCH --output=logs/%x_%j_%D.out
#SBATCH --error=logs/%x_%j_%D.err

module purge
module load cuda
module load python
source /home/21010294/VSR/VSREnv/bin/activate
module list
python -c "import sys; print(sys.path)"

which python
python --version
python /home/21010294/VSR/cudacheck.py
squeue --me
cd /work/21010294/VSR/
python create_LR.py
python conv-VTV.py /work/21010294/VSR/VTV-Data/Ver4


