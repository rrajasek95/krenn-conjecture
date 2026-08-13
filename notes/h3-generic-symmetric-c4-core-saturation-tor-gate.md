# The C4 square gives a unit-or-one-Tor-line theorem

## Result

The exact local `E2/E3/E4` coherence–curvature square gives a sharp
unit-or-colon theorem for the generic symmetric C4 branch.  It does not
justify cancellation of the physically typed common core from the active
coloop equation alone.

Let the three four-site matching occurrences be

\[
 m_0=23|45,\qquad m_1=24|35,\qquad m_2=25|34,
\]

and put

\[
 s=m_0+m_1+m_2,\quad d_{01}=m_0-m_1,\quad
 d_{12}=m_1-m_2.
\]

The complete response/Hasse face supplies the symmetric row `g*s`; the two
flat `E2` transports supply `g*d01,g*d12`.  `E3/E4` are their Bianchi and
tetrahedral coherences.  Over characteristic zero,

\[
\begin{aligned}
 m_0&=(s+2d_{01}+d_{12})/3,\\
 m_1&=(s-d_{01}+d_{12})/3,\\
 m_2&=(s-d_{01}-2d_{12})/3.             \tag{1}
\end{aligned}
\]

Checker:
[`verify_h3_generic_symmetric_c4_core_saturation_tor_gate.py`](../computations/verify_h3_generic_symmetric_c4_core_saturation_tor_gate.py).

This discussion is needed only on the flat side of `E2`.  If its curvature
minor `Delta` is nonzero, the undivided identity already exposes the literal
curved common-q carrier and exits the generic-flat branch.  When `Delta=0`,
the two transports are flat and common-core saturation is the first remaining
source question.

## What a genuine unit core would construct

If the entire physically typed common core `g` has a same-grade inverse
`c_g`, then

\[
                         g c_g=1.                      \tag{2}
\]

Multiplying the three undivided rows by `c_g` gives

```text
c_g*(g*s, g*d01, g*d12) = (s,d01,d12).
```

Equation (1) then isolates each literal matching occurrence.  No formal
denominator or localization symbol is added.  `E3/E4` ensure that the two
`E2` path choices are coherent.  This is an explicit construction of the
local `U_C4` under the same-grade unit hypothesis.

For the one `DQ` label whose visible q edge equals the active coloop `e`, the
known relation is only

\[
                         q_e C_e=1.                    \tag{3}
\]

It proves that the `q_e` factor is a unit.  The physical H2 object also
retains its direction/reinsertion and one-sided pivot data.  No pinned theorem
identifies the *entire* E2 core `g` with the bare factor `q_e`.  Using (3) to
cancel all of `g` would therefore assume the word/fine/direction-pair
comparison isolated in `dc7c7ef`.

## Why this does not close every C4 grade

The complete second-Hasse census contains

```text
15 DQ grades: 1 coloop-aligned, 14 unaligned,
30 PS grades: no q-coloop common core.
```

For an unaligned `DQ` grade the visible common matching factor is `q_uv`, not
`q_e`.  For a `PS` grade the visible common occurrence factor is `p_u*s_v`.
The active-coloop and pure-trapped hypotheses do not make either full core a
unit.

There are literal local guards.  Keep `q01=1` as the active coloop, set an
unaligned common edge `q02=0`, and set all six residual K4 edges on
`1,3,4,5` to one.  The common core vanishes while the symmetric C4 tail has
value three.  Likewise, set `p0=s1=0` and all six residual K4 edges on
`2,3,4,5` to one.  The `PS` core vanishes while its C4 tail is three.

These are exact local H2-grade evaluations, not standalone complete GHZ
sources.  Their role is precise: the branch hypotheses alone cannot be used
to declare every common core invertible.

## The first colon/Tor obstruction

Let `R=k[g]` in one fixed word/fine/direction-pair grade and let
`M=R^3` be the three-occurrence module.  The undivided response and `E2`
columns span

\[
                         gM.
\]

Consequently the raw colon is

\[
                    (gM:g)/gM=M/gM.                   \tag{4}
\]

After passing to the symmetric quotient by the two standard `E2`
directions, write `u=s/3`.  The exact remaining complex is

\[
                      Ru\xrightarrow{\ g\ }Ru,         \tag{5}
\]

and its primitive colon is

\[
 {((gu):g)\over(gu)}=(R/(g))u.                        \tag{6}
\]

On the fibre `g=0`, (6) is exactly the one-dimensional `Tor_1` class of
(5).  `E3/E4` do not kill it: they are syzygies among the standard `E2`
paths and project to zero on the invariant quotient.

The first missing source datum is therefore completely finite:

> either a degree-one excess/relative generator `tau_C4` with
> `d tau_C4=g*u`, or an independent full-source column proving that the
> class of `u` vanishes in `(im d:g)/im d` in the literal augmented grade.

This is the exact saturation test; it is not another C4 polynomial identity.

## Augmented promotion

The primitive local dual

\[
                         \epsilon=(1,1,1)/3
\]

reads one on `s` and zero on every standard `E2/E3/E4` boundary.  After a
same-grade physical placement, let `mu_j` be its values on the four literal
cap corners.  The theorem `4373ae6` extends it by

```text
target_j = W_j = -mu_j,
ores_j = mu_j,
ridge = -sum_j alpha_j*mu_j,
q = ainc = Eq = 0,
alpha = (-1,1,1,-1).
```

Hence there are exactly two physical outcomes after placement:

1. the colon class lies in the exhaustive physical image and gives the
   protected relative filler/generator; or
2. it lies outside and the displayed extension is an augmented terminal.

The four cap corners here are not the three C4 occurrences or the six pure
tail columns.  The coefficient colon guard is not called a physical terminal
before this placement is supplied.

## Frontier

No full physical grade is retired unconditionally.  The positive formula is
complete once one proves `g*c_g=1` in the exact H2 grade.  Otherwise the
uniform generic C4 branch is the single invariant colon membership test (6).
Coherence is no longer the missing theorem; the first missing source datum is
the full-core saturation/excess generator, followed by the already explicit
augmented terminal alternative.

Run normally, optimized, and isolated/no-site.  The checker records the
frozen ledger digest:

```text
1459d3ba5d21d11802a5f05e0e730d86fd67a06c8e22484b5c062ae111c05aea
```
