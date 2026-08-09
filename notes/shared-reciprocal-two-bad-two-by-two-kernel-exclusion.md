# Two minimal kernel bridges cannot carry the pure quotient class

## 1. Result

Continue in the coordinate-diagonal five-site quotient of
[`the two-bad cofactor theorem`](shared-reciprocal-two-bad-cofactor-quotient.md).
The
[`parity-straightening lemma`](shared-reciprocal-two-bad-two-centre-parity-straightening.md)
makes every minimal two-centre kernel relation contributing to a pure
`t` product a target-axis bridge.

> **Two-by-two bridge lemma.**  Suppose both kernel rows `U,V` are minimal
> two-centre relations, the two known pure tensors have distinct one-centre
> preimages, and `PUVq` has a nonzero `X_t` coefficient.  If the internal
> quadratic is colour-diagonal, the equations are inconsistent over every
> integral domain.

This closes the first packet in which both kernel rows are genuinely
multi-centre.  The argument uses the two kernel zero classes and the bright
pure rows exactly; the other common-hafnian zero classes are not needed in
this stratum.

## 2. Normalization and bridge incidence

Choose a nonzero pure monomial and normalize

```text
selected U centre 0, selected V centre 1,
selected P centre 2, q_34(t,t) != 0.
```

Let `u'` and `v'` be the alternate centres of the two bridges.  Parity
straightening gives

\[
 K_0=e_t^{(u')}Z_U,\quad K_{u'}=e_t^{(0)}Z_U,
 \qquad
 K_1=e_t^{(v')}Z_V,\quad K_{v'}=e_t^{(1)}Z_V.          \tag{1}
\]

There are `4 x 4=16` labelled alternate-centre pairs.  Their bridge
supports have intersection sizes

```text
same pair (intersection 2)       1
one shared centre                9
disjoint                         6
```

A one-centre lift of `X_a` or `X_c` cannot be centred on a bridge endpoint:
its cofactor is pure `a` or `c`, whereas (1) gives a nonzero target factor
at the opposite endpoint.  A disjoint pair uses four of the five sites and
leaves only one possible bright centre.  It therefore cannot host the two
distinct pure lifts.  This closes all six disjoint incidences without a
matching case split.

## 3. Unique mixed words

For the same/shared incidences, choose one nonzero monochromatic matching
term in each pure cofactor.  Together with `q_34(t,t)`, these are mandatory
nonzero diagonal cells.  Two disjoint mandatory edges of different colours
inside a four-site cofactor give a 2+2 word with exactly one compatible
matching.  Hence its coefficient cannot cancel after arbitrary additional
diagonal cells are added.

The checker tests this word against the four target-factor conditions in
(1) and the two pure cofactors.  It closes all

\[
 54\ \text{same-pair configurations}
 \quad+\quad
 162\ \text{one-shared-centre configurations}.         \tag{2}
\]

The deterministic first-witness histogram is

```text
U-left factor       104
U-right factor       56
V-left factor        24
V-right factor        6
pure-a cofactor      26
```

Deleting all four bridge-factor tests leaves 80 configurations; deleting
both pure-cofactor tests leaves 26.  Thus both structural inputs are
load-bearing even though individual conditions have redundant coverage.

This is a coefficient-independent finite audit of a hand normal form, not
a support-face CEGAR.

## 4. Remaining coordinate-diagonal boundary

Combining the atomic, parity, one-by-two, and present two-by-two lemmas, a
coordinate-diagonal survivor with one-centre bright lifts cannot contain a
one- or two-centre kernel component that contributes to the pure product.
The remaining theorem-level branches are:

- a minimal kernel circuit on at least three centres; or
- a multi-centre preimage of one of the two known pure tensors.

Mixed-colour internal cells remain a separate later branch, as intended.

## 5. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_two_by_two_kernel_exclusion.py
python3 -O computations/verify_shared_reciprocal_two_bad_two_by_two_kernel_exclusion.py
```

The checker uses only the standard library, pins the parity-straightening
dependency, and reconstructs all 216 same/shared matching configurations.
