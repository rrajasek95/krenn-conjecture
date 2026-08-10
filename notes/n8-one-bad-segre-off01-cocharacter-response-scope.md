# The off-`01` cocharacter exposes the top face but loses the responses

## Exact verdict

The 24-cell class in `c9b2571` is an honestly exposed affine face for the
residual quadratic and its unary top equation.  One integral cocharacter
works for all twelve pure-`00` anchor matchings avoiding edge `01`:

```text
site 0: 0 0 0       site 3: 0 0 1
site 1: 0 1 1       site 4: 0 1 0
site 2: 0 1 0       site 5: 0 0 1.
```

It has weight zero on the fourteen cells of `H`, all twenty-four cells of
the face, and every pure-`00` cell.  On the other 52 mixed cells its weights
are 44 copies of `1` and eight copies of `2`.

This does **not**, however, put a full common-`q` one-bad packet on the
24-cell face.  The response anchors are lost in the affine limit.

## The exact cone

For every off-`01` anchor, the face equalities have rank twelve.  Their
annihilator consists exactly of the six coordinates

\[
 u_{11},u_{12},u_{21},u_{32},u_{41},u_{52}.
\]

Each coordinate occurs alone as the incidence of a remaining mixed cell.
Therefore strict positivity on all 52 remaining mixed cells forces all six
parameters to be positive.  This is not an accident of the displayed
integral point.

For colour `1`, the zero-weight diagonal graph consequently has only

```text
03, 05, 35,
```

and for colour `2` it has only

```text
02, 04, 24.
```

Neither triangle contains two disjoint edges.  A term of
`p1*s1*q^[2]` or `p2*s2*q^[2]` needs a two-edge matching after deleting the
two star sites.  Hence, for every choice of limiting stars,

\[
 p_1s_1(q_0)^{[2]}=p_2s_2(q_0)^{[2]}=0,
\]

where `q0` is the affine zero-weight limit.  It cannot retain the required
targets `X1` and `X2`.

## Why endpoint rescaling does not repair the chart argument

The displayed cocharacter gives pure-word weights `(0,3,3)`.  Endpoint or
star scalar shifts can formally subtract the last two weights, but then
some source-star valuations are negative.  More importantly, every physical
monomial in a fixed response coefficient has weight

\[
 a_i+b_j+\sum_r u_{r,w_r},
\]

independent of the two holes and of the residual matching.  Thus restoring a
diagonal target retains the positive-weight `q` terms in the same associated
response row; it does not replace that row by the response polynomial of the
affine 24-cell support.

Accordingly the all-subsets response theorem at `4a213d8` is exact once the
fixed face has been reached, but this cocharacter alone does not prove the
upstream chart-cover statement.  A source-preserving filtered-response
lemma, or a different re-selection producing response anchors in the affine
limit, is still required.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_one_bad_segre_off01_cocharacter_response_scope.py
.venv/bin/python -O computations/verify_n8_one_bad_segre_off01_cocharacter_response_scope.py
```
