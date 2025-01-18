import csv
from collections import defaultdict


def group_and_sort_within_group(input_csv, column_group_by, column_sort_by, keep_columns, output_csv=None):
    """
    Grupuje wiersze pliku CSV na podstawie wartości w kolumnie `column_group_by`,
    a następnie sortuje wiersze w każdej grupie według kolumny `column_sort_by`.

    :param keep_columns:
    :param input_csv: Ścieżka do pliku CSV wejściowego.
    :param column_group_by: Indeks kolumny, według której grupujemy dane.
    :param column_sort_by: Indeks kolumny, według której sortujemy dane w grupie.
    :param output_csv: Opcjonalna ścieżka do pliku wyjściowego.
    :return: Tablica tablic, gdzie każda podtablica zawiera wiersze jednej grupy.
    """
    grouped_data = defaultdict(list)

    # Wczytanie CSV
    with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        dups = True
        for row in reader:
            if dups:
                dups = False
                continue
            # Sprawdź, czy indeksy kolumn istnieją w wierszu
            if max(column_group_by, column_sort_by) < len(row):
                key = row[column_group_by]
                grouped_data[key].append(row)
            else:
                raise IndexError(f"Jeden z indeksów kolumn {column_group_by}, {column_sort_by} wykracza poza zakres wiersza: {row}")

    # Posortowanie wierszy w każdej grupie według `column_sort_by`
    sorted_groups = []
    for key, group in grouped_data.items():
        sorted_group = sorted(group, key=lambda x: x[column_sort_by])
        sorted_groups.append(sorted_group)

    sorted_groups2 = []

    if keep_columns != []:
        for group in sorted_groups:
            tmp_group = []
            tmp_is_attack = 0
            for item in group:
                tmp_element = []

                for i in keep_columns:
                    tmp_element.append(item[i])
                    tmp_is_attack = item[10]

                tmp_group.append(tmp_element)
            sorted_groups2.append([tmp_group, tmp_is_attack])
    else:
        return sorted_group

    return sorted_groups2


# input_csv = "generated_logs.csv"
#
# data = group_and_sort_within_group(input_csv, 2, 1, [2, 9])
#
# for i in data:
#     print(f"Grupa: {i[1]}")
#     for ii in i:
#         for iii in ii:
#             print(iii)
