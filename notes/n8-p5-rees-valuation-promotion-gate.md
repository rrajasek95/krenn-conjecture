# The P5 contact bounds do not yet promote by Rees valuations

## Exact valuation obstruction

Work in the smallest exact associated chart behind the exceptional-torus
contact calculation: the 56-variable second-lift tangent ring, with its 39
literal quadratic obstruction forms $I_2$.  In P5 coordinates put

\[
 q_0=z_{12},\ q_1=z_{13},\ q_2=z_{14},\ q_3=z_{15}-z_{16},
 \quad q_4=z_{17},\ldots,q_{10}=z_{23}.
\]

Define the centered discrete monomial valuation $v$ by

\[
 v(q_i)=8\quad(0\le i\le10),
 \qquad v(z_j)=1
\]

on the other 45 linear coordinates.  The coordinate change is invertible
and all weights are positive with gcd one, so this is a divisorial monomial
valuation centered at the tangent origin.

Exact substitution into all 39 obstruction quadrics gives

\[
                         v(I_2)=9.                    \tag{1}
\]

The nine cubic members of the frozen 48-element tangent standard basis have
orders $(10,10,10,17,17,17,17,17,17)$, so none lowers (1).  On the other
hand the first unresolved pure residual is

\[
 R=z_{16}^2z_{41}(z_{44}+z_{45})(z_{53}-z_{51})
       (z_9z_{25}-z_{11}z_{46}),
\]

and

\[
                         v(R)=7<9=v(I_2).              \tag{2}
\]

Thus $R\notin\overline{I_2}$.  By the Rees-valuation criterion, at least
one Rees valuation of $I_2$ violates the required integral-closure
inequality.  This is stronger than saying that a bounded reduction stopped:
the committed second-lift/contact data themselves do not support the desired
promotion.

There is also a literal arc over `Q[[t]]`.  Give every new coordinate token
`w_i` coefficient `i+2`.  Thus `(q0,q1,q2,q3,q4,...,q10)` has leading
coefficients `(14,15,16,58,19,...,25)` at order eight, while every
complementary coordinate has coefficient `i+2` at order one (so
`z15=18t+58t^8`).  All 39 obstruction initials are nonzero at order
nine; the coefficient of $R$ at order seven is
$-847372104$.  Its leading ambient tangent vector has 110 nonzero source
coordinates on 20 physical edges.  Hence this arc does not directly supply
the single-edge response required by the intrinsic cap theorem; no claim is
made that a further source-faithful contraction cannot do so.

## Why the later strict-seven row matters

The dense generic-$L$ strict-seven initial chart contains an additional
source row $G$.  It is independent of the eleven newest transverse pivot
variables and is monic in the third bend $r$:

\[
                         \partial G/\partial r=-1.
\]

The pivot block is $bI_{11}$, where $b=z_{44}+z_{45}$ is localized.
Over the dense-branch coefficient field, a triangular coordinate change
therefore identifies the localized initial ideal with

\[
                         (y_1,\ldots,y_{11},r).
\]

This coordinate ideal is integrally closed.  Its blow-up has one exceptional
divisor, so its only Rees order gives value one to each displayed generator.
The committed source identity

\[
 H_0^{(10)}=UG,
 \qquad
 U=z_{11}z_{16}^2z_{41}b(z_{53}-z_{51}),
\]

therefore satisfies every Rees-valuation inequality on this finite initial
chart.  In other words, the later row $G$ genuinely repairs the early
valuation obstruction; the contact estimate alone did not.

## Proof impact

This route does **not** yet construct the source-valid clean cap or
annihilator required by `SP-CLEAN-BRIDGE`.  The repaired calculation is an
initial-form theorem, not a presentation of the full completed local mixed
ideal.  The missing object is still the finite iterated source-chart map
from all 252 translated coordinates (retaining the 196 smooth-normal
remainders), or an all-orders filtered-Rees standard-basis theorem.  Until
that object exists, Rees valuations of the triangular initial ideal are not
the Rees valuations of the relevant full source ideal.

The conclusion is therefore sharp:

* the already committed contact bounds cannot be promoted directly, by
  (2);
* the checked strict-seven initial does satisfy the valuation test;
* no full source-valid clean/annihilator class follows from either fact.

## Reproduction

```bash
.venv/bin/python computations/verify_n8_p5_rees_valuation_promotion_gate.py
.venv/bin/python -O computations/verify_n8_p5_rees_valuation_promotion_gate.py
```
