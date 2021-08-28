
# Tutorial

# Download and extract the scripts

1. Go to the [main github page](https://github.com/aariani/bioinformatics_pipeline) of this repo and click on code (righ upper part) and click download ZIP.

2. Once downloaded copy the entire `NGSEP_varcall_full` folder in your working directory

# Prepare data and folder

How to use this script:

1. Copy your demultiplexed and trimmed fastq a folder within your working directory (name the directory `FASTQ`). There should be **a single FASTQ file for each sample** and each sample name must be unique

2. Copy your reference genome in a folder within your working directory (name the directory `REF`).

3. Chek that python3 is installed in your system


# Run the script

One you have prepared the different folders with the FASTQ and REF just type:

    python NGSEP_pipeline_full.py -i FASTQ -r REF/Pvulgaris_reference_genome.fa
    
After waiting (it might take long depending on your resources), you will have a file named FINAL_SNP_file.vcf in this folder. This is the unfiltered VCF file