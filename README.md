# PosSpacer
A framework for preprocessing multiplexed CRISPR libraries

___
## Process FASTQ files
### Assemble paired-end reads into single read format
- Tool: [PEAR - Paired-End reAd mergeR](https://www.h-its.org/software/pear-paired-end-read-merger/)
- Tasks:
  - Assemble and keep reads with significant overlapping regions

### Trimming task
- Tool: [Cutadapt](cutadapt.readthedocs.io)
- Tasks:
  - Exclude low qulity reads
  - Keep reads with 5' adaptor sequences of both R1 and R2
  - Trim adaptors from the reads
  - Keep reads with desired assembly size

## Count and location of spacers in sequencing reads
### Find location of given sequence 
- Tool: [Seqkit locate](https://bioinf.shenwei.me/seqkit/usage/#locate)
- Tasks:
  - Pattern matching for given sequences (e.g. direct repeats (DR) and spacers)
  - Record location of the patten matching 

### Count expected oligo elements and report recombination events 
