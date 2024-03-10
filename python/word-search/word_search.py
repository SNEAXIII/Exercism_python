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
        size = len(word)
        if x + size > self.x_size:
            return False
        extract = self.puzzle[y][x:x + size]
        if extract != word:
            return False
        return True

    def check_w(self, word, point):
        x,y = point.x,point.y
        size = len(word)
        if x - size + 1 < 0:
            return False
        extract = self.puzzle[y][x - size + 1:x + 1][::-1]
        if extract != word:
            return False
        return True

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.y_size = len(puzzle)
        self.x_size = len(puzzle[0])
        self.check_methods = [
            self.check_e,
            self.check_w,
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


wordsearch = WordSearch(["clojurermt"])
print(wordsearch.search("clojure"))
# print(wordsearch.check_e("clojure", 0, 0))
