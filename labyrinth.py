# This is the new version of the Florentian Labyrinth code.
#
# A Florentian Labyrinth is parameterized by a string $S$ of length $l$, indexed
# from $0$ to $l-1$, and a prefix $P$ of $S$ of length $w$, indexed from $0$ to $w-1$.
# This naturally defines a suffix $S'$ of $S$ of length $h$, indexed from $0$ to $h-1$,
# where $h = l - w$.
#
# Assocated with the Florentian Labyrinth is a matrix of width $2w+1$ and height $h$.
# The columns of the matrix are indexed from $-w$ to $w$, and the rows are indexed from $0$ to $h-1$.
# Each cell $(j,k)$ of the matrix contains a character $c$ from $S$ such that $c = S[j+|k|]$.
#
# For example, if $S = "abcde"$ and $P = "ab"$, then $S' = "cde"$, and the matrix is:
#
#     -2 -1  0  1  2
# 0    c  b  a  b  c
# 1    d  c  b  c  d
# 2    e  d  c  d  e
#
# A _step_ in the Florentian Labyrinth is a pair of cells $(j,k)$ and $(j',k')$ such that
# $|j-j'| = 1$ or $|k-k'| = 1$. The _value_ of a step is the concatenation of the characters
# in the cells $(j,k)$ and $(j',k')$.
# A _path_ in the Florentian Labyrinth is a sequence of steps, and the _value_ of a path is the
# concatenation of the values of the steps in the path.
# A _solution_ to the Florentian Labyrinth is a path from $(0,0)$ to $(h,-(w-1))$ or from $(0,0) to $(h,w-1)$
# such that the value of the path is $S$.
#
# An example of a solution to the Florentian Labyrinth above
# is the path $(0,0,a) \rightarrow (1,0,b) \rightarrow (1,1,c) \rightarrow (2,1,d) \rightarrow (2,2,d)$
# Another example is the path $(0,0,a) \rightarrow (-1,0,b) \rightarrow (-1,1,c) \rightarrow (-1,2,d) \rightarrow (-2,2,e)$
#
# One question of interest is: given a string $S$,and a prefix $p$, how many solutions are there to the Florentian Labyrinth?
#
# Note that a Florentian Labyrinth is a bilaterally symmetric matrix, and so the number of solutions is the same
# for the "left" and "right" sides of the matrix. Thus, we can restrict our attention to the "right" side of the matrix.
# The "left" sid of the matrix are the columns indexed from $-(w-1)$ to $9$, and the "right" side of the matrix are the columns
# indexed from $0$ to $w-1$.
#
# The special case where $|p| = 0$  or $|p| = |S|$ is easy to solve. In each case,
# there is exactly one solution, either the row or column of the matrix that is defined.
#
# But in general, we only need to solve the problem for the right side of the matrix, because the left side is symmetric;
# every path in the right side of the matrix has a corresponding path in the left side of the matrix, and vice versa.
#

import functools
import math
import sys
from collections import Counter


def prod(iterable):
    return functools.reduce(lambda x, y: x * y, iterable, 1)


# T(n,k) = binomial(n,k)*binomial(n+2,k)
def T0(n, k):
    return math.comb(n, k) * math.comb(n + 2, k)


# T(n,k) = (k+1)*binomial(n+1,k+1)*binomial(n+1,k)/(n+1)
def T1(n, k):
    return int((k + 1) * math.comb(n + 1, k + 1) * math.comb(n + 1, k) / (n + 1))


# T(n,k) = binomial(2*n+1,k)*binomial(n,k)
def T2(n, k):
    return math.comb(2*n + 1, k) * math.comb(n, k)


def T(n, k):
    return T0(n, k)

# Display code.
# Display the matrix of the Florentian Labyrinth.
def display_matrix(S, P):
    w = len(P)
    h = len(S) - w
    # Display the column indices.
    print(" ", end=" ")
    for k in range(-(w - 1), w):
        print(k, end=" ")
    print()
    for j in range(h + 1):
        print(j, end=" ")
        for k in range(-(w - 1), w):
            print(S[abs(k + j)], end=" ")
        print()


def display_right_matrix(S, P):
    w = len(P)
    h = len(S) - w
    # Display the column indices.
    print(" ", end=" ")
    for k in range(0, w):
        print(k, end=" ")
    print()
    for j in range(h + 1):
        print(j, end=" ")
        for k in range(0, w):
            print(S[abs(k + j)], end=" ")
        print()


# display_right_matrix("abcdefghi", "abcde")


class Cell:
    def __init__(self, j, k, character):
        self.j = j
        self.k = k
        self.ch = character

    def __str__(self):
        return "({},{},{})".format(self.j, self.k, self.ch)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.j == other.j and self.k == other.k and self.ch == other.ch

    def __hash__(self):
        return hash((self.j, self.k, self.ch))


class Path:
    def __init__(self, Cells):
        self.Cells = Cells

    def __str__(self):
        return " → ".join(x.__str__() for x in self.Cells)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.Cells == other.Cells


class HalfLabyrinth:
    def __init__(self, S, p, verbose=False):
        self.S = S
        self.p = p
        self.P = S[0:p]
        self.verbose = verbose
        self.columns = p
        self.rows = len(S) - p + 1
        self.matrix = [
            [Cell(j, k, S[abs(j + k)]) for k in range(0, self.columns)]
            for j in range(self.rows)
        ]
        self.paths = []
        self.bfs = []
        # number of paths going through a cell
        self.path_counts = Counter()

        self.start = [self.retrieve(0, 0)]
        self.initiate_bfs()

    def display(self):
        if self.verbose:
            print(" ", end=" ")
            for k in range(0, self.columns):
                print(k, end=" ")
        print()
        for j in range(self.rows):
            if self.verbose:
                print(j, end=" ")
            for k in range(self.columns):
                print(self.matrix[j][k].ch, end=" ")
            print()

    def to_dot(self):
        def label(cell):
            ch = cell.ch
            j = cell.j
            k = cell.k
            #t = T(self.p, j)
            cc = self.path_counts[cell]
            label_list = [
                ch,
                f"({j},{k})",
               # f"T(p, j):{t}",
                f"count: {cc}"
                ]
            return "\n".join(label_list)
        print("digraph  {")
        print(f"	graph [label=\"{self.S} ({len(self.S)}: {self.p} x {len(self.S)- self.p}) paths={len(self.paths)}\n \" labelloc=t]")
        for j in range(self.rows):
            for k in range(self.columns):
                cell = self.matrix[j][k]
                print(f"{cell.j}{cell.k} [label=\"{label(cell)}\"]")
                if j < self.rows - 1:
                    print(f"{cell.j}{cell.k} -> {cell.j + 1}{cell.k}")
                if k < self.columns - 1:
                    print(f"{cell.j}{cell.k} -> {cell.j}{cell.k + 1}")
        print("}")

    def path_matches(self, path):
        s = "".join([Cell.ch for Cell in path.Cells])
        return s == self.S

    def path_prefix_matches(self, path):
        if not path.Cells:
            return False
        s = "".join([Cell.ch for Cell in path.Cells])
        return self.S.startswith(s)

    def retrieve(self, j, k):
        try:
            return self.matrix[j][k]
        except IndexError:
            return None

    def up(self, Cell):
        return self.retrieve(Cell.j - 1, Cell.k)

    def down(self, Cell):
        return self.retrieve(Cell.j + 1, Cell.k)

    def right(self, Cell):
        return self.retrieve(Cell.j, Cell.k + 1)

    def left(self, Cell):
        return self.retrieve(Cell.j, Cell.k - 1)

    def neighbors(self, Cell):
        ns = [self.right(Cell), self.down(Cell)]
        ns = [n for n in ns if n]
        return ns

    def extend(self, path):
        n = path.Cells[-1]
        Cells = path.Cells
        ns = self.neighbors(n)
        paths = [Path(Cells + [n]) for n in ns]
        goods = [p for p in paths if self.path_prefix_matches(p)]
        if goods:
            last = path.Cells[-1]
            s = "".join([Cell.ch for Cell in path.Cells])
            (j, k) = last.j, last.k
            if self.verbose:
                print(
                    "Extending {} extending from ({}, {}) by {} Cell(s)".format(
                        s, j, k, len(goods)
                    )
                )
        return goods

    def initiate_bfs(self):
        self.bfs = [Path([cell]) for cell in self.start]

    def search(self):
        while self.bfs:
            path = self.bfs.pop(0)
            if self.path_matches(path):
                if self.verbose:
                    print(f"Found path: {path}")
                for cell in path.Cells:
                    self.path_counts[cell] += 1
                self.paths.append(path)
            else:
                self.bfs += self.extend(path)

    def count_row_vs_column_counts(self):
        # collect all the second to last cells in the paths
        penults = [path.Cells[-2] for path in self.paths]
        row_count = 0
        column_count = 0
        # count the number of paths that end in the last row or the last column
        for penult in penults:
            if penult.j == self.rows - 1:
                row_count += 1
            else:
                column_count += 1
        if self.verbose:
            print(f"Row count: {row_count}, column count: {column_count}")
        return (row_count, column_count)

    def last_row_cells(self):
        return self.matrix[-1]

    def analytical_number_of_paths(self):
        return math.comb(len(self.S)-1, len(self.P)-1)


def main():
    str = sys.argv[1] if len(sys.argv) > 1 else "abcdefghijk"
    prefix = int(sys.argv[2]) if len(sys.argv) > 2 else len() // 2
    lh = HalfLabyrinth(str, prefix)
    lh.display()
    lh.search()
    print(len(lh.paths))
    counted_path_count = len(lh.paths)
    analytical_path_count = lh.analytical_number_of_paths()
    print(
        f"Counted path count: {counted_path_count}, analytical path count: {analytical_path_count}"
    )


def all_prefixes(text):
    for i in range(len(text)):
        yield text[0 : i + 1]


# sum_(n=1)^11 (n (n + 1) (n + 2) (n + 3) (n + 4) (n + 5) (n + 6))/(7!) = 43758


def fn(n, m):
    total = 0
    for i in range(1, n + 1):
        total += prod(range(i, i + m))
    return total // math.factorial(m)


# rewrite this to use math.comb
# def fn2(n, m):
#     total = 0
#     for i in range(1, n + 1):
#         total += math.comb(i + m - 1, m)
#     return total


# # rewrite fn2 to use list comprehensions only
# def fn3(n, m):
#     return sum([math.comb(i + m - 1, m) for i in range(1, n + 1)])


# def combo_count(x, y):
#     print(f"combo_count({x}, {y})")
#     return math.comb(y + x - 1, y)


# def triangle_count(w, h):
#     fn = lambda x, y: math.comb(y + x - 1, y)
#     return sum([combo_count(x, h - 1) for x in range(w)])


def triangle_count(n, m):
    return sum([math.comb(i + m - 1, m) for i in range(1, n + 1)])


def main2():
    text_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet += alphabet.upper()
    text = alphabet[0:text_size]
    row_n = 0
    headers = [
        "row",
        "prefix+suffix",
        "w",
        "h",
        "cn",
        "an",
        "same?",
        "fpn",
    ]
    print("\t".join(headers))
    for prefix in list(all_prefixes(text))[0:-1]:
        lh = HalfLabyrinth(text, prefix, verbose=False)
        # lh.display()
        analytical_path_count = 0
        # if lh.w > 2 and lh.h > 2:
        lh.verbose = True
        analytical_path_count = lh.analytical_number_of_paths()
        lh.verbose = False
        if analytical_path_count < 100000:
            lh.search()
        n_paths = len(lh.paths)
        counted_path_count = len(lh.paths)
        is_eq = "n/a"
        is_eq = n_paths == analytical_path_count
        # rp = lh.removable_paths()
        row_n += 1
        vals = [
            row_n,
            prefix + ":" + text[-lh.h :],
            lh.w,
            lh.h,
            counted_path_count,
            analytical_path_count,
            is_eq,
            analytical_path_count * 2,
        ]
        vals = [str(x) for x in vals]
        print("\t".join(vals))


def main3():
    text_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet += alphabet.upper()
    text = alphabet[0:text_size]
    row_n = 0

    headers = [
        "row",
        "prefix",
        "suffix",
        "w",
        "h",
        "counted_path_count",
        "j",
        "k",
        "v",
    ]
    print("\t".join(headers))
    for prefix in list(all_prefixes(text)):
        suffix_len = len(text) - len(prefix)
        suffix = text[-suffix_len:]
        lh = HalfLabyrinth(text, prefix)
        if lh.analytical_number_of_paths() < 50000:
            lh.search()
        n_paths = len(lh.paths)
        rp = lh.removable_paths()
        c = Counter(rp)
        for k, v in sorted(c.items(), key=lambda item: item[1]):
            row_n += 1
            vals = [row_n, prefix, suffix, lh.w, lh.h, n_paths, k.j, k.k, v]
            vals = [str(x) for x in vals]
            print("\t".join(vals))


def main4():
    text_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    prefix_size = int(sys.argv[2]) if len(sys.argv) > 2 else text_size // 2
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet += alphabet.upper()
    text = alphabet[0:text_size]
    prefix = text[0:prefix_size]
    lh = HalfLabyrinth(text, prefix, verbose=True)
    lh.display()
    # lh.verbose = False
    if lh.analytical_number_of_paths() < 50000:
        lh.search()
    lh.verbose = True
    print("Counted paths: ", len(lh.paths))
    print(lh.analytical_number_of_paths())


def main5():
    prefix_size = 2
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet += alphabet.upper()
    for prefix in [p for p in list(all_prefixes(alphabet)) if len(p) >= 2]:
        text = prefix
        p1 = text[:2]
        p2 = text[-2:]
        lh1 = HalfLabyrinth(text, p1, verbose=False)
        lh2 = HalfLabyrinth(text, p2, verbose=False)
        lh1.search()
        lh2.search()
        n_paths1 = len(lh1.paths)
        n_paths2 = len(lh2.paths)
        a_paths1 = lh1.analytical_number_of_paths()
        a_paths2 = lh2.analytical_number_of_paths()
        vals = [
            p1,
            p2,
            n_paths1,
            a_paths1,
            n_paths1 == a_paths1,
            n_paths2,
            a_paths2,
            n_paths2 == a_paths2,
            lh1.w,
            lh1.h,
            lh2.w,
            lh2.h,
            text,
        ]
        vals = [str(x) for x in vals]
        print("\t".join(vals))

def main6():
    text_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    prefix_size = int(sys.argv[2]) if len(sys.argv) > 2 else text_size // 2
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet += alphabet.upper()
    text = alphabet[0:text_size]
    lh = HalfLabyrinth(text, prefix_size, verbose=False)
    # lh.display()
    # lh.verbose = False
    if lh.analytical_number_of_paths() < 50000:
        lh.search()
        lh.to_dot()
    #lh.verbose = True
    #print("Counted paths: ", len(lh.paths))
    #print(lh.analytical_number_of_paths())


def main7():
    text_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    prefix_size = int(sys.argv[2]) if len(sys.argv) > 2 else text_size // 2
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet += alphabet.upper()
    text = alphabet[0:text_size]
    lh = HalfLabyrinth(text, prefix_size, verbose=False)
    # lh.display()
    # lh.verbose = False
    if lh.analytical_number_of_paths() < 500000:
        lh.search()
    counts = [lh.path_counts[cell] for cell in lh.last_row_cells()]
    s = text_size
    p = prefix_size
    label = f"{s}\t{p}\t{len(lh.paths)}"
    cs = []
    for ss in range(s-1, s+2):
        for pp in range(p-1, p+2):
            cs.append((ss, pp, math.comb(ss, pp,)))
    cs_label = "\t".join([f"({x[0]},{x[1]}:{x[2]})" for x in cs])
    # print(f"{label}: ", end="")
    # print(",".join([str(x) for x in counts]))
    print(label,"\t", lh.analytical_number_of_paths(), "\t", cs[0])


def main8():
    text = "FLORENTIUMINDIGNUMMEMORARE"
    text = sys.argv[1] if len(sys.argv) > 1 else text
    headers = ["text len", "prefix", "prefix_size", "half lab", "full lab", "counted paths", "full paths"]
    print("\t".join(headers))
    for prefix in all_prefixes(text):
        prefix_size = len(prefix)
        lh = HalfLabyrinth(text, prefix_size, verbose=False)
        if lh.analytical_number_of_paths() < 500000:
           lh.search()
        np = lh.analytical_number_of_paths()
        cp = len(lh.paths)
        results = [len(text), prefix, prefix_size, np, 2*np, cp, 2*cp]
        print("\t".join([str(x) for x in results]))

if __name__ == "__main__":
    main8()
