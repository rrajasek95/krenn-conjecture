# All-star singularity does not force a binary source to be diagonal

Let `B={0,1,2,3,4,5}`, with binary variables `x_i,y_i`, and put

\[
 q=2x_0x_1+x_2x_3+x_4x_5
      +y_0y_5+y_1y_2+y_3y_4
      -2x_0y_1-2x_0x_4-y_1x_5.                    \tag{1}
\]

Thus (1) contains the genuinely off-diagonal endpoint-color cells `x_0y_1`
and `y_1x_5`.  Every one of its nine nonzero scalar cells is tensor-active.
Nevertheless it gives an exact counterexample to the proposed implication

\[
 H(q)=2X+Y,\quad \ker F_i\ne0\ (i=0,\ldots,5)
 \quad\Longrightarrow\quad q\text{ is diagonal}.         \tag{2}
\]

Here the full common-cofactor star map is

\[
 F_i:\bigoplus_{j\ne i}V_j\longrightarrow
       \bigotimes_{v\ne i}V_v,
 \qquad
 F_i(e_{j,a})=e_a^{(j)}H_{B\setminus\{i,j\}}(q).          \tag{3}
\]

## Exact output

The first six cells in (1) are the two alternating factors of the cycle

\[
 01\mid23\mid45,\qquad 05\mid12\mid34.                    \tag{4}
\]

Their matching products are respectively `2` and `1`.  Besides these two
constant matchings, the underlying support has only the matching

\[
                         04\mid15\mid23.                    \tag{5}
\]

There are two decorated terms with the mixed coloring

\[
                         (x_0,y_1,x_2,x_3,x_4,x_5).         \tag{6}
\]

One uses the off-diagonal cell on `01` followed by `23|45`, and has weight
`-2`.  The other uses (5), and has weight `(-2)(-1)(1)=2`.  They cancel.
There are no other supported decorated matching terms.  Therefore,
coefficientwise,

\[
                         H(q)=2X+Y.                         \tag{7}
\]

Moreover every displayed cell lies in one of these four decorated terms,
and the complementary product in that term is nonzero.  Thus every scalar
cell, including both off-diagonal cells, has a nonzero derivative cofactor.

## Exact star kernels

Write `e_{j,x},e_{j,y}` for the standard ten domain vectors of (3).  Direct
deleted-pair matching expansion gives the following nonzero kernel vectors:

\[
\begin{array}{c|c}
i&\text{a nonzero vector in }\ker F_i\\ \hline
0&e_{1,y}+e_{4,x}\\
1&e_{3,x}\\
2&e_{4,x}\\
3&e_{1,x}\\
4&e_{2,x}\\
5&e_{1,x}-e_{1,y}+e_{4,x}.
\end{array}                                                \tag{8}
\]

The relations for `i=1,2,3,4` are zero-cofactor columns; those for `i=0,5`
are genuine cancellations between common-cofactor tensors.

In fact exact row reduction of the six `32 by 10` matrices gives

\[
 (\operatorname{rank}F_0,\ldots,\operatorname{rank}F_5)
       =(8,7,8,7,8,9),                                    \tag{9}
\]

so their nullities are `(2,3,2,3,2,1)`.

The audit
[`computations/verify_all_star_singular_offdiagonal.py`](../computations/verify_all_star_singular_offdiagonal.py)
enumerates all 64 output coefficients over the integers, checks activity of
all nine cells, constructs every star matrix from common hafnian cofactors,
checks (8), and independently row-reduces to (9).

## Scope of the counterexample

This example refutes (2) even after adding the hypothesis that every cell is
tensor-active.  The three cells

\[
                       x_0y_1,\quad x_0x_4,\quad y_1x_5
\]

do form a globally removable zero-output cancellation module: deleting all
three leaves the alternating Hamilton source.  Thus the example does not
refute a still stronger statement formulated modulo removable modules or
with an appropriate global inclusion-minimality hypothesis.  Such a
hypothesis would need to be stated and used explicitly; tensor activity and
all-star singularity do not supply it.
