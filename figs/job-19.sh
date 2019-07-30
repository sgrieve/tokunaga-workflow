#!/bin/bash
#$ -cwd
#$ -j y
#$ -N toku-figs19
#$ -o /data/Geog-c2s2/toku/
#$ -pe smp 1
#$ -l node_type=dn
#$ -l h_vmem=10G
#$ -l h_rt=20:00:0

module load python/3.6.3
module load gdal/2.3.1
module load proj/5.2.0

source /data/home/faw513/toku-fig-env/bin/activate

python /data/home/faw513/tokunaga-workflow/figs/precip_TSS.py 0.98
