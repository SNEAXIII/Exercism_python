from itertools import product


class Point:
    def __repr__(self):
        return f"{self.x = }, {self.y = }"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class WordSearch:

    def universal_check(self, word, point, x_coef, y_coef):
        size = len(word)
        x, y = point.x, point.y
        x_new = x + (x_coef * size) - x_coef
        if any((x_new >= self.x_size, x_new < 0)):
            return False
        y_new = y + (y_coef * size) - y_coef
        if any((y_new >= self.x_size, y_new < 0)):
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

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.y_size = len(puzzle)
        self.x_size = len(puzzle[0])

    def find_all_one_letter_in_a_dict(self, letter):
        indices = []
        for y, line in enumerate(self.puzzle):
            x = line.find(letter)
            while x != -1:
                indices.append(Point(x, y))
                x = line.find(letter, x + 1)
        return indices

    def search(self, word):
        first_letter = word[0]
        coefs = (-1, 0, 1)
        combinaison = [(x, y) for x, y in product(coefs, coefs) if any((x, y))]
        indices = self.find_all_one_letter_in_a_dict(first_letter)
        for (x_coef, y_coef), start_point in product(combinaison, indices):
            if result := self.universal_check(word, start_point, x_coef, y_coef):
                return result
