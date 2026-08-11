# A physical zero-target two-chart packet retains the terminal scalar

## Outcome

At (h=3), complete literal full-nine rows and their automatic adjacent
two-chart overlap do **not** kill the terminal response scalar without the
nonzero diagonal GHZ anchors.  There is one actual eight-site decorated
edge array (A) such that

\[
                         H_8(A)=0
\]

coefficientwise on all (3^8) words.  Both endpoint-star triples in the
pair charts (67) and (60) have rank three, and the physical curvature
on sites ((6,7,0,3)), with labels ((0,1,2,2)), is

\[
                         \kappa=-19\ne0.
\]

Nevertheless the selected (67)-row has direct scalar
(alpha=A_{67}(0,1)=1) and exact response layers

\[
             (Q_0,Q_1,Q_2,Q_3)=(-36,36,-18,6).
\]

Hence every through-Hamming-two response equation vanishes,

\[
 \alpha Q_0+Q_1=0,qquad
 \alpha Q_1+2Q_2=0,qquad
 \alpha Q_2+3Q_3=0,
\]

while

\[
                         \boxed{\chi=\alpha Q_2+Q_3=-12.}
\]

This upgrades the abstract normal-plane separator of commit `87304b5` to
a single physical block array with complete coefficient rows and adjacent
source provenance.  It is not a Krenn counterexample: its target is zero,
not (Delta_{8,3}).  Its exact force is that a universal contraction made
only from target-zero full-nine/overlap identities cannot kill the terminal
class.  A positive rootless theorem must use the nonzero diagonal anchor
equations source-relatively; duplicating the selected chart, Segre exchange,
curvature, and ordinary overlap are insufficient.

## 1. The residual rank-one response pencil

Split the residual sites as

\[
 U=\{0,1,2\},\qquad V=\{3,4,5\}.
\]

On physical colour (2), take the (U\times V) internal matrix

\[
 B=\begin{pmatrix}
 -18&14&0\\
 0&-1&-2\\
 0&0&-2
 \end{pmatrix}.
\]

Let the selected endpoint forms be the all-ones forms on the two shores,
so their response (R=p_0s_1) is the all-ones (U\times V) matrix.
Then

\[
 \operatorname {per}(B+t\mathbf1\mathbf1^{\mathsf T})
       =-36+36t-18t^2+6t^3.                       \tag{1}
\]

Equation (1) gives the displayed (Q_j)'s and realizes six times the
primitive Fredholm vector
((-6,6,-3,1)).  In the repeated-star normal plane,

\[
 A=4Q_2=-72,qquad B_{\rm normal}=6Q_3=36.
\]

Thus the literal Hamming-two and clean functionals read

\[
 {\alpha\over4}A+{1\over2}B_{\rm normal}=0,
 \qquad
 {\alpha\over4}A+{1\over6}B_{\rm normal}=-12.       \tag{2}
\]

The missing row is exactly the independent normal-sum weighting in (2),
or equivalently (Q_3=0).

## 2. Completing all nine homogeneous rows

Use endpoint-star matrices, with rows indexed by (U) and (V),

\[
 P=\begin{pmatrix}1&1&0\\1&0&1\\1&0&0\end{pmatrix},
 \qquad
 S=\begin{pmatrix}1&1&0\\0&1&1\\0&1&0\end{pmatrix}.
\]

The selected columns are still (P_0=S_1=(1,1,1)^{\mathsf T}), and both
matrices are invertible.  The permanental adjugate of (B) is

\[
 C(B)=\begin{pmatrix}
 2&0&0\\-28&36&0\\-28&36&18
 \end{pmatrix}.
\]

Since (operatorname {per}B=-36), set

\[
                         d={1\over36}P^{\mathsf T}C(B)S. \tag{3}
\]

Then (d_{01}=1) and every one of the nine endpoint rows is zero:

\[
        d_{ij}\operatorname {per}B+P_i^{\mathsf T}C(B)S_j=0. \tag{4}
\]

The sign in (4) is encoded by (operatorname {per}B=-36); equivalently
(-36d+P^{\mathsf T}CS=0).
All displayed cells have residual colour (2), so (4) is already the
complete all-word identity, not only one scalar coefficient.

To make the second endpoint star of the adjacent (60)-chart full rank,
adjoin on the internal edge (01) the invertible block

\[
 T=\begin{pmatrix}1&0&0\\0&0&1\\0&1&0\end{pmatrix},
 \qquad T_{22}=0.                                      \tag{5}
\]

No internal (V\!-!V) edge is present.  Therefore a perfect matching
using (5) is shore-imbalanced and vanishes, both in the direct sector and
after either endpoint response.  The block (5) changes neither (1) nor
(4), but supplies three independent labelled rows at endpoint (0).

The checker enumerates all (105) physical matchings on every one of the
(3^8) words and verifies (H_8(A)=0).  It separately re-expands all
nine rows on each of the (67)- and (60)-charts.  Thus their connection,
normal, curvature, and Bianchi overlap identities are those of one common
physical source array, rather than independently assigned tensors.

## 3. Scope and theorem consequence

The packet proves the following exact negative statement:

> No target-free, source-labelled identity generated universally by the
> complete pair rows and their automatic adjacent two-chart overlap can
> imply (chi=0), even after localizing a nonzero curvature and retaining
> rank-three endpoint stars.

It does not test an identity which uses the nonzero values of two or three
diagonal GHZ anchors.  Those rows fail on this packet by exactly their
target terms.  Consequently this is a counterguard to an anchor-blind
overlap contraction, not to the open rootless Component III theorem.

Combined with the endpoint fine-degree theorem of `87304b5`, the remaining
positive interface is now sharp: one needs a grade-changing comparison
whose anchor contribution survives while its target and ordinary residue
cancel.  Another homogeneous Hamming-two tag, Segre switch, or universal
two-chart overlap identity cannot provide it.

Run

```text
python3 computations/verify_h3_two_chart_terminal_zero_target_counterguard.py
python3 -O computations/verify_h3_two_chart_terminal_zero_target_counterguard.py
python3 -I -S computations/verify_h3_two_chart_terminal_zero_target_counterguard.py
```

The checker uses exact rational arithmetic and freezes the complete ledger.
