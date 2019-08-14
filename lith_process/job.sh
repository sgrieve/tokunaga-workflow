#!/bin/bash
#$ -cwd
#$ -j y
#$ -N lithology_1
#$ -o /data/Geog-c2s2/toku/
#$ -pe smp 1
#$ -l node_type=dn
#$ -l h_vmem=2G
#$ -l h_rt=0:30:0
#$ -t 1-8830
#$ -tc 100

module load python/3.6.3
module load gdal/2.3.1
module load proj/5.2.0

source /data/home/faw513/toku-env/bin/activate

# Parse parameter file to get variables.
number=$SGE_TASK_ID
paramfile=/data/home/faw513/tokunaga-workflow/bigfiles.txt

index=`sed -n ${number}p $paramfile | awk '{print $1}'`
variable1=`sed -n ${number}p $paramfile | awk '{print $2}'`

python /data/home/faw513/tokunaga-workflow/analysis/lith_para.py $variable1
