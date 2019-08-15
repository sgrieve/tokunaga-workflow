#!/bin/bash
#$ -cwd
#$ -j y
#$ -N a_c_dict
#$ -o /data/Geog-c2s2/a_c_data/
#$ -pe smp 1
#$ -l node_type=dn
#$ -l h_vmem=2G
#$ -l h_rt=0:25:0
#$ -t 1-91
#$ -tc 100

module load python/3.6.3
module load gdal/2.3.1
module load proj/5.2.0

source /data/home/faw513/toku-fig-env/bin/activate

# Parse parameter file to get variables.
number=$SGE_TASK_ID
paramfile=/data/home/faw513/tokunaga-workflow/analysis/start_end.txt

index=`sed -n ${number}p $paramfile | awk '{print $1}'`
variable1=`sed -n ${number}p $paramfile | awk '{print $2}'`
variable2=`sed -n ${number}p $paramfile | awk '{print $3}'`

python /data/home/faw513/tokunaga-workflow/analysis/a_c_dict.py variable1 variable2
