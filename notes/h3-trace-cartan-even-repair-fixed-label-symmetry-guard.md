# Canonical covariance does not exchange the two fixed repair labels

## Result

The even repair needs

\[
                 d_{\rm even}={d_{B_1}+d_{B_4}\over2}.
\]

Constructing one fixed Gate-I residue section and applying the known physical
symmetries does **not** supply the other.  The exhaustive automorphism census
of the canonical faces-`(3,5)` fine grade has four physical site/colour
automorphisms, but their image on the six pure labels is only

\[
                    (B_0\ B_5)(B_2\ B_3),                 \tag{1}
\]

with `B1` and `B4` fixed separately.  Its label orbits are

```text
{B0,B5}, {B1}, {B2,B3}, {B4}.
```

Thus a `B1` seed has orbit `{B1}` and a `B4` seed has orbit `{B4}`.  This
also excludes a path that leaves the canonical presentation through physical
site/colour symmetries and later returns: the composite is an automorphism of
the canonical fine grade and hence belongs to the already exhausted
stabilizer.

Checker:
[`verify_h3_trace_cartan_even_repair_fixed_label_symmetry_guard.py`](../computations/verify_h3_trace_cartan_even_repair_fixed_label_symmetry_guard.py).

## The two fixed outputs have different source-orbit presentations

The shared-loop C4 census makes the distinction sharper.  In every one of
the four support collapses, the two allowed fixed target choices are

```text
B4: a rho-fixed source matching, matching 7 or 14;
B1: the rho-average of the nonfixed pair matching 1, matching 9.
```

The target involution fixes both outputs, but it does not turn a fixed source
matching into the average of a two-cycle.  The existing frame-circuit result
types these as same-word C4 occurrence pairs; it explicitly does not promote
either pair to the protected relative binomial boundary.  Hence no current
source theorem makes the two presentations interchangeable.

There is a parallel linear guard.  The existing scalar diagonal residue and
physical Cartan line, together with either `d_B1` alone or `d_B4` alone, do
not span `(B1+B4)/2`.  Adjoining both fixed units does.  So neither the
aggregate scalar nor the Cartan correction recovers the missing second unit.

## What kind of uniform theorem would suffice?

The quantifier is decisive:

- “there exists one fixed repair section, in `B1` or `B4`” does not close the
  even repair;
- “a section constructed at one fixed seed is natural under the canonical
  symmetry” does not close it, because both seeds are singleton orbits;
- “for **every** allowed fixed C4 target, the same source construction gives
  a protected labelled-residue section” does close it, by applying the
  theorem at `B1` and `B4` and averaging;
- a direct theorem constructing only `d_even` also suffices for the even
  lane, although it is weaker than separate componentwise sections.

Thus the minimal next object is either the second independent fixed section
or the equal rho-even sum itself.  This is stronger than Gate I's current
existential fixed choice, which needs only one fixed direction plus one
paired direction.

## Denominator control

The evaluated face projection orders the two routes as

```text
face 3 -> B4,     face 5 -> B1.
```

The exact direct-free denominator packet has both projected memberships.
The tilted packet has only the first: it sees `B4` and misses `B1`.  These
facts are not physical labelled-residue constructions—the placement and
protected correction are still open—but they are a useful adversarial
control.  In particular, the tilted packet disproves any inference that one
visible fixed route forces the other.

## Frontier

No committed physical symmetry, Cartan covariance theorem, or Gate-I source
theorem currently supplies both fixed sections.  A successful uniformization
must be componentwise in the chosen target label, not merely equivariant
under the canonical involution.  The alternative is to build `d_even`
directly in the two exact denominator grades identified in `73ee225`.

## Verification

Run:

```text
python3 computations/verify_h3_trace_cartan_even_repair_fixed_label_symmetry_guard.py
python3 -O computations/verify_h3_trace_cartan_even_repair_fixed_label_symmetry_guard.py
python3 -I -S computations/verify_h3_trace_cartan_even_repair_fixed_label_symmetry_guard.py
```

The frozen ledger digest is
`a831df876b698e2602bd7ff4171005130ab990ec5626016789fa4ed19fa4e856`.
