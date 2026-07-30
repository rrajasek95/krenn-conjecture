# Two-chart alignment gives a kernel normal form, not curvature vanishing

## 1. Outcome

Use the two literal charts \(pq\) and \(pr\) supplied by the
[joint-extraction theorem](two-chart-joint-hypothesis-extraction.md).  On a
common residual site \(x\), write

\[
 P=P_x,\qquad S=S_x,\qquad R=R_x
\]

for the \(p,q,r\) endpoint maps, and put

\[
 N^q_e=P^{\mathsf T}J_eS,\qquad
 N^r_e=P^{\mathsf T}J_eR,
 \qquad u^{\mathsf T}J_ev=\det(u,v,e_e).                 \tag{1}
\]

The source-level alignment residue from the
[full-nine selector theorem](full-nine-isotropic-selector-blocking-normal-form.md)
has an invariant classification.  It does not, however, make the physical
curvature vanish.  The exact conclusions are these.

1. If the direct block \(d\) has rank three, or if \(d=0\), an aligned site
   satisfies \(N^q_e=0\).  Equivalently, the images of \(P\) and \(S\) in
   \(V/\mathbb Ce_e\) are symplectic-orthogonal.  In particular

   \[
                      \operatorname {rank}P+
                      \operatorname {rank}S\leq4.       \tag{2}
   \]

2. If \(\operatorname {rank}d=2\) and
   \(N^q_e=\lambda d\) with \(\lambda\ne0\), then

   \[
   \operatorname {adj}(S)e_e\in\ker d\setminus\{0\},
   \qquad
   \operatorname {adj}(P)e_e\in\ker d^{\mathsf T}\setminus\{0\}.
                                                               \tag{3}
   \]

   Thus a same-target, nonzero-proportionality intersection of the two
   charts forces the two rank-two direct blocks to have the same literal
   left-kernel line.  This is a strict direct-block normal form, but is not
   a contradiction.

3. If \(d=\alpha\beta^{\mathsf T}\ne0\) has rank one, left-ruling
   alignment is exactly

   \[
   \overline{P(\alpha^\perp)}
       \perp_{e}\overline{\operatorname {im}S}
       \quad\hbox{in }V/\mathbb Ce_e,                    \tag{4}
   \]

   and right-ruling alignment is the transpose statement with
   \(\operatorname {im}P\) and \(S(\beta^\perp)\).  This treats the two
   rulings separately; a left-ruling condition must not be silently used as
   a right-ruling condition.

4. Alignment at two distinct fixed target labels gives a sharper local
   form.  In the zero branch, either the two relevant image dimensions sum
   to at most three, or both images are the literal coordinate plane
   \(\operatorname {span}(e_e,e_f)\).  In the rank-two nonzero branch both
   endpoint maps have rank exactly two.

At the eight-site \(8\to6\) boundary, if the two alignment sets for two
eligible labels do not meet, their cardinality bounds make them
complementary triples in the six-site residual set.  Comparing two such
partitions on the five residual sites common to the two charts gives one
last case-free alternative: either the charts assign the same label at a
common site, so the preceding same-target classification applies, or their
two binary label fields are pointwise opposite on all five sites.

The literal Bianchi and normal rows do not remove these alternatives.  At a
same-target proportionality site they give the exact identity

\[
 \det(Pe_i,D_x,e_e)=AB(\mu_x-\lambda_x),
 \qquad D_x=ARe_k-BSe_j,                                  \tag{5}
\]

where \(A=d_{ij}\), \(B=d'_{ik}\),
\(N^q_e=\lambda_xd\), and \(N^r_e=\mu_xd'\).  The entries of \(D_x\) are
physical curvature coordinates; the curvature chosen in the original
four-site minor is the corresponding coordinate of \(D_s\) at its
distinguished fourth site \(s\).  Bianchi transports this row; it does not
assert \(D_x=0\) or \(\lambda_x=\mu_x\).

Consequently the proposed alignment--Bianchi shortcut does not close the
conjecture.  What remains is narrower: the full-nine common-power target
rows must exclude the kernel-synchronized, coordinate-plane, and
five-site anti-aligned normal forms.  Two exact guards below show that this
source use is indispensable.

## 2. One-target invariant classification

Let \(V=\mathbb C^3\), and write \(\bar U_e\) for the image of a subspace
\(U\subseteq V\) in \(V/\mathbb Ce_e\).  The form

\[
 \omega_e(\bar u,\bar v)=\det(u,v,e_e)                  \tag{6}
\]

is a nondegenerate alternating form on this two-dimensional quotient.
Therefore

\[
 P^{\mathsf T}J_eS=0
 \quad\Longleftrightarrow\quad
 \overline{\operatorname {im}P}_e
       \perp_{\omega_e}
 \overline{\operatorname {im}S}_e.                       \tag{7}
\]

The dimensions of two orthogonal subspaces of a symplectic plane sum to at
most two.  Each original image can gain at most the line
\(\mathbb Ce_e\), proving (2).  More precisely, if \(P\) is invertible then
\(\operatorname {im}S\subseteq\mathbb Ce_e\), and the transposed statement
holds when \(S\) is invertible.

If \(\operatorname {rank}d=3\), the equality
\(P^{\mathsf T}J_eS=\lambda d\) forces \(\lambda=0\), since the left side
has rank at most two.  The rank-zero definition is already
\(P^{\mathsf T}J_eS=0\).  This proves assertion 1 for both ranks without
dividing by a direct entry.

For rank two, use the polynomial adjugate identity

\[
\begin{aligned}
 \operatorname {adj}(P^{\mathsf T}J_eS)
  &=\operatorname {adj}(S)\operatorname {adj}(J_e)
       \operatorname {adj}(P)^{\mathsf T}\\
  &=(\operatorname {adj}(S)e_e)
       (\operatorname {adj}(P)e_e)^{\mathsf T}.           \tag{8}
\end{aligned}
\]

Here \(\operatorname {adj}(J_e)=e_ee_e^{\mathsf T}\).  If
\(P^{\mathsf T}J_eS=\lambda d\), then

\[
 (\operatorname {adj}(S)e_e)
 (\operatorname {adj}(P)e_e)^{\mathsf T}
       =\lambda^2\operatorname {adj}(d).                  \tag{9}
\]

For rank-two \(d\), the column and row lines of
\(\operatorname {adj}(d)\) are respectively \(\ker d\) and
\(\ker d^{\mathsf T}\).  When \(\lambda\ne0\), (9) proves (3), including
both nonvanishings.

Now let \(d=\alpha\beta^{\mathsf T}\) have rank one.  On the left ruling,

\[
 P^{\mathsf T}J_eS=\alpha w^{\mathsf T}
 \quad\Longleftrightarrow\quad
 \det(P\xi,S\eta,e_e)=0
 \quad(\xi\in\alpha^\perp,\ \eta\in\mathbb C^3).       \tag{10}
\]

Applying (6) to
\(P(\alpha^\perp)\) and \(\operatorname {im}S\) gives (4).  On the right
ruling the same proof uses \(\eta\in\beta^\perp\), and gives

\[
 \overline{\operatorname {im}P}_e
       \perp_e\overline{S(\beta^\perp)}_e.               \tag{11}
\]

Equations (10)--(11) are also the honest lower-rank stopping point: when
different target labels require different rulings, only their two displayed
orthogonality conditions are automatic.

## 3. Two fixed target labels

Let \(e\ne f\), put \(E_{ef}=\operatorname {span}(e_e,e_f)\), and suppose

\[
               P^{\mathsf T}J_eS=P^{\mathsf T}J_fS=0.    \tag{12}
\]

For every \(u\in\operatorname {im}P\) and
\(v\in\operatorname {im}S\), (12) says that \(u\times v\) is perpendicular
to \(E_{ef}\).  If the two image dimensions sum to at least four, they are
both two: a three-dimensional image would force the other image to be zero.
Some cross product is then nonzero, and its direction forces both
two-planes to be \(E_{ef}\).  Hence

\[
 \boxed{\quad
 \operatorname {rank}P+\operatorname {rank}S\le3,
 \quad\hbox{or}\quad
 \operatorname {im}P=\operatorname {im}S=E_{ef},\ 
 \operatorname {rank}P=\operatorname {rank}S=2.
 \quad}                                                       \tag{13}
\]

The same argument applies to the two subspaces in (10), or in (11), when
two rank-one target alignments use the same ruling.

Suppose instead that \(\operatorname {rank}d=2\) and

\[
 P^{\mathsf T}J_eS=\lambda_ed,
 \qquad P^{\mathsf T}J_fS=\lambda_fd.                    \tag{14}
\]

If one scalar is nonzero and the other is zero, the nonzero matrix forces
both endpoint ranks to be at least two, while (2) forces their sum to be at
most four.  Both ranks are therefore two.  If both scalars are nonzero,
(9) makes both \(\operatorname {adj}(P)e_e\) and
\(\operatorname {adj}(P)e_f\) nonzero vectors on the same line.  An
invertible adjugate cannot do that to two independent coordinate vectors;
so \(P\) has rank two, and the same proof applies to \(S\).  If both scalars
are zero, use (13).  This proves assertion 4 in every branch.

## 4. Comparing the two charts

Assume \(d,d'\) both have rank two and that a common site is aligned at the
same fixed target \(e\):

\[
 P^{\mathsf T}J_eS=\lambda d,
 \qquad P^{\mathsf T}J_eR=\mu d'.                       \tag{15}
\]

If \(\lambda\mu\ne0\), equation (9), applied twice to the shared \(P\),
gives

\[
                       \ker d^{\mathsf T}=
                       \ker (d')^{\mathsf T}.            \tag{16}
\]

No analogous kernel conclusion is valid when one scalar vanishes or one
direct block has another rank; in those cases the applicable conclusion is
exactly (7), (10), or (11).

For selected labels \(i,j,k\), put \(A=d_{ij}\), \(B=d'_{ik}\), and

\[
                       D_x=ARe_k-BSe_j.                   \tag{17}
\]

Taking the determinant with \(Pe_i,e_e\) in (15) gives (5) directly.  At a
fourth-site colour \(l\),

\[
               (D_x)_l=A(A_{rx})_{kl}-B(A_{qx})_{jl}     \tag{18}
\]

is precisely the \(AU-BF\) curvature coordinate.  The literal connection
and normal identities are

\[
 P_{pq}t-P_{pr}y=Dz,
 \qquad L_{pq;r}-L_{pr;q}=-(m-2)D.                       \tag{19}
\]

Thus (19) retains \(D\); it supplies no equality of the two proportionality
scalars and no vanishing of (18).

Finally work specifically at the eight-site \(8\to6\) boundary and take two
eligible labels \(e,f\).  In one six-site chart, failure of every selector
dark cut gives alignment sets of size at least three.  If they do not meet,
they are complementary triples.  If this happens in both charts, restrict
the two resulting label functions to the five residual sites common to the
charts.  Either the functions agree somewhere, yielding a same-target site
to which (7), (10), (11), or (16) applies, or they disagree everywhere and
are pointwise complements.  This proves the claimed five-site anti-aligned
normal form without a case census.  No analogous cardinality conclusion is
claimed at a larger residual order.

## 5. Sharp block guard: Bianchi can carry nonzero curvature

There is an integral eight-site block guard on

\[
                    \{p,q,r,s,t,u,v,w\}.                 \tag{20}
\]

Let

\[
 J_0=\begin{pmatrix}0&0&0\\0&0&1\\0&-1&0\end{pmatrix},
 \qquad A_{pq}=A_{pr}=J_0,
 \qquad A_{qr}=0.                                        \tag{21}
\]

For \(x\in\{s,t,u\}\), take

\[
                A_{px}=A_{qx}=I,
                \qquad A_{rx}=2I,                        \tag{22}
\]

and set every other unlisted block to zero, with reverse orientations
given by transpose.  Both pair charts are good.  At each of \(s,t,u\),

\[
 P=S=I,\qquad R=2I,
 \qquad N^q_0=J_0=d,
 \qquad N^r_0=2J_0=2d'.                                  \tag{23}
\]

The special sites \(r\) and \(q\), and the zero sites \(v,w\), are aligned
as well, so each target-zero alignment set has all six sites.  With selected
labels

\[
                         (i,j,k,l)=(1,2,2,2),             \tag{24}
\]

one has \(A=B=F=1\), \(U=2\), and

\[
                              AU-BF=1.                    \tag{25}
\]

At the three common sites all of \(P,S,R\) are invertible.  The only forced
degeneracy is exactly (16): both direct blocks have left and right kernel
\(\mathbb Ce_0\).  Moreover the \(pq\)-internal support consists only of
the three edges \(rs,rt,ru\), and the \(pr\)-internal support only of
\(qs,qt,qu\).  Neither contains a perfect matching.  Hence no complementary
physical dark matching exists.  Since (21)--(22) are literal physical
blocks, all power-free Bianchi and normal identities hold.  This proves
that those identities cannot improve (16) to curvature zero or a dark cut.

The guard is not a GHZ source; it is an exact countermodel only to the
isolated block, goodness, alignment, and Bianchi implication.

## 6. The exact source row that is still missing

The stronger integral packet in the
[two-chart diagonal-row guard](curved-two-chart-omega-diagonal-row-guard.md)
has rank-one direct blocks \(d=d'=E_{00}\), four good endpoint stars,
nonzero curvature, both literal Bianchi packets, and all three diagonal
full-nine rows in both charts.  It also satisfies the present alignment
residue very strongly.  On the \(pq\) chart,

\[
\begin{aligned}
 T^{L}_{1}=T^{L}_{2}&=W_{pq},\\
 T^{R}_{1}&=W_{pq}\setminus\{r\},
 &T^{R}_{2}&=W_{pq},
\end{aligned}                                               \tag{26}
\]

and on the \(pr\) chart the same formulas hold with \(q\) replacing \(r\).
Indeed, every local wedge matrix is zero except

\[
 N^q_{r,1},N^r_{q,1}\in\mathbb C^*E_{02},                \tag{27}
\]

which is left-ruling aligned; the target-two matrices in (27) are zero.
The curvature remains \(AU-BF=1\).

That packet fails exactly the six off-diagonal full-nine rows.  For example,
the \(pq\) row \((i,j)=(0,1)\) requires

\[
                         P_0S_1q^{[2]}=0,                  \tag{28}
\]

but its mixed-word coefficient is

\[
             (as)_{0,1}(cd)_0(br)_1\ne0.                 \tag{29}
\]

Thus diagonal anchors, alignment, and the complete literal Bianchi packet
still do not couple the charts.  Any proof beyond the normal forms above
must use at least one of the omitted off-diagonal common-power rows such as
(28), while the seven-row guard in the blocked-site descent shows that the
off-diagonal rows without at least one of the other two diagonal anchors are
also insufficient.  The genuinely remaining source statement must
therefore couple off-diagonal and diagonal information from the available
full-nine system before passing to quotient planes or annihilator classes.
The two guards do not prove that every one of the nine rows is individually
indispensable.

The dependency-free
[checker](../computations/verify_two_chart_alignment_curvature_normal_form.py)
audits (8), the finite-field form of (13), both guards' alignment sets, the
curvature values, goodness, and the absence of a complementary matching in
the block guard.  It does not certify the still-open full-nine exclusion.
