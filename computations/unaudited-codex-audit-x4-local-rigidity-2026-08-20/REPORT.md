# Independent referee report: W40 X4 local rigidity

Status: **PASS over characteristic zero, with the producer's local scope
retained.**  The exact rank, gauge-tangent, local-germ, and active-cap
invariance claims all survive an independent reconstruction.  This proves a
local theorem at W40, not the universal `X4 => active clean cap` statement.

## Audited theorem

Let `X4` be the affine scheme in the 252 endpoint-ordered ternary source
coordinates cut out by the three pure target equations and the 4,878 mixed
amplitude equations of off-count at most four.  Let `A` be the integral W40
point with the 20 nonzero cells listed in `independent_audit.py`.

Over any characteristic-zero field:

1. `A` is a smooth point of `X4` of local dimension 12.
2. The scheme-theoretic Zariski germ of `X4` at `A` equals the germ of the
   target-preserving diagonal-gauge orbit through `A`.
3. Consequently, over `C` there is a Zariski, hence analytic, neighborhood
   of `A` in `X4` in which pair `67` retains an active clean cap.

Equivalently, an all-blocked `X4` counterexample cannot be obtained by a
sufficiently local deformation of W40.  This does not exclude a remote
point, another component, or a singular locus.

## Independent exact computation

The audit imports no producer code.  It hard-codes the 20 nonzero
endpoint-ordered W40 cells, verifies the resulting 252-cell source against
the pinned historical file with SHA-256
`30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f`,
and reconstructs every raw equation.

Two distinct derivative engines agree on all 4,881 X4 rows:

- direct term-by-term differentiation of all 105 perfect-matching
  monomials; and
- six-site hafnian cofactors from a subset recurrence.

The resulting `4881 x 252` Jacobian has 845 nonzero entries.  A canonical
`240 x 240` minor has determinant

```text
8589934592 = 2^33.
```

The normalized target-preserving gauge tangent is a `252 x 21` matrix.  It
has rank 12 (minor determinant `-1`), and exact multiplication gives
`Jacobian * gauge_tangent = 0`.  Thus the determinant supplies
`rank(J) >= 240`, while the 12-dimensional kernel supplies
`rank(J) <= 240`; the rank over `Q` is exactly 240 and the tangent dimension
is exactly 12.  This avoids treating a modular rank as an upper bound.

The fixed-nonzero-cell transversal was also replayed: restricting the
Jacobian to all 232 zero-cell coordinates has rank 232, with minor
determinant `-2^33`.

The source itself passes all X4 equations and has exactly the three expected
off-count-five defects:

```text
01110222 = 1
12221000 = 1
20002111 = -1
```

## Why tangent equality implies germ equality here

Tangent equality by itself would not justify the producer's conclusion.
The missing ingredient is the actual torus orbit contained in `X4`.

The target-preserving diagonal torus has parameters `lambda_(u,c)` subject
to `product_u lambda_(u,c)=1` for each color.  Mixed amplitudes remain zero
under its action, while the three pure amplitudes remain one, so its orbit is
contained in `X4`.  In characteristic zero its differential at W40 has rank
12, hence the orbit has dimension 12.

The `2^33` Jacobian minor makes the Zariski tangent dimension at most 12;
the contained orbit makes the local dimension at least 12.  Therefore local
dimension and tangent dimension coincide, so W40 is smooth and its regular
local ring has a unique local component.  The orbit closure is irreducible,
passes through W40, and has the same dimension 12.  Its local defining prime
there has height zero, hence is zero.  Finally, an algebraic-group orbit is
open in its closure.  This yields equality of the scheme germs, not merely
equality of their tangent spaces.

## Active-cap covariance

For a cap on `p,q`, transport its matrix contragrediently:

```text
K'_(i,j) = K_(i,j) / (lambda_(p,i) lambda_(q,j)).
```

Then the cap scalar is unchanged, each response cell on residual sites
`a,b` is multiplied by `lambda_(a,alpha) lambda_(b,beta)`, and each clean
error coefficient is multiplied by the corresponding nonzero product over
the six residual sites.  Diagonal nonvanishing of `K` is also preserved.
Thus active-clean-cap existence is invariant on the gauge orbit.

The executable audit checks this covariance with a nontrivial rational
product-one gauge.  For pair `67`, it evaluates all 729 clean-error
coefficients before and after scaling; all vanish.  The original activity
product is `1` and the scaled activity product is `-90`, both nonzero.

## Controls and field scope

All 13 declared controls ran.  In particular:

- changing `A_(2,6)[2,2]` from `-1` to `+1` creates four raw X4 failures;
- freezing the site-7 gauge parameters instead of enforcing the product-one
  constraints produces three nonzero rows in `Jacobian * tangent`;
- direct and cofactor Jacobians agree exactly; and
- the pair-67 cap and its covariance are evaluated from the raw source.

The script passed in all three requested modes:

```text
python3 independent_audit.py
python3 -O independent_audit.py
python3 -I -S independent_audit.py
```

The displayed rank minors remain nonzero in every odd characteristic.
This report limits the local-germ theorem to characteristic zero; it makes
no claim in characteristic two.

Machine-readable details are in `results.json`.
