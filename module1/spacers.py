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


def apply_pattern_matching(df: pl.DataFrame, pattern: str) -> pl.DataFrame:
    """
    Applies pattern matching to the 'seq' column of the input Polars DataFrame and creates a new column 'matches'
    that indicates whether each sequence contains the specified pattern.
    """
    # Apply pattern matching to the 'seq' column using Polars' str.contains() method
    matches = df['seq'].str.contains(pattern)

    # Create a new DataFrame with the 'matches' column added to the original DataFrame
    new_df = df.with_column('matches', matches)

    return new_df

