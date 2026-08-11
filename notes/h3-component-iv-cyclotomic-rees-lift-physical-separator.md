# The cyclotomic chart Rees chain lifts to all orders, but its physical cap map is the primitive missing datum

Research boundary only.  This is an all-order statement in the completed
two-chart comparison module.  It does not construct the physical relative
generator \(n_c\), define the target-augmented physical \(d_2\), or prove
Krenn's conjecture.

## Exact all-order Rees lift

The first-normal calculation gives five dual chord directions \(n^{(v)}\)
at the cyclotomic point and exact expansions

\[
 h_w(q_0+\tau n^{(v)})
   =\tau\delta_{wv}+\tau^2R_{wv}.                       \tag{1}
\]

There are no omitted higher terms: every \(h_w\) is the hafnian of a
four-site quadratic and is therefore quadratic in the chord coordinates.
After dividing the two tagged Schur sectors by \(\tau\), their chart-odd
boundary matrix is exactly

\[
                         B(\tau)=I_5+\tau R.            \tag{2}
\]

The checker reconstructs \(R\) from the literal matching formulas.  It is
the symmetric circulant matrix with first row

\[
 \left(-\frac1{12},\frac{1+\zeta}{12},
       \frac{\zeta}{6},\frac{\zeta}{6},
       \frac{1+\zeta}{12}\right).                       \tag{3}
\]

Its determinant polynomial begins with a unit:

\[
\begin{split}
 \det B(\tau)={}&1-\frac5{12}\tau
 +\left(\frac5{24}+\frac5{48}\zeta\right)\tau^2
 +\left(-\frac5{96}-\frac{35}{576}\zeta\right)\tau^3\\
 &+\frac5{576}\zeta\tau^4
 +\left(\frac5{6912}-\frac1{6912}\zeta\right)\tau^5.
                                                               \tag{4}
\end{split}
\]

Thus \(B(\tau)\) is invertible over the completed exact coefficient ring.
More concretely, the coefficient recurrence

\[
 C_0=I_5,\qquad C_n=-RC_{n-1}=(-R)^n                    \tag{5}
\]

proves

\[
             (I_5+\tau R)\sum_{n\ge0}(-\tau R)^n=I_5.  \tag{6}
\]

Combining the five divided comparison chains by this inverse normalizes
their chart-odd boundary to \(I_5\) at every order.  This is an algebraic
recurrence proof, not evidence from a finite jet.  The checker nevertheless
replays it through order thirteen as a mutation guard.

## Target and old ordinary residue vanish coefficientwise

The five complete words remain the same mixed words at both coefficients
of (1).  Hence the target is zero before passing to the completion.  The two
chart sectors contain the same coefficient with opposite signs, so the old
ordinary-residue sum is also zero coefficientwise.  Multiplication by the
formal inverse (6) preserves both zero readouts.  Localizing \(\kappa\)
only scales the unit boundary by another unit.

Consequently there is no higher normal/Rees separator:

\[
 \text{completed chart comparison boundary}=I_5,
 \qquad \mathrm{tgt}=\mathrm{ores}_{\rm old}=0.          \tag{7}
\]

## The remaining obstruction is physical, not normal

Equation (7) lives in the chart-odd comparison coordinate.  The physical
relative module uses the coordinates

\[
 (E,W,T,O)=(u\,\mathrm{Eq}|_{\rm edges=0},Yw,
            \mathrm{target},Y\,\mathrm{ores}).
\]

Its already-certified primitive separator is

\[
                  \lambda(E,W,T,O)=E+W+T-O.             \tag{8}
\]

Every currently available physical lower-face column lies in
\(\ker\lambda\).  Identifying one normalized chart-odd boundary in (7)
with the physical cap coordinate would add

\[
                         K=(0,1,0,0),
 \qquad                  \lambda(K)=1.                  \tag{9}
\]

The physical rank rises from three to four with determinant \(\pm1\).
Therefore this is a primitive integral gap, not torsion and not another
higher normal compatibility condition.

The exact remaining theorem is a source-provenant comparison map taking
the completed chart-odd class in (7) to physical \(Yw\), while preserving
the zero target and the correctly defined physical ordinary residue.
Equivalently, it is precisely the missing relative generator \(n_c\) from
the physical definability gate.  Declaring chart-odd mass to be \(W\) would
assume that theorem rather than prove it.

## Consequence

The cyclotomic route no longer has an order-by-order lifting problem in its
normal cone.  Its chart-level Rees lift is exact to all orders.  The route
still does not close Component IV because the map from that comparison
boundary to the physical cap boundary is unconstructed and is separated
primitively from every currently typed physical source column by (8).

## Verification

Run

```text
.venv/bin/python computations/verify_h3_component_iv_cyclotomic_rees_lift_physical_separator.py
.venv/bin/python -O computations/verify_h3_component_iv_cyclotomic_rees_lift_physical_separator.py
```

The checker reconstructs the exact quadratic remainder matrix, determinant
polynomial, formal inverse recurrence, literal target/old-residue readouts,
and the committed primitive physical separator.
