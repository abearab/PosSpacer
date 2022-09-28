fastqDIR=$1
sample_id=$2
length=$3
Jobs=$4

mkdir -p logs
mkdir -p logs/pear/

pear -j $Jobs -m $length -n $length \
    -f ${fastqDIR}/${sample_id}_R1.trim.fastq.gz \
    -r ${fastqDIR}/${sample_id}_R2.trim.fastq.gz \
    -o ${fastqDIR}/${sample_id} \
    &> logs/pear/${sample_id}.log.txt;
wait;

gzip -f ${fastqDIR}/${sample_id}.*.fastq
