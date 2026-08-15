# Normalization permits the B top map, but does not yet produce a physical cap

## The precise solutionwise statement

Write `t=H0-u`.  The response and cap fragments are

```text
N -> Y,                 dN=Y,
B -> Y + t E.           dB=Y+tE
```

After restricting to an exact normalized source, `t=0`, the evident map
`N -> B`, `Y -> Y` is a literal chain map.  Therefore an absolute Eq
preimage is **not logically necessary for the bare constructive coefficient
map**.  Projecting the selected tied top to its `B` coordinate is legitimate
on this fibre.

But the frequently suggested reason is backwards.  The class `[E]` is
`t`-torsion because `t[E]=0`; it does not vanish on the fibre `t=0`.
Indeed

```text
H(cone(N -> B)) = (H0,H1,H2) = (1,0,0),
surviving class = E=e_Eq.
```

Algebraically, `R/(t) tensor_R R/(t)=R/(t)`, not zero.  Thus what vanishes
solutionwise is the **defect** `tE`, while the protected `E` class remains.
The `B` projection is a quotient, not an equality between the tied lift and
a `B`-only lift.

The exact checker is
[`verify_h3_normalized_solutionwise_marked_cap_constructive_factor_gate.py`](../computations/verify_h3_normalized_solutionwise_marked_cap_constructive_factor_gate.py).

## What the divided-root construction now supplies

The marked construction has closed the following earlier local defects:

- the derived response-to-cap operation/word section;
- both `q23/q45` P2 restrictions;
- the pointed occurrence section; and
- the first `q/dq` product-rule faces, including detector `35/72`.

Consequently the surviving complete Eq class should no longer be described
as an obstruction to the bare selected coefficient map.  It belongs to the
universal/terminal comparison unless a downstream constructive operation
actually queries it.

## First obstruction independent of t

The current marked object still records a parent matching, collision mark,
and augmented target; it does not construct a realization

\[
 \operatorname{ev}_{\rm cap,A}:
 N\otimes_R R/(t)\longrightarrow \operatorname{Cap}_{\rm phys}(A;p,q)
\]

as an actual cap covector `K`.  In the finite type guard

```text
coordinates             parent coefficient, target, actual K
marked object            (1,1,0)
required physical cap    (1,1,1),
```

the last-coordinate covector kills the marked object and reads one on the
required cap.  This discrepancy is present after `t` has already been set
to zero.

That missing realization is exactly what the next constructive theorems
consume:

1. the private-site identity uses the physical source multiplication,
   cells `p_u,q_u,p_s,q_s`, and cofactors `C_s`, giving
   `sum_s Delta_us*C_s=-q_u`;
2. clean descent contracts the actual tensor by `K` and requires
   `s*kappa_0*kappa_1*kappa_2 != 0` (plus the clean error equation).

Neither operation is defined on a parent-labelled homology class alone.
Target `1` in the derived augmentation does not by itself give the actual
`K`, its contractions, or the displayed nonvanishing product.

## Constructive versus terminal fork

A constructive bypass remains possible and is strictly weaker than an
absolute Eq filler.  It would suffice to construct `ev_cap,A` on actual
solutions so that it:

- is pointed and `R/(t)`-linear for the physical source algebra;
- sends the selected marked class to an actual cap covector `K`;
- reflects target/nonvanishing; and
- commutes with private-site multiplication, cofactor contraction, and
  clean-cap reconstruction.

If this is proved, the extra Eq cokernel can be ignored by the constructive
branch.  No current theorem supplies this factorization, so active cap,
private-site fan, and `N -> N-2` descent do not yet follow.

Fredholm promotion remains different: a universal presentation-safe
comparison must either contract `E` absolutely or prove an exhaustive
physical terminal on which its covector extends.  The solutionwise top map
alone proves neither.

## Verification

```text
python3 computations/verify_h3_normalized_solutionwise_marked_cap_constructive_factor_gate.py --mode structural
python3 -O computations/verify_h3_normalized_solutionwise_marked_cap_constructive_factor_gate.py --mode full
python3 -I -S computations/verify_h3_normalized_solutionwise_marked_cap_constructive_factor_gate.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
5cc82789e11d4ff6c86a2787ce62a3cb6cc5d08c1d39c8b4bc48d40c9b69f496
```
