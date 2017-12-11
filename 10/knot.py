"""Day 10: Knot Hash."""

from functools import reduce
from itertools import chain, cycle, islice
from pathlib import Path
from typing import List

LENGTHS_SUFFIX = (17, 31, 73, 47, 23)


with open(Path(__file__).parent / 'input.txt') as fp:
    puzzle_input = fp.read().strip()


def chunks(l, n):
    return (l[i:i + n] for i in range(0, len(l), n))


class KnotHash:

    text: str
    rounds: int
    digest: List[int]
    pos: int
    skip: int

    def __init__(self, text: str, is_ascii: bool=True, rounds: int=64,
                 size: int=256) -> None:
        self._text = text
        self.is_ascii = is_ascii
        self.rounds = rounds
        self.digest = list(range(size))
        self.pos = 0
        self.skip = 0

    @classmethod
    def calculate(cls, text: str, is_ascii: bool=True, rounds: int=64,
                  size: int=256):
        k = cls(text=text, is_ascii=is_ascii, rounds=rounds, size=size)
        k.process()
        return k

    @property
    def text(self) -> List[int]:
        if self.is_ascii:
            return list(chain(map(ord, self._text.strip()), LENGTHS_SUFFIX))
        return [int(l.strip()) for l in self._text.split(',') if l]

    @property
    def size(self) -> int:
        return len(self.digest)

    def process(self):
        for _ in range(self.rounds):
            self._apply_round()

    def _apply_round(self):
        for l in self.text:
            end = self.pos + l
            if self.pos <= end <= len(self.digest):
                self.digest[self.pos:end] = list(
                    reversed(self.digest[self.pos:self.pos+l]))
            else:
                rev = list(reversed(list(
                    islice(cycle(self.digest), self.pos, end))))
                rev_split = self.size - self.pos
                self.digest[self.pos:self.size] = rev[:rev_split]
                self.digest[:(end - self.size)] = rev[rev_split:]
            self.pos = (end + self.skip) % self.size
            self.skip += 1

    @property
    def value(self):
        return ''.join('{:02x}'.format(reduce(lambda a, n: a ^ n, b))
                       for b in chunks(self.digest, 16))

    def __repr__(self):
        return f'<KnotHash: {self._text} - {self.value}>'


def test_knot_hash():
    assert KnotHash.calculate('').value == \
        'a2582a3a0e66e6e86e3812dcb672a272'
    assert KnotHash.calculate('AoC 2017').value == \
        '33efeb34ea91902bb2f59c9920caa6cd'
    assert KnotHash.calculate('1,2,3').value == \
        '3efbe78a8d82f29979031a4aa0b16a9d'
    assert KnotHash.calculate('1,2,4').value == \
        '63960835bcdc130f0b66d7ff4f6a5a8e'


def get_knot_hash(text: str) -> KnotHash:
    knot = KnotHash(text)
    knot.process()
    return knot


if __name__ == '__main__':
    print(f'knot hash: {KnotHash.calculate(puzzle_input)}')
