class CustomSet:
    def __init__(self, elements=[]):
        self.cset = set(elements)

    def isempty(self) -> bool:
        return not bool(self.cset)

    def __contains__(self, element) -> bool:
        return bool(element in self.cset)

    def issubset(self, other) -> bool:
        return bool(len(self.cset & other.cset) == len(self.cset))

    def isdisjoint(self, other) -> bool:
        return bool(len(self.cset & other.cset) == 0)

    def __eq__(self, other) -> bool:
        return self.cset == other

    def add(self, element) -> None:
        self.cset.add(element)

    def intersection(self, other):
        return self.cset & other.cset

    def __sub__(self, other):
        return self.cset - other.cset

    def __add__(self, other):
        return self.cset | other.cset
