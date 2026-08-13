# The generic cap jets already supply the upper root-decorated Cartan label

Research construction and sharp lower-face gate.  This closes the upper
target-label problem on `alpha*beta != 0`; it does not construct the lower
Cartan landing, settle its Rees class, treat `beta=0`, or prove Krenn's
conjecture.

## Result

At `h=3`, with selected diagonal colour first, the two literal cap rows have

\[
 T(J_1)=(\beta,-\alpha,-\alpha),\qquad
 T(J_2)=(-\beta,-2\alpha,-2\alpha).
\]

Neither row alone has the equal two-root weights required by the physical
`0 <-> 2` Weyl defect at a general point.  The first row works only when
`beta=-alpha`; the second only when `beta=2alpha`.  But their literal
combination

\[
 \boxed{J_*=(\beta-2\alpha)J_1+(\beta+\alpha)J_2}
\]

satisfies

\[
                 T(J_*)=-3\alpha\beta\Delta,
       \qquad 3T(J_*)=-9\alpha\beta\Delta.             \tag{1}
\]

The coefficients are source scalars disjoint from the two local root sites.
The complete physical Cartan source-orbit theorem therefore applies to this
literal row.  If `w` is the simultaneous two-root Weyl action and
`rho=(1 4)`, then

\[
 C_+=\frac1{9\alpha\beta}(1+\rho)H_w(P(J_*))            \tag{2}
\]

has upper physical target

\[
                    \operatorname {tgt}(C_+)
                       =-2(w-1)\Delta.                  \tag{3}
\]

Thus the generic upper root-decorated label map requested in `3b8bcfc` is
not a new generator.  It is supplied by one exact `J1/J2` recombination and
the already source-provenant Cartan orbit.  More generally, at order `h`,

\[
 J_*=(\beta-(h-1)\alpha)J_1+(\beta+\alpha)J_2,
 \qquad T(J_*)=-h\alpha\beta\Delta.                    \tag{4}
\]

Checker:
[`verify_h3_generic_cartan_adjacent_target_label_prolongation.py`](../computations/verify_h3_generic_cartan_adjacent_target_label_prolongation.py).

## The full adjacent cell reduces to one lower Cartan remainder

The row `P(J*)` is not a closed Cartan input: its differential records the
adjacent `lambda A / p t_c B` filtration.  Applying the Cartan identity to
(2) gives

\[
 dC_+(P(J_*))=
 {1\over9\alpha\beta}(1+\rho)(w-1)P(J_*)
 -{1\over9\alpha\beta}(1+\rho)H_wd(P(J_*)).            \tag{5}
\]

The first term is the constructed upper face.  Hence the entire physical
landing theorem has reduced to the one explicit source-provenant remainder

\[
 \boxed{R_+={1\over9\alpha\beta}(1+\rho)H_wd(P(J_*))}. \tag{6}
\]

One must identify (6), modulo literal adjacent boundaries, with the desired
lower `p t_c B` face.  Equivalently the only remaining finite class is

\[
 [R_+-L_{\rm adj}\bmod\ell^r]
 \in(\ker\epsilon/N_{\rm lit})\otimes
        \mathbb Q[\ell]/(\ell^r),\qquad r\le2.          \tag{7}
\]

Vanishing of (7) gives the physical adjacent target cone.  A nonzero class
is the exact literal Rees obstruction/typed exit.  Hasse/Rees linearity
propagates the three chart coherences, but does not by itself prove (7): two
jets can have the same evaluated coefficients and different classes in
`ker(epsilon)/N_lit`.

This is materially smaller than the earlier target-label problem.  There is
no longer an unknown map between the monochromatic `J` target and the mixed
two-root target; only the lower face of a known physical Cartan chain remains.

## The Gate-I remainder is a different parity component

Write

\[
 K_-=(1-\rho)H_w,\qquad K_+=(1+\rho)H_w.
\]

Because `rho` commutes with `w`, `H_w`, and the physical differential,

\[
 \rho K_-=-K_-,\qquad \rho K_+=K_+.
\]

Therefore

```text
K_- d(u_012)       rho-odd,
R_+=K_+ d(P(J*))   rho-even.
```

The parity summands are a direct sum over characteristic zero.  Tensoring
with the invariant divided-power/Rees algebra preserves that splitting at
every jet order.  Consequently the new adjacent companion cannot absorb a
nonzero Gate-I residual `K_-d(u_012)`.  The two cells share the same Cartan
architecture but close different parity components.  Gate I must make its
odd remainder equal the already constructed `M_v` input boundary (or export
its typed defect) separately.

## Why the old fourth-Hasse filler still does not close (7)

The prolonged fourth-Hasse cone is the closest known filler.  In the
unrooted normalization its physical diagonal projection has boundary

\[
 ((H_0-u)e_{\rm Eq},Yw),
\]

whereas the desired physical boundary is `(0,Yw)`.  Transport it through
the constructed normalized root label `-2D`, with
`D=(w-1)Delta`.  Componentwise the two vectors are

\[
 \bigl(-2D(H_0-u)e_{\rm Eq},-2DYw\bigr),
 \qquad (0,-2DYw).                                     \tag{8}
\]

The old polynomial covector `(Y,-(H0-u))` kills the first vector and reads

\[
                    2D(H_0-u)Y\ne0                    \tag{9}
\]

on the second.  Since `D` has four nonzero word coordinates, root decoration
does not erase the conormal obstruction.  With the signs in (8), the
smallest new relative correction has boundary

\[
                 +2D(H_0-u)e_{\rm Eq},                 \tag{10}
\]

zero target and zero ordinary residue, and must be Hasse/Rees-linear and
`rho`-even.  The source-valid fourth-tower theorem excludes obtaining (10)
from the old top-selector template: its informative selector sends `H_m` to
one, whereas a source-valid tower sends the source ideal back into itself.

Equation (10) is a no-go for the **known formal filler**, not a proof that
the actual physical remainder (6) is nonzero.  The shortest next attack is
to compute (6) in the literal two-step adjacent filtration.  Either it lands
in `L_adj+N_lit`, closing the generic inactive target cone, or its first
nonzero value is precisely (7), with (9) the first obstruction for the old
fourth-Hasse repair.

## Verification

Run:

```text
python3 computations/verify_h3_generic_cartan_adjacent_target_label_prolongation.py
python3 -O computations/verify_h3_generic_cartan_adjacent_target_label_prolongation.py
python3 -I -S computations/verify_h3_generic_cartan_adjacent_target_label_prolongation.py
```

Frozen ledger SHA-256:

```text
693b007a6dda020a6a075fe291e418c781a6ee1c00d6fb3a4ad669294c372239
```
