# Independent audit of the fixed-(q,z) three-cell cancellation frontier

## 1. Scope and conclusion

This is a clean-room audit of the three-cell theorem at the single displayed
polarized seed

\[
\begin{aligned}
q={}&23_{00}+45_{00}+67_{00}+01_{11}+36_{11}+57_{11}\\
   &+02_{22}+14_{22}+56_{22},\\
z={}&01_{00}+24_{11}+37_{22}.
\end{aligned}
\]

The independent checker is
[`verify_polarized_eight_site_fixed_q_three_extra_frontier_independent.py`](../computations/verify_polarized_eight_site_fixed_q_three_extra_frontier_independent.py).
It imports neither the primary checker nor any exploration module.  It starts
from the two literal cell lists above.

For three distinct cells \(e<f<g\) outside the nine-cell support of \(q\), it
exhausts all \(\binom{243}{3}=2{,}362{,}041\) triples and solves

\[
 z(q+te+uf+vg)^{[3]}=\Delta_{8,3}
 \quad\text{on}\quad (t,u,v)\in(\mathbb C^\times)^3.
\]

The exact classification agrees with the claimed theorem:

| class | exact count |
|---|---:|
| identically zero debt | 87,027 |
| one soluble binomial relation | 187 |
| exceptional insoluble system | 1 |
| rejected by a singleton Laurent monomial | 2,274,826 |

The independent projective Gram audit closes 180 of the 187 binomial
families.  Changed-order localized ideals over \(\mathbb Q\) have reduced
Groebner basis \([1]\) in each of the remaining seven cases.  Hence, for all
187 genuinely new families and every torus point on the stated binomial
locus,

\[
 (aQ+4ps)Q^{[3]}\ne\Delta_{8,3}
\]

for every scalar \(a\) and linear forms \(p,s\).

This conclusion is strictly about the fixed literal pair \((q,z)\), exactly
three extra cells, and the 187 non-identical cancellation families.  It makes
no pair-cap claim for the 87,027 all-zero-debt triples, for four or more added
cells, for a varying certificate \(z\), or for arbitrary quadratics.  It is
not a proof of Krenn's conjecture.

## 2. Endpoint order and divided-power audit

A cell is represented as

\[
        (i,j,c_i,c_j),\qquad i<j,
\]

so the colour slots always follow increasing endpoint order.  The checker
constructs all \(28\cdot9=252\) endpoint-colour cells in precisely this
convention, asserts that the displayed \(q,z\) obey it, and verifies directly
that

\[
                     zq^{[3]}=\Delta_{8,3}
\]

with coefficient one on each of the three pure top words and zero elsewhere.

Every divided power is built with unordered combinations of distinct,
site-disjoint summands.  Thus each subset occurs once, with no hidden
factorial.  A second tagged expansion is performed for every one of the 188
non-singleton cases and agrees term by term with the debt construction.  The
audited debt support counts are

\[
 99\cdot0+135\cdot1+9\cdot2
\]

for one-cell debts and

\[
 25{,}830\cdot0+3{,}573\cdot1
\]

for all 29,403 pair debts.  Every nonzero incidence coefficient in the
one-, two-, and three-cell debts is exactly one.

The checker also reconstructs \(Q^{[3]}\) and \(Q^{[4]}\) independently for
each of the 187 families and verifies, tag by tag,

\[
                         Q Q^{[3]}=4Q^{[4]}.
\]

This fixes the direct term in the pair-cap equations as \(4aQ^{[4]}\), rather
than silently omitting or misnormalizing it.

## 3. Exact torus classification

For every triple the checker forms the seven exact debt vectors

\[
D_e,D_f,D_g,D_{ef},D_{eg},D_{fg},D_{efg}
\]

and labels their contributions by

\[
t,u,v,tu,tv,uv,tuv.
\]

If a top word occurs in only one of these Laurent monomials, its equation
cannot vanish on the complex torus.  This is an exact rejection certificate
for 2,274,826 triples.  Of the remaining cases:

* all seven debts vanish for 87,027 triples;
* every equation for 187 triples reduces, after removing a common nonzero
  torus monomial, to one of four binomials;
* the sole other triple is \((01_{00},24_{11},37_{22})\).

The 87,027 zero-debt triples are independently identified as exactly the
triangles in the 3,960-edge compatibility graph on the 99 invisible cells.
For every such triangle the three-cell debt also vanishes.

The four soluble relations and their counts are:

| relation | count | first lexicographic triple |
|---|---:|---|
| \(v+tu=0\) | 103 | \((03_{10},15_{10},35_{00})\) |
| \(t+uv=0\) | 48 | \((01_{00},05_{01},17_{01})\) |
| \(1+tv=0\) | 9 | \((04_{20},16_{00},25_{20})\) |
| \(1+tu=0\) | 27 | \((04_{10},15_{10},26_{00})\) |

Explicit nonzero witnesses show that each binomial really has torus points,
so the classification is sufficient as well as necessary.  Every one of
these 187 triples has exactly one individually visible cell.  Their physical
pair intersection profiles are 150 of type \((0,1,1)\) and 37 of type
\((0,0,0)\).

For the exceptional triple the equations are

\[
 t+u=0,\qquad u+v=0,\qquad tu+tv+uv=0.
\]

The first two give \(t=v=-u\), after which the last expression is
\(-u^2\), not zero on the torus.  This independently proves that the
exceptional case has no solution.  The audit exposed this sign typo in an
initial draft of the primary note; that note has now been corrected, and
the inconsistency conclusion was unchanged.

## 4. Independent projective closure

For each of the 187 families, the checker reconstructs every top coordinate
of

\[
                 4psQ^{[3]}+4aQ^{[4]}=\Delta_{8,3}.
\]

It uses only parameter-safe implications.  A non-target coordinate with no
direct \(aQ^{[4]}\) term and exactly one tagged Gram contributor forces that
Gram entry to zero.  A pure target coordinate with no direct term requires
at least one of its Gram contributors to be nonzero.  Branching over those
finite choices is exhaustive even when other contributors may cancel.

The orthogonality graph is checked by a parity union-find, rather than by the
primary implementation's route.  On the endpoints known to be nonzero, each
zero Gram edge flips projective line parity.  A required nonzero edge is
impossible when its endpoints are connected with odd parity or lie in the
same non-bipartite component.

This independently gives

\[
             159\cdot1+20\cdot2+1\cdot3=202
\]

closed branches, all by the isotropic-component certificate, and closes
exactly 180 families.  The seven cases deliberately left open are exactly

\[
\begin{gathered}
(01_{00},05_{01},17_{01}),\quad
(01_{00},06_{01},13_{01}),\quad
(01_{00},07_{01},15_{01}),\\
(03_{12},17_{12},37_{22}),\quad
(04_{11},12_{11},37_{22}),\\
(06_{12},15_{12},37_{22}),\quad
(07_{12},13_{12},37_{22}).
\end{gathered}
\]

In each, a pure coordinate has a direct \(aQ^{[4]}\) term, so the checker
does not make the unsafe inference that some Gram contributor alone must be
nonzero.

## 5. Seven localized ideals

For each residual case the checker writes every coordinate equation over
\(\mathbb Q\), includes its exact binomial relation, and localizes the
parameter torus with

\[
                         \rho tuv-1=0.
\]

There are 53 variables.  The seven generator counts, in the displayed order,
are

\[
                  290,284,284,284,319,284,290.
\]

The replay changes both orders relative to the primary computation:
parameters precede the scalar and reverse-ordered mode variables, while the
torus equation and binomial relation precede reverse-word coordinate
generators; direct \(aQ^{[4]}\) terms precede Gram terms.  Singular reduces
all seven ideals to the one-element basis \([1]\).  This is an exact
characteristic-zero conclusion, and localization makes it precisely a
statement on \((\mathbb C^\times)^3\).

Run the full audit with

```text
python3 computations/verify_polarized_eight_site_fixed_q_three_extra_frontier_independent.py --workers 3
```

The clean-room ledgers have SHA-256 digests

| ledger | SHA-256 |
|---|---|
| exhaustive classification | `cc8b33c9462d982788f368c8d1d89179b0ad0b27bd14faa6f7241e8dd4be0373` |
| 87,027 zero-debt triples | `47d231f82e3e6bd272e0b440667a06fc6fe110716a916512555330d644e08a22` |
| 187 ordered binomial families | `38daeebe50655f23d71ff78682466515e14b8d7167bddf0f8abfc080896aa7d0` |
| 187 projective outcomes | `f74dbe4f1c7c6e530576a0948d1abb8d92a3de683d99106c3d2004efd3f0693b` |
| seven changed-order ideal inputs | `7aa71d2391d0d11e044485d98ad859056b30692be5ee7574a759c3bd9a47744c` |

These hashes use an independent record encoding and therefore are not
expected to equal differently encoded primary ledgers.
