# The exact factorized SCC exports a mandatory private head face

## Outcome

The first private row exported by the exact SCC cycle is

\[
 F_{01}=P_0S_1Lb,qquad(001100;01),\quad
 \mathrm{PS},\quad60\mid73\mid12\mid45.                \tag{1}
\]

It has one unique positive minimum-cost mate.  The single new cell is

\[
                         J=q_{03}^{0,1},                \tag{2}
\]

and it contributes the DQ term (DJLb) on fine matching
(67\mid03\mid12\mid45).  Closing (F_{01}) forces the same cell to create

\[
 \boxed{F_{02}=TJLb,qquad(001100;02),\quad
 \mathrm{DQ},\quad67\mid03\mid12\mid45.}               \tag{3}
\]

The two complete rows obey

\[
 \boxed{D F_{02}-T F_{01}=-TP_0S_1Lb.}                 \tag{4}
\]

The right side is a unit on the active normalized chart.  Therefore the
exact SCC cannot absorb its first private face: every minimum closure exports
the nonzero head-(02) face (3).

The unique mate does not change any of the SCC rows.  Thus this is an export,
not a hidden return.  It also gives a sharp negative invariant result: word
and fine type are identical on (1) and (3), so no strictly monotone potential
depending only on private word/fine type can govern the chase.

## Minimum path census

Retain the exact factor chart

\[
 K=S_0c+ZL=0,qquad Z=-1,\quad L=1,                     \tag{5}
\]

together with the inherited source and the twelve nonlinear-octagon cells.
For word (001100) and head (01), exhaustive DQ/PS enumeration gives

\[
\begin{array}{c|rrrrr}
&0&1&2&3&4\\ \hline
\mathrm{PS}&1&0&11&28&50\\
\mathrm{DQ}&0&1&4&10&0.
\end{array}                                              \tag{6}
\]

The cost-zero path is (1).  The only cost-one path uses the inherited direct
coefficient (D=a_{01}), the new mixed edge (J), the cycle edge (L), and the
inherited pure edge (b):

\[
                         67\mid03\mid12\mid45.          \tag{7}
\]

All PS alternatives and all other DQ matchings cost at least two new source
cells.  Hence (2) is the entire minimum orbit.

## Exact head-migration certificate

With (J) symbolic, the two rows are

\[
\begin{aligned}
F_{01}&=Lb(P_0S_1+DJ),\\
F_{02}&=Lb(TJ).
\end{aligned}                                            \tag{8}
\]

Eliminating (J) gives (4) directly.  At the rational normalization,
(P_0=S_1=D=L=b=1) and (T=-1), so closing (F_{01}) forces (J=-1), while
(F_{02}=+1).  No division by (J) is used in (4).

The cell (J) leaves the exact SCC rows (R_0,R_3) unchanged symbolically.
It also does not create a landing on the unused (R_5) branch.  Thus the
three-row SCC structure from the parent theorem remains closed internally,
but its external boundary is nonzero.

## Exhaustive replay

Insert (J=-1) and replay all 6561 rows.  There are twelve incremental row
changes and 52 nonzero full residual rows.  The first two are

```text
001100:01  -1   final 0
001100:02  +1   final 1
```

Both exact-cycle rows remain zero.  The checker pins all twelve incremental
word/head/value entries, so the export claim is not inferred from the two
displayed rows alone.

## Invariant boundary and proof consequence

The transition

\[
 (001100;01,\ 03\mid12\mid45)
 \longrightarrow
 (001100;02,\ 03\mid12\mid45)                           \tag{9}
\]

preserves both word and internal fine matching exactly.  Consequently any
strict ranking based only on those data is false.  Head label changes, but
earlier branches already move heads in both directions, so this note does
not claim a global head order.

What is proved is the required alternative: the first closed exact SCC
exports a new private face, and the export has the exact unit certificate
(4).  The shortest continuation is the minimum-mate classification of
(001100;02), with (K=0) and (J=-1) retained.

## Verification

Run

```text
python computations/verify_n8_pure21_exact_scc_private_export_gate.py
python computations/verify_n8_pure21_exact_scc_private_export_gate.py --mode classification
python computations/verify_n8_pure21_exact_scc_private_export_gate.py --mode symbolic
python computations/verify_n8_pure21_exact_scc_private_export_gate.py --mode replay
python computations/verify_n8_pure21_exact_scc_private_export_gate.py --mode invariant
```

The checker derives the full 105-path census, proves uniqueness of (J),
preserves the word/head/operation/fine labels in (1)--(3), verifies (4),
checks absence of an SCC return, replays every row, and pins the word/fine
counterexample (9).
