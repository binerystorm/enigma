from typing import Optional, Final, Generator
import random as r
import sys

Wiring = list[tuple[int, int]]

WSIZE  : Final[int] = 4
WAMOUNT: Final[int] = 3
RSIZE  : Final[int] = WSIZE
RAMOUNT: Final[int] = 1

r.seed(69)

class Wheel:
    global WSIZE

    def __init__(self, wiring: Wiring) -> None:
        self.wiring = wiring
        self.pos = 0

    def rotate(self, amount: int = 1) -> None:
        self.pos = (self.pos + 1) % WSIZE
        for i, v in enumerate(self.wiring):
            assert len(self.wiring[i]) == 2, "Wiring must be of length 2"
            v2, v1 = v
            w1 = (v1 + amount) % WSIZE
            w2 = (v2 + amount) % WSIZE
            self.wiring[i] = (w1, w2,) 

    def __repr__(self) -> str:
        return str(self.wiring)

def print_usage() -> None:
        print("Usage:", file=sys.stderr)
        print("\tmain <subcommand> <message> [setting]", file=sys.stderr)
        print("\tsubcommands: enc | dec", file=sys.stderr)
        print("\tsetting: a series of 3 letters", file=sys.stderr)

def gen_wheels() -> tuple[Wheel, ...]:
    global WSIZE, WAMOUNT
    wheels: list[Wheel] = []
    
    to = [r.sample([x for x in range(WSIZE)], WSIZE) for _ in range(WAMOUNT)]
    prev = list(range(WSIZE))
    
    for nxt in to:
        wheels.append(Wheel([(v, nxt[v]) for v in prev]))
        prev = nxt

    return tuple(wheels)

def decode(letter: str, wheels: list[Wheel], mech: Generator) -> str:
    letters: Final[list[str]] = [chr(x+65) for x in range(WSIZE)]
    next(mech)
    if letter == ' ':
        return ' '

    idx = letters.index(letter)
    for w in wheels:
        idx = w.wiring.index(idx)

    for w in wheels[-2::-1]:
        idx = w.wiring.index(idx)

    return letters[idx]


def encode(letter: str, wheels: list[Wheel], mech: Generator) -> str:
    letters: Final[list[str]] = [chr(x+65) for x in range(WSIZE)]
    next(mech)
    if letter == ' ':
        return ' '

    idx = letters.index(letter)
    for w in wheels:
        idx = w.wiring[idx]

    for w in wheels[-2::-1]:
        idx = w.wiring[idx]

    return letters[idx]


def tick(wheels: list[Wheel]) -> Generator:
    global WSIZE, WAMOUNT
    # NOTE: this must assert `3` as the tick function is still not dynamic
    assert len(wheels) == 3
    w1, w2, w3, _ = wheels
    while(True):
        w1.rotate()
        # TODO: make more dynamic (accounting for more or less wheels)
        if w1.pos == 0:
            w2.rotate()
            if w2.pos == 0:
                w3.rotate()
        yield None

def parse_setting(setting: str) -> list[int]:
    global WAMOUNT
    assert len(setting) == WAMOUNT
    set_list: list[int] = []
    for l in setting:
        code = ord(l) - 65
        if not ((code < 0) or (code > 26)):
            set_list.append(code)
        else:
            print("error: only capital letters accepted in setting")
            print_usage()
            exit(1)
    return set_list

def main() -> None:
    for i in gen_wheels():
        print(i)


def main1() -> None:
    global WAMOUNT
    wheels: list[Wheel] = [Wheel() for _ in range(4)]
    mech: Generator = tick(wheels)

    # TODO: clean repetitive/messy code in main
    if (len(sys.argv) < 3):
        print("error: not enough arguments provided", file=sys.stderr)
        print_usage()
        exit(1)
    if (len(sys.argv) > 4):
        print("error: to many arguments provided", file=sys.stderr)
        print_usage()
        exit(1)

    if (len(sys.argv) == 4):
        _, subcmd, msg, setting = sys.argv
        if len(setting) != WAMOUNT:
            print("error: setting must be exactly 3 charecters long")
            print_usage()
            exit(1)
        for w, v in zip(wheels, parse_setting(setting)):
            w.rotate(v)
            
    elif (len(sys.argv) == 3):
        _, subcmd, msg  = sys.argv
        
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
