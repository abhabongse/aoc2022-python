#!/usr/bin/env python3
from __future__ import annotations

from mysolution.helpers.cli import command_with_input_file, open_input_file


@command_with_input_file
def program(input_file):
    """Main program.
    """
    data = read_input(input_file)
    print(data)


def read_input(input_file):
    """Reads and parses input file according to problem statement.
    """
    with open_input_file(input_file) as fobj:
        return [int(line) for line in fobj]


if __name__ == '__main__':
    program()
