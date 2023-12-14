import itertools
import sys
from collections import Counter
from pathlib import Path

data = Path(sys.argv[1]).read_text().splitlines()
HANDS = [(split[0], int(split[1])) for line in data if (split := line.split())]

CARD_VALUES = ["A", "K", "Q", "J", "T", *map(str, range(9, 1, -1))]
JOKER_CARD_VALUES = ["A", "K", "Q", "T", *map(str, range(9, 1, -1)), "J"]


def five_of_kind(hand: str):
    return any(hand.count(c) == 5 for c in CARD_VALUES)


def four_of_kind(hand: str):
    return any(hand.count(c) == 4 for c in CARD_VALUES)


def full_house(hand: str):
    return set(Counter(hand).values()) == {2, 3}


def three_of_kind(hand: str):
    return set(Counter(hand).values()) == {3, 1}


def two_pair(hand: str):
    return sorted(Counter(hand).values()) == [1, 2, 2]


def one_pair(hand: str):
    return sorted(Counter(hand).values()) == [1, 1, 1, 2]


def high_card(hand: str):
    return set(Counter(hand).values()) == {1}


HAND_TYPES = [
    five_of_kind,
    four_of_kind,
    full_house,
    three_of_kind,
    two_pair,
    one_pair,
    high_card,
]


def eval_hand_strength(hand):
    for strength_idx, hand_type_func in enumerate(HAND_TYPES):
        if hand_type_func(hand):
            return strength_idx
    assert False, "shouldn't be here"


def joker_score(hand: str):
    joker_count = hand.count("J")
    no_jokers = hand.replace("J", "")

    joker_combinations = itertools.combinations_with_replacement(
        JOKER_CARD_VALUES, joker_count
    )
    return min(eval_hand_strength(no_jokers + "".join(c)) for c in joker_combinations)


def eval_hand(hand, joker=False) -> int:
    base_hand_strength = eval_hand_strength(hand)
    if joker:
        return min(base_hand_strength, joker_score(hand))
    return base_hand_strength


def hand_values(hand, joker=False):
    card_values = JOKER_CARD_VALUES if joker else CARD_VALUES
    return tuple(card_values.index(c) for c in hand)


def part_1():
    total_winnings = 0
    results = []
    for hand, bid in HANDS:
        results.append((eval_hand(hand), hand_values(hand), bid, hand))
    for rank, (_, _, bid, hand) in enumerate(sorted(results, reverse=True), start=1):
        total_winnings += rank * bid
    print(total_winnings)


def part_2():
    total_winnings = 0
    results = []
    for hand, bid in HANDS:
        results.append((joker_score(hand), hand_values(hand, joker=True), bid, hand))
    for rank, (_, _, bid, hand) in enumerate(sorted(results, reverse=True), start=1):
        total_winnings += rank * bid
    print(total_winnings)


part_1()
part_2()
