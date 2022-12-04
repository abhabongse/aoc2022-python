#!/usr/bin/env python3
"""Solution to Day 4: Camp Cleanup
https://adventofcode.com/2022/day/4
"""
from __future__ import annotations

import dataclasses
from typing import Self, TextIO

from rich import print

from mysolution.helpers.cli import command_with_input_file, open_input_file


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        assignment_pairs = read_input(fobj)

    # Part 1: count assignment pairs where one fully contains the other
    fully_contains_assignments = [
        pair for pair in assignment_pairs
        if pair.fst.contains(pair.snd) or pair.snd.contains(pair.fst)
    ]
    p1_count = len(fully_contains_assignments)
    print("Part 1:", p1_count)

    # Part 2: count assignments where two overlap
    overlapped_assignments = [
        pair for pair in assignment_pairs
        if pair.fst.overlaps(pair.snd)
    ]
    p2_count = len(overlapped_assignments)
    print("Part 2:", p2_count)


def read_input(fobj: TextIO) -> list[AssignmentPair]:
    """Reads and parses input file according to problem statement.
    """
    return [AssignmentPair.from_str(line) for line in fobj]


@dataclasses.dataclass(frozen=True)
class AssignmentPair:
    fst: SectionRange
    snd: SectionRange

    @classmethod
    def from_str(cls, s: str) -> Self:
        fst, snd = s.split(',')
        return cls(fst=SectionRange.from_str(fst), snd=SectionRange.from_str(snd))


@dataclasses.dataclass(frozen=True)
class SectionRange:
    lower: int
    upper: int

    def __post_init__(self):
        assert self.lower <= self.upper

    @classmethod
    def from_str(cls, s: str) -> Self:
        lower, upper = s.split('-')
        return cls(lower=int(lower), upper=int(upper))

    def contains(self, other: SectionRange) -> bool:
        return self.lower <= other.lower and other.upper <= self.upper

    def overlaps(self, other: SectionRange) -> bool:
        return self.upper >= other.lower and self.lower <= other.upper


if __name__ == '__main__':
    program()
