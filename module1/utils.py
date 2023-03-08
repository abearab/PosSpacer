import pandas as pd


def read_fasta(path):
    file = open(path)
    lines = file.read().splitlines()
    ids = [s[1:] for s in lines if '>' in s]
    n = [i for i, s in enumerate(lines) if '>' in s]
    n.append(len(lines))
    sequences = [''.join(lines[i + 1:j]) for i, j in zip(n[:-1], n[1:])]
    file.close()
    fa = dict(zip(ids, sequences))
    return fa


def read_library_to_dataframe(path):
    fa = read_fasta(path)
    df = pd.Series(fa).reset_index().rename({'index': 'oligoname', 0: 'sequence'}, axis=1).set_index('sequence')
    return df

