# PosSpacer
A framework for preprocessing multiplexed CRISPR libraries

> This repository is now pulic archive and the algorithm / workflow will be maintained as part of [ScreenPro2](https://github.com/ArcInstitute/ScreenPro2/) package, NGS module.
___
## Process FASTQ files
also see https://github.com/ArcInstitute/ScreenPro2/issues/28

### Assemble paired-end reads into single read format
- Tool: [PEAR - Paired-End reAd mergeR](https://www.h-its.org/software/pear-paired-end-read-merger/)
- Tasks:
  - Assemble and keep reads with significant overlapping regions
  - Keep assembled reads larger than given length

### Trimming task
- Tool: [Cutadapt](cutadapt.readthedocs.io)
- Tasks:
  - Keep reads with R1 5' adaptor and reverse complement of R2 5' adaptor in 5' and 3' of assembled read
  - Trim adaptors from the reads

## Count and location of spacers in sequencing reads
### Find location of given sequence 
- Tool: [Seqkit locate](https://bioinf.shenwei.me/seqkit/usage/#locate)
- Tasks:
  - Pattern matching for given sequences (e.g. direct repeats (DR) and spacers)
  - Record location of the patten matching 

also see https://github.com/wheretrue/biobear/issues/106

### Count expected oligo elements and report recombination events 
