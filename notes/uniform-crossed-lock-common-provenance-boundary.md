# Common matching provenance permits a one-sided crossed lock

## Result

The injective/no-wedge residual of `016886b` is physically real before the
unary target is imposed.  On six residual sites there is one
colour-diagonal common quadratic with

\[
 p_i s_jq^{[2]}=\delta_{ij}X_i\qquad(i,j\in\{1,2\}),   \tag{1}
\]

and an anchor-safe supported-cell deletion whose full lock tuple is

\[
              (L_0,L_{11},L_{12},L_{21},L_{22})
                         =(0,0,Y,0,0),\qquad Y\ne0.     \tag{2}
\]

Thus the two crossed zero rows, even with genuine common-`q` matching
provenance and both diagonal targets, do not force an `L12` component to
have an `L21` mate.  The lock map is injective and its crossed incidence
graph has no complementary wedge.

The sole failed one-bad tensor is the unary top: `q^[3]=0`.  This omission
is load-bearing but completely understood.  The committed aggregate
diagonal source identity excludes **every** colour-diagonal enlargement
which tries to impose `q^[3]=X0` while retaining (1), with arbitrary complex
cancellation.  Therefore a full source extending this guard must introduce
an off-diagonal internal cell.  The nonanchor reselection theorem routes
such a cell whenever its physical pair lies outside the selected anchor
union.  The exact surviving branch is an off-diagonal decoration on an
anchor edge.

Checker:
[`verify_uniform_crossed_lock_common_provenance_boundary.py`](../computations/verify_uniform_crossed_lock_common_provenance_boundary.py).

## 1. The seven-cell packet

Normalize concentrated spokes

```text
p1=e1@0,  s1=e1@1,  p2=e2@2,  s2=e2@3
```

and put

```text
24:11 =  1       35:11 =  1
05:22 =  1       14:22 =  1
15:11 =  1       12:11 =  1       45:11 = -1.
```

Literal matching expansion gives

```text
11:  P1@0 S1@1 24:11 35:11                         = X1
22:  P2@2 S2@3 05:22 14:22                         = X2
12:  P1@0 S2@3 (15:11 24:11 + 12:11 45:11)         = 0
21:                                                       0.
```

The crossed `12` terms have the same word `111211` and coefficients `1,-1`.
Their internal matchings differ on the alternating cycle

```text
1--5--4--2--1.
```

There is no six-site perfect matching in the displayed internal support, so
`q^[3]=0` coefficientwise.

## 2. The exact one-sided lock

Delete the occupied cell `15:11`, i.e.

\[
                              d=-(15{:}11).              \tag{3}
\]

The direction is supported on one physical star and has `d^[2]=0`.  It is
anchor-safe: `15:11` shares `(1,1)` with `12:11` and `(5,1)` with both
`35:11` and `45:11`, so it is not a mutual coordinate anchor.  Every old
mutual anchor survives deletion.

The complete finite differences are

\[
 dq^{[2]}=0,qquad
 p_i s_jdq=0\quad\text{except}\quad
 [111211]p_1s_2dq=-1.                                  \tag{4}

Hence (2) follows directly.  There is one switch direction and one nonzero
lock coordinate, so the lock map has rank one and zero kernel.  Since
`L21=0`, no common-port `L12/L21` wedge exists.

This is not an artifact of the displayed unit weights.  On the nonzero
coefficient torus, the only matching-cycle character is

\[
 {q_{15}^{11}q_{24}^{11}\over q_{12}^{11}q_{45}^{11}}=-1, \tag{5}
\]

which is exactly the crossed-zero equation.  Coordinate rescaling
normalizes every such nonzero realization to the displayed signs.

## 3. What the unary row adds

The packet lies exactly in the hypotheses of
`n8-lemma-e-unary-top-diagonal-aggregate-identity.md`: the four spokes are
concentrated at ordered holes `(0,1)` and `(2,3)`, and the internal
quadratic is colour-diagonal.  That theorem permits arbitrary diagonal
cells on all physical pairs and proves the literal unit

\[
 X_0\text{-top}+X_1\text{-response}+X_2\text{-response}
       +\text{two crossed zero rows}\quad\Longrightarrow\quad 1=0. \tag{6}
\]

Therefore no further diagonal cycle, coefficient choice, or cancellation
mate can attach the missing unary target to (1).  A genuine full packet
must use an off-diagonal internal cell.

If that cell lies on a physical edge used by none of the three selected
pure target matchings, `uniform-one-bad-nonanchor-offdiagonal-good-pair.md`
reselects it to a doubly rank-three good pair and supplies an active
determinant/cofactor product.  The only source-valid escape not consumed by
that theorem is a cell on the selected anchor multigraph.  An alternating
cycle can restore the anchor colour at the endpoints after deleting such a
pair, but a further distinct-head/rank-completion transport is still needed
to obtain the four-good overlap.

## Scope

This is a sharp full-**response** boundary, not a Krenn counterexample.  It
does not satisfy `q^[3]=X0`; the pinned aggregate identity proves that its
whole diagonal unary-attachment chart is empty.  It establishes that the
unary row, not abstract lock rank or common matching provenance alone, must
force the complementary crossed mate.  It does not prove the remaining
decorated-anchor-edge implication.

## Verification

Run

```sh
python3 computations/verify_uniform_crossed_lock_common_provenance_boundary.py
python3 -O computations/verify_uniform_crossed_lock_common_provenance_boundary.py
python3 -I -S computations/verify_uniform_crossed_lock_common_provenance_boundary.py
```
