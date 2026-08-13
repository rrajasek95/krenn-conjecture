# Frame circuits lift by a common tail, or expose Tutte/collision debt

## Result

Let `C` be one of the protected-relative primitive circuits forced by the
minimum-support theorem.  Split its primitive vector into positive and
negative edge multisets `C+` and `C-`.  Every negative edge is protected.
There is an exact trichotomy.

1. **Squarefree with a common tail.**  If every physical site occurs at
   most once on each side and the unused physical sites have a supported
   decorated perfect matching `T`, then

   \[
                         C_+\sqcup T,\qquad C_-\sqcup T
   \]

   are two literal perfect-matching monomials in the same complete output
   word.  They retain the identical decorated complementary tail, so the
   circuit has the source type required by the matching-base/Fitting and
   Cartan identities.
2. **Squarefree without a common tail.**  The physical support graph on the
   unused sites has no perfect matching.  Tutte's theorem supplies a set
   `X` for which the number of odd components after deleting `X` exceeds
   `|X|`.  This is the exact matching-accessibility/Hall debt; it is not an
   unclassified circuit topology.
3. **Collision grade.**  Some physical site occurs in two colour ports, or
   the primitive odd-handcuff path has coefficient two.  The circuit
   monomial is not squarefree in physical sites.  It belongs to a repeated
   principal-parts/bar grade, the source type addressed by physical
   Cartan--Spencer comparison rather than by one ordinary matching row.

Thus the newly proved frame-circuit cover reduces its source lift to the two
already visible global interfaces: matching accessibility (Tutte/Hall) and
physical repeated-site comparison.  There is no fourth topological branch.

Checker:
[`verify_frame_circuit_matching_lift_trichotomy.py`](../computations/verify_frame_circuit_matching_lift_trichotomy.py).

## 1. Squarefree circuits give the same word

For every site-colour port `(v,i)`, circuit balance says

\[
             \deg_{C_+}(v,i)=\deg_{C_-}(v,i).          \tag{1}
\]

If the total physical degree is at most one, both sides are physical partial
matchings on the same site set `U`.  Equation (1) also says that they assign
the same colour to each site of `U`.  A decorated matching `T` on the
complement assigns colours to the remaining sites.  Hence `C+ union T` and
`C- union T` are distinct perfect matchings in one full endpoint-colour
coefficient and have exactly the same tail `T`.

This is a literal source-typing statement, not yet a cancellation theorem.
The complete coefficient may contain more than these two matchings.  Its
other terms are precisely the contamination debt handled by the global
signed-component/Fitting alternative.

The checker freezes the smallest example:

```text
C- = 01:00 | 23:11
C+ = 12:01 | 03:01
T  = 45:22
word = 001122.
```

Both completed monomials occur in the same word and differ only on the
typed `C4` core.

## 2. Failure of a tail is exactly a Tutte barrier

Ignore endpoint colours on the unused sites but retain only physical pairs
carrying at least one supported decorated cell.  Any perfect matching of
this graph can be decorated by its chosen cells and therefore supplies a
common tail; conversely every common decorated tail projects to such a
perfect matching.  Tail existence is exactly ordinary perfect-matching
existence.

Tutte's theorem therefore makes failure structural: there is `X` in the
unused vertex set with

\[
             o(G-X)>|X|.                                \tag{2}
\]

The audit uses the sharp triangle-plus-isolated-vertex complement, where
`X` is empty and there are two odd components.  In the endpoint-star
normalization, the smaller cross-intersecting shadows of (2) are exactly the
star, triangle, and `K2,2` Hall webs already isolated in the affine/Hall
theorem.  The present statement does not claim that every general Tutte
barrier has already been landed or that anchor-preserving reselection is
automatic.

## 3. Repeated physical sites are relative faces

Port squarefreeness and physical squarefreeness differ.  For example,

```text
C- = (0,0)-(1,0) | (0,1)-(2,1)
C+ = (1,0)-(0,1) | (2,1)-(0,0)
```

is a balanced port `C4`, but site zero occurs twice on both sides.  Its
physical site profile is `(2,1,1)`, so neither side is a matching monomial.
Likewise a loose odd handcuff uses its joining path with primitive
coefficient two.

These are not new mysterious support configurations.  They are exactly
the repeated-site degrees for which the complete principal-parts/Hasse
complex was introduced.  In the canonical repeated `P3+K2` grade, physical
endpoint-odd Cartan descent already constructs the required relative
comparison and its terminal alternative.  What remains is to extend that
physical comparison functorially to every protected-relative collision
circuit, not to enumerate more `C6/C8` supports.

## 4. Updated proof interface

Combining the circuit-cover and lift theorems gives the following source
exhaustivity map:

```text
occupied unprotected carrier
        |
        v
protected-relative even cycle / odd handcuff
        |
        +-- squarefree + common tail --> literal typed matching component
        |
        +-- squarefree - common tail --> Tutte/Hall accessibility barrier
        |
        `-- repeated site / doubled path --> Cartan-Spencer relative face
```

On the first branch, odd signed holonomy gives a unit and coherent even
holonomy is governed by the anchor and Cartan Schur amplitudes.  A dark
Cartan amplitude is an exact component potential.  The proof-completing
statements are now:

1. land every Tutte barrier by an anchor-preserving Hall exchange or a
   support dependence;
2. extend the canonical physical Cartan comparison to arbitrary collision
   circuits; and
3. turn an exact even potential into same-row deletion or an exchange which
   enlarges the typed component.

Transverse physical rank landing remains downstream.

## Scope

The trichotomy is exact for arbitrary palettes, endpoint asymmetry, and
parallel sources after aggregation.  It identifies the source type of a
frame circuit.  It does not say that a common-tail coefficient is binomial,
that its signed holonomy is nonzero, that every Tutte barrier is already
closed, or that the canonical Cartan construction has been proved in every
repeated multidegree.

Run:

```text
python3 computations/verify_frame_circuit_matching_lift_trichotomy.py
python3 -O computations/verify_frame_circuit_matching_lift_trichotomy.py
python3 -I -S computations/verify_frame_circuit_matching_lift_trichotomy.py
```

Frozen ledger SHA-256:

```text
243f96791994ea0104108f6425e8a19f08c58e7af6e4a026acd0049bc6c73e04
```
