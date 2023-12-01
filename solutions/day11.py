import time
import operator
import math
import functools
from collections import Counter


OPS_MAP = {
    '*': operator.mul,
    '+': operator.add,
}

MONKEYS = []

"""
2^6 * 3^4 + 2^2 * 5^2 =
2^2 * (2^4 * 3^4 + 5^2) =
...
"""

# ROUNDS = 20
# ROUNDS = 10_000
ROUNDS = 500
RIDICULOUS = True

@functools.cache
def prime_factors(num):
    print("called", num)
    if num == 1:
        return []

    factor = math.isqrt(num)

    while factor != 1:
        print("testing", factor)
        if num % factor == 0:
            print("return", [factor], "+ called", num // factor)
            return prime_factors(factor) + prime_factors(num // factor)
        else:
            factor -= 1
    print("return", [num])
    return [num]


def prime_factors_2(num, factor=2):
    pass
    if num < factor:
        return []
    if num % factor == 0:
        return [factor] + prime_factors(num // factor)
    return prime_factors(num, factor + 1)


class PFNum:

    def __init__(self, num=None, _factors=None):
        if _factors:
            self.factors = _factors
        else:
            self.factors = Counter(prime_factors(num))

    def is_divisible_by(self, other):
        return other in self.factors

    def __add__(self, other):
        if isinstance(other, PFNum):


    def __mul__(self, other):
        if isinstance(other, PFNum):
            return PFNum(_factors=other.factors + self.factors)
        else:
            return self * PFNum(other)


    @property
    def value(self):
        return math.prod(k ** v for k, v in self.factors.items())

    def __str__(self):
        return f"PFNum({self.factors})"

    __repr__ = __str__


class Monkey:

    id: int
    items: list
    test_div: int
    test_true: int
    test_false: int

    def __init__(self):
        self.inspections = 0

    def op(self, i):
        return self.op_a(
            i if self.op_l is None else self.op_l,
            i if self.op_r is None else self.op_r,
        )

    def test(self, w):
        if w % self.test_div == 0:
            return self.test_true
        else:
            return self.test_false

    def __str__(self):
        return f"Monkey({vars(self)})"

    __repr__ = __str__

def run(input_data: str, visualize=False):

    for m_data in [d.splitlines() for d in input_data.split('\n\n')]:
        m = Monkey()
        m.id = int(m_data[0][:-1].rsplit(" ", 1)[-1])
        m.items = list(map(int, m_data[1].rsplit(": ", 1)[-1].split(', ')))
        op = m_data[2].rsplit(" = ", 1)[-1]
        m.op_l, m.op_a, m.op_r = op.split(" ")
        m.op_l = None if m.op_l == "old" else int(m.op_l)
        m.op_r = None if m.op_r == "old" else int(m.op_r)
        m.op_a = OPS_MAP[m.op_a]

        m.test_div = int(m_data[3].rsplit(" ", 1)[-1])
        m.test_true = int(m_data[4].rsplit(" ", 1)[-1])
        m.test_false = int(m_data[5].rsplit(" ", 1)[-1])

        MONKEYS.append(m)

    for rnd_id in range(ROUNDS):
        print(rnd_id)
        for m in MONKEYS:
            # print(rnd_id, m.id)
            while m.items:
                # print(m.id, m.items)
                m.inspections += 1
                old = m.items.pop(0)
                new = m.op(old)
                # print(f"new = {m.op} = {m.op.replace('old', str(old))} = {new}")
                if not RIDICULOUS:
                    new //= 3
                # print(new)
                next_monkey = m.test(new)
                # print(f"Throwing {new} to {next_monkey}")

                MONKEYS[next_monkey].items.append(new)
                # time.sleep(0.1)

            # for m in MONKEYS:
            #     print(m)

    # for m in MONKEYS:
    #     print(m)
    top_monkeys = sorted(MONKEYS, key=lambda m: m.inspections)[-2:]
    monkey_business = top_monkeys[0].inspections * top_monkeys[1].inspections

    print(f"Part one: {monkey_business}")
    # print(f"Part two: {input_data}")
