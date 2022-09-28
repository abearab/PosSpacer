# PosSpacer
A framework for preprocessing multiplexed CRISPR libraries

___
## Step 1 
Raw sequecning reads data cleanning 
- Tool: [Cutadapt](cutadapt.readthedocs.io)
- Tasks:
  - Exclude low qulity reads 
  - Keep reads with adaptor sequences and trim adaptors from the reads

## Step 2 
Assemble paired-end reads into single read format
- Tool: [PEAR - Paired-End reAd mergeR](https://www.h-its.org/software/pear-paired-end-read-merger/)
- Tasks:
  - Assemble and keep reads with significant overlapping regions
  - Assemble and keep reads with desired assembly size 

## Step 3
Find position of given sequence within assembled reads
- Tool: [Seqkit locate](https://bioinf.shenwei.me/seqkit/usage/#locate)
- Tasks:
  - Pattern matching for given sequences (e.g. direct repeats (DR) and spacers)
  - Record location of the patten matching 

## Step 4
Count expected oligo elements and report for recombination events 
