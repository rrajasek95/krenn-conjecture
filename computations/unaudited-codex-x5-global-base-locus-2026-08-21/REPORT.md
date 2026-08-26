# Global base locus and border-versus-exact geometry at n=8

Status: **the extracted GHZ arc is an exact fourth-order exceptional jet, but
the exceptional fibre and the set of GHZ-reaching boundary types are already
too large for a finite/universal boundary classification**.

## 1. Literal n=8 Laurent packet

Expanding vertex zero of the audited six-site prism gives sites `1,...,8`
and the twelve one-hot cells

| colour | edge valuations |
|---|---|
| 0 | `12:-1`, `36:+1`, `45:0`, `78:0` |
| 1 | `14:0`, `27:0`, `35:0`, `68:0` |
| 2 | `18:0`, `25:0`, `34:0`, `67:0` |

The five supported perfect matchings give

```text
00000000 : 0
11111111 : 0
22222222 : 0
12012000 : 1
21000012 : 1
```

and every other amplitude is identically zero on the arc.  Thus

```text
H(A(t)) = GHZ + t(e_12012000+e_21000012).
```

The minimum source valuation is `-1`.  The minimal projective rescaling is

```text
B(t)=t A(t)=B0+t B1+t^2 B2,
B0=x_12^00,
B2=x_36^00,
```

with the ten valuation-zero cells in `B1`.  Since `H` is homogeneous of
degree four,

```text
H(B(t))=t^4 GHZ+t^5(e_12012000+e_21000012).        (1)
```

The exact first-jet census over all 6,561 output coordinates is:

| first nonzero order | coordinates |
|---:|---:|
| 4 | 3 pure words |
| 5 | 2 mixed words |
| identically zero | 6,556 |

## 2. The base point and its normal cone

The projective limit is the diagonal one-cell point `[x_12^00]`.  It is in
the base locus because one physical edge cannot contain a four-edge perfect
matching.

This is a highly singular base point.  Every amplitude vanishes locally to
order at least three, so the Jacobian and Hessian of the base ideal both
vanish and the projective Zariski tangent space has the full dimension 251.
The first meaningful normal-cone map is cubic:

```text
C3(B)=x_12^00 tensor H_6(B|{3,4,5,6,7,8}).          (2)
```

It occupies the 729 output coordinates with endpoint-1,2 colours `00` and
has `729*15=10,935` literal cubic matching monomials.  The other 5,832
coordinates begin in local degree four.

For the extracted `B1`, the residual physical support is the disjoint union
of triangles `345` and `678`, so it has no perfect matching.  Hence
`C3(B1)=0`; the arc lies in the cubic exceptional base and equation (1) is
its first nonzero, quartic normal direction.

## 3. Exceptional-fibre obstruction

The exceptional fibre over this one-cell point is already large in two
independent ways.

First, take arbitrary 3-by-3 first-order tensors on one residual perfect
matching, for example `34,56,78`.  Equation (2) contains

```text
x_12^00 tensor A_34 tensor A_56 tensor A_78,
```

so the cubic exceptional fibre contains

```text
Segre(P^8 x P^8 x P^8), dimension 24.
```

The GHZ-stabilizer identity component has dimension 21, so this family alone
has orbit-moduli dimension at least three.

Second, stay on the deeper cubic-kernel support of the extracted arc.  Its
three quartic pure coefficients are the three disjoint matching monomials

```text
alpha = x_12^00*x_36^00*x_45^00*x_78^00,
beta  = x_14^11*x_27^11*x_35^11*x_68^11,
gamma = x_18^22*x_25^22*x_34^22*x_67^22.
```

Varying one cell in each product realizes a dense open of

```text
[alpha e_00000000 + beta e_11111111 + gamma e_22222222] in P^2.
```

GHZ is only `[1:1:1]`.  The normalization torus fixes the three pure output
coordinates, and common `S3` merely permutes them, so `P^2/S3` remains
two-dimensional.  Symmetry therefore does not make the exceptional fibre
finite.

## 4. The one-cell boundary type is not universal

There is a still cheaper counterexample to a universal boundary-type lemma.
Keep the same one-hot graph and put valuation `-1` on respectively

```text
{12},
{12,45},
{12,45,78},
```

put valuation `1,2,3` respectively on `36`, and put zero on all remaining
cells.  Each colour product is normalized.  The three pure output orders are
zero and both mixed orders are positive in every case.  After the same
minimal projective rescaling, all three arcs have first output `t^4 GHZ`,
but their projective limits have support cardinalities one, two, and three.

Support cardinality is preserved by the GHZ port torus and site/colour
permutations, so these are three inequivalent base-locus strata reached by
literal GHZ arcs.  Thus even within this single properly coloured support,
not every GHZ-reaching arc has the extracted one-cell boundary type.

The global base locus is much larger: isolating one physical site leaves all
`C(7,2)*9=189` other cells arbitrary, giving eight linear `P^188` base
subspaces.  Their dimension exceeds the target-preserving torus dimension by
167.  Finite combinatorial support types cannot yield finitely many algebraic
orbit types.

## 5. Relation to the source-cycle invariant

For either mixed matching `M`, the existing degree-twelve source invariant

```text
I_M = H_m Q_M
```

has affine value one along the Laurent orbit and zero on every finite exact
GHZ source.  On the projectively rescaled arc,

```text
ord H_m(B)=5,
ord Q_M(B)=7,
ord I_M(B)=12,
ord P_G(B)=12,
I_M/P_G=1.                                               (3)
```

Thus the cycle separator is precisely a Rees coordinate retaining the
zero-times-infinity datum erased by the top amplitude map.  This is the
positive outcome of the audit: a source-relative blow-up can distinguish
the known boundary orbit from a finite exact source.

Its limitation is also exact.  Ratio (3) equals one on all three alternative
one-hot arcs.  It does not classify their base strata and cannot show that
an arbitrary GHZ-reaching arc is one-hot.  A border-to-exact proof would
need a separate theorem forcing every relevant arc into a source-cycle
chart; the exceptional geometry of `H` alone cannot do this.

## Ranked verdict

1. **Negative:** no finite/universal GHZ boundary-type lemma follows from
   symmetry or from the blow-up of the top amplitude map.
2. **Positive local interface:** the known arc is a fourth-order point of the
   cubic normal cone, and the degree-twelve cycle ratios record it exactly.
3. **Remaining theory target:** prove a source-relative one-hot/cycle
   accessibility theorem, or abandon global border classification in favour
   of direct exact source equations.

## Replay

```sh
python3 computations/unaudited-codex-x5-global-base-locus-2026-08-21/audit_x5_global_base_locus.py --write-results
python3 -O computations/unaudited-codex-x5-global-base-locus-2026-08-21/audit_x5_global_base_locus.py
python3 -I -S computations/unaudited-codex-x5-global-base-locus-2026-08-21/audit_x5_global_base_locus.py
```

All modes return logical SHA-256
`f78123a1763b9632b1a00b10f29acae7663a61d5b18f356e835e9be5ff5b9296`.

