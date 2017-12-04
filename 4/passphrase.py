"""Day 4: High-Entropy Passphrases."""

from collections import Counter
from pathlib import Path
from typing import Callable, Any, Tuple

with open(Path(__file__).parent / 'input.txt') as fp:
    puzzle_input = fp.read().strip()


def check_passphrase(phrase: str,
                     transform_word: Callable[[str], Any]=None) -> bool:
    transform_word = transform_word or str
    words = [transform_word(w) for w in phrase.split()]
    return all(v == 1 for v in Counter(words).values())


def sorted_tuple(word: str) -> Tuple[str, ...]:
    return tuple(sorted(word))


def check_passphrase_file(text: str) -> Counter:
    return Counter(check_passphrase(l) for l in text.splitlines())


def check_passphrase_set_file(text: str) -> Counter:
    return Counter(check_passphrase(l, sorted_tuple)
                   for l in text.splitlines())


def test_check_passphrase():
    assert check_passphrase('aa bb cc dd ee') == True
    assert check_passphrase('aa bb cc dd aa') == False
    assert check_passphrase('aa bb cc dd aaa') == True


def test_check_passphrase_set():
    assert check_passphrase('abcde fghij', sorted_tuple) == True
    assert check_passphrase('abcde xyz ecdab', sorted_tuple) == False
    assert check_passphrase('abcde fghij', sorted_tuple) == True
    assert check_passphrase('a ab abc abd abf abj', sorted_tuple) == True
    assert check_passphrase('iiii oiii ooii oooi oooo', sorted_tuple) == True
    assert check_passphrase('oiii ioii iioi iiio', sorted_tuple) == False


if __name__ == '__main__':
    print(f'Passphrase file: {check_passphrase_file(puzzle_input)}')
    print(f'Passphrase file: {check_passphrase_set_file(puzzle_input)}')
