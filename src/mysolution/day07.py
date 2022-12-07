#!/usr/bin/env python3
"""Solution to Day 7: No Space Left On Device
https://adventofcode.com/2022/day/7

Implementation Note: would be better to use a parser generator to handle input instead
"""
from __future__ import annotations

import collections
import dataclasses
from collections.abc import Sequence
from typing import Mapping, TextIO, TypeAlias

import more_itertools
from rich import print

from mysolution.helpers.cli import command_with_input_file, open_input_file

Path: TypeAlias = tuple[str, ...]


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        histories = read_input(fobj)

    # Part 1: directories with total size at most 100_000
    file_sizes = list_file_sizes(histories)
    dir_sizes = compute_dir_sizes(file_sizes)
    p1_sum_of_total_sizes = sum(
        size for size in dir_sizes.values()
        if size <= 100_000
    )
    print("Part 1:", p1_sum_of_total_sizes)

    # Part 2: find directory just large enough to remove so that
    # there is enough available space to system upgrade
    current_usage = dir_sizes[()]
    space_to_remove = current_usage - 40_000_000
    p2_matched_size = min(
        size for size in dir_sizes.values()
        if size >= space_to_remove
    )
    print("Part 2:", p2_matched_size)


def read_input(fobj: TextIO) -> list[History]:
    """Reads and parses input file according to problem statement.
    """
    stripped_lines = (line.strip() for line in fobj)
    line_groups = more_itertools.split_before(stripped_lines, lambda line: line.startswith("$"))
    histories = [
        History(
            command=lines[0].removeprefix("$").strip(),
            results=lines[1:],
        )
        for lines in line_groups
    ]
    return histories


@dataclasses.dataclass(frozen=True)
class History:
    """History of one single command.
    """
    command: str
    results: list[str]


def list_file_sizes(histories: Sequence[History]) -> dict[Path, int]:
    """Obtains the mapping of file paths to their sizes
    based on the list of command histories.
    """
    file_sizes = {}
    working_dir = None
    for history in histories:
        match history.command.split():
            case ["cd", "/"]:
                working_dir = []
            case ["cd", ".."]:
                working_dir.pop()
            case ["cd", name]:
                working_dir.append(name)
            case ["ls"]:
                for result in history.results:
                    match result.split():
                        case ["dir", _]:
                            pass
                        case [size, name]:
                            path = tuple(working_dir + [name])
                            size = int(size)
                            file_sizes[path] = size
                        case _:
                            raise ValueError(f"cannot parse history result: {result}")
            case _:
                raise ValueError(f"cannot parse history command: {history.command}")
    return file_sizes


def compute_dir_sizes(file_sizes: Mapping[Path, int]) -> collections.defaultdict[Path, int]:
    """Computes the mapping of container directories to their sizes
    based on the files sizes information returned by `list_file_sizes`.
    """
    dir_sizes = collections.defaultdict(int)
    for path, size in file_sizes.items():
        while path:
            path = path[:-1]
            dir_sizes[path] += size
    return dir_sizes


if __name__ == '__main__':
    program()
