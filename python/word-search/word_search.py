from dataclasses import dataclass
from itertools import product

values = (-1, 1, 0)
DIRECTIONS = list(product(values, values))
# We don't need (0,0) direction
DIRECTIONS.pop()


@dataclass
class Point:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class WordSearch:
    def __init__(self, puzzle: list):
        self.puzzle = puzzle
        self.y_size = len(puzzle)
        self.x_size = len(puzzle[0])

    def single_direction_find(self, word: str, point_base: Point, x_coef: int, y_coef: int) -> bool | None:
        for index, expected_letter in enumerate(word):
            x_actual = point_base.x + (index * x_coef)
            y_actual = point_base.y + (index * y_coef)
            actual_letter = self.puzzle[y_actual][x_actual]
            if actual_letter != expected_letter:
                return None
        return True

    def single_direction_check(self, word: str, point: Point, x_coef: int, y_coef: int) \
            -> bool | tuple[Point, Point] | None:
        size = len(word)
        x, y = point.x, point.y
        x_new = x - x_coef + x_coef * size
        y_new = y - y_coef + y_coef * size
        if not (0 <= x_new < self.x_size and 0 <= y_new < self.y_size):
            return False
        if self.single_direction_find(word, point, x_coef, y_coef):
            return Point(x, y), Point(x_new, y_new)
        return None

    def find_one_letter_indices_in_list_points(self, letter: str) -> list:
        indices = []
        for y, line in enumerate(self.puzzle):
            x = line.find(letter)
            while x != -1:
                indices.append(Point(x, y))
                x = line.find(letter, x + 1)
        return indices

    def search(self, word: str) -> bool | None:
        first_letter = word[0]
        indices = self.find_one_letter_indices_in_list_points(first_letter)
        for (x_coef, y_coef), start_point in product(DIRECTIONS, indices):
            if result := self.single_direction_check(word, start_point, x_coef, y_coef):
                return result
