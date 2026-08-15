# The diagonal-cap active saturation is already a no-zero ideal

## Verdict

The endpoint-polarized comparison constructs the full linear evaluation of a
supplied cap, but the nonlinear selection problem cannot be a constructive
shortcut at $h=3$.  Put

\[
 K(\lambda)=\lambda_0E_{00}+\lambda_1E_{11}
                    +\lambda_2E_{22},
 \qquad
 s(\lambda)=\sum_i\lambda_iA_{67}[ii],
 \qquad
 r(\lambda)=\sum_i\lambda_ir_i.                      \tag{1}
\]

The exact homogeneous cubic error is

\[
            \boxed{6{\cal E}(\lambda)
                    =3s(\lambda)r(\lambda)^2x+r(\lambda)^3.}   \tag{2}
\]

There are ten $\lambda$-monomials: three pure cubes, six ordered
$\lambda_i^2\lambda_j$, and one
$\lambda_0\lambda_1\lambda_2$.  For $i\ne j$,

\[
 C_{iij}:=[\lambda_i^2\lambda_j]\bigl(6{\cal E}\bigr)
 =3s_jr_i^2x+6s_ir_ir_jx+3r_i^2r_j,                  \tag{3}
\]

while

\[
 C_{012}:=[\lambda_0\lambda_1\lambda_2]\bigl(6{\cal E}\bigr)
 =6(s_0r_1r_2+s_1r_0r_2+s_2r_0r_1)x+6r_0r_1r_2.     \tag{4}
\]

An active diagonal zero would require all 729 coordinates of (2) to vanish
on

\[
          D(\lambda)=\lambda_0\lambda_1\lambda_2s(\lambda)\ne0. \tag{5}
\]

Exact descent plus the certified arbitrary-complex six-site theorem proves
that this never happens on a genuine exact eight-site source.  Consequently
the active saturation is the unit ideal.  A theorem forcing such a zero on
every exact source is therefore equivalent to proving that the $h=3$
source scheme is empty; it is not a weaker replacement for Gate II.

## Ordinary resultant is the wrong test

Even after all three coordinate cubics vanish, the pairwise mixed
coefficients can exclude the active torus.  The minimal exact guard is

\[
 F_0=\lambda_0^2\lambda_1,qquad
 F_1=\lambda_1^2\lambda_2,qquad
 F_2=\lambda_2^2\lambda_0.                            \tag{6}
\]

The ordinary homogeneous resultant is zero: all three coordinate-axis
points are common projective zeros.  None is active.  Localizing at the
three diagonal coordinates instead gives the one-line Laurent certificate

\[
             F_0F_1F_2=(\lambda_0\lambda_1\lambda_2)^3,          \tag{7}
\]

so

\[
     (F_0,F_1,F_2):(\lambda_0\lambda_1\lambda_2)^\infty=(1).     \tag{8}
\]

The reverse directed cycle has the same certificate.  This guard has zero
pure cubics and zero triple coefficient.  Thus coordinatewise cleanliness,
the triple polarization, and ordinary resultant vanishing can all hold while
the active diagonal locus is empty.  The six pairwise coefficients (3) are
the first load-bearing cross-colour layer.

The guard (6) is an abstract exact coefficient signature, not an asserted
eight-site source point.  Its role is to show precisely what the current
linear marked maps do not control.

## Saturation on the actual source scheme

Let $J_{\rm src}$ be the official $9\cdot3^6=6561$ coefficient ideal for
$H_8(A)=\Delta_{8,3}$, and let

\[
 I_{\rm diag}=J_{\rm src}
       +( {\cal E}_w(\lambda):w\in\{0,1,2\}^6).       \tag{9}
\]

Then, over $\mathbb C$,

\[
 \boxed{
 I_{\rm diag}:D(\lambda)^\infty=(1).}                 \tag{10}
\]

Equivalently, after adjoining an inverse variable $z$,

\[
 I_{\rm diag}+(zD(\lambda)-1)=(1).                    \tag{11}
\]

The proof is short and exact.  If (11) had a complex zero, it would give an
exact source and a diagonal cap with
$s\kappa_0\kappa_1\kappa_2\ne0$ and ${\cal E}=0$.  Exact cap descent
would produce a six-site aggregate whose three pure coefficients are
$\kappa_i/s$.  Scaling the colour-$i$ axis at one residual site by
$s/\kappa_i$ is invertible and sends that tensor to
$\Delta_{6,3}$, contradicting certified `SP-K6`.  The weak
Nullstellensatz gives (11), hence (10).

This is a genuine theorem about every actual exact-source fibre, even though
no eight-site source point is known or assumed.  It is not an extracted
Gröbner certificate: the direct universal calculation would contain 6,561
source generators, 729 error generators, and the affine inverse equation.
The committed certificate route is exact descent plus the independently
certified nineteen-stratum six-site theorem.

## What coefficient identity is actually missing?

The exact cap formula gives, word by word,

\[
 \operatorname{haf}_w(sq+R(K))
 =s(K)^2\sum_{l,m}K_{lm}\operatorname{Row}(l,m,w)
   +{\cal E}_w(K).                                    \tag{12}
\]

On the exact-source scheme the rows identify the first term with the
contracted GHZ target.  Equation (12) identifies ${\cal E}$ as the higher
clean error; it does not make it vanish.  The first colour-support not
controlled by the coordinate maps is support two, namely the six tensors
$C_{iij}$ in (3).

At minimum, a new source-derived mixed second-polarized syzygy would have to
exclude both directed Laurent cycles among

```text
C_001, C_112, C_220     and     C_002, C_110, C_221,
```

and then remain compatible with the triple tensor (4).  Stated invariantly,
it must prove that the active saturation of the full coefficient ideal is
proper.

But (10) says that on the genuine exact-source scheme this saturation is
already the unit ideal.  Therefore a relation making it proper for every
source point can hold only vacuously, after proving there are no source
points.  This is why there is no isolated missing local coefficient identity
whose addition would cheaply select a cap.  The proposed diagonal selection
has reached the original $h=3$ emptiness problem.

The identity specialization $\lambda=(1,1,1)$ says the same thing in its
smallest form:

\[
           \operatorname{tr}A_{67}\ne0,qquad {\cal E}_{6,7}(I)=0. \tag{13}
\]

That condition was already known to be equivalent to the open eight-site
case.

## Consequence for the proof plan

The endpoint-polarized evaluation remains useful as a typing theorem: given
a $K$, its nine coordinate contractions and all marked P2 faces are now
source-provenant.  It does not improve the selection problem.  The
constructive proof must either obtain an active clean cap from additional
minimum-support/global structure—thereby proving emptiness—or return to the
Gate-II/Fredholm route that contradicts the hypothetical source without
postulating a clean cap.

## Verification

Run:

```text
python3 computations/verify_h3_diagonal_cap_active_clean_saturation_gate.py --mode structural
python3 -O computations/verify_h3_diagonal_cap_active_clean_saturation_gate.py --mode full
python3 -I -S computations/verify_h3_diagonal_cap_active_clean_saturation_gate.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
527cb54f0ab0331f783d90b548c99999c1f0cee6003380772a2c8cda51907d42
```
