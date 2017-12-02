"""Day 1 captcha with step."""

from pathlib import Path

with open(Path(__file__).parent / 'input.txt') as fp:
    puzzle_input = fp.read().strip()


def captcha(s: str, step: int):
    s = str(s)
    return sum(int(n) for i, n in enumerate(s) if s[(i + step) % len(s)] == n)

def test_captcha_sum():
    assert captcha(1122, 1) == 3
    assert captcha(1111, 1) == 4
    assert captcha(1234, 1) == 0
    assert captcha(91212129, 1) == 9


def test_captcha_step():
    assert captcha(1212, len('1212') // 2) == 6
    assert captcha(1221, len('1221') // 2) == 0
    assert captcha(123425, len('123425') // 2) == 4
    assert captcha(123123, len('123123') // 2) == 12
    assert captcha(12131415, len('12131415') // 2) == 4


if __name__ == '__main__':
    print(f'captcha_1: {captcha(puzzle_input, 1)}')
    print(f'captcha_2: {captcha(puzzle_input, len(puzzle_input) // 2)}')
