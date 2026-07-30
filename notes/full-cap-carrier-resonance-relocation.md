# Full-nine response coefficients relocate a resonant cap edge

## 1. Outcome

Work on the nonzero-cross-block, double-zero branch on which the completed
missing square is valid. Thus

\[
 M=\{\alpha,\beta\},\qquad C=P_{M,M}\ne0,
\]

and the four rows indexed by \(M\times M\) may be used. The local analysis in
[the carrier-resonance note](full-missing-square-cap-carrier-resonance.md)
leaves, at one residual edge \(rs\) and one pair of local probes \(c,d\),

\[
 W_{rs}(c,d)={U_{rs}(c,d)\over h}C
   +R_r(c)Q_s(d)^{\mathsf T}
   +E_s(d)T_r(c)^{\mathsf T}=0,                         \tag{1}
\]

while the selected curvature matrix

\[
 K_{rs}(c,d)=U_{rs}(c,d)C-R_r(c)Q_s(d)^{\mathsf T}       \tag{2}
\]

is nonzero. Equation (1) is a genuine failure at that one decorated edge,
but it is not a global failure of the full-nine cap.

There are two exact relocation statements.

1. For fixed \(r,s\), allow arbitrary local probes rather than only basis
   colours. If the bilinear matrix map \(W_{rs}(-,-)\) is not identically
   zero, then some pair of probes satisfies

   \[
                         K_{rs}(c',d')\ne0,
             \qquad      W_{rs}(c',d')\ne0.               \tag{3}
   \]

   Thus a single resonant colour cell is bypassed on the same physical edge.
   The only fixed-edge survivor is the tensor identity

   \[
                         W_{rs}(-,-)\equiv0.               \tag{4}
   \]

2. Even under (4), all completed full-nine coefficients force a carrier on
   another decorated residual edge. More precisely, if
   \(W_\omega\in\operatorname{Mat}_{M,M}\) runs over the coefficient matrices
   of every decorated quadratic monomial on the residual sites, then

   \[
     \boxed{\quad
       \mathcal D:=\operatorname{span}\{E_{\alpha\alpha},
                                        E_{\beta\beta}\}
       \subseteq \operatorname{span}\{W_\omega:\omega\}.
       \quad}                                               \tag{5}
   \]

   Hence the matrices away from a resonant zero coefficient span a space of
   dimension at least two. Given the originally selected \(K_0\ne0\), one
   may choose one functional which detects \(K_0\), a nonzero diagonal
   target, and a nonzero relocated coefficient.

There is also a rank-one version:

\[
                         \ell=\xi\eta^{\mathsf T}.          \tag{6}
\]

Some such rank-one functional always satisfies

\[
              \ell(C)=0,\qquad
              (\ell(E_{\alpha\alpha}),
               \ell(E_{\beta\beta}))\ne(0,0).             \tag{7}
\]

It gives a factorized cap \(LS\) with a nonzero diagonal target, so that cap
has a nonzero decorated edge somewhere. If (1) holds, its nonzero edge is
necessarily elsewhere. When \(K_0\notin\mathbb C C\), the rank-one
functional may additionally be chosen with

\[
                              \ell(K_0)\ne0.                \tag{8}
\]

When \(K_0\in\mathbb C C\setminus\{0\}\), condition (8) is impossible for
every direct-zero functional. The resonance then forces a singular
common-line packet described in Section 5. The arbitrary-functional
relocation still retains the curvature evaluation, and the rank-one cap
still has a relocated edge, but these are not the same assertion.

This removes full-cap carrier resonance as an obstruction to the existence
of a literal source-provenant cap edge. It does **not** eliminate the radial
common-line packet while preserving a rank-one curvature detector. It also
does not eliminate the target-blocked incidence in the physical dark-cut
theorem, synchronize the relocated edge on the second chart, or identify a
sparse physical four-cycle differential with the dense weighted \(K_6\)
selector chart. The conjecture remains open at those later gates.

## 2. The matrix-valued completed cap

Let \(W=\mathcal V\setminus\{p,q\}\), so \(|W|=2h\). In the
site-square-zero algebra on \(W\), write \(q\) for the residual quadratic
and \(p_i,s_j\) for the two endpoint stars. Package the four completed caps
into the matrix-valued quadratic

\[
 \mathscr B={1\over h}Cq+(p_i s_j)_{i,j\in M}
       \in\operatorname{Mat}_{M,M}\otimes({\cal A}_W)_2.   \tag{9}
\]

The factor \(1/h\) is forced by
\(q q^{[h-1]}=h q^{[h]}\). The four full-nine rows are exactly

\[
 \boxed{\quad
 \mathscr Bq^{[h-1]}
      =E_{\alpha\alpha}X_\alpha
         +E_{\beta\beta}X_\beta.
 \quad}                                                     \tag{10}
\]

For a matrix functional \(\ell\), its scalar contraction is

\[
 \widehat r_\ell=\ell(\mathscr B)
   ={\ell(C)\over h}q+\sum_{i,j\in M}\ell_{ij}p_i s_j,     \tag{11}
\]

and (10) gives

\[
 \widehat r_\ell q^{[h-1]}
   =\ell(E_{\alpha\alpha})X_\alpha
      +\ell(E_{\beta\beta})X_\beta.                       \tag{12}
\]

Expand (9) in the literal decorated quadratic monomial basis:

\[
                         \mathscr B=\sum_\omega W_\omega m_\omega.
                                                                    \tag{13}
\]

For \(\omega=(rs;c,d)\), its coefficient is precisely

\[
 W_\omega={U_{rs}(c,d)\over h}C
       +R_r(c)Q_s(d)^{\mathsf T}
       +E_s(d)T_r(c)^{\mathsf T},                          \tag{14}
\]

including both endpoint-star assignments. Thus (14) agrees with the matrix
called \(W_{c,d}\) in the local resonance calculation.

## 3. The coefficient-span theorem

**Theorem 3.1 (full-nine response span).** The coefficient matrices in
(13) satisfy (5).

**Proof.** Taking the coefficient of the pure target word \(X_e\) in (10)
gives, for \(e\in M\),

\[
 E_{ee}=\sum_\omega
       [m_\omega q^{[h-1]}]_{X_e}\,W_\omega.               \tag{15}
\]

This directly puts both diagonal units in the coefficient span.

For the equivalent annihilator proof, put
\(S=\operatorname{span}\{W_\omega\}\). If \(\ell\in S^\perp\), then (13)
gives \(\widehat r_\ell=\ell(\mathscr B)=0\). Equation (12) becomes

\[
       \ell(E_{\alpha\alpha})X_\alpha
         +\ell(E_{\beta\beta})X_\beta=0.
\]

The two pure response tensors are distinct basis words and hence linearly
independent. Therefore \(\ell\) kills both diagonal units, proving

\[
                         S^\perp\subseteq\mathcal D^\perp.
\]

Taking annihilators in the finite-dimensional matrix space gives
\(\mathcal D\subseteq S\). \(\square\)

If one selected coefficient \(W_{\omega_0}\) vanishes, deleting it does not
change \(S\). The remaining coefficient matrices still span
\(\mathcal D\), so at least two of them are linearly independent. Choose
one nonzero \(W_{\omega_1}\), where necessarily
\(\omega_1\ne\omega_0\).

Now fix any nonzero selected curvature matrix \(K_0\). In the dual
four-dimensional matrix space, each of

\[
 K_0^\perp,\qquad W_{\omega_1}^\perp,
       \qquad\mathcal D^\perp                              \tag{16}
\]

is a proper linear subspace. Over \(\mathbb C\), three proper linear
subspaces do not cover the ambient vector space. Hence there is one
functional \(\ell\) outside their union. Its completed cap simultaneously
has

\[
 \ell(K_0)\ne0,\qquad
 \ell(W_{\omega_1})\ne0,\qquad
 \ell|_{\mathcal D}\ne0.                                 \tag{17}
\]

This proves the arbitrary-functional relocation. Notice that the curvature
matrix in (17) belongs to the originally selected edge, while the literal
cap coefficient may belong to another edge. No identity here equates those
two scalars.

## 4. Arbitrary probes close the nonidentical fixed-edge branch

Fix \(r,s\), but now let \(c\in V_r^*\) and \(d\in V_s^*\) be arbitrary
local probes. Contracting the physical blocks makes

\[
                   (c,d)\longmapsto K_{rs}(c,d),W_{rs}(c,d)
                                                                    \tag{18}
\]

bilinear matrix-valued maps. The selected curvature cell says that the
first map is not identically zero. Suppose the second map is also not
identically zero. The two loci

\[
 \{(c,d):K_{rs}(c,d)\ne0\},\qquad
 \{(c,d):W_{rs}(c,d)\ne0\}                                \tag{19}
\]

are nonempty Zariski-open subsets of the irreducible affine variety
\(V_r^*\times V_s^*\). Their intersection is nonempty, proving (3).

Consequently a basis-colour resonance does not require a support split or
a second chart. One first polarizes the two local probes. Only the full
tensor identity (4) survives this step. If (4) holds, Theorem 3.1 moves the
carrier to a different residual edge; it does not guarantee that only the
local colours change while \(r,s\) stay fixed.

The same reasoning applies independently to the \(pr\)-chart. It does not
force the two relocated coefficients to use the same physical residual
edge, local probes, or missing target label. Such synchronization would be
a new two-chart theorem, not a consequence of (10).

## 5. Rank-one relocation and the radial survivor

There is always a rank-one direct-zero target functional. Choose
\(\eta\in(\mathbb C^*)^2\) with \(C\eta\ne0\), and put, in the ordered
basis \((\alpha,\beta)\),

\[
        \xi=((C\eta)_\beta,-(C\eta)_\alpha).               \tag{20}
\]

Then \(\xi^{\mathsf T}C\eta=0\). Both entries of \(\eta\) are nonzero and
\(\xi\ne0\), so at least one diagonal product \(\xi_e\eta_e\) is nonzero.
For \(\ell=\xi\eta^{\mathsf T}\), define

\[
                   L=\sum_{i\in M}\xi_i p_i,
             \qquad S=\sum_{j\in M}\eta_j s_j.            \tag{21}
\]

Equations (7), (11), and (12) become

\[
 LSq^{[h-1]}
    =\xi_\alpha\eta_\alpha X_\alpha
       +\xi_\beta\eta_\beta X_\beta\ne0.                  \tag{22}
\]

Thus \(LS\ne0\), and it has a nonzero literal decorated edge coefficient.
If \(W_{\omega_0}=0\), that coefficient lies at
\(\omega\ne\omega_0\). This is the factor-rank-one relocation needed as
input to the physical dark-cut theorem.

The rank-one functional can detect \(K_0\) as well exactly off the radial
line. Projectivized rank-one functionals form the Segre quadric in
\(\mathbf P^3\). Its section by \(\ell(C)=0\) is an irreducible conic when
\(C\) is invertible and two ruling lines when \(C\) has rank one. The
section spans the hyperplane \(C^\perp\). Therefore \(K_0^\perp\) contains
the whole section exactly when \(K_0\in\mathbb C C\). The target-bad line

\[
        \mathcal D^\perp=\{\ell:\ell(E_{\alpha\alpha})
                             =\ell(E_{\beta\beta})=0\}
\]

contains neither ruling component and cannot contain the irreducible
conic. Removing the curvature-bad and target-bad proper closed subsets
leaves a rank-one \(\ell\) satisfying (7)--(8).

It remains to record exactly what happens on the excluded radial line.
At the selected probes abbreviate

\[
 u=U_{rs}(c,d),\qquad
 H=R_r(c)Q_s(d)^{\mathsf T},\qquad
 G=E_s(d)T_r(c)^{\mathsf T}.
\]

Assume

\[
 W_0={u\over h}C+H+G=0,\qquad
 K_0=uC-H=\lambda C\ne0.                                  \tag{23}
\]

Then

\[
             H=(u-\lambda)C,
       \qquad
             G=\left(\lambda-{h+1\over h}u\right)C.       \tag{24}
\]

Since \(H,G\) have rank at most one, (24) forces

\[
                              \operatorname{rank}C=1.       \tag{25}
\]

Indeed, if \(C\) were invertible, the first equality in (24) would give
\(u=\lambda\), and the second would then give \(u=0\); this contradicts
\(\lambda\ne0\). The two \(u\)-branches are therefore

\[
\begin{array}{c|cc}
 &H&G\\ \hline
 u=0&-\lambda C&\lambda C,\\[1mm]
 u\ne0&(u-\lambda)C&
       \left(\lambda-{h+1\over h}u\right)C.
\end{array}                                                \tag{26}
\]

Every nonzero assignment matrix in (26) has the same left and right lines
as the rank-one compression \(C\). This is the exact singular common-line
packet. Every direct-zero functional kills \(K_0=\lambda C\), so no
rank-one/direct-zero selection can retain its curvature scalar. Equations
(20)--(22) still give a factorized target cap with a relocated edge, while
Theorem 3.1 and (17) give a generally nonfactorized completed cap retaining
the curvature evaluation.

## 6. Exact remaining gate

The local equality \(W_{\omega_0}=0\) is no longer a separate carrier
obstruction:

* arbitrary probe polarization produces \(K,W\ne0\) on the same residual
  edge unless the full bilinear tensor \(W_{rs}\) vanishes;
* the full-nine response span relocates the edge to another residual
  coefficient even when that tensor vanishes;
* a rank-one direct-zero cap with a nonzero target and some nonzero edge
  always exists on the completed \(2\times2\) missing square;
* off \(K_0\in\mathbb C C\), that rank-one cap may retain the selected
  curvature evaluation.

What remains is not another matrix-support census. For the rank-one cap,
the physical coefficient-cut theorem can still fail when every active
target colour is locally blocked at one of the four sites complementary to
its relocated edge. Even after obtaining a nonzero physical four-cycle
differential, the source-faithful comparison with the dense weighted
\(K_6\) Lefschetz selector is still required. On two charts, a further
synchronization argument is needed if the later proof requires the same
relocated edge or target label on both charts. Finally, the radial packet
(26) remains the exact obstruction to keeping the original curvature
evaluation inside a rank-one direct-zero cap.

The dependency-free
[checker](../computations/verify_full_cap_carrier_resonance_relocation.py)
audits the rank-one selector over a finite field of characteristic larger
than three and exhaustively verifies the radial classification (24)--(26).
It performs no matching or support enumeration.
