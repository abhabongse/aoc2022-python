#!/usr/bin/env python3
"""Solution to Day 6: Tuning Trouble
https://adventofcode.com/2022/day/6
"""
from __future__ import annotations

from typing import TextIO

from rich import print

from mysolution.helpers.cli import command_with_input_file, open_input_file


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        datastream = read_input(fobj)

    # Part 1:
    p1_first_marker = find_first_marker(datastream, marker_length=4)
    print("Part 1:", p1_first_marker)

    # Part 2:
    p2_first_marker = find_first_marker(datastream, marker_length=14)
    print("Part 2:", p2_first_marker)


def read_input(fobj: TextIO) -> str:
    """Reads and parses input file according to problem statement.
    """
    return fobj.readline().strip()


def find_first_marker(datastream: str, marker_length: int) -> int:
    """Naive implementation of finding the first substring with unique characters.
    Excluding the performance overhead of using Python strings,
    a better approach is to use sliding window while maintaining character frequency counters.
    """
    for i in range(marker_length, len(datastream)):
        if len(set(datastream[i - marker_length: i])) == marker_length:
            return i
    raise IndexError


if __name__ == '__main__':
    program()
