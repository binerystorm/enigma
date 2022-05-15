from typing import Optional, Final, Generator
import random as r
import sys

WSIZE: Final[int] = 27

r.seed(69)

class Wheel:
    global WSIZE

    def __init__(self) -> None:
        self.wheel = r.sample([x for x in range(WSIZE)], WSIZE)
        self.pos = 0

    def rotate(self, amount: int = 1) -> None:
        self.pos = (self.pos + 1) % WSIZE
        for i, v in enumerate(self.wheel):
            self.wheel[i] = (v + amount) % WSIZE

    def __repr__(self) -> str:
        return str(self.wheel)

def decode(letter: str, wheels: list[Wheel], mech: Generator) -> str:
    letters: Final[list[str]] = [chr(x+65) for x in range(WSIZE-1)]
    letters.append(' ')
    next(mech)
    idx = letters.index(letter)
    for w in wheels:
        idx = w.wheel.index(idx)

    for w in wheels[-2::-1]:
        idx = w.wheel.index(idx)

    return letters[idx]


def encode(letter: str, wheels: list[Wheel], mech: Generator) -> str:
    letters: Final[list[str]] = [chr(x+65) for x in range(WSIZE-1)]
    letters.append(' ')
    next(mech)
    idx = letters.index(letter)
    for w in wheels:
        idx = w.wheel[idx]

    for w in wheels[-2::-1]:
        idx = w.wheel[idx]

    return letters[idx]


def tick(wheels: list[Wheel]) -> Generator:
    global WSIZE
    assert len(wheels) == 4
    w1, w2, w3, _ = wheels
    while(True):
        w1.rotate()
        if w1.pos == 0:
            w2.rotate()
            # if w2.pos == 0:
            #     w3.rotate()
        yield None

def print_usage() -> None:
        print("Usage:", file=sys.stderr)
        print("\tmain <subcommand> <message>", file=sys.stderr)
        print("\tsubcommands: enc | dec", file=sys.stderr)

def main() -> None:
    wheels: list[Wheel] = [Wheel() for _ in range(4)]
    mech: Generator = tick(wheels)

    if (len(sys.argv) != 3):
        print("error: not enough, or to many arguments provided", file=sys.stderr)
        print_usage()
        exit(1)

    else:
        _, subcmd, msg = sys.argv
        if subcmd == "enc":
            command = encode
        elif subcmd == "dec":
            command = decode
        else:
            print(f"error: invalid subcommand {subcmd}", file=sys.stderr)
            print_usage()
            exit(1)

        new_msg: list[str] = []
        for l in msg:
            new_msg.append(command(l, wheels, mech))
        print("".join(new_msg))

    

main()
    
