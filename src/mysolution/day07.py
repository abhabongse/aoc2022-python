#!/usr/bin/env python3
"""Solution to Day 7: No Space Left On Device
https://adventofcode.com/2022/day/7
"""
from __future__ import annotations

import dataclasses
import operator
from collections.abc import Sequence
from typing import TextIO, TypeAlias

import more_itertools
from rich import print
from rich.pretty import pprint

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
    pprint(file_sizes)
    print("Part 1:", ...)

    # Part 2:
    print("Part 2:", ...)


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


@dataclasses.dataclass(frozen=True)
class FileSize:
    """Full path and size of a single file.
    """
    #: List of path components from root
    path: Path
    #: Size of file
    size: int


def list_file_sizes(histories: Sequence[History]) -> list[FileSize]:
    """Obtains file paths and sizes based on the command histories.
    """
    file_sizes = []
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
                            file_sizes.append(FileSize(path=path, size=size))
                        case _:
                            raise ValueError(f"cannot parse history result: {result}")
            case _:
                raise ValueError(f"cannot parse history command: {history.command}")
    return sorted(file_sizes, key=operator.attrgetter('path'))


if __name__ == '__main__':
    program()
