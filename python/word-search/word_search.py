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
        size = len(word)
        x, y = point.x, point.y
        index_last = x + size
        if index_last > self.x_size:
            return False
        extract = self.puzzle[y][x:index_last]
        if extract != word:
            return False
        return Point(x,y),Point(index_last-1,y)

    def check_w(self, word, point):
        size = len(word)
        index_last = point.x + 1
        index_first = index_last - size
        if index_first < 0:
            return False
        extract = self.puzzle[point.y][index_first:index_last][::-1]
        if extract != word:
            return False
        return Point(point.x,point.y),Point(index_first,point.y)

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


wordsearch = WordSearch(["rixilelhrs"])
print(wordsearch.search("elixir"))
# print(wordsearch.check_e("clojure", 0, 0))
