# Calculate the entropy of a sequence
#   Given a sequence S, this script calculates a matrix M
#   where each coefficient m_ij of M is the information entropy
#   of the subsequence S_ij of all elements from i-th to j-th
#   positions (inclusive) of S.

import argparse
import re
import pandas as pd
import numpy as np
import os.path
import matplotlib.pyplot as plt


class _RegExLib:
    """Set up regular expressions"""
    _reg_two = re.compile(r'(?P<index>[0-9]+) (?P<term>[0-9]+)')
    _reg_three = re.compile(r'(?P<num>[0-9]+),(?P<next>[0-9]+),(?P<steps>[0-9]+)')

    # use __slots__ to help with memory and performance
    __slots__ = ['two', 'three']

    def __init__(self, line):
        # check whether line has a positive match with all of the regular expressions
        self.two = self._reg_two.match(line)
        self.three = self._reg_three.match(line)


def parse(seq_file):
    data = []
    with open(seq_file, 'r') as file:
        line = next(file)
        while line:
            reg_match = _RegExLib(line)
            line = next(file, None)
            if reg_match.two:
                index = reg_match.two.groupdict()['index']
                term = reg_match.two.groupdict()['term']
            elif reg_match.three:
                index = reg_match.three.groupdict()['num']
                term = reg_match.three.groupdict()['steps']
            else:
                continue

            record = {'index': index,
                      'term': term}
            data.append(record)

        data = pd.DataFrame(data)

    return data


def entropy(s):
    h = np.zeros(s.size)
    dict = {}
    tot = 0

    for i in range(s.size):
        tot = tot + 1
        k = s[i]
        v = dict.get(k, 0)
        dict[k] = v + 1
        values = np.array(list(dict.values()))
        p = values / tot
        lp = np.log(p)
        h[i] = np.sum(-p*lp)

    return h


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Sequence file")
    args = parser.parse_args()

    if args.file:
        seq_file = args.file
    else:
        seq_file = 'a070165.txt'

    entropy_file = "entropy_" + seq_file

    if os.path.exists(entropy_file):
        h = pd.read_csv(entropy_file)["entropy"].to_numpy()
    else:
        data = parse(seq_file)
        terms = data['term'].to_numpy(dtype = int)
        h = entropy(terms)
        pd.DataFrame(h, columns=["entropy"]).to_csv(entropy_file)

    print(f'{ h = }')
    plt.subplot(121)
    plt.ylabel("Entropy")
    plt.xlabel("n")
    plt.title('Collatz, H(#steps from n to 1)')
    plt.plot(h, 'b')

    h1 = pd.read_csv("entropy_b181391.txt")["entropy"].to_numpy()
    print(f'{ h1 = }')
    plt.subplot(122)
    plt.ylabel("Entropy")
    plt.xlabel("n")
    plt.title('Van-Eck, H(n)')
    plt.plot(h1, 'r')

    plt.show()
