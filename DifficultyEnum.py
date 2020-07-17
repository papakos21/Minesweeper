from enum import Enum


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

    @staticmethod
    def get( input: str ):
        if input == "Difficulty.EASY":
            return Difficulty.EASY
        elif input == "Difficulty.MEDIUM":
            return Difficulty.MEDIUM
        elif input == "Difficulty.HARD":
            return Difficulty.HARD
