# Interface II needs an anchor-faithful central comparison, not another Hall case

## Exact answer

Let `X` be the complete unary-plus-four-response deformation domain and
let

\[
 A:X\longrightarrow Y,\qquad H,\Lambda\in X^*.
\]

The full-q Interface-II alternative leaves exactly

\[
 \Lambda\in\operatorname {row}(A),\qquad
 H\notin\operatorname {row}(A).                       \tag{1}
\]

A bare physical central cell

\[
                         dK_{\rm Eq}=-E               \tag{2}
\]

does **not** exclude (1).  Equation (2) is a boundary in the central Eq
output complex; it contains no map on `X` and hence changes neither row-space
membership in (1).  The direct sum of the frozen three-coordinate guard

```text
A      = (1,0,0),
H      = (0,1,0),
Lambda = (1,0,0)
```

with the exact one-dimensional complex `K -> E` retains (1) literally.

The central comparison closes (1) precisely when it is **anchor-faithful**.
Write its protected square as

\[
 \begin{array}{ccc}
 X&\xrightarrow{\Phi}&C_{\rm Eq}\\
 A\downarrow&&\downarrow D\\
 Y&\xrightarrow{B}&Z,
 \end{array}
 \qquad D\Phi=BA,                                    \tag{3}
\]

and let `h_Eq` be the physically typed central readout.  The one load-bearing
row law is

\[
 \boxed{
 H-h_{\rm Eq}\Phi\in\operatorname {row}(A)
 }
 \quad\Longleftrightarrow\quad
 [H]=\Phi^*[h_{\rm Eq}]
       \text{ in }X^*/\operatorname {row}(A).         \tag{4}
\]

Because `H` is nonzero modulo `row(A)`, exact duality gives
`xi in ker(A)` with `H(xi)!=0`.  Equations (3)--(4) give

\[
 D\Phi(\xi)=0,
 \qquad h_{\rm Eq}(\Phi(\xi))=H(\xi)\ne0.            \tag{5}
\]

Thus the Interface-II survivor is a nonzero central protected-kernel class.
If the assumed central comparison includes its protected-kernel
generator/separator alternative, that alternative consumes the survivor.
Conversely, if the central complex has no such visible kernel, (4) forces
`H in row(A)`, contradicting (1).

Checker:
[`verify_h3_interface_ii_anchor_faithful_central_comparison.py`](../computations/verify_h3_interface_ii_anchor_faithful_central_comparison.py).

## What “central physical comparison” must mean

There are two different hypotheses in the current map.

1. A physical cell with boundary `-E` closes the final coordinate **after**
   the response packet has been compared to the reduced-Eq packet.
2. A source-valid off-diagonal comparison (3)--(4) performs that comparison
   and transports the anchor differential.

If “central physical comparison” includes both clauses, no separate
Interface-II theorem remains.  If it means only the physical cell (2), then
(4) is still a genuinely separate Hasse-algebraization/anchor-visibility
lemma.  The two apparent obligations—algebraizing the Hasse response and
proving anchor visibility—are the same quotient identity (4), not two
successive lemmas.

The comparison square (3) alone is insufficient.  It can collapse the
marked `H` direction: take

\[
 \Phi=\begin{pmatrix}1&0&0\\0&0&0\end{pmatrix},\qquad
 D=(1,0),\qquad B=(1).
\]

Then `D Phi = B A`, but `h_Eq Phi=0`; the vector `(0,1,0)` is still read by
`H` and is invisible centrally.  Hence noncollapse is not an additional
condition once (4) is proved—it follows from (4)—but it cannot be inferred
from a commuting protected square.

## Why the current central assembly does not already prove (4)

The conditional central-Eq checker sets the complete response symbol equal
to the required symbol and then inserts the sole residual by

```text
symbol_required = symbol_actual
residual[EQ] = 1
```

It correctly proves that `K_Eq` closes Interface II **conditional on the
off-diagonal comparison**, but it has no `X`, `A`, `H`, or `Phi` data and
therefore cannot establish (4).

The pinned Hessian audit identifies the same boundary sharply.  The
diagonal principal-parts/Hasse symbol lands in response endpoint-tail grade;
its projection to the independently labelled pure-Eq conormal is zero.
The transpose closes the sixteen-term associated symbol, and the `theta`
groupoid closes repeated-grade holonomy, but `K_Eq` cannot be the grade
arrow because it has no private matching-feature component.  What remains
is exactly the source-labelled **off-diagonal response-to-Eq mapping-cone
comparison**.

## Shortest remaining theorem

> Construct one physical off-diagonal comparison `Phi` in the common word,
> fine, repeated, and endpoint grade, with the complete unary/four-response
> `q` columns and protected target/residue/eta/sigma rows, such that
> `D Phi=B A` and `[H]=Phi^*[h_Eq]` modulo `row(A)`.

That theorem sends (1) directly to the already central
generator/separator alternative.  It requires no Hall reselection, no new
six-term factorization theorem, and no second anchor-noncollapse lemma.

## Scope and verification

This is an exact linear-algebra reduction, an independent-direct-sum
counterguard to the bare-central-cell claim, and an audit of the currently
pinned source maps.  It does not construct `Phi` or identify the diagonal
Hasse symbol with the reduced-Eq row.

Run:

```text
python3 computations/verify_h3_interface_ii_anchor_faithful_central_comparison.py
python3 -O computations/verify_h3_interface_ii_anchor_faithful_central_comparison.py
python3 -I -S computations/verify_h3_interface_ii_anchor_faithful_central_comparison.py
```

Frozen ledger SHA-256:

```text
153729f4238ba144abcac2e6ce93418798fb4869480a06e899a259f0c1d6f9bb
```
