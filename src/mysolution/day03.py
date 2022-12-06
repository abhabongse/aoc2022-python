#!/usr/bin/env python3
"""Solution to Day 3: Rucksack Reorganization
https://adventofcode.com/2022/day/3
"""
from __future__ import annotations

import dataclasses
from typing import Self, TextIO

import more_itertools
from rich import print

from mysolution.helpers.cli import command_with_input_file, open_input_file

#: Item types where the i-th item has the priority value i
ITEM_BY_PRIORITIES = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        rucksacks = read_input(fobj)

    # Part 1: sum of priorities for item types
    # that appear in both compartments of each rucksack
    p1_sum_priorities = sum(
        item_priority(item_type)
        for rucksack in rucksacks
        for item_type in set(rucksack.fst_compartment) & set(rucksack.snd_compartment)
    )
    print("Part 1:", p1_sum_priorities)

    # Part 2: sum of priorities for item types
    # that appear in each group of three consecutive rucksacks
    p2_sum_priorities = sum(
        item_priority(item_type)
        for chunk in more_itertools.chunked(rucksacks, n=3, strict=True)
        for item_type in set(chunk[0].content) & set(chunk[1].content) & set(chunk[2].content)
    )
    print("Part 2:", p2_sum_priorities)


def read_input(fobj: TextIO) -> list[Rucksack]:
    """Reads and parses input file according to problem statement.
    """
    return [Rucksack.from_str(line) for line in fobj]


@dataclasses.dataclass(frozen=True)
class Rucksack:
    """Information for each rucksack.
    """
    content: str

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls(content=s.strip())

    @property
    def fst_compartment(self) -> str:
        length = len(self.content) // 2
        return self.content[:length]

    @property
    def snd_compartment(self) -> str:
        length = len(self.content) // 2
        return self.content[length:]


def item_priority(item_type: str) -> int:
    """Priority based on the given item type.
    """
    return ITEM_BY_PRIORITIES.index(item_type)


if __name__ == '__main__':
    program()
