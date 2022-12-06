#!/usr/bin/env python3
"""Solution to Day 5: Supply Stacks
https://adventofcode.com/2022/day/5
"""
from __future__ import annotations

import copy
import dataclasses
import itertools
import re
from collections.abc import Sequence
from typing import Self, TextIO, TypeAlias

from rich import print

from mysolution.helpers.cli import command_with_input_file, open_input_file

#: Mapping from stack number to a list representing a stack of crates
#: where the first item in then list corresponds to the bottom of the stack, etc.
StackConfig: TypeAlias = dict[str, list[str]]

REARRANGE_OP_RE = re.compile(r'move (?P<count>\d+) from (?P<src>\d+) to (?P<dest>\d+)')


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        stack_config, rearrange_ops = read_input(fobj)

    # Part 1: Rearrange crates by CrateMover 9000
    final_config = simulate_cratemover_9000(stack_config, rearrange_ops)
    p1_desired_crates = ''.join(crates[-1] for crates in final_config.values())
    print("Part 1:", p1_desired_crates)

    # Part 2: Rearrange crates by CrateMover 9001
    final_config = simulate_cratemover_9001(stack_config, rearrange_ops)
    p2_desired_crates = ''.join(crates[-1] for crates in final_config.values())
    print("Part 2:", p2_desired_crates)


def read_input(fobj: TextIO) -> tuple[StackConfig, list[RearrangeOp]]:
    """Reads and parses input file according to problem statement.
    """
    stack_lines = list(itertools.takewhile(lambda line: line.strip(), fobj))

    stack_config = {}
    for col, stack_no in enumerate(stack_lines[-1]):
        if not stack_no.isdigit():
            continue
        column_chars = (line[col] for line in stack_lines[-2::-1])
        crates = list(itertools.takewhile(lambda char: char.isalpha(), column_chars))
        stack_config[stack_no] = crates

    rearrange_ops = [RearrangeOp.from_str(line) for line in fobj]
    return stack_config, rearrange_ops


@dataclasses.dataclass(frozen=True)
class RearrangeOp:
    """A rearrangement operation to move the given number (count) of crates
    from the source stack pile (src) to the destination stack pile (dest).
    """
    count: int
    src: str
    dest: str

    @classmethod
    def from_str(cls, s: str) -> Self:
        data = REARRANGE_OP_RE.fullmatch(s.strip()).groupdict()
        return cls(count=int(data['count']), src=data['src'], dest=data['dest'])


def simulate_cratemover_9000(config: StackConfig, rearrange_ops: Sequence[RearrangeOp]) -> StackConfig:
    """Simulates CrateMover 9000: moves one crate at a time.
    See problem statement for a thorough description of this machine.
    """
    config = copy.deepcopy(config)
    for op in rearrange_ops:
        for _ in range(op.count):
            crate = config[op.src].pop()
            config[op.dest].append(crate)
    return config


def simulate_cratemover_9001(config: StackConfig, rearrange_ops: Sequence[RearrangeOp]) -> StackConfig:
    """Simulates CrateMover 9000: moves multiple crates at once.
    See problem statement for a thorough description of this machine.
    """
    config = copy.deepcopy(config)
    aux = []  # achieves reverse-stack behavior by introducing auxiliary stack
    for op in rearrange_ops:
        for _ in range(op.count):
            crate = config[op.src].pop()
            aux.append(crate)  # temporary move to auxiliary stack
        for _ in range(op.count):
            crate = aux.pop()  # now move them to destination
            config[op.dest].append(crate)
    return config


if __name__ == '__main__':
    program()
