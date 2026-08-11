# A repeated-site dark-plane overlap coefficient has an exact degree-two source identity

This is an exact positive source-membership result for one coefficient of the
first overlap cap.  It supersedes the lower-degree obstruction for that
coefficient in
[`n8-rank11-scalar-dark-plane-overlap-constant-span-guard.md`](n8-rank11-scalar-dark-plane-overlap-constant-span-guard.md),
but it does not prove the full cap clean, active, or source-forced.

## 1. The coefficient

Retain the arbitrary 135-cell internal six-site quadratic and the fixed
endpoint stars/direct block of the dark-plane guard.  For the overlap cap

\[
                     (uv,K)=(17,E_{02}+I),
\]

take residual word \((0,0,0,1,2,2)\), in residual-site order
\((0,2,3,4,5,6)\).  Its clean-error coefficient is

\[
24\bigl(
  2q_{01}(0,1)q_{13}(1,0)
 +q_{01}(0,1)q_{13}(2,0)
 +q_{01}(0,2)q_{13}(1,0)
\bigr).                                                     \tag{1}
\]

Every monomial in (1) reuses physical site 1.  The previous guard proved
that no source identity with multiplier q-degree at most one can produce
this coefficient, because every quadratic source-row monomial is supported
on two disjoint edges and there is no linear source part.

## 2. Exact degree-two identity

The new checker reconstructs all 4,737 nonzero coefficient rows of the nine
original full-pair equations, preserving their endpoint labels.  It verifies
an equality over \(\mathbb Q\)

\[
       (1)=\sum_{r=1}^{448} c_r m_r(q)F_r(q),                \tag{2}
\]

where every \(F_r\) is one of those original labelled source rows,
\(\deg m_r\le2\), and every \(c_r\) is an integer with
\(|c_r|\le168\).  The multiplier-degree census is

\[
                 11\text{ of degree }0,qquad
                  6\text{ of degree }1,qquad
                431\text{ of degree }2.
\]

All nine endpoint-label pairs occur.  The identity is checked by exact
`Fraction` expansion to the three target monomials with zero remainder; the
committed verifier does not depend on a modular rank inference.

## 3. How the certificate was found

The complete target-driven degree-at-most-two Macaulay component has 856,163
monomials, 410,339 source-labelled columns, and 5,841,159 nonzero incidences.
Its degree-five page consists of 57,282 proportional triples, one for each
of three direct-row labels.  Replacing those triples by labelled differences
leaves a degree-four transfer with eleven incidence components.  At both
audit primes 1,000,003 and 1,000,033, the degree-four rank is 81,319 and only
786 new lower classes survive above a 1,657-dimensional raw lower basis.
The target reduces to zero.  Rational reconstruction of the target's small
376-node provenance sub-DAG, followed by expansion back to original source
columns, gives (2).

These page ranks document the discovery and reproducibility path.  The
mathematical claim used by the proof frontier is only the exact identity
(2), which the compact checker verifies independently of those ranks.

## 4. Proof impact and next gate

For this repeated-site coefficient the lower-degree obstruction is sharp:
degree zero and one are impossible, while degree two succeeds.  Thus the
coefficient is not a surviving obstruction to the dark-plane pair exchange.
It is also not enough to promote the rational overlap guard.  The first cap
has 339 coefficients, the second has 489, and (2) treats one coefficient of
the first cap only.

The highest-value next calculation is therefore simultaneous rather than
deeper: transport (2) under the physical/color symmetries, then decide
whether the resulting labelled degree-two identities close the whole
339-coordinate cap error (and subsequently the 489-coordinate cap), or
leave a common quotient class.  A common survivor would identify the exact
two-chart attaching obstruction; complete closure would supply a concrete
source-level candidate for the missing dark-plane activity-conversion map.

## 5. Audit

[`verify_n8_rank11_scalar_dark_plane_overlap_degree2_identity.py`](../computations/verify_n8_rank11_scalar_dark_plane_overlap_degree2_identity.py)
reconstructs the source rows and target from the base checker, verifies row
ordering, expands all 448 labelled terms with exact rational arithmetic, and
checks the degree census, coefficient bound, label usage, and ledger

```text
8743832e58871c07427cb3af6f1114fdf05c0172ae7c5c92f8ba7f8f64237fcc
```

It passes Python 3.13 and 3.14 in normal and optimized mode.
