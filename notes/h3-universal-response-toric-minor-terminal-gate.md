# The universal response shear first meets a physical toric conormal

## Exact result

In one endpoint/matching rectangle of the response head/word `11:110000`,
put

\[
\begin{array}{ll}
x=u_{(0,1;24|35)},&y=u_{(1,0;23|45)},\\
z=u_{(0,1;23|45)},&w=u_{(1,0;24|35)}.
\end{array}
\]

The physical factorization

\[
 e_{01}=p_0s_1,\quad e_{10}=p_1s_0,\quad
 q_A=q_{23}q_{45},\quad q_B=q_{24}q_{35}
\]

gives

\[
 (x,y,z,w)=(e_{01}q_B,e_{10}q_A,e_{01}q_A,e_{10}q_B)
\]
and hence the literal same-grade toric relation

\[
                         F=xy-zw=0.                  \tag{1}
\]

Its conormal annihilates every physical factor tangent.  On the constant
four-occurrence shear `v=(1,1,1,1)`, however,

\[
 \boxed{dF(v)=(p_1s_0-p_0s_1)
                    (q_{23}q_{45}-q_{24}q_{35}).}    \tag{2}
\]

Thus a nonzero value of (2) excludes the proposed shear as an honest
first-order physical-source tangent.  For a higher KS/principal-parts
comparison it is instead a compulsory proper face: the total cell must
cancel (2), or its fully augmented conormal must be promoted to a physical
terminal.

Checker:
[`verify_h3_universal_response_toric_minor_terminal_gate.py`](../computations/verify_h3_universal_response_toric_minor_terminal_gate.py).

## This is not the scalar KS normal

Normalize the marked occurrence

\[
                    f=(p_0s_1)(q_{23}q_{45})=1.
\]

The universal response family has scalar face `90f=90`.  Keeping that face
fixed, exact examples give toric values

```text
(e10,qB)=(1,0)  ->  0,
(e10,qB)=(0,0)  -> -1,
(e10,qB)=(3,0)  ->  2.
```

So (2) and `90f` are independent proper faces.  Cancelling the cap/scalar
normal does not cancel the toric conormal, and conversely a toric-dark chart
does not remove the scalar face.

## What the two factors do prove

The factorization is useful and physically sharper than an abstract
occurrence covector.

- `p1*s0-p0*s1` is the endpoint-odd orientation/KS line.
- `q23*q45-q24*q35` is the evaluated alternating residual-`C4` or
  common-tail Fitting factor.
- Both live in one response head and one output word, and the two products
  in (1) have the same fine multidegree.

Consequently (2) supplies exactly the block-local, decomposable curvature
*shape* requested by the trapped-Hessian shortcut.  It is not merely a
rank-five covector in a free occurrence permutation module.

It nevertheless does not finish the active landing.  The four displayed
tail cells have decoration `00`; (2) supplies no nonzero offdiagonal
physical cell `A_vu^{ba}`, `a!=b`, to which the target-augmented private-site
identity applies.  The endpoint wedge is an orientation line, not by itself
a new physical deleted-star head.

There is also no pure-support conclusion.  With the same nonzero local data

```text
e01=1, e10=0, qA=1, qB=2,
```

one literal completion takes every diagonal edge nonzero (`q35=2`, all
others one), so all fifteen `K6` matchings occur and the deleted-star ranks
on the adjacent residual edges `23,24` are `(3,3)`.  A second keeps exactly
the colour-zero cells `23,45,24,35,05,14` nonzero.  Despite the same four
local values, its only nonzero pure-zero matching is `05|14|23`; hence `23`
is a literal colour-zero coloop and the ranks are `(2,3)`.  Take the other
two colour supports dense in both completions.  These are exact
support/readout completions, not asserted full GHZ sources.  They prove that
toric brightness alone does not choose the four-good or coloop branch.

## Shortest physical alternative

The source-valid statement now needed is narrower:

> **Protected toric-face landing.** Construct the endpoint/matching-natural
> KS/PP comparison so that every relation (1) has its product-rule conormal
> (2) cancelled in the same word/fine/repeated grade.  Retain target,
> `ainc/q`, `W`, shifted ridge, eta and sigma.  If the first conormal cannot
> be cancelled, extend it through that complete augmented map as an accepted
> exchange, relative-generator or Fredholm terminal.

On the nonzero arm, the residual factor is already the named typed
`C4`/Fitting interface and the endpoint factor is already the endpoint-odd
interface.  A further theorem must supply an offdiagonal private-site
reference or the complete pure-support deleted-star/coloop data before the
coloop-or-four-good theorem can be invoked.

## Scope

This is exact for the canonical four-occurrence rectangle at `h=3`.  It
proves the toric identity, its physical conormal, the shear factorization,
independence from `90f`, and the two pure-support completions.  It does not
claim a complete GHZ counterexample, a four-good landing, or a fully typed
terminal.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
82e6fd5666464fa1c49e6d518a54e414248112465f558158ab996070a43bd336
```
