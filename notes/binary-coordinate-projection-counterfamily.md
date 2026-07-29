# Every coordinate binary projection has a finite matching source

## 1. Outcome

Coordinate-degenerate binary projections cannot obstruct the Krenn model.
Let `n>=8` be even.  At every vertex let

\[
                  P_v:\mathbb C^3\longrightarrow\mathbb C^2             \tag{1}
\]

have rank two, with every nonzero column on one of the two coordinate
lines.  Then the projected tensor

\[
                  T(P)=\sum_{r=0}^2\bigotimes_vP_ve_r                    \tag{2}
\]

is the matching tensor of a finite binary source.  The construction uses
only `n+2` nonzero scalar cells.  It allows different projections at every
site, arbitrary nonzero column scalings, coincident projected summands, and
zero columns by specialization.

This gives a uniform finite countermodel to the most degenerate version of
the binary-projection route.  It does not settle the case in which all three
projected colour lines are distinct at every site.  That genuinely
rank-three case includes the fixed projection in
[`binary-rank3-projection-counterexample.md`](binary-rank3-projection-counterexample.md).

## 2. Reduction to three partition words

First suppose all columns are nonzero.  At a fixed site, rank two says that
the three coordinate columns do not all lie on the same line.  After a
local binary bit flip, exactly one ternary species maps to the `1` line and
the other two map to the `0` line.  Let `S_r` be the set of sites at which
species `r` is singled out.  The three sets form a partition of the vertex
set, and after suppressing column scalars the target is

\[
                  |1_{S_0}\rangle+|1_{S_1}\rangle+|1_{S_2}\rangle.       \tag{3}
\]

If `c_r` is the product of the column scalars in summand `r`, the actual
coefficient of the corresponding word is `c_r`.  Thus it is enough to
construct three distinguished matching terms for the indicator words and
give each term a private scalar cell.  Coincident words cause no problem:
their separate matching products simply add in the common coefficient.

## 3. The ten eight-site seeds

Up to permuting species, the unordered size triple

\[
                     (|S_0|,|S_1|,|S_2|)                  \tag{4}
\]

is one of the ten partitions of eight into at most three parts.  Number the
vertices consecutively through `S_0,S_1,S_2`.  For each row below, put the
endpoint bits of `1_(S_r)` on every edge of `P_r`, aggregate coincident
cells, and give every retained cell unit weight.

\[
\begin{array}{c|c|c|c}
(|S_0|,|S_1|,|S_2|)&P_0&P_1&P_2\\ \hline
(8,0,0)&04|15|26|37&02|13|47|56&02|16|35|47\\
(7,1,0)&04|17|23|56&02|14|35|67&06|14|27|35\\
(6,2,0)&05|17|23|46&02|13|45|67&02|13|47|56\\
(6,1,1)&07|13|25|46&02|14|35|67&02|14|37|56\\
(5,3,0)&05|12|34|67&03|15|26|47&03|14|25|67\\
(5,2,1)&04|12|37|56&02|16|34|57&02|15|34|67\\
(4,4,0)&04|12|37|56&02|13|45|67&02|17|34|56\\
(4,3,1)&04|12|36|57&01|23|47|56&01|23|45|67\\
(4,2,2)&03|14|25|67&01|23|45|67&01|27|35|46\\
(3,3,2)&02|13|45|67&05|14|23|67&03|16|27|45.
\end{array}                                               \tag{5}
\]

In every row, aggregation leaves exactly ten distinct decorated cells.
The only supported decorated matching terms are the three displayed ones,
with multiplicity when two target words coincide.  Moreover, every `P_r`
contains a decorated cell used by neither of the other two terms.  Scaling
that private cell by `c_r` gives the arbitrary coefficient in (2).

The assertions in this paragraph are finite exact statements: the checker
enumerates all 105 perfect matchings and all 256 binary words for every row.

## 4. The two-vertex extension

Suppose a finite decorated source has exactly the three desired terms and
term `r` uses a private cell of weight `z` on `uv`.  Delete that cell,
introduce two new vertices `a,b`, and insert the three cells

\[
 (u,a;w_r(u),1)=z,
 \qquad(a,b;0,0)=1,
 \qquad(b,v;1,w_r(v))=1.                                  \tag{6}
\]

Other cells of the old `uv` matrix, if any, remain in place.  Extend word
`r` by `11` and the other two words by `00`.  These are exactly the
coordinate projection bits for two new sites of type `r`.

**Lemma 4.1 (subdivision bijection).**  The new source has exactly the
three extended matching terms, with their old weights.  Each term still
has a private cell.

**Proof.**  A new perfect matching either uses `ab` or does not.  If it uses
`ab`, deleting that edge gives an old supported matching which avoids the
deleted private cell, hence one of the other two distinguished terms.  If
it avoids `ab`, the degree-two new vertices force `ua` and `bv`; adjoining
the deleted cell `uv` then gives an old supported term using that private
cell, hence precisely term `r`.  The two operations are inverse.  The new
outer path cells are private to term `r`, while the old private cells of the
other terms were untouched. `QED`

The operation deletes one cell and adds three, so it increases both the
order and the cell count by two.

## 5. Uniform conclusion

Given nonnegative sizes `(s_0,s_1,s_2)` of even total `n>=8`, repeatedly
subtract two from any part until the total is eight.  This never gets stuck
above eight and leaves one of the ten triples in (5), up to permutation.
Starting with that seed and reversing the subtractions via Lemma 4.1 gives
the desired source at order `n`.  Its cell count is

\[
                            10+(n-8)=n+2.                 \tag{7}
\]

Local bit flips undo the normalization preceding (3), and private-cell
scalings restore all nonzero column products.  If a projected summand is
zero, set its private cell to zero; deleting a term cannot create a new
matching term.  This proves the stated result for every coordinate-line
rank-two projection.

## 6. Exact audit

Run

```text
.venv/bin/python computations/verify_binary_coordinate_projection_counterfamily.py
```

The script checks all ten seeds, their ten-cell counts, the exact projected
targets including coincident-word multiplicities, the existence of three
private cells, and all 30 one-step extensions from order eight to order ten.
