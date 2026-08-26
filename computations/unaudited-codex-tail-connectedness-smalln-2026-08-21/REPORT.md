# Tail connectedness and small-order deformation audit

Status: **UNAUDITED exact no-go**.  Connectedness cannot eliminate the full
`n=8` remote tail factor.  The audited diagonal obstruction reverses the
proposed argument: the zero-tail fibre is empty, so the full tail ideal is
already the unit ideal and every hypothetical exact source is remote.

## The decisive ring calculation

Let

```text
A8 = Q[all 252 source cells] /
     (F_w for mixed w, F_00000000-1, F_11111111-1, F_22222222-1)
J8 = (A_uv[a,b] : a != b), all 168 cross-colour cells.
```

Then `A8/J8` is exactly the normalized block-diagonal `n=8,d=3` fibre.
The audited `N8-DIAGONAL` theorem says that this fibre is empty over every
field.  Over `Q`, Nullstellensatz/base change therefore gives

```text
A8/J8 = 0, hence J8=A8.
```

Thus `J8=J8^2` holds in the full fibre for the unhelpful reason `J8=A8`.
In the idempotent-ideal notation, `e=1`; the zero-tail factor is zero and the
entire hypothetical fibre is the remote factor.  Connectedness is perfectly
compatible with this.  It cannot force `e=0` without a nonempty zero-tail
fibre, which is known not to exist.

The statement that connectedness makes the remote component “meet” the
zero-tail component is also literally inaccurate: an idempotent splitting
gives disjoint open-and-closed factors.  Connectedness forces one factor to
be empty.  At `n=8` it is the zero-tail factor that is already empty.

This conclusion concerns the **full 168-generator tail ideal**.  A selected
twelve-column tail ideal can still have a nonempty zero set, but connectedness
of that different quotient would not establish elimination of the other 156
tail cells.

## Exact `n=4` analogue

The standard `K4` one-factorization source has one colour on each of the
three perfect matchings.  The checker rebuilds all 81 output coordinates:
only `0000`, `1111`, and `2222` are nonzero, each with value one.

At this point the exact Jacobian of the 81 normalized equations in the 54
source cells has ranks

```text
all columns       51
cross-colour      36 of 36
diagonal          15 of 18
tangent dimension  3
```

The cross block is a monomial `36 x 36` matrix: exactly 36 output rows have
one nonzero cross derivative, and the other 45 have none.  The six live
diagonal cells, with one complementary-edge product equal to one for each
colour, form a closed `(G_m)^3`.  Its dimension equals the tangent dimension,
so it is a smooth irreducible component.  The same monomial normal minor is
nonzero everywhere on the torus.

Consequently any remote component at `n=4` cannot meet this zero-tail
component.  Proving the whole fibre connected would already amount to proving
that no other component exists; connectedness is not supplied by the source
grading or by the initial matrix.

## Exact `n=6` analogue

The frozen unrestricted theorem makes the normalized full `n=6,d=3` fibre
empty.  The checker also replays the diagonal Erhard Laurent family at
`x=2`.  Its only nonzero outputs are

```text
F_000000=F_111111=F_222222=1,
F_012021=1/64.
```

Symbolically the mixed residue is `x^-6`; GHZ is approached only as
`x -> infinity`, never at a finite parameter.  Hence the empty `n=6` fibre
provides no connected component from which to induct, while its exact border
family supplies the source-shaped escape-at-infinity control.

## Why grading and Rees deformation do not repair the argument

Before normalization, every matching coefficient is site-multihomogeneous.
The equations `F_(c^n)=1` destroy every positive version of that grading.
The pure-normalization-preserving torus still acts, but every pure
perfect-matching monomial has character zero; the degree-zero ring is much
larger than `Q`.  A torus fixes an idempotent, but “weight zero” does not mean
“scalar.”

Flat affine Rees degeneration also does not preserve component incidence.
The exact model

```text
Q[s,t]/(t-s*t^2) = Q[s] x Q[s,s^-1]
```

has a remote branch `t=1/s` absent from the special fibre.  The `n=6`
Laurent family is the matching-source analogue.  The hypothesis that would
exclude this behavior is a proper flat compactification that preserves the
three nonzero pure anchors.  The normalized source fibre is affine and those
anchors are open normalization data; known Laurent arcs explicitly escape at
infinity.

## Verdict

There is no connectedness/graded-deformation shortcut to the remote `n=8`
branch:

```text
n=4: zero-tail (G_m)^3 is already a smooth component;
n=6: the full exact fibre is empty, with a Laurent border at infinity;
n=8: the full zero-tail fibre is empty, so J8=A8 and e=1.
```

A useful continuation must attack the remote equations themselves (or prove
the whole ring `A8=0`); it cannot derive emptiness from connectedness with the
zero-tail fibre.

## Replay

```sh
python3 computations/unaudited-codex-tail-connectedness-smalln-2026-08-21/audit_tail_connectedness_smalln.py --write-results
python3 -O computations/unaudited-codex-tail-connectedness-smalln-2026-08-21/audit_tail_connectedness_smalln.py
python3 -I -S computations/unaudited-codex-tail-connectedness-smalln-2026-08-21/audit_tail_connectedness_smalln.py
```

All three modes pass with logical SHA-256
`e20b84ebd5674d7fb77e4d2b74d06c0a669202a6edef837a729563a60651be6d`.
