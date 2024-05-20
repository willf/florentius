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
    def __init__(self, x, y, character):
        self.x = x
        self.y = y
        self.ch = character

    def __str__(self):
        return "({},{},{})".format(self.x, self.y, self.ch)


class Path:
    def __init__(self, Cells):
        self.Cells = Cells

    def __str__(self):
        s = "".join([Cell.ch for Cell in self.Cells])
        return " → ".join(x.__str__() for x in self.Cells)


class HalfLabyrinth:
    def __init__(self, S, P):
        self.S = S
        self.P = P
        self.w = len(P)
        self.h = len(S) - self.w
        self.matrix = [
            [Cell(j, k, S[abs(j + k)]) for j in range(0, self.w)]
            for k in range(self.h + 1)
        ]
        self.paths = []

    def display(self):
        print(" ", end=" ")
        for k in range(0, self.w):
            print(k, end=" ")
        print()
        for j in range(self.h + 1):
            print(j, end=" ")
            for k in range(self.w):
                print(self.matrix[j][k].ch, end=" ")
            print()


lh = HalfLabyrinth("abcdefghijk", "abcde")
lh.display()
