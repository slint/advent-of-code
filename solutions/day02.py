DRAW = 3
WIN = 6

VALUE_OF = {
    "🪨": 1,
    "🧻": 2,
    "✂️": 3,
}

LOSER_OF = {
    "🪨": "✂️",
    "✂️": "🧻",
    "🧻": "🪨",
}

BEATER_OF = {v: k for k, v in LOSER_OF.items()}
DRAW_OF = {v: v for v in VALUE_OF}

OLD_TRANSLATE = str.maketrans({
    "X": "🪨",
    "Y": "🧻",
    "Z": "✂️",
    "A": "🪨",
    "B": "🧻",
    "C": "✂️",
})

NEW_TRANSLATE = str.maketrans({
    "X": "L",
    "Y": "D",
    "Z": "W",
    "A": "🪨",
    "B": "🧻",
    "C": "✂️",
})


STREATEGY_MAP = {
    "L": LOSER_OF,
    "D": DRAW_OF,
    "W": BEATER_OF,
}


def _round_score(their, our):
    if their == our:
        return VALUE_OF[our] + DRAW
    else:
        if LOSER_OF[our] == their:
            return VALUE_OF[our] + WIN
    return VALUE_OF[our]


def run(input_data: str):
    old_score = 0
    new_score = 0
    for game in input_data.splitlines():
        their_move, our_move = game.translate(OLD_TRANSLATE).split()
        old_score += _round_score(their_move, our_move)

        their_move, result = game.translate(NEW_TRANSLATE).split()
        our_move = STREATEGY_MAP[result][their_move]
        new_score += _round_score(their_move, our_move)

    print(f"Part one: {old_score}")
    print(f"Part two: {new_score}")
