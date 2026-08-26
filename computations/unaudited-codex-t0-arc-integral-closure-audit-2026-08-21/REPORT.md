# Projective T0 arcs, integral closure, and Rees-divisor audit

## Outcome

Status: **UNAUDITED exact structural PASS / terminal no-go**.  The stabilizer
torus does expose a unique source cell, but the resulting one-cell arc is only
a projectivized symmetry orbit: every matching term of a fixed word has the
same order.  Arc/integral-closure theory does not reduce the proof to the
known finite arc list, and neither the one-cell local ideal nor the remote
tail ideal gives a smaller source-faithful blowup controlling cap failure.

## Exact T0 calculation

The pure-normalization-preserving character lattice is

```text
Z^24 / <p_0,p_1,p_2>,   p_c=sum_i e_(i,c),   rank 21.
```

All 252 literal cell characters remain distinct.  A generic cocharacter
therefore exposes a unique live cell.  Every normalized pure matching has
four weights summing to zero, so the global minimum is strictly negative.
For a hypothetical exact source `A`, projective rescaling gives

```text
B(t)=t^(-m) lambda(t)A,       H(B(t))=t^(-4m) GHZ.
```

This is correct but tautological.  Semi-invariance makes every term of
`F_w` have order `chi_w-4m`, independent of its matching, so the mixed
initial equation is exactly the original cancellation `F_w(A)=0`.

The frozen one-/two-/three-minimal-cell variants and the earlier infinite
two-edge redistribution are literal T0 shifts.  They collapse in the torus
quotient.  A different family, obtained by adding valuations

```text
v(A_23[00])=N,  v(A_02[00])=N,  v(A_13[00])=3N,   N>=2,
```

has invariant `|v01+v23-v02-v13|=3N+1`.  This is unchanged by endpoint
potentials, projective shift, and only permuted/signed by the finite symmetry.
Thus contact arcs have infinitely many symmetry-quotient types.  This does
**not** mean there are infinitely many Rees divisors.

## Contact arcs are not Rees divisors

In the one-cell chart `A_01[00]=1`, each displayed `N`-arc has only 14
nonzero local coordinates.  Its order semivaluation has a kernel containing
237 coordinate functions.  A divisorial valuation of the ambient function
field has zero kernel, so these curves are not themselves ambient divisorial
valuations and cannot be assigned canonically to exceptional divisors without
computing the normalized blowup.  Their contact order with the all-amplitude
base ideal is four.

Noetherianity still says that a fixed ideal has finitely many Rees divisors.
It supplies neither their equations nor a proof that they are represented by
the frozen arcs.

## One-cell local complexity

The dehomogenized local ring has 251 variables and the base ideal has 6,561
generators.  The exact leading profile is

```text
729 rows:  H_6 + quartic correction,
            10,935 cubic matching monomials in 135 residual variables;
5,832 rows: quartic-leading,
total quartic matching monomials: 677,970.
```

The known GHZ arc kills every cubic `H_6` row and first appears in the
quartic normal direction.  Therefore the 729-row cubic initial ideal cannot
replace the full Rees algebra.  Normalizing the complete
6,561-generator Rees algebra in 251 variables, with a chosen carrier
rank/pivot branch, is the honest remaining computation; no small local ideal
was found.

## Remote-tail ideal

In the smooth ambient source chart, the 168 cross-colour variables generate
the coordinate ideal of an irreducible codimension-168 linear subspace; its
ordinary blowup has one exceptional divisor.  On the normalized exact X5
ring `A8`, however, the frozen diagonal theorem gives

```text
A8/J8=0, hence J8=A8.
```

The corresponding blowup is the identity and has no Rees divisor.  A selected
12-column tail ideal may be nontrivial, but it omits 156 literal tail variables
and is not a source-faithful substitute.  Moreover no-cap is a locally closed
union of 728 carrier rank/pivot and blocker-membership branches, not the zero
set of one canonical small invariant ideal.

## Terminal verdict

Arc theory gives a finite divisorial test only after the relevant normalized
blowup is known.  Here the one-cell truncation loses the GHZ direction and the
remote-tail blowup becomes trivial on the exact source ring.  There is no
finite computable source-relative blowup smaller than global base/cap
normalization currently justified.  A new route must either normalize that
full branchwise Rees data or first derive a source polynomial that canonically
encodes cap failure.

## Replay

```sh
python3 computations/unaudited-codex-t0-arc-integral-closure-audit-2026-08-21/audit_t0_arc_integral_closure.py --write-results
python3 -O computations/unaudited-codex-t0-arc-integral-closure-audit-2026-08-21/audit_t0_arc_integral_closure.py
python3 -I -S computations/unaudited-codex-t0-arc-integral-closure-audit-2026-08-21/audit_t0_arc_integral_closure.py
```

All modes return logical SHA-256
`8913f13990ebe5e8549033589667ce9d424362b7264239bc8556ea13b089b14f`.
