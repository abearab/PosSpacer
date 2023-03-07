import gzip
from Bio import SeqIO
from time import time
import pandas as pd
import polars as pl
import multiprocessing as mp


def read_records(file_path, queue, seq_only = True):
    if file_path.endswith('.gz'):
        handle = gzip.open(file_path, "rt")
    else:
        handle = open(file_path, "rt")

    for record in SeqIO.parse(handle, "fastq"):
        if seq_only:
            queue.put((str(record.seq)))
        else:
            queue.put((str(record.id), str(record.seq), str(record.letter_annotations["phred_quality"])))

    handle.close()
    queue.put(None)


def fastq_to_dataframe(fastq_file_path: str, num_threads: int, seq_only=True) -> pl.DataFrame:
    """
    Reads a FASTQ file and returns a Polars DataFrame with the following columns:
    - 'id': the sequence ID (e.g. "@SEQ_ID")
    - 'seq': the nucleotide sequence
    - 'qual': the sequence quality scores
    """
    t0 = time()
    print('load FASTQ file as a Polars DataFrame')

    manager = mp.Manager()
    queue = manager.Queue()
    pool = mp.Pool(num_threads, initializer=read_records, initargs=(fastq_file_path, queue, seq_only))

    results = []
    while True:
        record = queue.get()
        if record is None:
            break
        results.append(record)

    pool.close()
    pool.join()

    # Create a Polars DataFrame from the list of tuples
    if seq_only:
        df = pd.DataFrame(results, columns=['seq'], dtype='str')
    else:
        df = pd.DataFrame(results, columns=['id', 'seq', 'qual'], dtype='str')
    df = pl.from_pandas(df)

    print("done in %0.3fs" % (time() - t0))

    return df


def fastq_to_count_unique_seq(fastq_file_path: str, num_threads: int) -> pl.DataFrame:
    t0 = time()
    print('Count unique sequences')

    df = fastq_to_dataframe(fastq_file_path, num_threads)
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

