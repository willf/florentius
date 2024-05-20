import sys


def flatten(lst):
    return sum(lst, [])


def mirror(s):
    return s[0 : len(s) - 1] + s[::-1]


def create_labyrinth(text, prefix_length=-1):
    if prefix_length < 0:
        prefix_length = len(text) // 2
    width = prefix_length * 2 - 1
    mirrored_text = mirror(text[::-1])  # note reverse text first!
    start = len(mirrored_text) // 2 + 1  # get middle of text
    rows = len(text) - width // 2  # get # of rows
    offset = width // 2 + 1  # how much offset
    result = []
    for i in range(0, rows):
        x = mirrored_text[start - offset - i : start - i]
        result.append(mirror(x))
    return result


class Cell:
    def __init__(self, x, y, character):
        self.x = x
        self.y = y
        self.ch = character

    def __str__(self):
        return "<Cell ({},{}) {}>".format(self.x, self.y, self.ch)


class Path:
    def __init__(self, Cells):
        self.Cells = Cells

    def __str__(self):
        s = "".join([Cell.ch for Cell in self.Cells])
        return "<Path {} : {}>".format(", ".join(x.__str__() for x in self.Cells), s)


class Labyrinth:

    def __init__(self, string, strings, p):
        self.w = len(strings[0])
        self.h = len(strings)
        self.p = p
        self.b1 = 2 * self.h + 1
        self.b3 = self.h - 1
        self.b2 = (self.w * self.h) - (self.b1 + self.b3)
        self.n_paths = self.b3 * 3 + self.b2 * 2
        self.base = {}
        self.string = string
        self.strings = strings
        self.found = []
        self.bfs = []
        for y, s in enumerate(strings):
            for x, ch in enumerate(s):
                n = Cell(x, y, ch)
                self.base[(x, y)] = n
        self.initiate_bfs()

    def path_matches(self, path):
        s = "".join([Cell.ch for Cell in path.Cells])
        return s == self.string

    def path_prefix_matches(self, path):
        if not path.Cells:
            return False
        s = "".join([Cell.ch for Cell in path.Cells])
        return self.string.startswith(s)

    def up(self, Cell):
        (x, y) = (Cell.x, Cell.y - 1)
        if self.base.get((x, y)):
            return [self.base.get((x, y))]
        else:
            return []

    def down(self, Cell):
        (x, y) = (Cell.x, Cell.y + 1)
        if self.base.get((x, y)):
            return [self.base.get((x, y))]
        else:
            return []

    def right(self, Cell):
        (x, y) = (Cell.x - 1, Cell.y)
        if self.base.get((x, y)):
            return [self.base.get((x, y))]
        else:
            return []

    def left(self, Cell):
        (x, y) = (Cell.x + 1, Cell.y)
        if self.base.get((x, y)):
            return [self.base.get((x, y))]
        else:
            return []

    def neighbors(self, Cell):
        return self.up(Cell) + self.down(Cell) + self.left(Cell) + self.right(Cell)

    def extend(self, path):
        n = path.Cells[-1]
        Cells = path.Cells
        ns = self.neighbors(n)
        paths = [Path(Cells + [n]) for n in ns]
        goods = [p for p in paths if self.path_prefix_matches(p)]
        if goods:
            first = path.Cells[0]
            s = "".join([Cell.ch for Cell in path.Cells])
            (x, y) = first.x, first.y
            # print(
            #    "Extending {} starting at ({}, {}) by {} Cell(s)".format(
            #        s, x, y, len(goods)
            #    )
            # )
        return goods

    def initiate_bfs(self):
        self.bfs = [Path([n]) for n in list(self.base.values())]

    def search(self):
        while self.bfs:
            path = self.bfs.pop(0)
            if self.path_matches(path):
                # print("Found path: {}".format(path))
                self.found.append(path)
            else:
                self.bfs += self.extend(path)


if __name__ == "__main__":
    text = "FLORENTIUMINDIGNUMMEMORARE"
    # get the string from sys.argv if present
    # get the width from sys.argv if present
    text = sys.argv[1] if len(sys.argv) > 1 else text
    p = int(sys.argv[2]) if len(sys.argv) > 2 else -1
    strings = create_labyrinth(text, p)
    print("\n".join(strings))
    lab = Labyrinth(text, strings, p)
    lab.search()
    print("Found {} paths".format(len(lab.found)))
    # print all the internal variables
    print("Width: {}".format(lab.w))
    print("Height: {}".format(lab.h))
    print("Prefix length: {}".format(lab.p))
    print("b1: {}".format(lab.b1))
    print("b2: {}".format(lab.b2))
    print("b3: {}".format(lab.b3))
    print("Number of paths: {}".format(lab.n_paths))

    # for path in lab.found:
    #    print("Path: {}".format(path))
    #    print("".join([Cell.ch for Cell in path.Cells]))
    #    print()

# DCBABCD
# EDCBCDE
# FEDCDEF
