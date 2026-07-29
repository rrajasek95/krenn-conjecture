# All compatible three-cell families miss the pair-cap locus

## 1. The exact theorem

In the eight-site ternary square-zero algebra, put

\[
\begin{aligned}
q={}&23_{00}+45_{00}+67_{00}+01_{11}+36_{11}+57_{11}\\
   &+02_{22}+14_{22}+56_{22},\\
z={}&01_{00}+24_{11}+37_{22}.
\end{aligned}
\]

Choose three distinct cells \(e<f<g\) outside the displayed support of
\(q\), take \(t,u,v\in\mathbb C^\times\), and set

\[
                         Q=q+te+uf+vg.                   \tag{1}
\]

There are exactly 87,027 triples for which

\[
                         zQ^{[3]}=\Delta_{8,3}           \tag{2}
\]

holds identically in \(t,u,v\).  None of them has a pair-cap preimage:
for every such triple and every nonzero parameter choice,

\[
              (aQ+4ps)Q^{[3]}\ne\Delta_{8,3}            \tag{3}
\]

for all \(a\in\mathbb C\) and all site-linear forms \(p,s\).

Combined with the separately audited
[three-cell cancellation theorem](polarized-eight-site-fixed-q-three-extra-cancellation-frontier.md),
this excludes every fixed-\((q,z)\) family obtained by adding exactly three
distinct outside-support cells with nonzero coefficients while retaining
(2).  This is still a fixed sparse seed theorem.  It does not allow four or
more added cells, vary \(z\), or treat an arbitrary quadratic, and it does
not prove Krenn's conjecture.

The primary exact ideal checker is
[`verify_polarized_eight_site_fixed_q_compatible_three_extra_survivor_ideals.py`](../computations/verify_polarized_eight_site_fixed_q_compatible_three_extra_survivor_ideals.py).
The clean-room reconstruction is
[`verify_polarized_eight_site_fixed_q_compatible_three_extra_independent.py`](../computations/verify_polarized_eight_site_fixed_q_compatible_three_extra_independent.py),
documented in the
[independent audit](polarized-eight-site-fixed-q-compatible-three-extra-projective-frontier-independent-audit.md).

## 2. Compatible triples and projective closure

Among the 243 cells outside \(\operatorname{supp}(q)\), exactly 99 have
zero individual debt \(zeq^{[2]}\).  Exactly 3,960 pairs of those cells
also have zero cross debt \(zefq\).  The triangles of this compatibility
graph whose triple debt \(zefg\) vanishes are precisely the 87,027 triples
in (2).  Their physical-pair census is

| distinct physical pairs | compatible triples |
|---:|---:|
| 1 | 924 |
| 2 | 28,512 |
| 3 | 57,591 |

For every triple, expand the pair-cap equation as

\[
                  4psQ^{[3]}+4aQ^{[4]}=\Delta_{8,3}.    \tag{4}
\]

Parameter-safe projective Gram parity closes 86,284 cases.  The exact
ledger is

| physical pairs | projectively closed | open branch | pure direct term |
|---:|---:|---:|---:|
| 1 | 923 | 1 | 0 |
| 2 | 28,283 | 165 | 64 |
| 3 | 57,078 | 320 | 193 |

Thus 743 triples survive projective closure.  The sole one-pair survivor is

\[
                    (17_{00},17_{02},17_{22}).          \tag{5}
\]

It is a literal specialization of the independently audited arbitrary
full-block theorem on pair 17, which allows all nine complex entries of that
block, including zero entries.  Hence (5) is already excluded.  Exactly 742
multi-pair triples remain for full ideals.

## 3. The 742 saturated ideals

For each residual triple, both checkers write every nonzero coordinate of
(4) over \(\mathbb Q\) and localize the parameter torus by adjoining

\[
                         h t u v-1=0.                   \tag{6}
\]

There are 53 variables: 48 coordinates of \(p,s\), the scalar \(a\), the
three parameters, and the localization variable.  Depending on the triple,
there are between 223 and 343 nonzero equations, including (6).

The primary batch uses ascending words and its original variable order.
The independent batch reverses word, term, site, colour, mode, and parameter
orders, places the torus generator first, and regenerates the divided powers
without importing either primary three-cell checker.  Singular over
\(\mathbb Q\) reduces every one of the 742 ideals to the one-element basis
\([1]\) in both batches.  Scalar extension and the localization equation
therefore prove the exact complex-torus exclusion (3), with no genericity or
positivity assumption.

## 4. Frozen ledgers and reproduction

The exact SHA-256 ledgers are

| ledger | SHA-256 |
|---|---|
| compatible triples | `47d231f82e3e6bd272e0b440667a06fc6fe110716a916512555330d644e08a22` |
| canonical 743 projective survivors | `b481e4abddc0e98e8cbde9486d7d384a821430b15964dde6e9b279367988a57a` |
| independent projective closures | `c3d4eb15e6ad9f53eee400197be8d1e5e68ab7a8b274c5377712935689f6d58a` |
| exact 742 multi-pair list | `025cb3d4d283ef8bab747ccf587eb97bd8741f0bc5bc642b3524b74dc44cbb0b` |
| independent ideal programs | `ddb50c85a030b693c98d5161a7fcc67ee26f269aaadb07b2013ad0d52d2aab9e` |
| primary 742 unit results | `7ea7959152651bf9564d5d21222afdc93c6158ea116d13e85341d63c3ddeed77` |
| independent 742 unit results | `2e9ecab9ee8a62e41d6e7683bab9731138a137ca9e2662a6ff843a9f901e4e84` |

Run the primary replay with

```text
uv run python computations/verify_polarized_eight_site_fixed_q_compatible_three_extra_survivor_ideals.py --workers 8
```

and the independent replay with

```text
uv run python computations/verify_polarized_eight_site_fixed_q_compatible_three_extra_independent.py --all-ideals --workers 8
```

The audited full runs ended with \(742/742\) unit ideals.  The primary and
independent result hashes intentionally differ because their polynomial-ring
and generator orderings differ.

## 5. Combined exactly-three-cell consequence

The exhaustive classification of all
\(\binom{243}{3}=2{,}362{,}041\) outside-support triples is now logically
complete at this fixed \((q,z)\):

| class | count | exact conclusion |
|---|---:|---|
| singleton Laurent debt | 2,274,826 | cannot satisfy (2) on \((\mathbb C^\times)^3\) |
| exceptional triple | 1 | its three equations are torus-inconsistent |
| binomial cancellation | 187 | satisfies (2) on a binomial locus; independently excluded from pair-cap |
| identically compatible | 87,027 | satisfies (2) identically; excluded here from pair-cap |

Thus every exactly-three-cell route at the displayed seed either fails the
polarized target identity or misses the pair-cap variety.  The next sparse
frontier must add at least four cells, vary \(z\), or leave this fixed seed.
