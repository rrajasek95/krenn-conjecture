# Actual divided-Hasse extraction does not isolate the retained pair

## The exact product-rule boundary

Let `F` be any complete target or response matching coefficient and let an
actual bivariate source lift have the form

\[
 X(s,t)=x+s\xi+t\zeta+st\eta+\cdots .
\]

Because every source occurrence is multiaffine, literal coefficient
extraction gives

\[
 [st]F(X)=J_xF(\eta)+B_xF(\xi,\zeta).                 \tag{1}
\]

Here `B` is the sum over **every ordered pair** of varied cells which occurs
in one literal matching.  The retained pair is only one summand.  Thus an
exact source family proves

\[
 J_xF(\eta)+\sum_{(a,b)}
 \xi_a\zeta_b\,H_{a,b}(x)=0,                         \tag{2}
\]

not `H_(a,b)=0` for a selected pair.

The checker enumerates the literal complements in all six relevant pair
types:

```text
QQ target:       1 one-edge complement
QQ response:     3 C2+ complements
DQ response:     3 C4 complements
PS response:     3 C4 complements
PQ response:     3 P2 complements
SQ response:     3 P2 complements.
```

Checker:
[`verify_h3_retained_pair_divided_hasse_min_support_gate.py`](../computations/verify_h3_retained_pair_divided_hasse_min_support_gate.py).

## Literal mixed-word guard

Work in the physical mixed output word `001122`.  Retain the diagonal tail
`q45[22]=1`, put every varied cell equal to zero at the base point, and use
the actual polynomial family

```text
q01[00] = s,      q02[01] = s,
q23[11] = t,      q13[01] = -t,
q45[22] = 1.
```

The supported target matchings are

```text
q01[00] q23[11] q45[22],
q02[01] q13[01] q45[22].
```

They have the same word and give the literal identity

\[
 H_{001122}=q_{45}(q_{01}q_{23}+q_{02}q_{13})
             =st-st=0.                               \tag{3}
\]

With the direct response scalar `D=1` and all endpoint cells zero, the
complete direct-response row is `D H_(001122)=0` as well.  This is an
actual coefficient identity in `Q[s,t]`, not a derivative evaluated at one
point.

The union of the five displayed `q` cells has exactly those two perfect
matchings, and both have word `001122`.  Hence every other mixed target word
is identically zero on this packet.  The first missing equations needed for
a full GHZ source are the three normalized pure target coefficients, followed
by their full response and augmented companions.  The checker does not hide
that completion requirement.

Nevertheless its divided-Hasse faces are

\[
 H_{q_{01},q_{23}}=+q_{45}=1,
 \qquad
 H_{q_{02},q_{13}}=-q_{45}=-1.                       \tag{4}
\]

Equation (2) is `1-1=0`; the marked lower packet is nonzero.

## Why minimum support does not route the guard

At the base point the only occupied `q` cell is the diagonal tail
`q45[22]`.  The four varied cells are all zero.  For generic `(s,t)` the
family activates four cells and kills none, so it leaves the minimum-support
stratum rather than producing an occupied-coordinate deletion.

The two offdiagonal cells `q02[01]` and `q13[01]` are also zero at the base.
The target-augmented active-minor theorem starts from a **nonzero** physical
offdiagonal cell, so it does not fire here.  Nor do the identically zero
mixed target/direct-response rows themselves provide an augmented terminal
separator.

The previously proved positive routes remain exact under their hypotheses:

- an anchor-safe kernel supported on occupied occurrence-incompatible cells
  gives affine support deletion; and
- a nonzero offdiagonal base cell gives an active determinant/cofactor
  product.

Actual divided-Hasse extraction supplies neither hypothesis.

## Sharp remaining theorem

To force the selected retained-pair packet, the complete unary, four
response, anchor, physical-`q`, and ridge rows must do one of two things:

1. kill every silent same-grade mate and the mixed correction `J eta`; or
2. force a mate/correction cell to be already occupied with the incidence
   needed by the deletion or active/terminal theorem.

Without that full-row statement, minimum support and coefficient extraction
alone do not prove `H=0`.  The guard is a literal complete mixed target and
direct-response packet, not a claimed completion of the normalized pure
targets or all GHZ source rows.

Pinned ledger:

```text
299f3d06b8dc986bc900d28072a95b320e900f69139f5b34b7d7301f44f1814d
```
