#!/bin/bash
#SBATCH --job-name=VSR-CAL
#SBATCH --account=ddt_acc23
#SBATCH --partition=normal
#SBATCH --ntasks=1
#SBATCH --time=08:30:00
#SBATCH --cpus-per-task=1
#SBATCH --array=1-3
#SBATCH --mail-type=end          
#SBATCH --mail-user=21010294@st.phenikaa-uni.edu.vn
#SBATCH --output=logs/%x_%j_%D.out
#SBATCH --error=logs/%x_%j_%D.err

# Specify the path to the config file
config=/work/21010294/VSR/CALGAN-J.config

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


INPUT=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $2}' $config)

OUTPUT=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $3}' $config)

#echo "This is array task ${SLURM_ARRAY_TASK_ID}, the sample name is ${INPUT} and the sex is ${OUTPUT}." >> output.txt


srun --quiet -n1 -c1 --exclusive python VTV-AVI.py -i $INPUT -o $OUTPUT
wait




