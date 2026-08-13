# Anchor faithfulness is functorial only for a pointed source comparison

## Exact answer

The anchor law

\[
 [H]=\Phi^*[h_{\rm Eq}]
       \quad\text{in }X^*/\operatorname {row}(A)       \tag{1}
\]

does follow formally from a correctly **pointed source-algebra** comparison.
It does not follow from the currently specified `k[beta]`-linear chain map
`Phi_beta`, even when every output terminal is retained.

The distinction is structural.  The committed master comparison has type

\[
 \Phi_\beta:k[\beta][\rho]\{K_{\rm Eq}\}
       \longrightarrow C_{\rm phys};                  \tag{2}
\]

it is a chain map on the regular rank-two `K_Eq` orbit.  Equation (1), by
contrast, is a cotangent identity on the complete 171-column response
deformation domain `X`.  A morphism of pointed source presentations would
induce this cotangent map by differentiation.  A chain map on (2) does not
define it.

Checker:
[`verify_h3_anchor_conormal_functoriality_bridge.py`](../computations/verify_h3_anchor_conormal_functoriality_bridge.py).

## 1. The functorial conormal lemma

Let `P` be the physical coefficient algebra, let
`I=(F_1,...,F_m)` be the complete unary-plus-four-response source ideal,
and let `x` be the source point.  Suppose a pointed algebra comparison
`phi^#` carries a central anchor function `a_Eq` to the marked physical
occurrence `f` modulo `I`:

\[
 f-\phi^\#(a_{\rm Eq})=\sum_j c_jF_j.                 \tag{3}
\]

Differentiate (3) at `x`.  Since every `F_j(x)=0`, the product rule gives

\[
 df_x-d\phi_x^*(da_{\rm Eq})
  =\sum_j c_j(x)dF_{j,x}
   +\sum_jF_j(x)dc_{j,x}
  =\sum_j c_j(x)dF_{j,x}.                             \tag{4}

The right side is in `row(A)`.  Thus (4) is exactly (1).  No separate
noncollapse lemma is needed: if `H` is nonzero on a vector in `ker(A)`,
then its transported central readout is nonzero on the image of that vector.

This remains true over `k[beta]`.  If (3) is an integral identity, reduction
at `beta=0`, generic specialization, parity projection, and the Bockstein
all preserve (4).  A comparison constructed only after inverting `beta`
does not supply the special-fibre law.

## 2. What the complete response product rule actually proves

For the literal mixed response coefficient,

\[
                         R=f+G=0,                     \tag{5}
\]

the canonical occurrence graph is

\[
               E=f-u_f=0,\qquad M=G+u_f=0.           \tag{6}

Here `u_f` is the private coordinate of the selected occurrence.  The first
Hasse/product-rule face of (6) gives the positive identity

\[
                         [H]=[du_f].                  \tag{7}

This is source-valid and exact.  It is also the strongest conclusion forced
by the complete response equation.  The central reduced-Eq graph instead
uses the global homogenizing target coordinate:

\[
                         F_0=H_0-u=0,                 \tag{8}
\]

and hence proves only `[dH0]=[du]`.  The occurrence graph and the central Eq
graph share no equation identifying `u_f` with `u` or `H0`.

Consequently the desired anchor law is equivalent to one literal diagonal
bridge:

\[
 \boxed{[d(u_f-u)]=0}
 \quad\text{or, using (8),}\quad
 \boxed{[d(u_f-H_0)]=0}.                              \tag{9}

This is the degree-zero shadow that the off-diagonal response-to-Eq
comparison must carry.

## 3. Sharp complete-source counterguard

Use coordinates `(f,G,u_f,H0,u)` and retain all three graph rows

\[
\begin{aligned}
 dE  &=(1,0,-1,0,0),\\
 dM  &=(0,1, 1,0,0),\\
 dF_0&=(0,0, 0,1,-1).
\end{aligned}                                         \tag{10}

Then

\[
 H=(1,0,0,0,0),\qquad du_f=(0,0,1,0,0),\qquad
 du=(0,0,0,0,1).
\]

We have `H-du_f=dE`, so the private law (7) holds.  But neither
`du_f-du` nor `H-du` is in the span of (10).  The tangent

\[
                         \xi=(1,-1,1,0,0)             \tag{11}

kills all three rows while `H(xi)=1` and `du(xi)=0`.  Thus even the complete
response graph plus the exact central Eq graph does not force (1).

Adjoining either row in (9) immediately repairs the guard:

\[
 H-du=dE+d(u_f-u),
\]

or

\[
 H-du=dE+d(u_f-H_0)+d(H_0-u).
\]

This counterguard is stronger than an abstract commuting-square example:
it keeps the actual response normalization and the actual central Eq
normalization simultaneously.

## 4. Impact on `Phi_beta`

Calling (2) “fully augmented” currently means that its chain image has the
required word/fine/repeated labels and target, residue, anchor, eta/sigma,
`W`, and physical-`q` output readouts.  Those are values of the image of
`K_Eq`.  They do not assert the degree-zero function identity (3), so they
cannot be differentiated into (1).

There are therefore two exact ways to state the master theorem.

1. Strengthen `Phi_beta` to a morphism of pointed source presentations and
   require

   \[
              u_f-\Phi_\beta^*(u)\in I
   \]

   (equivalently `u_f-Phi_beta^*(H0) in I` modulo `F0`).  Then anchor
   faithfulness is automatic by (4), including at `beta=0`.
2. Keep `Phi_beta` as a chain comparison and append the first-order clause
   `[d(u_f-u)]=0` in the complete conormal quotient.  This is sufficient for
   Interface II but does not by itself provide higher Hasse/arc coherence.

The first formulation is preferable if the same comparison is intended to
algebraize the whole Hasse arc.  The second is the shortest theorem needed
only for the current anchor landing.

## 5. Audit of the universal graph / derived-diagonal route

The categorical route has a correct positive core.  The marked anchor is
indeed an actual regular function on the universal coefficient source:

\[
 f=p_1[0,1]s_1[1,1]q_{23}[0,0]q_{45}[0,0],
 \qquad H=df_x.                                      \tag{12}
\]

Thus there is no obstruction at the first proposed step.  Its graph
`Gamma_f`, with coordinate `u_f=f`, is canonically isomorphic to the source,
and the cotangent complex is functorial under bar/principal-parts resolution.

The nonformal step is the derived base change at the diagonal.  Pulling
`Gamma_f` back along `Delta:u_f=u` adjoins the Koszul relation

\[
                         u_f-u=0.                    \tag{13}

On that derived fibre, cotangent naturality proves (1), exactly as hoped.
But (13) is also exactly the missing class (9).  In the guard (10), adjoining
`d(u_f-u)` raises the conormal rank from three to four and removes the
tangent (11).  Hence the derived diagonal fibre is not automatically a new
presentation of the old physical source: it is a different derived
intersection whose relative conormal is the desired theorem.

Equivariance does not remove this issue.  A selected occurrence is not
invariant under the full site/colour action.  For an occurrence orbit
`{u_mu}`, the invariant map to a trivial global target sees the aggregate
or average.  The marked-minus-average vector lies in the nonzero
augmentation-zero permutation module.  A fully equivariant graph therefore
needs either the whole occurrence orbit plus a stabilizer section, or a
bar contraction of this augmentation-zero part.  Declaring that contraction
physical is precisely the occurrence projector/descent problem; it is not
implied by equivariance of the abstract bar resolution.

There is a second, independent descent check.  The existing terminal theorem
is formulated on literal physical matching, `ainc`, common-`q`, word/fine/
repeated, eta/sigma, and protected rows.  The contractible graph presentation
alone preserves tangent and obstruction spaces, but its private coordinate
has no canonical six-term or repeated-`q` readout.  The diagonal base change
actually changes the tangent space.  Therefore ordinary derived
quasi-isomorphism is not enough: the route must produce an **augmented**
quasi-isomorphism carrying all these physical readouts.  Once that is proved,
the existing generator/separator alternative is invariant and the
categorical route closes Interface II.  Without it, the route proves the
anchor law only after replacing the physical source by the desired fibre.

The exact categorical closure theorem is consequently:

> Construct the `G`-equivariant pointed graph/bar/PP comparison over
> `k[beta]`, together with a homotopy-cartesian lift to `u_f=u`, and prove
> that its augmentation to the original physical source is a
> word/fine/repeated- and terminal-preserving quasi-isomorphism.

Its cotangent shadow is just (9).  For the shortest proof of the current
landing, proving the shadow directly is enough; for higher Hasse-arc
algebraization, the full categorical statement is the right target.

## Scope

This proves the conormal functoriality lemma, identifies the exact positive
private occurrence law supplied by the complete response product rule, and
freezes the first private/global diagonal counterguard.  It does not
construct the pointed algebra comparison or the bridge (9).

Run:

```text
python3 computations/verify_h3_anchor_conormal_functoriality_bridge.py
python3 -O computations/verify_h3_anchor_conormal_functoriality_bridge.py
python3 -I -S computations/verify_h3_anchor_conormal_functoriality_bridge.py
```

Frozen ledger SHA-256:

```text
d12c576a1bad5a3ad25974fb35580ebaa703bb5150e4c2b076c3cbbf8f957df4
```
