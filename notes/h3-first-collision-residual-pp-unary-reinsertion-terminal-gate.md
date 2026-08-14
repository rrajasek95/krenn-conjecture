# The first 24-term collision residual reduces to a two-hole unary reinsertion class

## Verdict

Fix the first root sector

```text
root             E01: p0 -> D, q01 -> -s1
response word    11:110000
fine sector      missing 0 / doubled S
topology         P3+2K2
```

and write `C` for its symmetric 45-term collision row and `R` for the
signed 24-term residual.  The top covector

\[
                         \lambda_R=R/24
\]

satisfies `lambda_R(C)=0` and `lambda_R(R)=1`.

On all 180 occurrence-labelled first-principal-parts flags, its canonical
reinsertion-natural normalized descendant is

\[
                         \lambda_{PP}^{0}=dR/96.       \tag{1}
\]

It has values `+1/96` on 48 flags, `-1/96` on 48 flags, and zero on the
remaining 84.  It kills `dC` and reads one on `dR`.

The complete distinct-direction boundary is not an anonymous cokernel.
Every flag away from the varied edge belongs to a literal `C2+`, `C4`, or
`P2` packet.  After those packets are removed, exactly 24 same-cell flags
remain.  They form

\[
 J_{E01}=(U_{dD}-K_{D,q01})-(U_{ds1}-K_{p0,s1}),       \tag{2}
\]

the **two-hole unary reinsertion anti-diagonal**.  It is detected by
`+1/24` on the twelve `p0->D,dD` flags and `-1/24` on the twelve
`q01->-s1,ds1` flags.  This detector kills the symmetric collision, every
repeated group, and every distinct-direction `C2+/C4/P2` packet.

Neither unary cofactor in (2) is the physical six-site unary row.  Their
vertex sets are respectively

```text
S,1,2,3,4,5        and        P,S,2,3,4,5,
```

not `0,1,2,3,4,5`.  Thus the existing lower coefficient packets do not
fill the residual.  The shortest missing datum is one root-labelled,
one-hole unary PP/reinsertion section connecting these two augmented
cofactors in the same word/fine grade.

Exact checker:
[`verify_h3_first_collision_residual_pp_unary_reinsertion_terminal_gate.py`](../computations/verify_h3_first_collision_residual_pp_unary_reinsertion_terminal_gate.py).

## 1. Forced values on the 21 complete PP groups

The 180 flags split canonically into

```text
6 unary groups,       15 flags each,
15 repeated groups,   6 flags each.
```

For the raw descendant (1), the six unary sums are

| removed doubled-star endpoint | value |
|---|---:|
| `P` (`dD`) | `+1/8` |
| `1` (`ds1`) | `-1/8` |
| `2,3,4,5` | `0` |

The only nonzero repeated sums are, for `x=2,3,4,5`,

\[
       \lambda_{PP}^{0}(V_{p_x})=-1/32,
       \qquad
       \lambda_{PP}^{0}(V_{q_{1x}})=+1/32.           \tag{3}
\]

All other repeated sums vanish.  Hence the collected charge is the exact
`K2,4` cut

\[
 32g=\sum_{x=2}^{5}(U_P-U_1-V_{p_x}+V_{q_{1x}}).     \tag{4}
\]

These values are forced by equal reinsertion weight on the four flags of
each collision occurrence together with the normalization on `dR`.

## 2. Literal source-direction packet census

Retain the original response occurrence, the root branch, the removed
edge, and the output collision monomial.  A flag for which the removed edge
differs from the root image has two distinct source directions.  The exact
30-packet census is

| lower packet | packets | nonzero under (1) |
|---|---:|---:|
| `C4` from `DQ` or distinct `PS` | 6 | 4 |
| `C2+` from disjoint `QQ` | 6 | 6 |
| `P2` from disjoint `PQ` or `SQ` | 18 | 18 |

Every packet contains three flags.  Their value histograms are

```text
C4:   4*(+1/32), 2*0
C2+:  6*(-1/48)
P2:   8*(-1/32), 6*(+1/48), 4*(+1/32).
```

The apparent `C4` and `C2+` charges cancel after collection against sibling
`P2` charges: the `U_x` groups and residual `q_xy` groups have total zero.
The four surviving repeated terms in each direction are the `K2,4` cut in
(4).

There are two exceptional families.  If `p0` is changed to `D` and the PP
edge is that same `D`, or if `q01` is changed to `-s1` and the PP edge is
that same `s1`, the pair of source directions is repeated rather than
distinct.  Multiaffine second-Hasse classification does not put these flags
in `C2+`, `C4`, or `P2`.  They are PP/reinsertion faces.

At the level of flagged vectors the exact identity is

\[
        dR=J_{E01}+\sum_{K\in C2^+,C4,P2}\epsilon_K K. \tag{5}
\]

The signs `epsilon_K` are `+1` for the `p0->D` branch and `-1` for the
`q01->-s1` branch.  Exact rank calculation verifies that `dR-J_E01` lies
in the 30-packet span, while neither `dR` nor `J_E01` does.

## 3. The corrected terminal dual

Require a covector to:

1. retain the root branch and be symmetric in the four residual sites;
2. kill `dC` and every distinct-direction lower packet; and
3. read one on `dR`.

Every non-reinsertion orbit belongs to a three-term lower packet, so its
weight is forced to zero.  If `a` and `b` are the two same-cell weights,
killing `dC` gives `a+b=0`, while normalization gives
`12a-12b=1`.  Therefore

\[
                      a=1/24,\qquad b=-1/24.          \tag{6}

This gives a 24-supported exact detector `mu_E01`.  Its remaining group
values are

```text
mu_E01(U_dD)=+1/2,
mu_E01(U_ds1)=-1/2,
all repeated groups and all other unary groups = 0.
```

Thus the full first collision residual does not stop at a 45-coordinate
collision separator.  After mandatory first-PP completion it stops at the
smaller, explicitly placed class (2).

## 4. Why existing columns do not fill it

The column verdict, with all labels retained, is:

| family | effect |
|---|---|
| complete symmetric collision / `P3+2K2` | killed by `lambda_R` and `mu_E01` |
| repeated six-term rows | killed by `mu_E01` |
| distinct-direction `C2+/C4/P2` | remove the corresponding part of `dR`, but leave `J_E01` |
| physical unary on `0,1,2,3,4,5` | not one of the two forward-sector cofactors |
| canonical AugP2 | word `01211222`, not the response word `11:110000` |

Topology therefore does not authorize the last identification.  The pinned
lower `P2` audit independently says that even in the canonical cap word its
first physical placement needs an occurrence-local one-endpoint PP section.
Here there is an earlier word/fine/root-labelled one-hole unary section.

The exact terminal fork is:

```text
face-natural E01 one-hole unary reinsertion landing exists
    -> fills J_E01 and this residual lane;

the complete same-word/fine/root augmented map has no such landing
    -> mu_E01 is the first-collision terminal detector.
```

The second arm is unconditional only after the detector is extended through
all target, Eq, `q`, anchor, `W`, ordinary-residue and ridge rows in this
same physical grade.  The present calculation proves the exact local fork,
not that global exhaustivity statement.

## Verification

Run

```text
python3 computations/verify_h3_first_collision_residual_pp_unary_reinsertion_terminal_gate.py
python3 -O computations/verify_h3_first_collision_residual_pp_unary_reinsertion_terminal_gate.py
python3 -I -S computations/verify_h3_first_collision_residual_pp_unary_reinsertion_terminal_gate.py
```

The checker uses exact rational arithmetic, reconstructs all 180 flags from
the 105 complete response occurrences, retains source/root/removed-edge
tags, verifies the packet-span identity, and freezes both normalized duals.
