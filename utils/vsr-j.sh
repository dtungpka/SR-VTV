#!/bin/bash
#SBATCH --job-name=VSR-VTV
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=00:30:00
#SBATCH --mail-type=end          
#SBATCH --mail-user=21010294@st.phenikaa-uni.edu.vn
#SBATCH --gres=gpu:1
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err

module load cuda
module load python
python tools/test.py configs/001_localimplicitsr_rdn_div2k_g1_c64b16_1000k_unfold_lec_mulwkv_res_nonlocal.py pretrain_model/rdn-ciaosr.pth
