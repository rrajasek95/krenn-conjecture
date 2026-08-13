# The placed Cartan prism carries physical `q` exactly through an augmented comparison

## Result

In the canonical faces-`(3,5)`, `h=3` repeated grade, the physical readout is
already defined on the complete relative source domain:

\[
                 q_{h=3}=\sum_{i=1}^{6}m_i-\operatorname{ainc}.       \tag{1}
\]

For a placed Cartan prism in another component grade, the exact minimal
hypothesis for `q` itself is an augmented protected chain comparison

\[
              \Phi:L_{\rm placed}\longrightarrow L_{h=3},\qquad
              J_{h=3}\Phi=A J_{\rm placed},                       \tag{2}
\]

on the **whole** placed source domain, together with the one-row identity

\[
                         q_{\rm placed}=q_{h=3}\Phi.               \tag{3}
\]

A source-valid physical realization of (3) identifies its two constituent
rows:

\[
 \sum_i m_i^{\rm placed}=(\sum_i m_i^{h=3})\Phi,\qquad
 \operatorname{ainc}^{\rm placed}
    =\operatorname{ainc}^{h=3}\Phi.                               \tag{4}
\]

It is not necessary to identify the six selected rows one by one: opposite
changes of two rows preserve their aggregate and hence preserve physical
`q`.  Individual row pullbacks are a convenient stronger labelled
criterion, not the minimal theorem.

For the **complete terminal packet**, rather than `q` alone, one also needs
the independent residue/ridge condition

\[
                        T=wT=sT=swT,                               \tag{5}
\]

with `dT=0` and `T=1` in the terminal quotient for fixed eta/sigma
normalization.  The `pq` and `xv` halves of `-dOmega_v` must remain separate
shifted labels, and `Omega`, eta, and sigma must be relabelled together.

Then

\[
 q_{\rm placed}=q_{h=3}\Phi
     =\sum_i m_i^{\rm placed}-\operatorname{ainc}^{\rm placed}   \tag{6}
\]

is the physical readout on the complete protected kernel.  Equation (2)
sends protected-kernel classes to protected-kernel classes, and (3)
preserves their numerical physical values.  The existing generator,
whole-kernel Fredholm, and terminal-safe cancellation theorems therefore
apply without a new branch.

Checker:
[`verify_dark_cartan_physical_q_transport_gate.py`](../computations/verify_dark_cartan_physical_q_transport_gate.py).

## The tail and row conditions are genuinely different

Commit `83151bf` proves that (5) is the sharp criterion for multiplication by
`T` to commute with the four-corner Cartan difference.  It also proves that
an ordinary common tail cannot homogenize the two site degrees in

\[
                 -d\Omega_v=-da+dt+db-du.                         \tag{7}
\]

The normalized shifted-Kähler condition transports the ordinary residue and
eta/sigma packet.  It says nothing about the six private matching rows or
physical anchor incidence in (1).  Those are independent rows of the
augmented source presentation.  Thus (5), even with `dT=0` and terminal
value one, does not imply (3).  Conversely, (3) defines physical `q` without
using eta/sigma.  The two conditions are combined only when the proof needs
the entire augmented terminal packet.

This distinction prevents a category error: a critical-component charge
detects a selected occurrence of the placed Cartan prism, whereas physical
`q` is a covector on the entire relative correction domain.  They have
different domains and meanings and are never substituted for one another.

## Minimal exact no-go guard

Let

\[
 J_0=(1\;0),\qquad G=(1,0),\qquad k=(0,1)\in\ker J_0.              \tag{8}
\]

Take the identity tail, so all four tail values are one, `dT=0`, and its
terminal value is one.  Let the known six-matching sum be
`m=(1,0)`.  The two anchor-incidence extensions

\[
 a_0=(0,0),\qquad a_1=(0,-1)                                     \tag{9}
\]

agree on the placed Cartan coordinate.  Consequently

\[
 q_0=m-a_0=(1,0),\qquad q_1=m-a_1=(1,1)                          \tag{10}
\]

also agree on `G`.  But

\[
 q_0(k)=0,\qquad q_1(k)=1.                                      \tag{11}
\]

The first readout kills the whole kernel and factors through `J_0`, giving
the Fredholm separator.  The second normalizes `k` to the physical
generator.  Both completions have the same placed coordinate and the same
strongest ordinary-tail data.  Only the missing anchor row in (4) decides
between them.

Dimension two is minimal: one needs one placed direction and one independent
protected-kernel direction whose readout is not fixed by placement.  A
separate component charge, represented in the checker by `chi=(2,1)`, may
see either direction but does not choose either physical extension in (10).

## What transports uniformly once (2)--(5) hold

The uniform consequences are exactly:

1. the oriented four-corner residue and covariantly labelled eta/sigma
   ridge;
2. membership in the complete protected kernel;
3. the physical six-term/anchor value;
4. normalization of a nonzero value to the existing relative generator;
5. the exhaustive whole-kernel generator/Fredholm alternative; and
6. cancellation of a unit kernel line when its physical `q` value is zero.

What does not transport from component placement alone is the value of
`ainc`, hence the restriction of `q` to an unseen protected-kernel line.

## Frontier

The canonical `h=3` branch needs no new terminal construction: take
`Phi=id`.  For a noncanonical placed component, the remaining object is not
another component charge or an ordinary common multiplier.  It is the
labelled shifted-Kähler/anchor comparison (2)--(4) on the complete source
domain.  Constructing it immediately feeds commits `941f4b6` and `00db7ee`;
failure to construct (4) leaves the two exact outcomes (10)--(11)
indistinguishable.

## Verification

Run:

```text
python3 computations/verify_dark_cartan_physical_q_transport_gate.py
python3 -O computations/verify_dark_cartan_physical_q_transport_gate.py
python3 -I -S computations/verify_dark_cartan_physical_q_transport_gate.py
```

Frozen ledger SHA-256:

```text
cdaa9ccb732794fc2dd1a5e45983f0e9716245948e29a0c1a0252f90e5a51252
```
