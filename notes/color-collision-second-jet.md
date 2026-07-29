# The characteristic-zero color-collision arc

Let (n=2m), write the local basis as (x,y,z), and collide two ternary
colors by

\[
 e_0\mapsto x,\qquad e_1\mapsto y,\qquad e_2\mapsto x+t z.
\]

An arbitrary source becomes

\[
 Q(t)=Q_0+tQ_1+t^2Q_2,
\]

where (Q_i) has exactly (i) local (z)-labels on every edge term.  The
target is

\[
 X+Y+\bigotimes_v(x_v+t z_v).
\]

Thus (Q_0) realizes (2X+Y), the first jet has coefficient one at every
coloring with one (z) and otherwise (x), and the second jet has
coefficient one at every coloring with two (z)'s and otherwise (x).
The map from the original nine edge cells to the (4+4+1) cells of
((Q_0,Q_1,Q_2)) is invertible, so these are arbitrary variables subject
only to their displayed (z)-degrees.

## Two exact second-order obstructions at six sites

For the Hamilton base take

\[
 P_x=01\mid23\mid45,qquad P_y=12\mid34\mid05,
\]

with (x)-weights (2,1,1) and unit (y)-weights.  The complete first
jet solution space has dimension 24.  Its forced visible entries are

\[
 B_{01}^{zx}=B_{01}^{xz}=1,qquad
 B_{23}^{zx}=B_{23}^{xz}=B_{45}^{zx}=B_{45}^{xz}=\frac12.
\]

The remaining parameters are precisely the four one-(z) cells on each of
the six same-parity chords

\[
 02,04,24,13,15,35.
\]

At the coloring ((x,x,x,z,x,z)), every (Q_2) contribution and every
kernel-dependent product vanishes.  The sole contribution is

\[
 A_{01}^{xx}B_{23}^{xz}B_{45}^{xz}
 =2\left(\frac12\right)^2=\frac12,
\]

contradicting the required coefficient one.  The same happens for all six
same-parity choices of the two (z)-vertices.

The obstruction survives the simplest non-Hamilton binary fiber.  Take two
unit (x)-matchings

\[
 01\mid23\mid45,qquad02\mid13\mid45
\]

and the unit (y)-matching (12\mid34\mid05).  They realize (2X+Y).
The first-jet space now has dimension 14.  At the same displayed coloring,
two matching terms give

\[
 \frac12(1-\tau_7)+\frac12\tau_7=\frac12,
\]

independently of all fourteen kernel parameters; again every (Q_2) term
vanishes.  Eight coefficients are frozen this way, with one (z)-vertex in
({0,1,2,3}) and the other in ({4,5}).

The verifier
[`verify_color_collision_second_jet.py`](../computations/verify_color_collision_second_jet.py)
constructs all 192 first-jet equations, proves the displayed affine
families exhaustive by exact rank/nullity certificates, and audits the
frozen second coefficients symbolically over the rationals.

## The four-site exception and exact scope

At four sites the three one-factors give a regular arc: keep one factor in
color (x), one in color (y), and put (x+t z) on the third.  Its output
is exactly

\[
 X+Y+\bigotimes_v(x_v+t z_v)
\]

to every order.  The verifier checks this directly.

These calculations identify a genuine second-order obstruction on two
substantially different six-site binary fibers, including every derivative
kernel direction.  They do **not yet** prove the universal statement for an
arbitrary complex binary base (Q_0).  Dense binary fibers may have larger
cofactor images, so a uniform proof still needs a base-independent dual
functional or Hessian-quotient argument.
