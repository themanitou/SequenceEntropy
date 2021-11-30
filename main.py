# Calculate the entropy of a sequence
#   Given a sequence S, this script calculates a matrix M
#   where each coefficient m_ij of M is the information entropy
#   of the subsequence S_ij of all elements from i-th to j-th
#   positions (inclusive) of S.

import argparse
import re
import pandas as pd


class _RegExLib:
    """Set up regular expressions"""
    _reg_entry = re.compile(r'(?P<index>[0-9]+) (?P<term>[0-9]+)')

    # use __slots__ to help with memory and performance
    __slots__ = ['entry']

    def __init__(self, line):
        # check whether line has a positive match with all of the regular expressions
        self.entry = self._reg_entry.match(line)


def parse(seq_file):
    data = []
    with open(seq_file, 'r') as file:
        line = next(file)
        while line:
            reg_match = _RegExLib(line)
            if reg_match.entry:
                index = reg_match.entry.groupdict()['index']
                term = reg_match.entry.groupdict()['term']
                record = {'index': index,
                          'term': term}
                data.append(record)
            line = next(file, None)
        data = pd.DataFrame(data)

    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Sequence file")
    args = parser.parse_args()

    if args.file:
        seq_file = args.file
    else:
        seq_file = 'b181391.txt'

    data = parse(seq_file)
    print(f'{ seq_file = }')
