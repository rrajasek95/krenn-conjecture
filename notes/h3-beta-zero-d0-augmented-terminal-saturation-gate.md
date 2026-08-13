# The beta-zero `D0` dual is bounded until one terminal comparison is made

## Outcome

Failure of

\[
                            1\in\theta(Z)                    \tag{1}
\]

does give an exact left separator, but only for the complete **local
protected map** in the fixed beta-zero order-(h) grade.  The separator is
not the raw target covector `[D0]^*`: it must be completed by a covector on
all protected rows.  Even after that completion, it is not automatically
the physical Fredholm/Macaulay terminal of the inactive proof.  One still
must extend it across the exhaustive augmented Interface-III map and land
it on the physical six-term and `W` packet.

The generic root-even product-rule orbit does not remove this obligation.
Its unnormalized source has an explicit factor `beta`, while its normalized
version divides by `beta`.  Its order-(h) leading coefficient is therefore
a normal-cone/Tor class at `beta=0`, not a source cell in the beta-zero
fibre.  Even granting the most favourable identification of its target line
with `[D0]`, the rank-one map

\[
                         \beta:R\longrightarrow R             \tag{2}
\]

is a sharp counterexample: it is an isomorphism after inverting `beta`, its
beta derivative is one, and its special-fibre image is zero.  A positive
limit theorem requires beta-saturation of the complete physical image.

Thus the beta-zero corner is reduced to one alternative:

* construct a beta-saturated protected lift of `[D0]`; or
* extend the completed local dual to the exhaustive physical terminal map
  (with failure of extension routed to the existing relative generator).

No coefficient-support enumeration is involved.

## 1. The exact augmented beta-zero map

Fix the selected final word, fine grade, repeated label, endpoint
orientation, and order-(h) beta-zero source grade.  Let

\[
                         C_0=C_{\beta=0}^{(h)}                 \tag{3}
\]

be the complete module of source-valid physical chains in that grade.
After quotienting the already known complementary `D2` target line and the
pure target cap, collect every row which must vanish on the desired cell in

\[
\begin{aligned}
 R_{\rm prot}={}&R_{\rm lower}\oplus R_{\rm descent}
 \oplus R_{\rm ridge}\oplus R_{\rm wrong\ word}\\
 &\oplus R_{\rm Eq}\oplus R_{\rm ores}\oplus R_{\rm ainc}
 \oplus R_{Yw/W}.                                           \tag{4}
\end{aligned}
\]

Here `R_(Yw/W)` retains both the derived cap boundary and the independent
physical `W` readout; projecting away `W` is unsound by the augmented
inactive-cap theorem.  Let

\[
 P:C_0\longrightarrow R_{\rm prot},\qquad
 \theta:C_0\longrightarrow Q_0=k[D_0]                       \tag{5}
\]

be respectively the protected packet and the remaining selected-root target
coefficient.  Then

\[
 J_0=(P,\theta):C_0\longrightarrow
             Y_0=R_{\rm prot}\oplus Q_0,qquad
 b_0=(0,[D_0]).                                             \tag{6}
\]

Writing `Z=ker(P)`, the desired cell exists precisely when

\[
 b_0\in\operatorname {im}J_0
       \quad\Longleftrightarrow\quad 1\in\theta(Z).          \tag{7}
\]

This is the full-column form of the membership isolated in `fc89523`.

## 2. What failure of membership actually gives

Work first over a field.  If (7) fails, then `theta` kills `ker(P)`.  Exact
row-space duality gives a covector

\[
                     \lambda\in R_{\rm prot}^{*},\qquad
                     \theta=\lambda P.                       \tag{8}
\]

Consequently

\[
             \epsilon_0=(-\lambda,[D_0]^*)\in Y_0^*          \tag{9}
\]

satisfies

\[
                    \epsilon_0J_0=0,qquad
                    \epsilon_0(b_0)=1.                       \tag{10}
\]

This corrects a tempting shorthand.  Raw `[D0]^*` is only known to kill
`theta(Z)`; it can be nonzero on an unprotected source column.  The actual
local separator is (9), including all compensating protected rows.  Over a
coefficient ring, reduce modulo a maximal ideal containing `theta(Z)` and
apply the same statement over the residue field.

Equations (9)--(10) are an exact bounded Macaulay separator for the cell
construction problem.  They are not yet a contradiction to the physical
source equation.  The vector `b0` is the desired auxiliary comparison
boundary, not by itself the normalized right-hand side of the final Krenn
coefficient map.

## 3. The single terminal-extension equation

Let

\[
             J_{\rm phys}:C_{\rm phys}\longrightarrow Y_{\rm phys} \tag{11}
\]

be the exhaustive augmented inactive map, retaining the complete literal
lower rows, reduced Eq, target, labelled ordinary residue, anchor incidence,
`Yw`, `W`, and the physical six-term/eta/sigma terminal.  Let

\[
                         i:Y_0\hookrightarrow Y_{\rm phys}    \tag{12}
\]

be the fixed-grade inclusion.  Promotion of (9) is exactly the lifting
problem

\[
 \boxed{
 i^*\widetilde\epsilon=\epsilon_0,qquad
 J_{\rm phys}^{*}\widetilde\epsilon=0,qquad
 \widetilde\epsilon(b_{\rm phys})=1.}                        \tag{13}
\]

The first two equations are solvable precisely when `epsilon_0` kills the
intersection

\[
          i(Y_0)\cap\operatorname {im}J_{\rm phys}.           \tag{14}
\]

Equation (14) is the one missing terminal comparison.  In physical terms it
must identify the completed `D0` dual with the same six-term/
`Yw=W` terminal used by the exhaustive generator/Fredholm theorem.  The
existing `r0-T` cap supplies the `W` value once the Interface-III repair is
constructed, but it does not prove (13).

The distinction is sharp.  The checker gives two full maps with exactly the
same local `J0`.  In the first, one added comparison column determines a
terminal coefficient and (13) has a solution.  In the second, a further
terminal-only column forces an inconsistent coefficient, so no extension
exists.  Thus local target duality alone cannot decide physical terminal
typing.

If (14) fails in the physical map, the detecting source class is a new
relative class.  It enters the already proved relative-generator branch
only after its quotient value is compared with the physical six-term
readout.  This is the dual formulation of the same single comparison, not a
new terminal mechanism.

## 4. Why the order-(h) generic limit does not supply `theta`

The generic trace-Cartan input is

\[
                            J_*=-h\alpha\beta I.                \tag{15}
\]

The normalized root-even orbit uses `(alpha beta)^(-1)`.  Grant, more
strongly than the current typing theorem proves, that its target line has
already been identified with the beta-zero `[D0]` line.  At Rees order
`ell^h`, its scalar shadow then has the form

\[
                 J(x)=-h\alpha\beta\,\ell^h[D_0].              \tag{16}
\]

For `beta != 0`, the rational source

\[
                   -{1\over h\alpha\beta}x                    \tag{17}
\]

maps to `ell^h[D0]`.  At `beta=0`, however, the order-(h) `ell`
coefficient of (16) is zero.  Applying one additional beta Hasse derivative
returns `-h alpha [D0]`, but this is a normal-cone coefficient: beta
differentiation is transverse to the special fibre and is not a physical
source chain there.

Algebraically, put `R=k[beta]`, `I=im(J)`, and `b=[D0]`.  Generic membership
only proves

\[
                       \beta^m b\in I                           \tag{18}
\]

for some `m`.  It proves `b in I` exactly when the image is beta-saturated
along this class:

\[
                  (I:\beta^m)\cap Rb=I\cap Rb.                 \tag{19}
\]

For (2), `I=beta R`, so `1` is present after localization and the first Hasse
coefficient is one, but the specialized map has zero image.  Notice that
`I tensor_R k` itself is one-dimensional: it is the inclusion
`I -> R` which loses injectivity after base change.  The defect is measured
by `Tor_1^R(R/(beta),k)`, and the cokernel is the literal beta-torsion module
`R/(beta)`.  Tensoring this example with `ell^h` preserves the counterguard
at every desired Rees order.

Therefore the order-(h) root-even product rule supplies a symbol/normal
class, not `theta`.  A positive theorem must prove (19) for the **complete
augmented physical image**, retaining the same descent, ridge, word, Eq,
residue, anchor, and `W` rows.  The current formal Hasse top fails exactly
those descent/ridge/word tests, so no saturation theorem is presently
available.

## Frontier consequence

The beta-zero corner has not produced a new support branch.  Its shortest
exact resolution is one of:

1. prove beta-saturation (19) and obtain the protected `[D0]` cell; or
2. solve the terminal extension (13), with a nonextendable class routed by
   the same physical six-term comparison to the established relative
   generator.

Until one of these complementary sides is proved, `[D0]^*` is a bounded local
separator rather than the final inactive Fredholm/Macaulay terminal.

## Verification

Run:

```text
python3 computations/verify_h3_beta_zero_d0_augmented_terminal_saturation_gate.py
python3 -O computations/verify_h3_beta_zero_d0_augmented_terminal_saturation_gate.py
python3 -I computations/verify_h3_beta_zero_d0_augmented_terminal_saturation_gate.py
python3 -S computations/verify_h3_beta_zero_d0_augmented_terminal_saturation_gate.py
```

All modes print ledger digest
`b457daee759404cf53999f93ecd0d443021fd04cb9633d73ca15cd5eec73bcdf`.
