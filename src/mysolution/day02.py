#!/usr/bin/env python3
"""Solution to Day 2: Rock Paper Scissors
https://adventofcode.com/2022/day/2
"""
from __future__ import annotations

import dataclasses
from enum import IntEnum
from typing import Self, TextIO

from rich import print

from mysolution.helpers.cli import command_with_input_file, open_input_file


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        round_strategies = read_input(fobj)

    # Part 1: interpret the second column as the response to the opponent's action
    p1_round_scores = [
        round_score(strategy.opponent_action, strategy.p1_response_action)
        for strategy in round_strategies
    ]
    p1_scores = sum(p1_round_scores)
    print("Part 1:", p1_scores)

    # Part 2: interpret the second column as the desired outcome of the game
    p2_round_responses = (
        Action.proper_response(strategy.opponent_action, strategy.p2_desired_outcome)
        for strategy in round_strategies
    )
    p2_scores = sum(
        round_score(strategy.opponent_action, response)
        for strategy, response in zip(round_strategies, p2_round_responses)
    )
    print("Part 2:", p2_scores)


def read_input(fobj: TextIO) -> list[RoundStrategy]:
    """Reads and parses input file according to problem statement.
    """
    return [RoundStrategy.from_str(line) for line in fobj]


@dataclasses.dataclass(frozen=True)
class RoundStrategy:
    """Strategy information for a single round of Rock Paper Scissors.
    """
    #: First column character
    fst: str
    #: Second column character
    snd: str

    @classmethod
    def from_str(cls, s: str) -> Self:
        fst, snd = s.strip().split()
        return cls(fst=fst, snd=snd)

    @property
    def opponent_action(self) -> Action:
        mapping = {'A': Action.ROCK, 'B': Action.PAPER, 'C': Action.SCISSORS}
        return mapping[self.fst]

    @property
    def p1_response_action(self) -> Action:
        mapping = {'X': Action.ROCK, 'Y': Action.PAPER, 'Z': Action.SCISSORS}
        return mapping[self.snd]

    @property
    def p2_desired_outcome(self) -> Outcome:
        mapping = {'X': Outcome.LOSE, 'Y': Outcome.DRAW, 'Z': Outcome.WIN}
        return mapping[self.snd]


class Action(IntEnum):
    """Actions for the game of Rock Paper Scissors.
    """
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    @classmethod
    def proper_response(cls, opponent: Action, outcome: Outcome) -> Self:
        """Determine the proper response to the opponent's action
        in order to obtain the desired outcome.
        """
        response = (outcome + opponent) % 3
        return Action(response)


class Outcome(IntEnum):
    """Outcomes for the game of Rock Paper Scissors.
    The values are assigned so that the following congruence holds:
        outcome ≡ response - opponent (mod 3)
    """
    WIN = 1
    DRAW = 0
    LOSE = 2

    @classmethod
    def from_actions(cls, opponent: Action, response: Action) -> Self:
        """Determine the outcome based on actions of two players.
        """
        outcome = (response - opponent) % 3
        return cls(outcome)


def round_score(opponent: Action, response: Action) -> int:
    """Computes the score for a single round of Rock Paper Scissors
    based on actions of opponent's and your response's.
    """
    outcome = Outcome.from_actions(opponent, response)
    outcome_score = {Outcome.WIN: 6, Outcome.DRAW: 3, Outcome.LOSE: 0}[outcome]
    response_score = {Action.ROCK: 1, Action.PAPER: 2, Action.SCISSORS: 3}[response]
    return outcome_score + response_score


if __name__ == '__main__':
    program()
