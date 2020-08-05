"""Difficulty Enum"""
from enum import Enum


class Difficulty(Enum):
    """Difficulty Class"""
    EASY = 1
    MEDIUM = 2
    HARD = 3

    @staticmethod
    def get(input_str: str):
        """Get"""
        if input_str == "Difficulty.EASY":
            return Difficulty.EASY
        if input_str == "Difficulty.MEDIUM":
            return Difficulty.MEDIUM
        return Difficulty.HARD
