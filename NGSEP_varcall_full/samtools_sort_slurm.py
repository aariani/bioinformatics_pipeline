import os
import argparse
import glob
from os.path import basename

parser=argparse.ArgumentParser(prog='samtools_sort_slurm', description='Script for creating slurm jobs for samtools sort')
parser.add_argument('-i', '--input', dest='fastqreads', help='The folder with your fastq reads')
arg=parser.parse_args()

## Check if there is some parameter missing
if 'None' in str(arg):
        parser.error('Input parameter missing!! Please check your command line parameters with -h or --help')

## sample params
fastq=arg.fastqreads.split('/')[0] # just for avoid to duplication of the '/' at the end
reads=glob.glob('%s/*' % fastq)

slurm_header = '''#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --mem=64gb
#SBATCH --time=10:00:00
#SBATCH --job-name=sortReads_%s
#SBATCH --mail-user=sybarreral@huskers.unl.edu
#SBATCH --mail-type=ALL
#SBATCH --error=/work/agrobinf/SHARED/agrobinf2020/users/sybarreral/log/sort_%s.err
#SBATCH --output=/work/agrobinf/SHARED/agrobinf2020/users/sybarreral/log/sort_%s.out

module load samtools/1.9

'''

for i in reads:
    sample = basename(i).split('.')[0]
    slurm = slurm_header%(sample, sample, sample)
    aln_cmd='''samtools sort -o aln_res/%s_pha.bam aln_res/%s_pha.sam\n''' % (sample, sample)
    slurm += aln_cmd
    with open('samtools_sort_%s.slurm'%sample, 'w') as f:
                f.write(slurm)
