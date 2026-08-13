# Two-site contraction is deletion plus one cross-source derivative

## Exact identity

Let `S` be an even set of sites, let `p,q` be distinct, and put
`R=S-{p,q}`. For every pair `u<v`, retain the completely arbitrary endpoint
matrix

\[
 A_{uv}\in V_u\otimes V_v.
\]

No symmetry, rank-one, positivity, or same-endpoint-colour assumption is
made. Let `C` be an arbitrary bilinear covector on `V_p tensor V_q`. Define

\[
 s_C=\langle C,A_{pq}\rangle
\]

and, for `i,j in R`,

\[
 B^C_{ij}=\operatorname{contr}_{p,q}^C
 \big(A_{pi}\otimes A_{qj}+A_{pj}\otimes A_{qi}\big).
\]

Splitting matchings according as they use `pq` or send `p,q` to two
different residual sites gives

\[
 \boxed{
 \operatorname{contr}_{p,q}^C H_S(A)
 =s_C H_R(A)+D H_R(A)[B^C].}
 \tag{1}
\]

The checker verifies (1) coefficientwise with arbitrary ordered endpoint
matrices.

For a matrix-unit cap `C=e_a^* tensor e_b^*`, let `u_i^a` be the vector at
site `i` obtained by contracting the `p` endpoint of `A_pi` against
`e_a^*`, and define `v_i^b` from the `q` star. Then

\[
 B^{a,b}_{ij}=u_i^a\otimes v_j^b+v_i^b\otimes u_j^a. \tag{2}
\]

This is the exact arbitrary-endpoint-colour formula.

Checker:
[`verify_decorated_hafnian_two_site_contraction_deletion_counterguard.py`](../computations/verify_decorated_hafnian_two_site_contraction_deletion_counterguard.py).

## What literal deletion means

Deleting `p,q` from the **same source system** gives exactly `H_R(A)`. Thus
the contraction is represented by a nonzero scalar literal deletion if and
only if

\[
 D H_R(A)[B^C]\in \langle H_R(A)\rangle
\]

and the resulting total scalar is nonzero. Equivalently, the projective
cross-source class

\[
 \kappa_{pq}^C=
 [D H_R(A)[B^C]]\quad\text{in}\quad
 T_R/\langle H_R(A)\rangle                              \tag{3}
\]

must vanish.

For the diagonal target,

\[
 \operatorname{contr}_{p,q}^C\Delta_{S,r}
 =\sum_{a=0}^{r-1}C_{aa}e_a^{\otimes R}.                 \tag{4}

Hence:

- an off-diagonal endpoint cap gives zero;
- `e_a^* tensor e_a^*` gives the pure tensor `e_a^(tensor R)`;
- the all-colours trace cap `C=I` gives `Delta_(R,r)`.

In the last case, assuming `H_S(A)=Delta_(S,r)`, condition (3) is equivalent
to

\[
                     H_R(A)\in\mathbb C^\times\Delta_{R,r}. \tag{5}
\]

Thus the tempting contraction step has not proved an induction theorem:
for `C=I`, finding a pair with no projective correction is exactly finding a
deleted subsystem which already realizes the smaller diagonal target.

## Square-free Grassmann formulation

The clean generating object is the commutative square-zero, or zeon,
algebra on the site-colour variables. If

\[
 Q=\sum_{u<v}A_{uv},
\]

then `H_S(A)` is the coefficient using every site once in `exp(Q)`. Splitting
off `p,q` and applying the cap gives

\[
 [\operatorname{contr}_{p,q}^C e^Q]_R
       =[(s_C+B^C)e^{Q_R}]_R,                            \tag{6}
\]

which is (1).

This distinction from the ordinary exterior algebra is load-bearing. In a
true Grassmann algebra the two cross matchings acquire opposite signs and
produce a Pluecker wedge. Hafnians use commuting square-zero variables, so
(2) has a plus sign. The cross star is not an alternating rank-one form, and
ordinary Pfaffian/Grassmann Schur-complement identities do not eliminate it.

## Why an ordinary Schur update also fails

Suppose `s_C` is a unit and put `K=B^C/s_C`. Taylor expansion gives

\[
 s_C H_R(A+K)=s_CH_R(A)+D H_R(A)[B^C]
 +s_C\sum_{j\ge2}{1\over j!}D^jH_R(A)[K^j].             \tag{7}
\]

The contraction contains only the first two terms. Replacing the cap by
effective pair edges is valid at top degree exactly when the higher Taylor
remainder in (7) vanishes.

The checker gives a scalar six-site counterexample. Let the two capped sites
be `p,q`, include the unit edge `pq`, connect `p` to boundary sites `0,2`,
and connect `q` to `1,3`, with no old boundary edges. Then

```text
literal contraction                        0
old deleted hafnian                        0
first derivative D H[ B ]                  0
hafnian after the Schur edge update A+B    2.
```

The value `2` is the two perfect matchings of the induced `K2,2`. It is the
first higher `B` term, which the true contraction never contained.

## Exact minimal counterguards

### Ternary four-site source

On `K4`, assign one perfect matching to each of three colours, with unit
same-colour cells. The resulting six-cell source realizes `Delta_(4,3)`.
Every cell is essential: removing it destroys the unique matching of its
colour.

For every one of the six pairs, literal deletion leaves one pure-colour
edge, while trace contraction gives `Delta_(2,3)`. The cross term supplies
the other two colours. Therefore

```text
trace pairs tested                         6
trace pairs giving scalar literal deletion 0.
```

All ordered endpoint colours are visible. At a fixed pair:

- the diagonal colour carried by `pq` is the direct `s_C H_R` term;
- each of the other two diagonal colours is supplied entirely by `B^C`;
- all six off-diagonal endpoint caps vanish termwise.

So even exact source-cell minimality does not force a cross-free pair.

### Six-site cancellation source

The exact nine-cell source from `small-tensor-findings.md` realizes
`Delta_(6,2)` using one mixed cancellation. Every decorated cell is
essential. The checker tests all fifteen trace contractions and finds

```text
trace pairs tested                         15
trace pairs giving scalar literal deletion 0.
```

Thus even order six plus cancellation-rich source minimality does not force
the deletion step in a uniform arbitrary-colour theorem.

The two examples deliberately leave one possible specialized theorem open:
the first is ternary but has only four sites, and the second has six sites
but is binary. They show that a positive result must use the conjunction
`r=3`, `|S|>=6`, and additional global incidence/source equations. Neither
minimality nor contraction algebra alone contains it.

## Frontier

The global contraction route has a sharp target now. A positive theorem
must prove, for a hypothetical minimal ternary source at even order at least
six, that some induced deletion satisfies (5), or directly that some
projective class (3) vanishes. It cannot replace the cap by an ordinary
hafnian Schur complement.

This artifact proves the contraction identity, its exact deletion and
edge-update criteria, and the minimal counterguards. It does not exclude a
specifically ternary `n>=6` global incidence theorem.

Run normally, optimized, and isolated/no-site. The checker records the
frozen ledger digest.
