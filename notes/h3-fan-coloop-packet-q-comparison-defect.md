# Fan-coloop packet disagreement is exactly one physical `q` defect class

## Result

The packet-agreement obstruction left by `e6b390a` has the same exact form
as the protected physical-`q` comparison theorem.

Let

\[
 J:L\longrightarrow E,
 \qquad J_0:L_0\longrightarrow E_0                  \tag{1}
\]

be the complete protected maps in the fan-coloop packet and the canonical
endpoint-odd packet.  Assume a source-valid physical comparison

\[
                   J_0\Phi=A J.                       \tag{2}
\]

On both sides write the odd packet readout in physical form

\[
                  q=M-a,\qquad q_0=M_0-a_0,           \tag{3}
\]

where `M` is the complete weighted matching aggregate of the oriented
`U/V` packet and `a` is physical anchor incidence.  Endpoint oddization
kills the invariant anchor contribution in the canonical normalization,
but retaining (3) is useful because it records exactly what must be
transported off that normalization.

Define

\[
 \mathfrak o_{\rm fan}(\Phi)
   =[(M-M_0\Phi)-(a-a_0\Phi)]
   =[q-q_0\Phi]
   \in L^*/\operatorname {row}(J)
   \simeq(\ker J)^*.                                  \tag{4}
\]

There is an exhaustive alternative.

1. If `o_fan(Phi)!=0`, there is `x in ker J` with

   \[
                         q(x)\ne q_0(\Phi x).          \tag{5}
   \]

   Since `Phi x in ker J0`, at least one of the two physical values in (5)
   is nonzero.  When `q,q0` are the relative terminal rows, normalize that
   kernel class to obtain the physical generator.  When the packet readout
   is only a saturated matching/exchange coordinate, the same witness is a
   literal typed exit rather than a generator.
2. If `o_fan(Phi)=0`, there is a row vector `lambda` with

   \[
                  q-q_0\Phi=\lambda J.                \tag{6}
   \]

   Thus the comparison extends to the augmented physical `q` maps.  Correct
   the actual odd Cartan row by `lambda J`; its complete packet is then the
   desired odd part of the already physical signless pivot.  The two
   oriented target-bearing rows follow from `(S+D)/2` and `(S-D)/2`.

There is no residual “packet mismatch” branch after a physical `Phi` and
the physical decompositions (3) have been constructed.  The remaining
constructive input is the separate anchor law

\[
                         h_{\rm phys}(k)\ne0            \tag{7}
\]

on the resulting minimum target circuit.

Checker:
[`verify_h3_fan_coloop_packet_q_comparison_defect.py`](../computations/verify_h3_fan_coloop_packet_q_comparison_defect.py).

## Quotient proof

Equation (4) vanishes exactly when `q-q0 Phi` annihilates `ker J`.  Over the
coefficient field, row-space/kernel-annihilator duality gives (6).  In that
case

\[
 \binom{J_0\Phi}{q_0\Phi}
 =
 \begin{pmatrix}A&0\\-\lambda&1\end{pmatrix}
 \binom Jq.                                            \tag{8}
\]

If (4) is nonzero, choose a kernel witness `x`.  The protected square (2)
puts `Phi x` in the canonical protected kernel.  Equation (5) implies that
`q(x)` and `q0(Phi x)` cannot both vanish.  This is the same two-sided
positive alternative as the existing all-dark physical-`q` theorem; no
global left separator has to be declared physical.

The checker audits both possible visible sides.  It also records the
strictly weaker success which is useful here: `M` and `a` may each fail to
transport modulo protected rows, while their two defect classes agree and
cancel in `q`.  Therefore constructing separate matching and anchor chain
homotopies is sufficient but not necessary for the packet split.

## The exact oriented split after transport

Use the orientation basis

```text
U+, U-, V+, V-, target.
```

The physical complete-row pivot is

\[
 S=\alpha(U_++U_-)-d(V_++V_-)-\alpha.                \tag{9}
\]

Suppose the actual endpoint-odd Cartan projection `D_phys` differs from the
desired packet

\[
 D_0=\alpha(U_+-U_-)-d(V_+-V_-)                       \tag{10}
\]

by `lambda J`.  Replace it by the source-valid protected-row correction

\[
                         D=D_{\rm phys}-\lambda J=D_0. \tag{11}
\]

Then

\[
\begin{aligned}
 {S+D\over2}&=\alpha U_+-dV_+-{\alpha\over2},\\
 {S-D\over2}&=\alpha U_--dV_--{\alpha\over2}.         \tag{12}
\end{aligned}
\]

Thus literal equality of the two complete packets is stronger than
necessary.  Equality of their physical `q` classes in
`L*/row(J)` is the exact condition.

## Why the physical anchor remains independent

The row `h_phys` used by the rectangular constructive landing is not the
packet terminal `q`.  The checker gives the minimal exact separation:

```text
J=(1,0,0),
q=q0=(0,1,0),
h_phys-h0=(0,0,1),
k=(0,0,1) in ker J.
```

The `q` comparison defect is zero, but the anchor defect is nonzero modulo
`row(J)` and reads one on the target circuit `k`.  Hence (6) does not prove

\[
                 h_{\rm phys}-e_\tau^*
                      \in\operatorname {row}(A_D).     \tag{13}
\]

This is useful rather than discouraging: the packet-agreement branch is now
closed by the same quotient theorem as Gate I, while (13) is one plainly
separate physical-anchor law shared by both constructive routes.

## Exact remaining theorem

The remaining fan-coloop comparison statement is now:

> Construct a complete physical protected comparison `Phi` in the
> fan-coloop fine grade and identify the two weighted matching/anchor rows
> in (3).  Then a nonzero class (4) is already the typed exit/generator,
> while a zero class gives the oriented affine rows (12).  Prove separately
> that their minimum target circuit is visible to `h_phys`, or type the dual
> failure as the saturated Hall/Fitting covector.

The six Hall symmetry types, common-`q` tail, endpoint orientation, and
fine-word provenance require no additional identity.

## Scope and verification

This is an exact protected-row quotient theorem.  It is conditional on the
physical comparison and on literal `q=M-a` typing on both source domains.
It does not construct `Phi`, a full Krenn source counterexample, or the
physical-anchor law.

Run

```text
python3 computations/verify_h3_fan_coloop_packet_q_comparison_defect.py
python3 -O computations/verify_h3_fan_coloop_packet_q_comparison_defect.py
python3 -I -S computations/verify_h3_fan_coloop_packet_q_comparison_defect.py
```

Frozen ledger SHA-256:

```text
f32c1f0c3fed7034c93e73fa078c520d14d5e28676551972869bd2202b0aae41
```
