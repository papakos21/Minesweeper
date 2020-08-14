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
        if input_str == "Difficulty.EASY" or input_str == '1':
            return Difficulty.EASY
        if input_str == "Difficulty.MEDIUM" or input_str == '2':
            return Difficulty.MEDIUM
        return Difficulty.HARD
