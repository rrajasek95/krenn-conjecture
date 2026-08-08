# Arbitrary-weight one-cell elimination at the anchored N=8 four-cut gate

## Outcome

The signed-unit gate in
[`n8-four-cut-full-sector-unit-cell-falsification-gate.md`](n8-four-cut-full-sector-unit-cell-falsification-gate.md)
extends exactly to every complex weight on every previously absent aggregate
cell.  Let \(A\) be that note's sixteen-source anchored family and let \(x\)
be one of the \(252-16=236\) endpoint-colour coordinates outside its support.
For

\[
                         A(t)=A+tE_x,
\]

there is no \(t\in\mathbb C\) for which the pure coefficients remain
\((1,1,1)\), the complete active cuts \(z=2,3,4\) remain, and a fourth
complete active cut appears in \(z=0,1,5\).

This is an exact elimination of the note's next admissible one-cell search,
not a sample of weights and not a floating-point rank calculation.

## The 230 torus-normalizable directions

Give a coordinate \((u,v;i,j)\) its diagonal-torus character

\[
                         e_{u,i}+e_{v,j}\in\mathbb Z^{24}.
\]

The sixteen characters in the support of \(A\), together with the three
target-stabilizer equations

\[
                         \sum_{u=0}^7 e_{u,i}=0
                         \qquad(i=0,1,2),
\]

have rank 15 over \(\mathbb Q\).  For 230 of the 236 absent coordinates, the
new character raises this rank to 16.  Consequently there is an integral
one-parameter subgroup which fixes every base source, fixes the three pure
target coefficients, and scales the new coordinate nontrivially.  Over
\(\mathbb C\), every nonzero \(t\) is therefore torus-equivalent to the
representative \(t=1\).

The checker reconstructs that representative from literal sources.  All 230
retain the pure anchors, 14 also retain cuts \(2,3,4\), and none of those 14
acquires a complete active cut in \(0,1,5\).  The case \(t=0\) is the audited
base, which also has no fourth cut.

## The six dependent directions

Exactly six new characters lie in the rank-15 constraint span, so torus
normalization does not decide their weights:

| coordinate \(x\) | failing fixed cut \(z\) | boundary row on \(C_z\) |
|---|---:|---:|
| \((2,4;2,0)\) | 2 | 211 |
| \((2,6;0,1)\) | 3 | 211 |
| \((3,4;0,0)\) | 3 | 022 |
| \((3,7;0,2)\) | 2 | 122 |
| \((4,6;0,1)\) | 2 | 011 |
| \((5,7;0,2)\) | 2 | 112 |

For a listed cut, write its fifteen labelled insertion columns as
\(c_k(t)\) and the listed high-sector residual row as \(r(t)\).  A source can
use the added cell at most once, so both are affine:

\[
              c_k(t)=c_k(0)+t\dot c_k,
              \qquad r(t)=r(0)+t\dot r.
\]

The checker verifies this identity coefficient by coefficient at
\(t=0,1,2\), forms the universal cofactor space

\[
              U=\operatorname{span}_{\mathbb Q}
                 \{c_k(0),\dot c_k:1\leq k\leq15\},
\]

and obtains \(\dim U=14\) in every case.  It then verifies that \(r(0)\) lies
in the base insertion span while \(\dot r\) is a one-sparse coefficient-one
vector outside \(U\).  Hence \(r(t)\) is outside the actual cofactor span for
every nonzero \(t\).  One of the original three complete cuts already fails,
so none of these six directions can be a four-cut repair.  This universal
span witness also removes any concern about exceptional parameter values at
which a symbolic rank might specialize.

## Scope and significance

The theorem covers arbitrary complex additions at all 236 coordinates absent
from the anchored support.  It does not cover changing the weights of the 16
occupied cells, adding two cells, changing the anchor family, or proving a
uniform four-cut theorem.  It also does not require the eight mixed output
coefficients of the base family to vanish.

The obstruction remains source-faithful: it rebuilds both crossing sectors,
the labelled cofactor maps, and the high-sector residual rows from finite
decorated sources.  It therefore distinguishes finite realizability from the
border theorem, unlike an invariant of the output tensor alone.

The next bounded experiment, if this local lane is continued, is a
character-orbit-reduced two-cell search retaining all three pure anchors.
Stop that enumeration if it finds a four-cut source.  If the character
classification does not reduce the two-cell parameter families to a bounded
exact list, the correct next step is a structural identity coupling the four
cut cylinders rather than an unbounded weight scan.

## Reproduction

```sh
python3 computations/verify_n8_four_cut_arbitrary_weight_one_cell_elimination.py
python3 -O computations/verify_n8_four_cut_arbitrary_weight_one_cell_elimination.py
python3 -I computations/verify_n8_four_cut_arbitrary_weight_one_cell_elimination.py
python3 -S computations/verify_n8_four_cut_arbitrary_weight_one_cell_elimination.py
```

The checker uses only the Python standard library and exact rational sparse
row reduction.  All audits use raising checks, so optimized mode does not
weaken the result.
