#! /usr/bin/env python
### Script for aligning reads
import argparse
import glob
from os.path import basename
from subprocess import call

parser=argparse.ArgumentParser(prog='NGSEP_pipeline_full', description='Script for align, postprocess and call reads using entirely NGSEP')
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

call('mkdir -p aln_res', shell=True)
call('mkdir -p logs', shell=True)
# java -jar NGSEPcore_<VERSION>.jar ReadsAligner -r <REF.fa> -i <SMPL>.fastq -s <SMPL> -o <SMPL>.bam > <SMPL>_aln.log
# java -jar picard.jar SortSam SO=coordinate CREATE_INDEX=true I=<SMPL>.bam O=<SMPL>_sorted.bam >& <SMPL>_sort.log
for i in reads:
    smpl = basename(i).split('.')[0]
    try:
        print('Start aligning sample %s' % smpl)
        bam_out= smpl +'_aln.bam'
        aln_cmd='''java -Xmx8g -jar src/NGSEPcore_4.1.0.jar ReadsAligner -r %s -i %s -s %s -o aln_res/%s > logs/%s_aln.log''' % (ref, i, smpl, bam_out, smpl)
        print(aln_cmd)
        call(aln_cmd, shell=True)
        picard_cmd = '''java -Xmx8g -jar src/picard.jar SortSam SO=coordinate CREATE_INDEX=true I=aln_res/%s O=aln_res/%s_sorted.bam >& logs/%s_sort.log''' % (bam_out, smpl, smpl)
        print(picard_cmd)
        call(picard_cmd, shell=True)
    except:
        print('Sample %s failed' % smpl, file=open('logs/failed_samples_info.txt', 'a'))

# Multisamples SNPs calling

#java -jar src/NGSEPcore_4.1.0.jar MultisampleVariantsDetector -maxBaseQS 30 -maxAlnsPerStartPos 100 -r <REF.fa> -o population.vcf <BAM_FILES>* >& population.log
snp_allign_cmd = '''java -Xmx8g -jar src/NGSEPcore_4.1.0.jar MultisampleVariantsDetector -maxBaseQS 30 -maxAlnsPerStartPos 100 -r %s -o FINAL_SNP_file.vcf res_aln/*_sorted.bam >& logs/population.log''' % ref
print(snp_allign_cmd)
call(snp_allign_cmd, shell=True)