#import "@preview/toffee-tufte:0.1.1": *


#show: template.with(
  title: [Labyrinth Paths],
  // authors: "Jian Wei Cheong",
  date: none,
  // toc: true,
  // full: true,
  // bib: bibliography("main.bib"),
)

//#set text(font: ("Georgia", "Gentium Book Plus", "Times New Roman"))
//#show: set text(size: 16pt)
#set heading(numbering: none)
#set math.equation(numbering: none)

= Problem: Paths in a Labyrinth

== Problem:

You have a string, and you want to create a labyrinth of width $n$, where each row is a "sliding window", resulting in $m$ sliding windows (that is, $l-n+1$ rows).#sidenote(numbered: false)[For example, if if the string is "KALAMAZOO", and n is 4, the matrix would have 6 rows, and look like this:
  #let route-arrow = text.with(fill: rgb("#0b7285"), weight: "bold")
  #table(
    columns: (auto, 1.1em, auto, 1.1em, auto, 1.1em, auto),
    stroke: none,
    align: center,
    column-gutter: 0.2em,
    row-gutter: 0.3em,

    // Top heavy rule
    table.hline(stroke: 1pt),
    [$upright(K)_(1,1)$],
    [#route-arrow[→]],
    [$upright(A)_(1,2)$],
    [#route-arrow[→]],
    [$upright(L)_(1,3)$],
    [→],
    [$upright(A)_(1,4)$],
    [↓], [], [↓], [], [#route-arrow[↓]], [], [↓],
    [$upright(A)_(2,1)$], [→], [$upright(L)_(2,2)$], [→], [$upright(A)_(2,3)$], [#route-arrow[→]], [$upright(M)_(2,4)$],
    [↓], [], [↓], [], [↓], [], [#route-arrow[↓]],
    [$upright(L)_(3,1)$], [→], [$upright(A)_(3,2)$], [→], [$upright(M)_(3,3)$], [→], [$upright(A)_(3,4)$],
    [↓], [], [↓], [], [↓], [], [#route-arrow[↓]],
    [$upright(A)_(4,1)$], [→], [$upright(M)_(4,2)$], [→], [$upright(A)_(4,3)$], [→], [$upright(Z)_(4,4)$],
    [↓], [], [↓], [], [↓], [], [#route-arrow[↓]],
    [$upright(M)_(5,1)$], [→], [$upright(A)_(5,2)$], [→], [$upright(Z)_(5,3)$], [→], [$upright(O)_(5,4)$],
    [↓], [], [↓], [], [↓], [], [#route-arrow[↓]],
    [$upright(A)_(6,1)$], [→], [$upright(Z)_(6,2)$], [→], [$upright(O)_(6,3)$], [→], [$upright(O)_(6,4)$],
    table.hline(stroke: 1pt),
  )
]Further, we can define the labyrinth as having one starting point at the top-left corner (cell (1,1)) and one ending point at the bottom-right corner (cell (m,n)). The only allowed moves are "down" (from cell (i,j) to cell (i+1, j)) and "right" (from cell (i,j) to cell (i, j+1)), for all valid indexed cells.

The question is: how many unique paths are there from the starting point to the ending point?

== Solution:
Based on the problem description, we can model the $m times n$ matrix as a grid graph where the cells are vertices and the allowed movements define directed edges.

=== Assumptions
- The vertices of the graph are the cells $(i, j)$ where $1 <= i <= m$ and $1 <= j <= n$.
- The problem is interpreted as finding the number of unique paths from the top-left vertex $(1, 1)$ to the bottom-right vertex $(m, n)$.
- The only allowed moves are "down" (from $(i, j)$ to $(i+1, j)$) and "right" (from $(i, j)$ to $(i, j+1)$).

=== Path Decomposition
To travel from the starting vertex $(1, 1)$ to the ending vertex $(m, n)$, any path must consist of a specific number of "down" and "right" moves.
- To change the row index from $1$ to $m$, a total of $m-1$ "down" moves are required.
- To change the column index from $1$ to $n$, a total of $n-1$ "right" moves are required.

Therefore, every path from $(1, 1)$ to $(m, n)$ is a sequence of moves with a total length of $(m-1) + (n-1) = m+n-2$.

=== Combinatorial Analysis
The problem reduces to finding the number of distinct sequences of length $m+n-2$ that can be formed using $n-1$ "down" moves and $m-1$ "right" moves. This is a classic problem in *combinatorics*.

We can determine the total number of paths by calculating how many ways we can choose the positions for the $n-1$ "down" moves out of the $m+n-2$ total available positions in the sequence. The remaining $m-1$ positions will be filled by "right" moves.

=== Calculation
This selection can be calculated using the *binomial coefficient*, denoted as $binom(N, k)$, which calculates the number of ways to choose $k$ elements from a set of $N$ elements.

Let $N$ be the total number of moves and $k$ be the number of "down" moves.
- Total moves, $N = m+n-2$
- Number of "down" moves, $k = m-1$

The total number of paths is:
$ binom(N, k) = binom(m+n-2, m-1) $

Using the formula for the binomial coefficient, $binom(N, k) = frac(N!, k!(N-k)!)$, we get:
#sidenote(numbered: false)[
  For the string "KALAMAZOO" and $n=4$, we have $m = 6$ (since there are 6 sliding windows). The number of paths from the top-left to the bottom-right corner would be:
  $ binom(6+4-2, 6-1) = binom(8, 5) = frac(8!, 5!3!) = 56 $
]

$
  binom(m+n-2, m-1) & = frac((m+n-2)!, (m-1)!(n-1)!)
$

Thus, the number of unique paths from the starting point to the ending point in the labyrinth is given by:

#align(center)[
  #rect(inset: 8pt)[
    $ frac((m+n-2)!, (m-1)!(n-1)!) $
  ]
]
