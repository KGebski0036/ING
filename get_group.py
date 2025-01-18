import pandas as pd
from collections import defaultdict


def group_and_sort_within_group(input_csv, group_column_index, extract_columns):

    df = pd.read_csv(input_csv, skiprows=1, header=None)

    # Replace NaN values in the payload column with empty strings
    df[extract_columns[0]] = df[extract_columns[0]].fillna("").astype(str)

    # Group by the group_column_index and sort within each group
    grouped = df.groupby(df[group_column_index])

    # Concatenate payloads within each group
    concatenated_payloads = (
        grouped[extract_columns[0]]
        .apply(lambda x: " ".join(filter(None, map(str.strip, x))).strip())
        .tolist()
    )
    # Extract the first label from the second specified column within each group
    labels = grouped[extract_columns[1]].first().tolist()
    return concatenated_payloads, labels
