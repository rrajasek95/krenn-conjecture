# A rank-one response cap relocates radial curvature to a nonradial transition

## 1. Outcome

Work in one full-nine deleted-pair chart.  Let \(p,q\) be the deleted
sites, let \(q_0\) be the residual quadratic, and let \(p_i,s_j\) be the
two endpoint stars.  On the two missing physical labels

\[
                         M=\{\alpha,\beta\},
\]

write

\[
                         C=(A_{pq})_{M,M}.
\]

Assume only that \(C\ne0\) and retain the four literal full-nine rows

\[
 C_{ij}q_0^{[h]}+p_i s_jq_0^{[h-1]}
       =\delta_{ij}X_i,
 \qquad i,j\in M.                                           \tag{1}
\]

Then there is a rank-one matrix functional

\[
                         \ell=\xi\eta^{\mathsf T}             \tag{2}
\]

which kills \(C\) and has a nonzero diagonal response:

\[
 \beta:=\left(\sum_{i\in M}\xi_i p_i\right)
          \left(\sum_{j\in M}\eta_j s_j\right),
 \qquad
 \beta q_0^{[h-1]}
   =\ell(E_{\alpha\alpha})X_\alpha
      +\ell(E_{\beta\beta})X_\beta\ne0.                    \tag{3}
\]

In particular \(\beta\ne0\), so it has a nonzero literal decorated edge
coefficient.

The key point is that such a coefficient is already a sum of the two
oriented transition curvatures at that edge.  If the coefficient occurs
at residual sites \(x,y\), with local probes \(c,d\), put

\[
\begin{aligned}
 H^\rightarrow_{xy}(c,d)
   &=(A_{px})_{M,c}(A_{qy})_{M,d}^{\mathsf T},\\
 H^\leftarrow_{xy}(c,d)
   &=(A_{py})_{M,d}(A_{qx})_{M,c}^{\mathsf T},\\
 K^\rightarrow_{xy}(c,d)
   &=(A_{xy})_{cd}C-H^\rightarrow_{xy}(c,d),\\
 K^\leftarrow_{xy}(c,d)
   &=(A_{xy})_{cd}C-H^\leftarrow_{xy}(c,d).
                                                               \tag{4}
\end{aligned}
\]

These are not merely formal matrices.  With the repository's
endpoint-ordered block convention, their entries are

\[
\begin{aligned}
 (K^\rightarrow_{xy}(c,d))_{ij}
  &=A_{pq}(i,j)A_{xy}(c,d)
      -A_{px}(i,c)A_{qy}(j,d),\\
 (K^\leftarrow_{xy}(c,d))_{ij}
  &=A_{pq}(i,j)A_{xy}(c,d)
      -A_{py}(i,d)A_{qx}(j,c).                              \tag{4a}
\end{aligned}
\]

The first is the \(y,d\) coefficient of the canonical transition
\(D_{qx}^{\,i}(j,c)\).  The second is the \(x,c\) coefficient of
\(D_{qy}^{\,i}(j,d)\): in that orientation its first product contains
\(A_{yx}(d,c)\), which equals \(A_{xy}(c,d)\) by the physical unordered-edge
symmetry \(A_{yx}=A_{xy}^{\mathsf T}\).  Thus both entries have the literal
repository form \(AU-BF\) on the four physical sites \(p,q,x,y\).

Thus \(K^\rightarrow\) compares the matchings
\(pq\mid xy\) and \(px\mid qy\), while \(K^\leftarrow\) compares
\(pq\mid xy\) and \(py\mid qx\).  If \(b_{xy;c,d}\) is the coefficient of
\(\beta\), then

\[
 \boxed{
 b_{xy;c,d}
   =\ell(H^\rightarrow+H^\leftarrow)
   =-\ell(K^\rightarrow)-\ell(K^\leftarrow).}              \tag{5}
\]

The second equality uses only \(\ell(C)=0\).  Consequently

\[
 b_{xy;c,d}\ne0
 \quad\Longrightarrow\quad
 \ell(K^\rightarrow_{xy}(c,d))\ne0
 \ \hbox{or}\
 \ell(K^\leftarrow_{xy}(c,d))\ne0.                         \tag{6}
\]

The same factorized, source-provenant cap therefore carries a nonzero
literal edge, a nonzero diagonal target, and a nonradial physical
transition curvature at that edge.  No goodness assumption, second chart,
common power cancellation, or support enumeration is needed.  When
\(\operatorname{rank}C=1\), the selector may be chosen with a unary target
\(X_e\).

Applied to the singular common-line packet in
[the carrier-relocation note](full-cap-carrier-resonance-relocation.md),
this gives the exact resolution.  The originally selected curvature
\(K_0=\lambda C\ne0\) cannot be detected by any direct-zero functional.
But (1) forces the rank-one cap to relocate to another coefficient, and
(5) forces at least one of the two transition curvatures at the relocated
coefficient to leave the line \(\mathbb C C\).  Thus the radial line is an
obstruction only to retaining the *original* four-cut, not to obtaining a
factorized curvature-bearing cap.

## 2. Rank-one selection on the missing square

### 2.1 Every nonzero square has a target-active isotropic selector

Choose \(\eta\in(\mathbb C^*)^2\) such that \(C\eta\ne0\), and put

\[
 \xi=((C\eta)_\beta,-(C\eta)_\alpha).
                                                               \tag{7}
\]

Then \(\xi^{\mathsf T}C\eta=0\).  Both coordinates of \(\eta\) are
nonzero and \(\xi\ne0\), so at least one diagonal product
\(\xi_e\eta_e\) is nonzero.  This proves the target-active assertion used
in (2)--(3) for every \(C\ne0\), including an invertible square.

### 2.2 A singular square has a unary selector

Write \(C=ab^{\mathsf T}\), with \(a,b\ne0\).  Choose a nonzero vector
\(\xi\in\ker C^{\mathsf T}=a^\perp\), and choose a label \(e\in M\) with
\(\xi_e\ne0\).  Set

\[
                         \eta=e_e/\xi_e.                    \tag{8}
\]

Then

\[
 \ell(C)=\xi^{\mathsf T}C\eta=0,
 \qquad
 \ell(E_{ff})=\delta_{ef}.                                 \tag{9}
\]

Contracting (1) against \(\ell\) proves (3).  Notice that this is stronger
than merely finding a nonzero binary target: a singular full missing
square always has a unary direct-zero rank-one cap.

There is also a prescribed-label version.  For \(e\in M\), such a unary
rank-one functional exists if and only if

\[
                              C\notin\mathbb C E_{ee}.       \tag{10}
\]

Indeed, if the left null vector has nonzero \(e\)-coordinate, (8) works.
If not, use a right null vector \(\eta\in\ker C\) with \(\eta_e\ne0\) and
take \(\xi=e_e/\eta_e\).  Both null coordinates can vanish only when both
factors \(a,b\) are supported on \(e\), which is exactly
\(C\in\mathbb C E_{ee}\).  Necessity follows by applying any direct-zero
functional to a scalar multiple of \(E_{ee}\).

This recovers the detector criterion in
[the common-label repair](double-zero-common-label-repair.md), now with a
factorization built in.  In particular, every rank-one hook or crossed-cell
repair with unary target \(X_e\) may be fed directly into the relocation
argument below.

## 3. Proof of curvature relocation

Write the two factors of \(\beta\) as

\[
 L=\sum_{i\in M}\xi_i p_i,
 \qquad
 S=\sum_{j\in M}\eta_j s_j.                               \tag{11}
\]

At the decorated edge \((xy;c,d)\), the site-square-zero product gives

\[
\begin{aligned}
 b_{xy;c,d}
  ={}&L_x(c)S_y(d)+L_y(d)S_x(c)\\
  ={}&\ell\!\left(
       (A_{px})_{M,c}(A_{qy})_{M,d}^{\mathsf T}
       +(A_{py})_{M,d}(A_{qx})_{M,c}^{\mathsf T}
       \right),                                             \tag{12}
\end{aligned}
\]

which is the first equality in (5).  From (4),

\[
 K^\rightarrow+K^\leftarrow
   =2(A_{xy})_{cd}C-H^\rightarrow-H^\leftarrow.
\]

Applying \(\ell\) and using \(\ell(C)=0\) proves the second equality in
(5), over any characteristic.

Equation (3) has a nonzero right side, so \(\beta\ne0\) in the decorated
site-square-zero algebra.  Therefore some coefficient (12) is nonzero.
Equation (6) then supplies a transition curvature detected by the same
\(\ell\).  Since \(\ell(C)=0\), a detected curvature cannot belong to
\(\mathbb C C\).  This proves the claim.

Equivalently, suppose every oriented transition curvature at every
decorated residual edge lay in \(\mathbb C C\).  The functional \(\ell\)
would kill both curvatures in (5), hence every coefficient of \(\beta\).
That would make \(\beta=0\), contradicting (3).  This is the short
structural reason the full-nine rows force a nonradial curvature somewhere.

## 4. Sharpness at the selected radial coefficient

At the selected common-line packet, write

\[
 K_0=\lambda C\ne0,
 \qquad
 W_0={u\over h}C+H_0^\rightarrow+H_0^\leftarrow=0.         \tag{13}
\]

Every direct-zero functional, of any matrix rank, satisfies

\[
                         \ell(K_0)=\lambda\ell(C)=0.        \tag{14}
\]

It also has zero cap coefficient at the selected decorated edge:

\[
 \ell(H_0^\rightarrow+H_0^\leftarrow)
   =\ell(W_0)-{u\over h}\ell(C)=0.                          \tag{15}
\]

Thus same-coefficient retention is algebraically impossible in this
packet.  Taking cofactors or differentiating the determinant does not
change this: the rank-one line \((1+t\lambda)C\) stays inside the
determinantal hypersurface, so every determinant polar along that radial
direction vanishes.  A functional with \(\ell(C)\ne0\) detects \(K_0\),
but its completed cap contains the internal term \(\ell(C)q_0/h\) and is
not the required product \(LS\).

Relocation is therefore not a weakness of the argument; it is forced by
(13)--(15).  The full-nine target identity (3) is precisely the additional
global coefficient information missing from the isolated matrix packet.

## 5. Two-chart consequence and remaining gate

For the hook and crossed-cell branches of the common-label repair, both
charts have rank-one direct-zero caps with the same unary target.  Applying
the theorem on each chart gives a nonradial curvature-bearing cap on each
side while preserving that common target label.  The opposite-pure-diagonal
packet remains the exact prescribed-label mismatch already recorded there.

The theorem does not force the two relocated coefficients to use the same
physical residual edge or the same local probes.  If a later subtraction
requires that stronger conclusion, the missing statement is a genuine
two-chart coefficient-incidence lemma: two overlapping unary caps with
the same target must have a common nonzero oriented-transition coefficient,
or their two coefficient arrays must have a nonzero source-level
Koszul/Bianchi pairing.  The separate full-nine target equations imply
nonempty supports, but do not by themselves imply that those supports
intersect.

For the one-chart radial common-line obstruction, however, no further gate
remains: the originally selected radial curvature is discarded and a
nonradial curvature is forced at the cap's relocated edge.

The dependency-free
[checker](../computations/verify_radial_common_line_curvature_relocation.py)
exhausts rank-one \(2\times2\) compressions over small finite fields,
verifies the prescribed unary-selector criterion, and audits (5)--(6).
It also checks the two endpoint-ordered \(AU-BF\) index formulas in
(4a).  It performs no matching-support enumeration.
