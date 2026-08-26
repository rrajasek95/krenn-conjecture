# Doubled norm / Gram screen

## Outcome

The proposed doubled-norm inequality presently collapses to the output
coordinate identity

\[
 \|F(A)\|^2=|H_0|^2+|H_1|^2+|H_2|^2+P_{\rm mixed}
            =3+P_{\rm mixed}.
\]

Thus equality is exactly `X5`; this is Bessel/orthogonal-coordinate SOS, not
an inequality that uses moment balance or no-cap data.

Writing `T e_M=v_M` for the 105 perfect matchings and `G=T^*T`, the
multiplicity-free PM8 module has dimensions

```text
[8]  1,   [6,2] 20,   [4,4] 14,   [4,2,2] 56,   [2^4] 14.
```

But

\[
 \|F\|^2={\bf1}^*G{\bf1}=105\operatorname{tr}(P_{[8]}G),
\]

so the four nontrivial association-scheme energies do not enter the desired
norm.  PSD gives no coupling to the trivial block.  Producing such a coupling
would itself require a new source-relative identity.

## Exact controls

* The balanced rank-one-block `n=4` source is exact GHZ and has `P=0`.
* The balanced triangular-prism `n=6` source has `P=1`.
* The balanced form of the known `n=8` Laurent source has twelve unit cells,
  exactly two unit mixed outputs, and `P=2`.
* A second balanced `n=8` base-locus control has two disjoint complete `K4`
  blocks in colour 0.  The first has matching products `1, omega, omega^2`,
  the second `1,1,1`; hence the full nine matching terms cancel exactly.
  Every colour-0 port energy is three.  This rules out support/Tutte-only
  control of the base locus: phases are essential.
* Raw W40 has `P=3`; raw W25 has `P=70873613/2304`.  Neither stored point is
  moment-balanced.

Consequently the Laurent `P -> 0` degeneration is removed by balancing and is
not a counterexample to a positive balanced gap.  Conversely, the controls do
not prove such a gap.

## First exact base-locus jet test

For the balanced base direction consisting of the colour-0 graph
`C3(012) disjoint_union C5(34567)`, the literal first derivative has 252
source columns and exact rank 77.  Its image is:

* one pure colour-0 ray, receiving the fifteen `00` cross-edge cells; and
* 76 mixed rows.  Sixty (both endpoint colours nonzero) are singleton rows;
  ten have three columns and six have five columns when one endpoint is zero.

There is no pure colour-1 or colour-2 derivative.  Hence no nonzero first jet
is proportional to ternary GHZ.  More strongly, in a straight line
`F(B+tC)`, every coefficient below degree four contains colour-0 sites; if all
lower coefficients vanish and the leading coefficient is GHZ, it is the
degree-four term `F(C)`, so `C` is already an exact GHZ source.  This rules out
this base direction only as a non-circular straight-line escape.  Curved or
Puiseux jets remain the actual global boundary problem.

## Terminal scope

A bounded balanced sequence with `P -> 0` converges (after a subsequence) to
an exact moment-zero X5 source, so excluding bounded sublevels is the original
conjecture.  An unbounded sequence normalizes to a moment-zero base-locus
direction and requires a rank-stratified exceptional-fiber theorem.  Gram PSD
does not supply that theorem.

## Full-isotropy five-sector relaxation: terminal negative

For the two-switch graph on the 105 perfect matchings of eight sites, the five
primitive sectors and exact eigenvalue/multiplicity pairs are

```text
[8]: 12/1, [6,2]: 5/20, [4,4]: 2/14,
[4,2,2]: -1/56, [2^4]: -6/14.
```

The exact projector calculation in `audit_isotropic_scheme_relaxation.py`
produces fully port-isotropic source samples whose five sector-energy vectors
have affine rank five.  Hence full port isotropy forces no affine trace
identity among these energies.  This is not only a dimension count: putting
`I/sqrt(2)` on `C3 disjoint_union C5` is fully isotropic and has no perfect
matching, so its entire matching Gram matrix is zero.

After imposing only pure-output normalization, the invariant relaxation is

```text
e_lambda >= 0,             105 e_[8] >= 3.
```

It has the exact zero-mixed-energy witness
`e=(1/35,0,0,0,0)`, equivalently
`G=(1/35)P_[8]=J/3675`.  The exact `n=4` GHZ sector vector `(1,2)` and the
phased `n=6` fully isotropic block-injective local minimum both pass the same
relaxation.  Thus the five-sector SDP supplies neither a positive mixed norm
floor nor a cap equality condition; any useful Gram argument needs a new
source-relative constraint beyond isotropy and association-scheme PSD.
