# The Gate-II root character reaches one invariant C4 face

## Exact identification

The missing root-only character `chi_w` from `dd01569` is not merely
analogous to the chart-complete even Hasse packet. It is that packet.

Order the three matching charts by

```text
A = 01|PS,   B = 0P|1S,   C = 1P|0S.
```

The complete row, endpoint-odd Cartan line, and missing endpoint-even line
are respectively

\[
 (1,1,1),\qquad (0,1,-1),\qquad (2,-1,-1).             \tag{1}
\]

They are pairwise orthogonal. The formal switch carriers obey

\[
             t_1+t_2=(-2,1,1)=-(2A-B-C).              \tag{2}
\]

Thus the scalar proper face of the required `chi_w` cell is exactly the
fixed-chart Spencer generator `L_3=(2A-B-C)H_2`.

Checker:
[`verify_h3_gate_ii_chiw_chart_complete_h2_face.py`](../computations/verify_h3_gate_ii_chiw_chart_complete_h2_face.py).

## Literal first principal-parts packet

With direction order

```text
dD, dq01, dp0, ds1, dp1, ds0,
```

the first Hasse boundary has coefficient

\[
                  \kappa=(2,2,-1,-1,-1,-1).           \tag{3}
\]

After forgetting the duplicate orientation of each direction-pair type,
its `C4` projection is

\[
                         2e_{DQ}-e_{PS,1}-e_{PS,2}.    \tag{4}
\]

This is exactly the unique invariant line of the pinned 140-dimensional
H2 direction-tag quotient. The other `C2+`, `P2/P2^T`, theta-odd `C4`, and
nontrivial site representations are action-groupoid boundaries, provided
the comparison is defined termwise and equivariantly.

The qualification is load-bearing. Locally the complete row and endpoint
flip relation span

```text
(1,1,1), (0,1,-1),
```

and have rank two. Adding (4) raises the rank to three. Consequently neither
complete rows nor the normalized characteristic-zero endpoint bar can
totalize the invariant face.

## Target correction and the first physical datum

The root-only target defect has literal word signature

```text
word basis              m_(c|i), m_(i|c), p_i, p_c
chi_w defect                 1,       1,    -1,  -1
C2+ J*/even correction      -1,      -1,     1,   1
sum                           0,       0,     0,   0.
```

Thus there is no independent target-normal obstruction after the physical
`P2` placement is granted. The endpoint-odd prism alone still does not do
this: it kills the target only by replacing `chi_w` with the already-known
mixed character.

After the target correction and groupoid contractions, the first
uncontracted same-grade source datum is precisely

```text
U_C4[D,Q01;2345]

domain       Hasse[2](D,Q01), residual sites 2345
local face   q23*q45 + q24*q35 + q25*q34
word/grade   original fan word/fine/repeated grade, with the DQ tag retained
tail         one literal augmentation-one C4 tail
target       0
ainc         0
q=M-a        0
Eq, W        0, 0
ores, ridge  0, 0
```

Here “augmentation one” is occurrence augmentation in the three-matching
`C4` tail. It is not the physical `ainc` readout; the latter is zero. The
`PS` representative is `Hasse[2](P0,S1)` in the same transported fan grade.
It cannot be relabelled into `P2`, because the operation tag and repeated
grade differ.

This gives the exact first irreducible face, not a new conjectural packet:
it is the already isolated generic relative-C4 column. If it is absent after
literal same-grade placement, the committed augmented extension promotes
its dual to a terminal. Before that placement, the coefficient covector is
not yet a physical terminal.

## The downstream P2 face remains separate

The tag quotient contracts the original `P2/P2^T` sector, but restriction
and word promotion create the known private carrier in a different grade:

```text
lower word          0112
intermediate word   0102
residual             q45:12
reinsertion          q23:21
top grade            01211222 / repeated P3+K2
carrier              t_zpriv.
```

Its augmented signature is not defined until a physical placement is
constructed. Assigning target, anchor, or physical `q` values to the formal
graph carrier would be an overclaim. The existing target/Eq cone then
closes its target-normal part, but not this source placement.

Therefore the shortest construction of the target-corrected `chi_w` cell
has exactly two typed source inputs:

1. the same-grade protected relative-C4 column above; and
2. after restriction, the word-`0102` `t_zpriv` augmented landing.

The first is invariant and cannot be removed by endpoint groupoid or
complete rows. The second is downstream and cannot be identified with it.
This note constructs neither column; it proves the exact chain from
`chi_w` to them and freezes the first irreducible face with all known
physical readouts.

Run normally, optimized, and isolated/no-site. The checker pins all inputs
and records a frozen ledger digest.
