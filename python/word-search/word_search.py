from itertools import product

DIRECTIONS = {
    "south": (0, 1),
    "north": (0, -1),
    "east": (1, 0),
    "weast": (-1, 0),
    "south-east": (1, 1),
    "south-weast": (1, -1),
    "north-east": (-1, 1),
    "north-weast": (-1, -1),
}


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class WordSearch:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.y_size = len(puzzle)
        self.x_size = len(puzzle[0])

    def universal_check(self, word, point, x_coef, y_coef):
        size = len(word)
        x, y = point.x, point.y
        x_new = x + (x_coef * size) - x_coef
        y_new = y + (y_coef * size) - y_coef
        if not (0 <= x_new < self.x_size and 0 <= y_new < self.y_size):
            return False
        extract = self.universal_extract(size, point, x_coef, y_coef)
        if extract == word:
            return Point(x, y), Point(x_new, y_new)
        return False

    def universal_extract(self, size, point_base, x_coef, y_coef):
        extracted_word = ""
        for index in range(size):
            x_actual = point_base.x + (index * x_coef)
            y_actual = point_base.y + (index * y_coef)
            selected_letter = self.puzzle[y_actual][x_actual]
            extracted_word += selected_letter
        return extracted_word

    def find_one_letter_indices_in_list_points(self, letter):
        indices = []
        for y, line in enumerate(self.puzzle):
            x = line.find(letter)
            while x != -1:
                indices.append(Point(x, y))
                x = line.find(letter, x + 1)
        return indices

    def search(self, word):
        first_letter = word[0]
        indices = self.find_one_letter_indices_in_list_points(first_letter)
        for (x_coef, y_coef), start_point in product(DIRECTIONS.values(), indices):
            if result := self.universal_check(word, start_point, x_coef, y_coef):
                return result
