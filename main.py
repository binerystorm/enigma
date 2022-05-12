from typing import Optional, Final, Generator
import random as r


WSIZE: Final[int] = 4

r.seed(69)

class Wheel:
    global WSIZE

    def __init__(self) -> None:
        self.wheel = r.sample([x for x in range(WSIZE)], WSIZE)
        self.wheel_pos = 0

    def rotate(self, amount: int = 1) -> None:
        self.wheel_pos = (self.wheel_pos + 1) % WSIZE
        for i, v in enumerate(self.wheel):
            self.wheel[i] = (v + amount) % WSIZE

    def __repr__(self) -> str:
        return str(self.wheel)



def tick(wheels: list[Wheel]) -> Generator:
    global WSIZE
    assert len(wheels) == 3
    w1, w2, w3 = wheels
    while(True):
        w1.rotate()
        if w1.wheel_pos == 0:
            w2.rotate()
            if w2.wheel_pos == 0:
                w3.rotate()
        yield None

def main() -> None:
    wheels: list[Wheel] = [Wheel() for _ in range(3)]
    letters = {x: chr(x) for x in range(65, 65+WSIZE)}

    t = tick(wheels)
    for _ in range(26):
        next(t)
        for w in wheels:
            print(w)
        print()
    

main()
    
