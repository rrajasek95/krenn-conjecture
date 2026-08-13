# All occurrences reduce the anchor bridge to one centered descent

## Exact outcome

The exact unscaled bridge

\[
                         [d(u_f-u)]=0                 \tag{1}
\]

is stronger than the all-occurrence algebra supplies.  For the `N=90`
literal occurrences, the full formal occurrence simplex plus target
normalization instead gives

\[
                         \boxed{90[du_f]=[du]}.        \tag{2}
\]

This is enough for Interface II: anchor landing uses nonzero visibility, so
the nonzero unit `90` is harmless in characteristic zero.  The remaining
physical problem is one centered occurrence class, not the target-trivial
class and not the unscaled difference (1).

Checker:
[`verify_h3_scaled_occurrence_anchor_bridge_alternative.py`](../computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py).

## 1. Integral all-occurrence identity

Let `z_M` be the 90 occurrence-graph coordinates and let `u` be the global
target coordinate.  Put

\[
 B=\sum_Mz_M-u,
 \qquad c_f=90z_f-\sum_Mz_M.                          \tag{3}
\]

The 89 star edges `z_f-z_M`, `M!=f`, form an integral saturated basis of
the occurrence augmentation ideal, and

\[
 c_f=\sum_{M\ne f}(z_f-z_M).                          \tag{4}
\]

Consequently

\[
                    90z_f-u=c_f+B.                   \tag{5}
\]

After differentiation, (5) is (2).  Equivalently, the occurrence simplex
identifies the marked graph coordinate with the **average** target:

\[
                         [du_f]=\frac1{90}[du].        \tag{6}
\]

This coefficient is not an artifact.  In the target-augmented module, the
primitive covector

\[
                 \lambda=(1,\ldots,1;90)              \tag{7}
\]

kills every occurrence edge and `B`, but

\[
                 \lambda(z_f-u)=1-90=-89.             \tag{8}
\]

Thus `z_f-u` is not in the formal image.  By contrast,
`lambda(90z_f-u)=0`, and (5) supplies its explicit boundary.

## 2. Why the scaled law closes anchor visibility

The anchor-faithful proof only needs a unit-scaled row congruence.  If

\[
 90H-h_{\rm Eq}\Phi\in\operatorname {row}(A),         \tag{9}
\]

then for every `xi in ker(A)`,

\[
 h_{\rm Eq}(\Phi\xi)=90H(\xi).                       \tag{10}
\]

Hence `H(xi)!=0` still gives an `h_Eq`-visible central kernel.  There is no
need to rescale the entire odd/even comparison or any of its fixed output
packets; (9) is a statement about the anchor readout only.  Thus (2), once
physically descended, is exactly as strong as (1) for the accessibility
landing.

## 3. Formal bars are not yet physical bars

Equation (4) is a boundary in the free occurrence simplex.  The committed
physical group/bar theorem makes the crucial distinction: a complete
physical source row is an orbit sum in the occurrence/matching factor.
Target-preserving site bars and paired Cartan/Weyl prisms made from such a
row remain in the trivial occurrence representation.  They do not realize
the star edges in (4).

The raw coefficient Euler projector does isolate `f`, but it is not a
source operation: at the trapped source the complete mixed response is zero
while `f` is nonzero, so the projector has scalar zero-face `f(x)`.  Every
target-compatible diagonal Euler field sees the common character of all 90
occurrences and returns the aggregate `3R`, not `df`.

Therefore the exact positive content of all-occurrence algebra is a
compression:

```text
private/global anchor bridge
        |
        +-- symmetric normal B = sum z_M-u       already central Eq
        |
        `-- centered star c_f = 90z_f-sum z_M   one physical descent left.
```

## 4. Maximum-anchor/minimum-support does not force the class to vanish

Extremal selection alone cannot turn an anchor-changing tangent into a
support deletion.  The smooth torus curve

\[
                          xy=1                       \tag{11}
\]

with marked anchor function `f=x` is the sharp local guard.  At `(1,1)`,

\[
 d(xy-1)=(1,1),\qquad \xi=(1,-1),\qquad df(\xi)=1.   \tag{12}
\]

Along the entire curve both scalar coordinates remain occupied and `f`
remains nonzero.  Thus occupied support and active-anchor count are
constant, although the marked anchor differential is visible.  This is an
exact guard to the extremal-selection inference, not a standalone Krenn
source counterexample.

To use extremality positively one needs more: algebraize the tangent inside
the complete source and prove the resulting curve meets a boundary stratum
with lower support or more protected anchors.  Smoothness or first-order
visibility alone does not imply that global line-hitting statement.

## 5. The sharp physical alternative

Let `C(Phi_beta)` be the complete augmented physical comparison cone,
retaining word/fine/repeated degree, target, labelled residue, anchor
incidence, physical six-term `q`, eta/sigma, and `W`.  The single new
candidate is

\[
             \gamma_f=90,du_f-\sum_Mdu_M,            \tag{13}
\]

or, after adding the already central normal `B`,

\[
                         90,du_f-du.                 \tag{14}
\]

Exact Fredholm duality gives only two outcomes once (13) is actually placed
in that complete physical cone:

1. it is a physical comparison boundary; then (9) holds and Interface II
   closes through the central protected-kernel alternative;
2. a complete augmented cokernel covector detects it.

The second covector is a terminal only if it is typed through the literal
physical readouts of the cone.  A covector on the free occurrence simplex,
including (7), is not automatically a Fredholm terminal.  This is why the
physical descent-or-terminal clause cannot be replaced by formal group
homology or maximum-anchor selection.

## Minimal theorem for the master comparison

> **Centered occurrence descent-or-terminal.** Promote
> `c_f=90du_f-sum_Mdu_M` to the complete augmented physical comparison cone.
> Either it is a physical boundary, or its first nonzero augmented cokernel
> class is detected by an already accepted physical exchange,
> relative-generator, or Fredholm readout.

In the boundary arm, adding `B=sum_Mdu_M-du` proves the sufficient scaled
anchor law (9).  In the dual arm, the master comparison terminates directly.
This is the shortest exact Interface-II clause to append to `Phi_beta`.

## Scope

This proves the integral all-occurrence identity, the primitive obstruction
to the unscaled law, sufficiency of the scaled law, and a sharp extremal-
selection guard.  It does not physically realize the centered star class or
type an arbitrary occurrence-simplex dual as a terminal.

Run:

```text
python3 computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py
python3 -O computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py
python3 -I -S computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py
```

Frozen ledger SHA-256:

```text
91b63b6f603bcf6fc98854d3ae4cbe00b21d9536028a98c6f265d935ad1e0afb
```
