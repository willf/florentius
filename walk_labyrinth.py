def flatten(lst):
    return sum(lst, [])

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
        s = ''.join([Cell.ch for Cell in self.Cells])
        return "<Path {} : {}>".format(', '.join(x.__str__() for x in self.Cells), s)


class Labyrinth:

    def __init__(self, string, strings):
        self.base = {}
        self.string = string
        self.strings = strings
        self.found = []
        self.bfs = []
        for y, s in enumerate(strings):
            for x, ch in enumerate(s):
                n = Cell(x, y, ch)
                self.base[(x,y)] = n
        self.initiate_bfs()


    def path_matches(self, path):
        s = ''.join([Cell.ch for Cell in path.Cells])
        return s == self.string

    def path_prefix_matches(self, path):
        if not path.Cells:
            return False
        s = ''.join([Cell.ch for Cell in path.Cells])
        return self.string.startswith(s)

    def up(self, Cell):
        (x,y) = (Cell.x, Cell.y-1)
        if self.base.get((x,y)):
            return [self.base.get((x,y))]
        else:
            return []

    def down(self, Cell):
        (x,y) = (Cell.x, Cell.y+1)
        if self.base.get((x,y)):
            return [self.base.get((x,y))]
        else:
            return []

    def right(self, Cell):
        (x,y) = (Cell.x-1, Cell.y)
        if self.base.get((x,y)):
            return [self.base.get((x,y))]
        else:
            return []

    def left(self, Cell):
        (x,y) = (Cell.x+1, Cell.y)
        if self.base.get((x,y)):
            return [self.base.get((x,y))]
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
            s = ''.join([Cell.ch for Cell in path.Cells])
            (x,y) = first.x, first.y
            print("Extending {} starting at ({}, {}) by {} Cell(s)".format(s, x, y, len(goods)))
        return goods

    def initiate_bfs(self):
        self.bfs = [Path([n]) for n in list(self.base.values())]

    def search(self):
        while self.bfs:
            path = self.bfs.pop(0)
            if self.path_matches(path):
                print("Found path: {}".format(path))
                self.found.append(path)
            else:
                self.bfs += self.extend(path)
                
