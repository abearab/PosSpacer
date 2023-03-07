import gzip
from Bio import SeqIO
import pandas as pd
import polars as pl


def fastq_to_dataframe(fastq_file_path: str) -> pd.DataFrame:
    """
    Reads a FASTQ file and returns a Polars DataFrame with the following columns:
    - 'id': the sequence ID (e.g. "@SEQ_ID")
    - 'seq': the nucleotide sequence
    - 'qual': the sequence quality scores
    """
    def read_records(file_path):
        if file_path.endswith('.gz'):
            handle = gzip.open(file_path, "rt")
        else:
            handle = open(file_path, "rt")

        for record in SeqIO.parse(handle, "fastq"):
            yield (str(record.id), str(record.seq), str(record.letter_annotations["phred_quality"]))

        handle.close()

    # Read the FASTQ file into a list of tuples
    records = list(read_records(fastq_file_path))

    # Create a Polars DataFrame from the list of tuples
    df = pd.DataFrame(records, columns=['id', 'seq', 'qual'], dtype='str')

    df = pl.from_pandas(df)

    return df


def fastq_to_count_unique_seq(fastq_file_path: str) -> pl.DataFrame:
    df = fastq_to_dataframe(fastq_file_path)
    df_count = df.groupby('seq').count()

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

