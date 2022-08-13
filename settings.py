from typing import Final

WSIZE  : Final[int] = 26
WAMOUNT: Final[int] = 3
RSIZE  : Final[int] = WSIZE
RAMOUNT: Final[int] = 1
SEED   : Final[int] = 69

assert WSIZE % 2 == 0, "Reflector will not work with uneven wheels size"
