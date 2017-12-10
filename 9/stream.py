"""Day 9: Stream Processing."""

from pathlib import Path
from functools import reduce


with open(Path(__file__).parent / 'input.txt') as fp:
    puzzle_input = fp.read().strip()


class StreamState:

    score: int = 0
    total_groups: int = 0
    group_level: int = 0
    total_garbage: int = 0
    in_garbage: bool = False
    skip: bool = False

    def __repr__(self):
        return f'{self.__dict__}'


def process_stream(stream_text: str) -> StreamState:
    # reduce_stream
    state = StreamState()

    def reduce_stream(state: StreamState, c: str) -> StreamState:
        if state.skip:
            state.skip = False
            return state

        if c == '!':
            state.skip = True

        if state.in_garbage:
            if c not in '!>':
                state.total_garbage += 1
            if c == '>':
                state.in_garbage = False
            return state
        if c == '<':
            state.in_garbage = True
            return state
        if c == '{':
            state.total_groups += 1
            state.group_level += 1
        if c == '}':
            state.score += state.group_level
            state.group_level -= 1
        return state

    return reduce(reduce_stream, stream_text, state)


def test_process_stream():
    assert process_stream('{}').score == 1
    assert process_stream('{{{}}}').score == 6
    assert process_stream('{{},{}}').score == 5
    assert process_stream('{{{},{},{{}}}}').score == 16
    assert process_stream('{<a>,<a>,<a>,<a>}').score == 1
    assert process_stream('{{<ab>},{<ab>},{<ab>},{<ab>}}').score == 9
    assert process_stream('{{<!!>},{<!!>},{<!!>},{<!!>}}').score == 9
    assert process_stream('{{<a!>},{<a!>},{<a!>},{<ab>}}').score == 3


def test_grabage_count():
    assert process_stream('<>').total_garbage == 0
    assert process_stream('<random characters>').total_garbage == 17


if __name__ == '__main__':
    print(f'stream state: {process_stream(puzzle_input)}')
