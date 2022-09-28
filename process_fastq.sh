fastqDIR=$1
logDIR=$2
sample=$3
adaptor5p=$4
adaptor3p=$5
length=$6
Jobs=$7

mkdir -p ${fastqDIR}
mkdir -p ${logDIR}
mkdir -p ${logDIR}/cutadapt
mkdir -p ${logDIR}/pear/


echo -e `date`"\t"$sample"\tassemble";


pear -j $Jobs -q 10 -n ${length} \
    -f ${fastqDIR}/${sample}_R1.fastq.gz \
    -r ${fastqDIR}/${sample}_R2.fastq.gz \
    -o ${fastqDIR}/${sample} &> ${logDIR}/pear/${sample}.log.txt;
wait;
gzip -f ${fastqDIR}/${sample}.*.fastq
seqkit stats -j $Jobs ${fastqDIR}/${sample}.assembled.fastq.gz -T


echo -e `date`"\t"$sample"\ttrim";

cutadapt \
    -j ${Jobs} \
    --discard-untrimmed \
    --action "trim" \
    -a $adaptor5p";e=0.0001;required;..."$adaptor3p";e=0.0001;required" \
    -o ${fastqDIR}/${sample}.assembled.trim.fastq.gz \
    ${fastqDIR}/${sample}.assembled.fastq.gz \
    &> ${logDIR}/cutadapt/${sample}.log.txt;
wait;
seqkit stats -j $Jobs ${fastqDIR}/${sample}.assembled.trim.fastq.gz -T
