#!/bin/bash
#$ -cwd
#$ -j y
#$ -N precipitation
#$ -o /data/home/faw513/tokunaga-workflow/
#$ -pe smp 1
#$ -l node_type=dn
#$ -l h_vmem=2G
#$ -l h_rt=24:0:0

module load python/3.6.3
module load gdal/2.3.1
module load proj/5.2.0

source /data/home/faw513/toku-env/bin/activate

python /data/home/faw513/tokunaga-workflow/analysis/precip.py

