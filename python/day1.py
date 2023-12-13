import sys

data = open(sys.argv[1]).read().splitlines()

DIGITS = {
    word: str(idx + 1)
    for idx, word in enumerate(
        ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    )
}


def first_match(text, search_values):
    return min(
        (pos, digit) for digit in search_values
        if (pos := text.find(digit)) != -1
    )


def last_match(text, search_values):
    return max(
        (pos, digit) for digit in search_values
        if (pos := text.rfind(digit)) != -1
    )


def part_1():
    total = 0
    for line in data:
        digits = DIGITS.values()
        _, first_digit = first_match(line, digits)
        _, last_digit = last_match(line, digits)
        total += int(first_digit + last_digit)
    print(total)


def part_2():
    total = 0
    for line in data:
        digits = DIGITS.values() | DIGITS.keys()
        _, first_digit = first_match(line, digits)
        _, last_digit = last_match(line, digits)

        # translate digit word (if needed)
        first_digit = DIGITS.get(first_digit, first_digit)
        last_digit = DIGITS.get(last_digit, last_digit)
        total += int(first_digit + last_digit)
    print(total)


part_1()
part_2()
