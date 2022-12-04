#!/usr/bin/env python3
from __future__ import annotations

import dataclasses
import heapq
from functools import cached_property
from typing import TextIO

import more_itertools
from rich import print

from mysolution.helpers.cli import command_with_input_file, open_input_file


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        elves = read_input(fobj)

    # Part 1: find the most calories carried by an elf
    p1_calories = max(elf.total_calories for elf in elves)
    print("Part 1:", p1_calories)

    # Part 2: find the sum of calories carried by top-3 elves
    top_three = heapq.nlargest(3, (elf.total_calories for elf in elves))
    p2_calories = sum(top_three)
    print("Part 2:", p2_calories)


@dataclasses.dataclass(frozen=True)
class Elf:
    """Information associated with a single elf.
    """
    #: List of calories carried by the elf
    calories: list[int]

    @cached_property
    def total_calories(self) -> int:
        return sum(self.calories)


def read_input(fobj: TextIO) -> list[Elf]:
    """Reads and parses input file according to problem statement.
    """
    calories_groups = more_itertools.split_at(fobj, lambda line: not line.strip())
    return [
        Elf(calories=[int(calorie) for calorie in calories])
        for calories in calories_groups
    ]


if __name__ == '__main__':
    program()
