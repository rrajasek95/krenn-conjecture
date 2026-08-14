# Two spectators add Beck--Chevalley squares, not a new `Phi` associator

## Verdict

Condition on one source-labelled, pointed, normalized
`Phi_KS,r0/P_f` schema.  Its fixed-tail prolongation from `h=3` through two
spectator edges has no new local operation-changing obstruction at `h=5`.

There is one important qualification.  The four inherited `h=4` overlap
triangles are not by themselves coherent: on the six `h=3` windows of a
four-edge tail they leave a three-dimensional `H1`.  The three standard
disjoint-edge Beck--Chevalley squares have three independent boundary
classes and kill that `H1` exactly.  After those ordinary Hasse faces are
retained, the augmented presentation complex is exact and no higher
associator cell is needed.

```text
six window objects                              6
one-edge overlap arrows                        12
cycle-space dimension                           7
rank of four inherited h4 triangles             4
H1 after h4 triangles only                      3
rank after three Beck--Chevalley squares         7
H1, H2 after the standard squares             0,0.
```

At the fixed-window chain level the result is even stricter: the two top
insertion orders agree, the two restrictions commute, and the mixed
`dq67*dq89` face appears with coefficients `(-1,+1)` and cancels.

Exact checker:
[`verify_h5_pointed_phi_two_spectator_beck_chevalley_coherence.py`](../computations/verify_h5_pointed_phi_two_spectator_beck_chevalley_coherence.py).

## 1. The two-spectator total complex

Use spectator state order

```text
00 = q67*q89,
10 = dq67*q89,
01 = q67*dq89,
11 = dq67*dq89.
```

For any element `z` of the `h=3` response/cap two-term complex,

\[
\begin{aligned}
 d(00z)&=00(dz)+10z+01z,\\
 d(10z)&=-10(dz)-11z,\\
 d(01z)&=-01(dz)+11z,\\
 d(11z)&=11(dz).
\end{aligned}                                        \tag{1}
\]

The signs on the middle two lines are the exterior shuffle signs.  The
checker builds the literal `16 x 16` matrix over the `h=3` basis

```text
(epsilon_s,r0,c_f,E)
```

and verifies `d^2=0` exactly.

Insertion of the squarefree top has defect

\[
 dI_{67,89}-I_{67,89}d
  =(dq_{67}q_{89}+q_{67}dq_{89})\otimes 1.            \tag{2}
\]

Applying `d` to its two terms gives

\[
             -dq_{67}dq_{89}+dq_{67}dq_{89}=0.       \tag{3}
\]

Thus the two-spectator degree complex is

\[
 \mathbf Q\xrightarrow{(1,1)}\mathbf Q^2
 \xrightarrow{(-1,1)}\mathbf Q,                     \tag{4}
\]

which is exact.  The primitive mixed face is hit, not a new cokernel class.
An unsigned comparison would give `2*dq67*dq89` in (3); the exterior sign is
therefore essential.

## 2. Restriction, insertion order, and graded shuffle

Define the two restrictions by

```text
rho67: retain states 00,01; kill 10,11,
rho89: retain states 00,10; kill 01,11.
```

Both are chain maps.  Restricting twice gives

\[
       \rho_{89}\rho_{67}=\rho_{67}\rho_{89}
       =\rho_{67,89},                                \tag{5}
\]

where `rho67,89(q67*q89*z)=z` and every state containing a `dq` is killed.
The two degree-zero insertion orders also agree strictly:

\[
                         I_{67}I_{89}=I_{89}I_{67}.   \tag{6}
\]

The graded transposition interchanges `10` and `01` and sends `11` to
`-11`.  Its square is the identity and it commutes with (1).  Equations
(3), (5), and (6) are the fixed-window Beck--Chevalley coherence.  They need
no additional operation generator.

## 3. The six-window presentation complex

A fixed `h=5` tail has four edge positions `0,1,2,3`.  Its `h=3` windows are
the six two-subsets

```text
01, 02, 03, 12, 13, 23.
```

Two windows have a one-edge `h=4` overlap when their labels share one
position.  These twelve arrows form the octahedral Johnson graph `J(4,2)`.
Its vertex incidence has rank five, so its cycle space has dimension seven.

The four three-edge sub-tails give the inherited `h=4` triangles

```text
(01,02,12), (01,03,13), (02,03,23), (12,13,23).       (7)
```

Their boundaries have rank four.  Hence the complex using only the `h=4`
triangles has

\[
                              \dim H_1=7-4=3.          \tag{8}
\]

This is the exact apparent higher-coherence debt.

The standard disjoint-edge restriction/reinsertion squares may be chosen as

```text
(01,02,23,13),
(01,03,23,12),
(02,03,13,12).                                       (9)
```

Their three boundaries are independent modulo (7).  Adding them raises the
two-face boundary rank from four to seven.  The augmented complex has

```text
dimensions       7 -> 12 -> 6 -> 1
ranks            7     5     1,
```

so it is exact: both `H1` and `H2` vanish.  The three squares in (9) are
ordinary Beck--Chevalley faces for commuting disjoint spectator operations,
not new response-to-cap maps.  Consequently no degree-three associator is
needed at this first iterative stage.

This also gives a useful sharp guard: **four `h=4` triangles alone are not a
valid `h=5` prolongation**.  Any proposed construction that omits (9) leaves
the exact rank-three coherence obstruction (8).

## 4. Selected first faces and protected readouts

On one fixed window, the selected local face consists of the old six
`db01` terms multiplied by `q67*q89`.  The spectator part adds

```text
3 terms dq67*q89*p0*s1*q_e*q_e',
3 terms q67*dq89*p0*s1*q_e*q_e',
3 terms dq67*dq89*p0*s1*q_e*q_e',
```

for `e|e'` equal to `23|45`, `24|35`, or `25|34`.  The last three occur
with opposite signs from the two first-face routes, exactly as in (3).

For a selected cap corner, every local `db01*r0` term has conditional row
signature, in order

```text
B, Eq, target, M, ainc, q, P_f, ores, W, ridge, eta, sigma,
```

equal to

```text
(1,1,1,-1,-1,0,1,0,0,0,0,0).                       (10)
```

Any protected row that is linear for the spectator Hasse action sees the
two mixed faces as `-r0+r0=0`.  Thus there is no new scalar mismatch at
`h=5`.  This last sentence is conditional: the current theorem checks the
source/Hasse coherence and the consequences of protected-row linearity; it
does not construct physical `PP/AugP2` Hasse-linearity.

## 5. Exact scope and remaining global work

This theorem is exact on one four-edge tail and all six of its window
presentations.  It proves that, once a source-valid natural `Phi_KS,r0/P_f`
exists, iterating the first `h=4` structure step through two spectators does
not demand another local operation type or a genuine higher associator.
The only additional cells are the standard shuffle/Hasse triangles and
disjoint-edge Beck--Chevalley squares.

It does not prove full `PAComp(5)`.  At `h=5` there are

```text
tail matchings                                  7!! = 105
h3 window presentations per matching          C(4,2) = 6
tails covered by one fixed h3 partition                  9
cross-partition tails still requiring descent           96.
```

The remaining uniform inputs are therefore:

1. existence of the single physical `Phi_KS,r0/P_f` schema;
2. physical Hasse-linearity of its `PP/AugP2` and protected readouts; and
3. normalized descent/exhaustivity over the complete 105-matching cover.

The two-spectator calculation removes a potential new *local coherence*
theorem.  It does not remove the already isolated physical covariance and
global cover obligations.
