import random


class Math:
    @staticmethod
    def randin(min:int, max:int) -> int:
        return random.randint(min, max)
