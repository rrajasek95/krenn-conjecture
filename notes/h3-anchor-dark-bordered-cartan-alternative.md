# An anchor-dark target circuit gives a bordered separator or a unit Cartan kernel

## Result

Let `A_D` be the complete physically typed target-augmented response map on
a minimum target-circuit block, with

\[
                         \ker A_D=\langle k\rangle.
\]

Let `h_phys` be the physical pure/target anchor row, and let `(g,alpha)` be
the complete placed Cartan column including its physical anchor entry.  The
bright condition used by the rectangular theorem is

\[
                         h_{\rm phys}(k)\ne0.          \tag{1}
\]

If (1) fails, row-space/kernel duality gives an exact factorization

\[
                         h_{\rm phys}=\lambda A_D.    \tag{2}
\]

Put

\[
                         \beta=\alpha-\lambda g.      \tag{3}
\]

Then the dark branch is already exhaustive.

1. If `beta!=0`, the output covector

   \[
                          \sigma=(-\lambda,1)
   \]

   kills every old column of the physical bordered map
   `(A_D;h_phys)`, including the homogenizing target column, while
   `sigma(g,alpha)=beta`.  After normalization it is a target-dark separator
   detecting the Cartan column.
2. If `beta=0` and `g` is external to `im(A_D)`, an ordinary cokernel
   covector `mu A_D=0`, `mu g!=0`, extended by zero on `h_phys`, is again a
   target-dark separator.
3. If `beta=0` and `g=A_D y`, equation (2) gives

   \[
                       h_{\rm phys}(y)=\lambda g=\alpha.
   \]

   Hence `(-y,1)` is a unit-Cartan kernel of the complete bordered map.

There is no fourth anchor-dark linear branch.  Checker:
[`verify_h3_anchor_dark_bordered_cartan_alternative.py`](../computations/verify_h3_anchor_dark_bordered_cartan_alternative.py).

## Composition with the bright theorem

The complete bordered alternative can now be stated without assuming
anchor brightness in advance.

```text
h_phys(k) != 0, g external -> two-rank rectangular landing;
h_phys(k) != 0, g internal -> adjusted unit-Cartan kernel;
h_phys(k)  = 0             -> target-dark separator or unit-Cartan kernel.
```

Thus Route A does not need maximum-anchor/minimum-support to *force*
`h_phys(k)!=0`.  Extremality is used upstream to isolate the minimum
target-circuit block.  Once the shared odd comparison has supplied the
complete physical packet, failure of the anchor law is itself a bordered
Fredholm output.

The qualification “complete physical packet” is load-bearing.  The rows of
`A_D`, `h_phys`, and both parts of `(g,alpha)` must be literal rows/columns
in one common fine grade.  Under this hypothesis `(-lambda,1)` is a
localized combination of complete physical output rows, with coefficient
one on the actual anchor row, and it kills the actual target column.  An
occurrence selector substituted for `h_phys` would only give a formal
separator.

## The actual fan-pivot guard

Use the exact dark packet frozen by `e6b390a` and `cc75050`:

\[
 A_D=
 \begin{pmatrix}
 4&-2&-1\\
 3&-2&0\\
 0&0&0
 \end{pmatrix},
 \qquad k=(2,3,2),
 \qquad h_{\rm dark}=(4,-2,-1).
\]

Here `h_dark=(1,0,0)A_D`.  Therefore

\[
                         \sigma=(-1,0,0,1)            \tag{4}
\]

kills the complete old bordered block.

* For `g=(0,0,1)` and `alpha=1`, (4) reads one on the Cartan column.
* For the same external `g` and `alpha=0`, the third output-coordinate
  covector is the ordinary target-dark separator.
* For the internal column `g=A_D(1,0,0)=(4,3,0)` and `alpha=4`, the vector
  `(-(1,0,0),1)` is the unit-Cartan kernel.
* Changing that last `alpha` to `5` makes (4) the separator again.

The checker exhausts all `81` choices of `g in {-1,0,1}^3` and
`alpha in {-1,0,1}` on this packet.  Every choice lands in exactly one of
the three dark outcomes.

## Why minimum support does not force brightness

The first two rows of the same packet describe the affine problem

\[
 C_1=(4,3),\qquad C_2=(-2,-2),\qquad t=(1,0).
\]

The two occupied columns are independent, neither coordinate line contains
`t`, and the unique affine solution is

\[
                         x=(1,3/2).
\]

It is therefore already support-minimal, while the target circuit remains
anchor-dark.  This is a sharp linear obstruction to deriving (1) from
minimum affine support alone.  It is not asserted to be a full Krenn source;
the positive content is that the exact bordered alternative closes the dark
linear branch once the rows are physically typed.

If the internal unit-Cartan kernel is supported on literal occupied endpoint
coordinates and its deletion is anchor-safe, the existing minimum-support
argument upgrades it to a support deletion.  Without that extra support
typing it remains the already established physical unit-kernel/terminal
branch; no deletion is claimed silently.

## Effect on the frontier

After a complete physical shared odd `Phi`, `7a3ad78` already closes packet
disagreement.  The constructive fork is now:

```text
anchor bright -> rectangular two-rank landing or unit kernel;
anchor dark   -> normalized physical target-dark separator or unit kernel.
```

Consequently a separate theorem forcing marked noncollapse is needed only
if one insists that every external Cartan column land in the bright
two-rank arm.  It is not needed for the exhaustive bordered alternative.

## Scope and verification

This is exact localized linear algebra and uses the actual fan-pivot guard.
It does not construct the shared odd comparison, global source entry, or a
full Krenn source from the numerical packet.

Run

```text
python3 computations/verify_h3_anchor_dark_bordered_cartan_alternative.py
python3 -O computations/verify_h3_anchor_dark_bordered_cartan_alternative.py
python3 -I -S computations/verify_h3_anchor_dark_bordered_cartan_alternative.py
```

Frozen ledger SHA-256:

```text
9f5e47e711a6249d256a09a3374b978a14f11f2dea77238a4a265e6816174cbf
```
