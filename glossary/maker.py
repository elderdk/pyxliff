import pandas as pd
from collections import Counter


def _collapse_source(df):
    # Check for duplicates in the source terms and collapse
    count = dict(Counter(df[0]))
    for k, v in count.items():
        if v > 1:
            temp_df = df[df[0] == k]
            terms = '|'.join(list(temp_df[1]))

            new_row = pd.Series(data=[k, terms], index=df.columns)

            df = df[df[0] != k]
            df = df.append(new_row, ignore_index=True)

    return df


def _collapse_target(df):
    # Check for duplicates in the target terms and collapse
    count = dict(Counter(df[1]))
    for k, v in count.items():
        if v > 1:
            temp_df = df[df[1] == k]
            terms = '|'.join(list(temp_df[0]))

            new_row = pd.Series(data=[terms, k], index=df.columns)

            df = df[df[1] != k]
            df = df.append(new_row, ignore_index=True)

    return df


def collapse_duplicate_terms(df):
    
    df = _collapse_source(df)
    df = _collapse_target(df)

    return df
    

def make(filepath):

    df = pd.read_excel(filepath, header=None)
    df = collapse_duplicate_terms(df)
    return df


if __name__ == '__main__':
    
    filepath = './pyxliff/tests/testdata/excel_glossary.xlsx'
    df = make(filepath)