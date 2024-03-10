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
    def check_e(self, word, point):
        x, y = point.x, point.y
        index_last = x + len(word)
        if index_last > self.x_size:
            return False
        extract = self.universal_extract(word, point, 1, 0)
        if extract != word:
            return False
        return Point(x, y), Point(index_last - 1, y)

    def check_w(self, word, point):
        index_last = point.x + 1
        index_first = index_last - len(word)
        if index_first < 0:
            return False
        extract = self.universal_extract(word, point, -1, 0)
        if extract != word:
            return False
        return Point(point.x, point.y), Point(index_first, point.y)

    def check_n(self, word, point):
        index_last = point.y + 1
        index_first = index_last - len(word)
        if index_first < 0:
            return False
        extract = self.universal_extract(word, point, 0, -1)
        print(f"{extract = }")
        if extract != word:
            return False
        return Point(point.x, point.y), Point(point.x, index_first)

    def check_s(self, word, point):
        index_last = point.y + len(word)
        if index_last > self.y_size:
            return False
        extract = self.universal_extract(word, point, 0, 1)
        if extract != word:
            return False
        return Point(point.x, point.y), Point(point.x, index_last - 1)

    def universal_extract(self, word, point_base, x_coef, y_coef):
        size, x, y = len(word), point_base.x, point_base.y
        return "".join(self.puzzle[y + (index * y_coef)][x + (index * x_coef)] for index in range(size))

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.y_size = len(puzzle)
        self.x_size = len(puzzle[0])
        self.check_methods = [
            self.check_e,
            self.check_w,
            self.check_s,
            self.check_n
        ]

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
        indices = self.find_all_one_letter_in_a_dict(first_letter)
        for check, start_point in product(self.check_methods, indices):
            if result := check(word, start_point):
                return result


puzzle = WordSearch(
    [
        "jefblpepre",
        "camdcimgtc",
        "oivokprjsm",
        "pbwasqroua",
        "rixilelhrs",
        "wolcqlirpc",
        "screeaumgr",
        "alxhpburyi",
        "jalaycalmp",
        "clojurermt",
    ]
)
print(puzzle.universal_extract("ecmascript", Point(9, 0), 0, -1)[::-1])
# wordsearch = WordSearch(["rixilelhrs"])
# print(wordsearch.search("elixir"))
# print(wordsearch.check_e("clojure", 0, 0))
