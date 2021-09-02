import os
import argparse
import glob
from os.path import basename

parser=argparse.ArgumentParser(prog='NGSEP_aln_slurm', description='Script for creating slurm jobs for aligning and postprocessing reads using entirely NGSEP')
parser.add_argument('-i', '--input', dest='fastqreads', help='The folder with your fastq reads')
parser.add_argument('-r', '--referencegenome', dest='ref',
                    help='The reference genome file')
#parser.add_argument('-o', '--output', dest='outfolder', help='The output folder')
arg=parser.parse_args()

## Check if there is some parameter missing
if 'None' in str(arg):
        parser.error('Input parameter missing!! Please check your command line parameters with -h or --help')

## sample params
fastq=arg.fastqreads.split('/')[0] # just for avoid to duplication of the '/' at the end
ref=arg.ref
reads=glob.glob('%s/*' % fastq)

slurm_header = '''#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --mem=64gb
#SBATCH --job-name=%s
#SBATCH --error=/work/agro932/sybarreral/agrobinf/sybarreral/log/%s.err
#SBATCH --output=/work/agro932/sybarreral/agrobinf/sybarreral/log/%s.out

module load java/12
module load python/3.8

mkdir -p logs
mkdir -p aln_res

'''

for i in reads:
    sample = basename(i).split('.')[0]
    slurm = slurm_header%(sample, sample, sample)
    bam_out= sample +'_aln.bam'
    aln_cmd='''java -Xmx64g -jar src/NGSEPcore_4.1.0.jar ReadsAligner -r %s -i %s -s %s -o aln_res/%s > logs/%s_aln.log\n''' % (ref, i, sample, bam_out, sample)
    slurm += aln_cmd
    picard_cmd = '''java -Xmx64g -jar src/picard.jar SortSam SO=coordinate CREATE_INDEX=true I=aln_res/%s O=aln_res/%s_sorted.bam >& logs/%s_sort.log\n''' % (bam_out, sample, sample)
    slurm += picard_cmd
    with open('NGSEP_align_%s.slurm'%sample, 'w') as f:
                f.write(slurm)
