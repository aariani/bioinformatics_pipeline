import os
import argparse
import glob
from os.path import basename

parser=argparse.ArgumentParser(prog='bowtie2_aln_slurm', description='Script for creating slurm jobs for aligning reads with bowtie2')
parser.add_argument('-i', '--input', dest='fastqreads', help='The folder with your fastq reads')
arg=parser.parse_args()

## Check if there is some parameter missing
if 'None' in str(arg):
        parser.error('Input parameter missing!! Please check your command line parameters with -h or --help')

## sample params
fastq=arg.fastqreads.split('/')[0] # just for avoid to duplication of the '/' at the end
reads=glob.glob('%s/*' % fastq)

slurm_header = '''#!/bin/sh
#SBATCH --ntasks-per-node=4
#SBATCH --nodes=1
#SBATCH --mem=56gb
#SBATCH --time=20:00:00
#SBATCH --job-name=BTmap_%s
#SBATCH --mail-user=sybarreral@huskers.unl.edu
#SBATCH --mail-type=ALL
#SBATCH --error=/work/agro932/sybarreral/agrobinf/sybarreral/log/map_bt2_%s.err
#SBATCH --output=/work/agro932/sybarreral/agrobinf/sybarreral/log/map_bt2_%s.out

module load bowtie/2.3

IDXPTH=/work/agro932/sybarreral/agrobinf/sybarreral/project/ucdReads/H2214/NGSEP_varcall_full/REF
READPTH=/work/agro932/sybarreral/agrobinf/sybarreral/project/ucdReads/H2214/NGSEP_varcall_full/FASTQ

'''

for i in reads:
    sample = basename(i).split('.')[0]
    slurm = slurm_header%(sample, sample, sample)
    aln_cmd='''bowtie2 --local -p 4 -N 1 -x $IDXPTH/Pacutifolius -U $READPTH/%s -S aln_res/%s_pha.sam\n''' % (basename(i), sample)
    slurm += aln_cmd
    with open('bowtie2_align_%s.slurm'%sample, 'w') as f:
                f.write(slurm)
