import gzip
from Bio import SeqIO
from time import time
import pandas as pd
import polars as pl
from joblib import Parallel, delayed


def read_records(file_path, seq_only=True):
    if file_path.endswith('.gz'):
        handle = gzip.open(file_path, "rt")
    else:
        handle = open(file_path, "rt")

    records = []
    for record in SeqIO.parse(handle, "fastq"):
        if seq_only:
            records.append((str(record.seq)))
        else:
            records.append((str(record.id), str(record.seq), str(record.letter_annotations["phred_quality"])))

    handle.close()

    return records


def fastq_to_dataframe(fastq_file_path: str, num_threads: int, seq_only=True) -> pl.DataFrame:
    """
    Reads a FASTQ file and returns a Polars DataFrame with the following columns:
    - 'id': the sequence ID (e.g. "@SEQ_ID")
    - 'seq': the nucleotide sequence
    - 'qual': the sequence quality scores
    """
    t0 = time()
    print('load FASTQ file as a Polars DataFrame')

    # Use joblib to parallelize the reading of the FASTQ file
    records = Parallel(n_jobs=num_threads)(delayed(read_records)(fastq_file_path) for i in range(num_threads))

    # Flatten the list of records
    results = [record for sublist in records for record in sublist]

    # Create a Polars DataFrame from the list of tuples
    if seq_only:
        df = pd.DataFrame(results, columns=['seq'], dtype='str')
    else:
        df = pd.DataFrame(results, columns=['id', 'seq', 'qual'], dtype='str')
    df = pl.from_pandas(df)

    print("done in %0.3fs" % (time() - t0))

    return df


def fastq_to_count_unique_seq(fastq_file_path: str, num_threads: int) -> pl.DataFrame:
    df = fastq_to_dataframe(fastq_file_path, num_threads)

    t0 = time()
    print('Count unique sequences')

    df_count = df.groupby('seq').count()

    print("done in %0.3fs" % (time() - t0))

    return df_count


def map_sample_counts_to_library(library, sample):
    counts_df = library.copy()

    ol = list(set(library.index.tolist()) & set(sample['seq'].to_list()))

    counts_df['counts'] = 0
    counts_df.loc[ol, 'counts'] = sample.to_pandas().set_index('seq').loc[ol, 'count']

    return counts_df.reset_index(drop=True).set_index('oligoname')


