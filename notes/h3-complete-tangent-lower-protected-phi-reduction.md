# The complete lower face reduces to one fifteen-label physical comparison

## Result

The determinant-dark filtered lift of `4be703c` has a universal
Cartan--Spencer nullhomotopy, but its physical descent is not a statement
about the eight-coordinate occurrence shadow `-v`.  The complete lower
Hasse face retains direction and collision labels.

For the explicit marked profile

\[
                     v=P_{024}-P_{012},                \tag{1}
\]

the complete difference of physical tangent-Hasse cubes has:

```text
18  direction-labelled lower terms;
15  physical (matching, repeated-edge) collision labels;
12  nonzero coefficients after physical shared-label cancellation;
 8  nonzero matching coordinates after occurrence aggregation.
```

The map from 18 direction labels to 15 physical collision labels has a
three-dimensional kernel.  Its generators are the differences of the two
cut copies of the three shared physical labels.  Consequently the physical
descent problem is exactly one protected comparison `Phi` on the
fifteen-label quotient.  Two independent cutwise fillers descend if and
only if they agree on those three overlap labels.

Checker:
[`verify_h3_complete_tangent_lower_protected_phi_reduction.py`](../computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py).

## 1. The complete lower-face inventory

For a three-site cut `S`, six of the fifteen perfect matchings cross the cut
and contribute to its top cut permanent.  Each of the other nine has a
unique matching edge internal to `S`; the two site-Euler directions at that
edge collide.  Thus one complete tangent-Hasse cube has nine labelled lower
terms.

Use `S0=012` and `S1=024`.  The top and lower profiles are

\[
 \operatorname{top}=P_{024}-P_{012}=v,
 \qquad
 \operatorname{low}=(1-P_{024})-(1-P_{012})=-v.       \tag{2}
\]

Equation (2) holds only after occurrence aggregation.  Before forgetting
labels, each cut contributes nine terms.  The two physical label sets meet
in exactly three entries, all on repeated edge `02`.  Identifying those
entries gives dimension

\[
                         9+9-3=15.                    \tag{3}
\]

The explicit direction-forgetting map has rank fifteen and a
three-dimensional kernel.  After applying the signed lower chain, three
pairs cancel and twelve physical collision coefficients remain.  Forgetting
the repeated edge then combines those twelve coefficients into the eight
matching coordinates of `-v`.

This is why a nullhomotopy of the aggregate vector alone is insufficient:
it may discard the exact fine labels on which source validity and physical
readouts depend.

## 2. The single comparison theorem

Let `U` be the fifteen-dimensional physical collision-label module, let

\[
                       J_{\rm col}:U\longrightarrow E \tag{4}
\]

be its complete protected boundary, and let `u in U` be the twelve-supported
lower chain above.  Its occurrence shadow satisfies

\[
                         J_{\rm col}u=-v               \tag{5}

in the filtered coefficient packet.

Suppose one source-valid word/fine/repeated-grade comparison

\[
 \Phi:U\longrightarrow L_3,
 \qquad J_3\Phi=A J_{\rm col}                          \tag{6}
\]

is constructed.  Applying (6) to (5) gives

\[
                         J_3\Phi(u)=-A v.              \tag{7}

Hence `(Av,Phi(u))` is the required protected marked kernel after extending
the comparison by `A` on ordinary top grade.  The ordinary occurrence
marker is zero on `Phi(u)` by grade, so its value remains the marked value
one from `v`.

Equation (7) is the promised reduction: constructing the Cartan--Spencer
nullhomotopy of this complete determinant-dark lower face is no more and no
less than constructing the single protected comparison (6) on the displayed
fifteen-label packet.

## 3. Why two cutwise comparisons do not suffice

Let `F:k^18 -> U` forget the Hasse cut direction.  A scalar component of a
map on the direction-labelled module factors through `F` exactly when it
annihilates `ker F`.  Componentwise, the same is true for a vector-valued
comparison.

Thus two maps on the `012` and `024` cubes define one physical `Phi` if and
only if their values agree on the three shared labels.  The checker freezes
both sides:

* a row pulled back from `U` kills all three chart differences;
* changing one cut copy while fixing the other reads one on a chart
  difference and therefore cannot descend.

This is the first exact physical obstruction.  It is a three-entry
matching-square/coherence condition, not another matching-support census.

## 4. Universal Spencer contraction versus physical descent

The normally ordered positive-degree Spencer complex has the universal
Euler homotopy

\[
               dH+Hd=1,
               \qquad H={i_E\over\text{total degree}}.            \tag{8}
\]

The checker replays (8) in total degree three, the degree of the tangent
cube.  Therefore the lower face has no universal-symbol homology
obstruction.  The obstruction lies entirely in descending this contraction
through the physical fine-label quotient.  Equations (3) and (6) isolate
that descent in a finite module.

The universal contraction must not itself be called physical: it does not
assign target, ordinary residue, physical anchor, or terminal values to the
fifteen collision labels.

## 5. Physical `q` after `Phi`

Once (6) is physical on the complete relative domains, `7efd10d` makes the
terminal question final.  Write `q=M-ainc`.  There are only two cases.

* If

  \[
   [M-M_3\Phi]-[ainc-ainc_3\Phi]\ne0
       \quad\text{in }U^*/\operatorname{row}(J_{\rm col}),        \tag{9}
  \]

  the quotient class has a protected-kernel witness.  Physicality of both
  `q` rows and `Phi` makes `q` nonzero on the witness or its canonical
  image, giving the normalized relative generator.
* If (9) is zero, `q-q_3 Phi=lambda J_col`; the augmented target comparison
  exists and the generator/Fredholm alternative applies.

Thus no additional terminal obstruction remains after construction of the
single physical `Phi`.

## 6. Physical anchor pairing is a separate law

The weakest `q` comparison does **not** determine physical anchor incidence.
The matching and `ainc` defects may be the same nonzero quotient class, so
their difference—and hence the `q` defect—is zero even though neither
transports separately.

The checker freezes the smallest example with protected row `(1,0,0)` and
kernel vector `(0,1,0)`.  Both pairs

```text
(matching, ainc) = (0,0),
(matching, ainc) = ((0,1,0),(0,1,0))
```

have the same `q=0`, while their `ainc` values on the kernel are zero and
one.  Therefore `q` transport cannot prove the nonzero physical anchor
pairing required by the bright rectangular branch.

After constructing `Phi`, one must additionally do one of the following:

1. transport `ainc` or the actual pure-anchor row separately modulo
   protected rows;
2. prove by fine-grade typing that the physical anchor kills `Phi(u)`, so
   the nonzero ordinary top value survives; or
3. compute the physical anchor directly on `(Av,Phi(u))`.

The ordinary occurrence marker already kills the lower grade, but it is an
auxiliary coordinate covector and cannot be substituted for this physical
anchor law.

## Updated frontier

```text
determinant-dark complete profile v
        |
        v
complete lower Hasse face (18 direction labels)
        |
        +-- three overlap equalities fail --> nonphysical chart residual
        |
        `-- one Phi on 15 collision labels
                |
                +-- q defect nonzero --> relative generator
                +-- q defect zero ----> augmented q comparison/Fredholm
                `-- anchor row -------> separate pairing computation
```

The next constructive target is now bounded: define `Phi` on fifteen named
collision labels and check three shared-label equalities, rather than search
for unrelated monomial fillers.

## Scope and verification

This is an exact reduction for the explicit determinant-dark balanced
six-site profile and its symmetries.  It does not construct `Phi`, prove its
separate physical-anchor law, or extend the construction uniformly to all
orders.

Run:

```text
python3 computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py
python3 -O computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py
python3 -I -S computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py
```

Frozen ledger SHA-256:

```text
fb3b3d40fc6eab23aa5c4d072d054e510b24f31967d13aa49f909fdfb69b2cb7
```
