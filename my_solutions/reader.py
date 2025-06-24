from collections.abc import Sequence
from csv import reader

class UniversalData(Sequence):
    def __init__(self, headers):
        self.data = [[] for _ in headers]
        self.keys = headers

    def __len__(self):
        return len(self.data[0])

    def __getitem__(self, index):
        if isinstance(index, slice):
            result = UniversalData(self.keys)
            result.data = [data[index] for data in self.data]
            return result
        else:
            return {key:self.data[i][index] for i, key in enumerate(self.keys)}

    def append(self, d : dict):
        for i, key in enumerate(self.keys):
            self.data[i].append(d[key])


def read_csv_as_dicts(path : str, types):
    result = None
    with open(path, "r") as file:
        rows = reader(file)
        headers = next(rows)
        result = UniversalData(headers)
        gen_data = ({ name:func(val) for name, func, val in zip(headers, types, row)} for row in rows)
        for row in gen_data:
            result.append(row)
    return result