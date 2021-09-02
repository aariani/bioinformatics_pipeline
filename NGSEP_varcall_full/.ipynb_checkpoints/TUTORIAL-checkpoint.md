
# Tutorial

# Download and extract the scripts

1. Go to the [main github page](https://github.com/aariani/bioinformatics_pipeline) of this repo and click on code button (green on the right upper part of the screen) and click download ZIP.

2. Once downloaded copy the entire `NGSEP_varcall_full` folder (with everything within)  in your working directory

# Prepare data and folder

How to use this script:

1. Copy your demultiplexed and trimmed fastq a folder within your working directory (name the directory `FASTQ`). There should be **a single FASTQ file for each sample** and each sample name must be unique

2. Copy your reference genome in a folder within your working directory (name the directory `REF`).

3. Chek that python3 is installed in your system


# Create slurm jobs

One you have prepared the different folders with the FASTQ and REF just type:

    python  NGSEP_aln_slurm.py -i FASTQ -r REF/YOUR_REFERENCE_GENOME_SEQUENCE
    
This sript will create a lot of different files (named NGSEP_align_SAMPLENAME.slurm) in the current folder. You can run them separately
