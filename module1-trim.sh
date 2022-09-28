fastqDIR=$1
sample_id=$2
adaptor5pR1=$3
adaptor5pR2=$4
Jobs=$5

mkdir -p ${fastqDIR}
mkdir -p logs
mkdir -p logs/cutadapt

cutadapt -q 10 \
    -j $Jobs \
    --discard-untrimmed \
    --action "trim" \
    --pair-filter=both \
    --pair-filter "both" \
    -g $adaptor5pR1 \
    -G $adaptor5pR2 \
    -o ${fastqDIR}/${sample_id}_R1.trim.fastq.gz -p ${fastqDIR}/${sample_id}_R2.trim.fastq.gz \
    ${fastqDIR}/${sample_id}_R1.fastq.gz ${fastqDIR}/${sample_id}_R2.fastq.gz \
    &> logs/cutadapt/${sample_id}.log.txt;
wait;
