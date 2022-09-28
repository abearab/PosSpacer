fastqDIR=$1
sample=$2
adaptor5pR1=$3
adaptor5pR2=$4
length=$5
Jobs=$6

mkdir -p ${fastqDIR}
mkdir -p logs
mkdir -p logs/cutadapt
mkdir -p logs/pear/

echo -e `date`"\t"$sample"\tassemble"
# pear -j $Jobs \
#     -f ${fastqDIR}/${sample}_R1.fastq.gz \
#     -r ${fastqDIR}/${sample}_R2.fastq.gz \
#     -o ${fastqDIR}/${sample} &> logs/pear/${sample}.log.txt;
# wait;

# gzip -f ${fastqDIR}/${sample}.*.fastq

echo -e `date`"\t"$sample"\ttrim"
cutadapt -q 10 \
    -j $Jobs \
    --discard-untrimmed \
    --action "trim" \
    -a $adaptor5pR1";e=0.0001;required..."$adaptor5pR2";e=0.0001;required" \
    -o ${fastqDIR}/${sample}.assembled.trim.fastq.gz \
    ${fastqDIR}/${sample}.assembled.fastq.gz \
    &> logs/cutadapt/${sample}.log.txt;
wait;

echo -e `date`"\t"$sample"\tfilter-by-length"
cutadapt -m $(expr ${length} - 100) -M $length \
    -o ${fastqDIR}/${sample}.processed.fastq.gz \
    ${fastqDIR}/${sample}.assembled.trim.fastq.gz \
    &> logs/cutadapt/${sample}.log.2.txt;

echo -e `date`"\t"$sample"\tprocessed stats"
seqkit stats ${fastqDIR}/${sample}.processed.fastq.gz -T
