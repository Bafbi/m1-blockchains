import random
from typing import Tuple


def rain_drop() -> Tuple[float, float]:
    return (random.random(), random.random())

def calculate_pi(iterations: int):
    inCircle = 0
    for i in range(iterations):
        pos = rain_drop()
        if (pos[0] - 0.5)**2 + (pos[1] - 0.5)**2 <= 0.25:
            inCircle += 1
    print(inCircle)
    return 4* inCircle/iterations