# The second-Hasse dual extends through the known augmented packet

## Result

Let

\[
             \mathfrak o_2=[F_{[2]}(\xi)]\in\operatorname{coker}A
\]

be the first nonlinear obstruction from the full `171`-column source
Jacobian, and let `psi` be a local output covector detecting it.  The first
physical augmented-row test is positive: every such `psi` extends through
the complete old `r0,T,rho` cap packet and the physical Cartan column `K`.

Write `mu_j=psi(B_j)` on the four literal corner boundaries and

\[
                       \alpha=(-1,1,1,-1).
\]

The exact extension is

\[
\begin{aligned}
 \widetilde\psi(\mathrm{target}_j)&=-\mu_j,&
 \widetilde\psi(W_j)&=-\mu_j,\\
 \widetilde\psi(\mathrm{ores}_j)&=\mu_j,&
 \widetilde\psi(\mathrm{ridge})&=-\sum_j\alpha_j\mu_j,
\end{aligned}                                             \tag{1}
\]

with `q=ainc=Eq=0`.  It annihilates every known column separately.

Checker:

```text
computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py
```

Frozen ledger SHA-256:

```text
1b7c2bcd9d381196c33fd10ee0f0cb26870b6c9a2e03549cb30616b40669c16e
```

## The first literal stress column

In the retained row order, the physical columns are

\[
\begin{aligned}
 r0_j&=B_j+Eq_j+\mathrm{target}_j-\mathrm{ainc},\\
 T_j&=-W_j+\mathrm{target}_j,\\
 \rho_j&=W_j+\mathrm{ores}_j,\\
 K&=\sum_j\alpha_j\mathrm{ores}_j+\mathrm{ridge}.     \tag{2}
\end{aligned}
\]

Physical `q` is zero on this old repeated packet.  On only
`q/ainc/target/W/ores`, the `13` source columns have rank `12`.  Their unique
kernel is

\[
 \sum_j\alpha_j(r0_j-T_j-\rho_j)+K=M_v,                 \tag{3}
\]

whose remaining signature is

```text
(local B, Eq, ridge) = (alpha, alpha, 1).
```

Thus `M_v` is exactly the first column on which the uncorrected local dual
can appear to fail: its value is `alpha.mu`.  It is not a genuine failure.
Formula (1) cancels that value on `K`, while cancelling `r0,T,rho`
cornerwise.  Equivalently, retaining either the four `Eq` rows or the
primitive ridge raises the rank from `12` to `13`; the pure-local
intersection is zero.

This is the concrete augmentation calculation missing from the earlier
abstract extension gate.  Neither `q` nor `ainc` needs a correction.  The
target, `W`, ordinary-residue, and ridge rows suffice.

## Exact generator-or-terminal fork

Now let

\[
                  J:C_{phys}\longrightarrow Y_{aug}
\]

be the exhaustive physical relative map in one fixed
word/fine/repeated grade, and let `i:Y_loc -> Y_aug` include the Hessian
output grade.  There are exactly two cases:

1. `i(o2)` lies in `im J`.  A source combination has local boundary `o2`
   and zero `q/ainc/target/ridge` and other augmented rows.  This is the
   protected-zero physical relative filler/generator.
2. `i(o2)` does not lie in `im J`.  Exact duality supplies

   \[
              \Psi J=0,\qquad \Psi(i(\mathfrak o_2))=1,               \tag{4}
   \]

   so `Psi` is the augmented terminal extending a suitable local Fredholm
   dual.

There is no third branch.  The checker exhausts the alternative on all
small binary maps through local dimension three and external dimension two.

Consequently a nonzero second-Hasse obstruction is consumed either by a
physical relative generator or by an augmented terminal.  The only source
arm left after this fork is `o2=0`, where the formal arc must be prolonged
to third and higher order.

## Literal `H2/P2/C4` scope

The complete second-Hasse census identifies every compatible response face
as a literal `C2+`, `C4`, or `P2` packet.  Representatives are

```text
C2+ : d*q45 + p4*s5 + p5*s4
C4  : q23*q45 + q24*q35 + q25*q34
P2  : s3*q45 + s4*q35 + s5*q34
```

The pure trapped assignment `q23=q45=d=s3=1` makes all three nonzero and
does not route through an offdiagonal base tail or an outside Hall hole.
These are therefore the literal lower faces to which the terminal fork must
apply.

Their raw coefficient polynomials have no canonical `AugP2` values.  The
minimal missing object is one **totalized source-labelled landing** from the
original response word/fine/direction-pair grade into the cap--Cartan grade,
with protected `q`, `ainc`, and target zero and with the shifted ridge
retained.  Once such a landing is present, (1) extends every local dual and
the filler/terminal alternative is automatic.

The newly exposed mixed unary row `H0[000011]` does not replace this map.  It
forces one of fourteen alternate matching mates, but does not select a
unique occurrence section or an augmented terminal value.

## What remains open

The required hypothesis in the preceding paragraph is not automatic from
the `171`-column calculation.  `F_[2](xi)` initially lives in the literal
response output word/fine/repeated grade.  The endpoint-polarization theorem
constructs its full sixteen-term symbol (using the physical transpose for
the second half), but it does not construct the source-labelled landing in
the canonical repeated/AugP2 relative codomain.

Thus the first missing datum is no longer a `q`, `ainc`, target, or ridge
correction.  It is the response-to-relative grade placement itself.  Once
that map is physical and exhaustive, (3)--(4) give the desired
generator-or-terminal dichotomy immediately.

## Scope

The cap/Cartan signatures, rank statement, dual extension, and final linear
alternative are exact on the normalized canonical `h=3` packet.  This does
not construct the cross-grade placement of `o2`, nor compute `o2` at every
unknown trapped source.
