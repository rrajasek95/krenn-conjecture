# One functional can carry a diagonal anchor and nonradial curvature

## 1. Outcome

Retain one full-nine deleted-pair chart on the double-zero branch.  Let

\[
 A=I^c,\qquad B=J^c,\qquad C=P_{A,B}\ne0                 \tag{1}
\]

be its missing-label compression.  Fix two residual sites \(r,s\) and
physical labels \(c,d\), and use the four-site blocks

\[
 P=A_{pq},\quad R=A_{pr},\quad E=A_{ps},\quad
 T=A_{qr},\quad Q=A_{qs},\quad U=A_{rs}.
\]

On \(\operatorname {Mat}_{A,B}\), put

\[
 \begin{aligned}
 K_{c,d}&=U_{cd}C-R_{A,c}Q_{B,d}^{\mathsf T},\\
 G_{c,d}&=E_{A,d}T_{B,c}^{\mathsf T},\\
 \mathcal D&=\operatorname {span}\{
      (E_{ee})_{A,B}:e\in A\cap B\}.
 \end{aligned}                                             \tag{2}
\]

Every entry of \(K_{c,d}\) is a literal canonical-transition curvature

\[
 (K_{c,d})_{ij}=P_{ij}U_{cd}-R_{ic}Q_{jd}.                 \tag{3}
\]

There is one matrix functional \(\ell\) which simultaneously

* annihilates the direct compression and the reverse star assignment;
* detects a nonzero diagonal target; and
* detects the curvature matrix

if and only if

\[
 \boxed{
 K_{c,d}\notin\operatorname {span}(C,G_{c,d}),\qquad
 \mathcal D\not\subseteq\operatorname {span}(C,G_{c,d}).}
                                                               \tag{4}
\]

For that same \(\ell\), the full-nine rows give the source-provenant cap

\[
 r_\ell q^{[h-1]}
   =\sum_{e\in A\cap B}\ell((E_{ee})_{A,B})X_e,            \tag{5}
\]

and its literal coefficient on the physical edge \(rs\), with endpoint
labels \((c,d)\), is

\[
 \boxed{[r_\ell]_{rs;c,d}=-\ell(K_{c,d})\ne0.}             \tag{6}
\]

Thus (4) constructs one object carrying both pieces of data before any
odd-residue or common-power quotient.  In the branch \(T=0\), the two
conditions reduce to

\[
 K_{c,d}\notin\mathbb C C,qquad
 \mathcal D\not\subseteq\mathbb C C.                       \tag{7}
\]

The second is exactly the complement of the two coordinate-cell anchor
boundaries already classified in the
[diagonal-anchor polar descent](double-zero-diagonal-anchor-polar-descent.md).
Hence the \(T=0\), non-coordinate, nonradial branch has a literal
**curvature-bearing diagonal cap**.  This closes the former logical gap
between choosing an anchor functional and choosing a curvature-detecting
functional on that branch.

Allowing the contracted cap to retain its forced internal-\(q\) term also
closes the radial exception whenever \(C\) is invertible.  More precisely,
if \(|A|=|B|=2\), \(\det C\ne0\), \(T=0\), and
\(K_{c,d}\ne0\), then some full contracted cap has both a nonzero diagonal
target and a nonzero literal \((rs;c,d)\) coefficient.  Thus every
invertible \(2\times2\), \(T=0\) curvature row is anchor-bearing.  A
one-dimensional, rectangular, or singular compression can still have the
scalar resonance in Section 4.

It does not yet prove the conjecture.  A nonzero decorated coefficient of
the cap need not have nonzero weighted four-cycle class after selector
normalization.  The remaining step is still a source-faithful,
grade-preserving coefficient-cut map, or an argument that the selected cap
has nonzero \(K_6\) normal.  On the \(\chi=0\), possibly nonzero-\(T\)
branch, (4) replaces the vague obstruction by the two explicit span
alignments displayed there.

## 2. The full-nine contraction

Let \(W=\mathcal V\setminus\{p,q\}\), \(|W|=2h\), and let \(q\) be the
literal decorated quadratic on \(W\).  The compressed rows are

\[
 C_{ij}q^{[h]}+p_i s_jq^{[h-1]}
       =\mathbf1_{i=j}X_i,qquad i\in A,\ j\in B.           \tag{8}
\]

Pair matrices and matrix functionals by

\[
                         \ell(M)=\sum_{i\in A,j\in B}
                                      \ell_{ij}M_{ij}.
\]

If \(\ell(C)=0\), define

\[
                         r_\ell=\sum_{i,j}\ell_{ij}p_i s_j. \tag{9}
\]

Applying \(\ell\) to (8) proves (5) as a full-colour tensor identity.
In particular, saying that the target in (5) is nonzero is exactly saying
that \(\ell\) does not vanish identically on \(\mathcal D\).  No binary
projection or cancellation of \(q^{[h-1]}\) is used.

Resolve the two residual sites \(r,s\).  At those sites the two endpoint
stars have local coefficients

\[
 \begin{array}{c|cc}
       &r,c&s,d\\ \hline
 p_i&R_{ic}&E_{id}\\
 s_j&T_{jc}&Q_{jd}.
 \end{array}                                                \tag{10}
\]

The coefficient of their product on the edge \(rs\) is therefore the sum
of the two possible assignments:

\[
 [r_\ell]_{rs;c,d}
   =\ell\!\left(R_{A,c}Q_{B,d}^{\mathsf T}
                   +E_{A,d}T_{B,c}^{\mathsf T}\right).      \tag{11}
\]

Equations (2) give

\[
 R_{A,c}Q_{B,d}^{\mathsf T}=U_{cd}C-K_{c,d}.
\]

Consequently every functional satisfying
\(\ell(C)=\ell(G_{c,d})=0\) obeys the exact signed identity (6).  The
minus sign is forced; the reverse assignment in (11) is precisely why
\(G_{c,d}\) must either vanish or be annihilated.

## 3. Simultaneous-selection lemma

The required functional is elementary linear algebra, but its simultaneous
form is the useful point.

**Lemma 3.1 (anchor--curvature selection).**  Let \(V\) be a
finite-dimensional complex vector space, let \(S,D\subseteq V\) be
subspaces, and let \(K\in V\).  There is \(\ell\in V^*\) such that

\[
 \ell|_S=0,\qquad \ell(K)\ne0,\qquad \ell|_D\ne0           \tag{12}
\]

if and only if

\[
                         K\notin S,\qquad D\not\subseteq S. \tag{13}
\]

**Proof.**  Necessity is immediate.  For sufficiency, put
\(H=S^\perp\subseteq V^*\).  The first condition in (13) says that
\(H\cap K^\perp\) is a proper subspace of \(H\); the second says that
\(H\cap D^\perp\) is also proper.  A complex vector space is not the
union of two proper linear subspaces.  Choose \(\ell\) outside their
union.  It satisfies (12).  \(\square\)

Apply the lemma with

\[
 V=\operatorname {Mat}_{A,B},\qquad
 S=\operatorname {span}(C,G_{c,d}),\qquad D=\mathcal D.
\]

This proves the equivalence (4), and Sections 1--2 then prove (5)--(6).
The statement is insensitive to whether the selected functional has rank
one.  Requiring rank one, or prescribing one particular target label,
adds a genuine condition and is not used in (4).

There is nevertheless an exact prescribed-label refinement.  Fix
\(e\in A\cap B\), and put

\[
 S_e=\operatorname {span}\left(
 C,G_{c,d},\{(E_{ff})_{A,B}:f\in A\cap B,\ f\ne e\}\right).
                                                               \tag{13a}
\]

There is a functional with

\[
 \ell|_{S_e}=0,\qquad \ell(K_{c,d})\ne0,
 \qquad \ell((E_{ee})_{A,B})=1                         \tag{13b}
\]

if and only if

\[
 K_{c,d}\notin S_e,qquad (E_{ee})_{A,B}\notin S_e.          \tag{13c}
\]

Indeed, apply Lemma 3.1 with
\(D=\mathbb C(E_{ee})_{A,B}\), then rescale.  Equations (5)--(6)
become the label-faithful packet

\[
                         r_\ell q^{[h-1]}=X_e,qquad
                         [r_\ell]_{rs;c,d}=-\ell(K_{c,d})\ne0.
                                                               \tag{13d}
\]

This is the appropriate version when a later two-chart subtraction needs
the same physical anchor label on both charts.  The unprescribed criterion
(4) on two charts separately does not imply that their detected labels
intersect.

## 4. The two exhaustive pure-overlap branches

The pure-\(\delta\) three-site overlap already proves

\[
                         T=0\quad\hbox{or}\quad\chi=0.       \tag{14}
\]

If \(T=0\), then \(G_{c,d}=0\) for every \((c,d)\), so Lemma 3.1 gives
(7).  Moreover

\[
 \mathcal D\subseteq\mathbb C C                              \tag{15}
\]

holds exactly when every restricted missing-label diagonal unit is zero
modulo \(\mathbb C C\).  With nonempty \(A,B\) inside the two labels
different from \(\delta\), these are precisely:

1. \(A\cap B=\varnothing\), so \(A,B\) are opposite singletons; or
2. \(A\cap B=\{e\}\) and \(C\) is supported only at \((e,e)\).

Thus there is no new anchor exception hidden in (7).

If \(T\ne0\), equation (14) gives \(\chi=0\).  The reverse assignment is
the rank-one matrix \(G_{c,d}=E_{A,d}T_{B,c}^{\mathsf T}\).  Lemma 3.1
still applies verbatim.  Failure is localized to either

\[
 K_{c,d}\in\operatorname {span}(C,G_{c,d})                 \tag{16}
\]

or

\[
 \mathcal D\subseteq\operatorname {span}(C,G_{c,d}).       \tag{17}
\]

These are at most two-dimensional alignments in a matrix space of dimension
at most four.  They are the exact next cases for the nonzero-\(T\) branch;
no enumeration of matching supports is needed.

For one useful refinement, if \(|A|=|B|=2\) and \(C\) is invertible, then

\[
 K_{c,d}\in\mathbb C C
 \quad\Longrightarrow\quad
 R_{A,c}Q_{B,d}^{\mathsf T}=0,
 \quad K_{c,d}=U_{cd}C.                                    \tag{18}
\]

Indeed, writing \(K_{c,d}=\lambda C\) makes the rank-at-most-one matrix
\(R_{A,c}Q_{B,d}^{\mathsf T}\) equal
\((U_{cd}-\lambda)C\).  An invertible \(2\times2\) matrix cannot be a
nonzero rank-one matrix.  Hence the scalar is zero.  The sole radial
failure of the *isotropic* selector in the invertible \(T=0\) chart is
therefore a triangular direct-free transition, not a generic cancellation.

That triangular case is still carried by a slightly more general cap.
For an arbitrary functional \(\ell\), put

\[
 \widehat r_\ell={\ell(C)\over h}q+
                    \sum_{i,j}\ell_{ij}p_i s_j.             \tag{19}
\]

Contracting (8), including its direct term, gives

\[
 \widehat r_\ell q^{[h-1]}
   =\sum_{e\in A\cap B}\ell((E_{ee})_{A,B})X_e.             \tag{20}
\]

When \(T=0\), its selected literal edge coefficient is

\[
 [\widehat r_\ell]_{rs;c,d}
  =\ell(H_{c,d}),\qquad
 H_{c,d}={U_{cd}\over h}C+R_{A,c}Q_{B,d}^{\mathsf T}
         ={h+1\over h}U_{cd}C-K_{c,d}.                      \tag{21}
\]

If \(C\) is invertible and \(K_{c,d}\ne0\), then
\(H_{c,d}\ne0\).  Indeed, \(H_{c,d}=0\) would make the rank-at-most-one
matrix \(R_{A,c}Q_{B,d}^{\mathsf T}\) a scalar multiple of the rank-two
matrix \(C\).  The scalar and the rank-one matrix would both vanish,
forcing \(U_{cd}=0\) and then \(K_{c,d}=0\), a contradiction.

The diagonal space \(\mathcal D\) is nonzero.  The two proper subspaces
\(H_{c,d}^\perp\) and \(\mathcal D^\perp\) cannot cover the whole dual
matrix space, so choose \(\ell\) detecting both.  Equations (20)--(21)
prove the invertible-\(2\times2\) claim from Section 1.  Outside that case,
and assuming \(\mathcal D\ne0\), the new obstruction at this coefficient
is exactly the explicit resonance

\[
 R_{A,c}Q_{B,d}^{\mathsf T}=-{U_{cd}\over h}C,
 \qquad
 K_{c,d}={h+1\over h}U_{cd}C.                              \tag{22}
\]

This completion guarantees a nonzero source-provenant edge coefficient,
not its prescribed normalization to one selected scalar curvature and not
a nonzero weighted four-cycle class.  If \(\mathcal D=0\), there is no
diagonal target to carry, independently of the resonance.

## 5. Relation to the cap-minor hierarchy

When \(|A|=|B|=2\), let \(C^\#=(\operatorname {Cof}_{ij}C)\) be the
cofactor matrix and put

\[
 \rho_C=\sum_{i,j}C^\#_{ij}p_i s_j,qquad
 \beta_C={2\det C\over h}q+\rho_C.                         \tag{23}
\]

Contracting (8) with \(C^\#\), and using
\(\sum C^\#_{ij}C_{ij}=2\det C\), gives

\[
 \boxed{
 \beta_Cq^{[h-1]}
   =\sum_{e\in A\cap B}C^\#_{ee}X_e.}                     \tag{24}
\]

This is the \(2\times2\) member of the older
[uniform cap-minor hierarchy](uniform-cap-minor-hierarchy.md), now viewed
as a canonical two-anchor quadratic.  Its coefficient on \((rs;c,d)\) is

\[
 {2\det C\over h}U_{cd}
 +\sum_{i,j}C^\#_{ij}
       (R_{ic}Q_{jd}+E_{id}T_{jc}).                         \tag{25}
\]

The adjugate packet explains structurally why two diagonal anchors and a
crossed row form a determinant polarization.  Lemma 3.1 is sharper for the
present purpose: instead of fixing the cofactor functional, it selects a
functional which kills both the direct/radial term and the reverse star
assignment, while retaining a diagonal target and the nonradial curvature.

The dependency-free checker
[`verify_curvature_bearing_anchor_selection.py`](../computations/verify_curvature_bearing_anchor_selection.py)
audits the rank-one-update/cofactor identity and exhausts the simultaneous
selection statement over every subspace generated by at most two vectors in
dimensions one through four over \(\mathbb F_3\).  It also checks the
invertible-\(2\times2\) radial rank comparison over \(\mathbb F_5\), without
enumerating response factorizations.  The proof above is over \(\mathbb C\);
the finite audit is a compact independent check of all matrix-space
dimensions occurring here.
