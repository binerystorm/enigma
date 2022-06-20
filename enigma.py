from typing import Final, NamedTuple, Optional as Op
from settings import *
import random as r
import string as s

Wiring = list[int]
Enigma = list['Wheel']

class Wheel:
    global WSIZE

    def __init__(self, wiring: Wiring) -> None:
        self.wiring = wiring
        self.pos = 0

    def rotate(self, amount: int = 1) -> None:
        self.pos = (self.pos + amount) % WSIZE
        for i, v in enumerate(self.wiring):
            self.wiring[i] = (v + amount) % WSIZE

    def __repr__(self) -> str:
        return str(self.wiring)

def init_reflector() -> Wheel:
    global WSIZE
    reflec: list[int] = [-1 for _ in range(WSIZE)]
    chcs = list(range(WSIZE))

    assert (len(chcs) % 2) == 0

    r.shuffle(chcs)
    while chcs:
        i = chcs.pop()
        j = chcs.pop()
        reflec[i] = j
        reflec[j] = i

    assert -1 not in reflec
    return Wheel(reflec)


def init_enigma_random() -> Enigma:
    global WSIZE, WAMOUNT, SEED
    r.seed(SEED)
    enigma: Enigma = []
    
    reflector = init_reflector()
    wheels = \
            [
                Wheel(r.sample([x for x in range(WSIZE)], WSIZE))
                for _ in range(WAMOUNT)
            ]

    enigma.extend(wheels)
    enigma.append(reflector)

    return enigma

if __name__ == '__main__':
    for x in init_enigma_random():
        print(x)
