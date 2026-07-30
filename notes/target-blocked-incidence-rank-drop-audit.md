# Target blocking is a common rank-drop problem, not a determinant cover

## 1. Outcome

Consider the rank-one cap produced on the double-zero, \(T=0\) branch,

\[
 \ell=\xi\eta^{\mathsf T},\qquad
 \xi^{\mathsf T}C\eta=0,\qquad
 \beta=L S,\quad L=p(\xi),\quad S=s(\eta).                 \tag{1}
\]

Let \(\{a,b\}\) be the two colours different from the synchronized pure
colour \(\delta\).  At every residual site \(x\), the channel definition
forces

\[
             L_{x,\delta}=S_{x,\delta}=0.                   \tag{2}
\]

This makes the initially tempting incidence polynomial

\[
 B_{x,e}(\xi,\eta)
   =\det(L_x,S_x,e_e^{(x)})                                \tag{3}
\]

identically zero for both missing target colours \(e=a,b\).  All three
columns in (3) lie in the same two-plane

\[
                    E_x=\operatorname{span}(e_a^{(x)},e_b^{(x)}).
\]

More importantly, the proposed equivalence

\[
 e_e^{(x)}\in\operatorname{span}(L_x,S_x)
 \quad\Longleftrightarrow\quad B_{x,e}(\xi,\eta)=0          \tag{4}
\]

is false when \(L_x,S_x\) are dependent.  In the present packet the
right side is always true, whereas the left side may be true or false.
Consequently an irreducible-conic finite-cover argument applied to (3)
cannot shrink the target-blocked obstruction: its alleged alignment matrix
is simply zero at every site.

There is an exact replacement.  Orient \(E_x\) by

\[
 \omega(u,v)=u_av_b-u_bv_a
             =u^{\mathsf T}Jv,qquad
 J=\begin{pmatrix}0&1\\-1&0\end{pmatrix},                  \tag{5}
\]

and let \(P_x,S_x:\mathbb C^2\to E_x\) be the two restricted local star
maps.  Put

\[
 D_x(\xi,\eta)=\omega(P_x\xi,S_x\eta)
      =\xi^{\mathsf T}N_x\eta,qquad
 N_x=P_x^{\mathsf T}J S_x.                                \tag{6}
\]

For the target \(a\), the exact local alternative is

\[
\begin{array}{c|c}
 D_x\ne0 & \operatorname{span}(L_x,S_x)=E_x,
            \text{ so }a\text{ and }b\text{ are both blocked},\\
 D_x=0 & a\text{ is blocked exactly when }
          L_{x,b}=S_{x,b}=0\text{ and }(L_x,S_x)\ne(0,0).
\end{array}                                                \tag{7}
\]

The transposed statement holds for target \(b\).  Thus visibility of one
fixed target on all four sites complementary to a selected edge first
requires the **common rank-drop equations**

\[
                         D_x(\xi,\eta)=0\qquad(x\in U),     \tag{8}
\]

followed by the coordinate-line exclusions in (7).  This reverses the
geometry of the proposed attack.  Target blocking contains the open set
\(D_x\ne0\); it is not a finite union of divisor zeros.  A finite union of
these open sets can cover the selector curve without forcing any one
\(N_x\) to align with \(C\).

The corrected formulation is nevertheless useful on the full
\(2\times2\) missing square.  For invertible \(C\),
(8) has at most two projective candidates unless every \(N_x\) is
proportional to \(C\).  For rank-one \(C\), it has at most one candidate
on each eligible ruling unless all local wedges align with that ruling.
Sections 3--4 give the exact statements.  Section 5 gives a literal
one-row guard showing that the remaining obstruction is genuine under the
currently isolated inputs: a rank-one diagonal cap identity, a nonradial
\(T=0\) curvature, and injective extensions of both endpoint stars can
coexist with a totally \(q\)-isotropic dark complement.

This does not prove the conjecture.  It says that varying only the
rank-one functional on its isotropic conic is not a natural closure of the
dark-cut route.  A positive theorem needs additional source input—for
example the other eight full-nine rows, the other two good endpoint maps,
or a source-faithful two-chart overlap—to force the common rank drops (8),
not merely avoid finitely many blocking hypersurfaces.

## 2. Exact local target incidence

Write

\[
 L_x=(l_a,l_b,0),\qquad S_x=(s_a,s_b,0).
\]

Then

\[
                         D_x=l_as_b-l_bs_a.                \tag{9}
\]

If \(D_x\ne0\), the two vectors span \(E_x\), proving the first row of
(7).  If \(D_x=0\), their span is either zero or a line.  The nonzero line
contains \(e_a\) exactly when both of its \(b\)-coordinates vanish.  Hence

\[
 e_a\notin\operatorname{span}(L_x,S_x)
 \Longleftrightarrow
 \left\{
 \begin{array}{l}
 D_x=0,\\
 (l_b,s_b)\ne(0,0)\ \text{or}\ (L_x,S_x)=(0,0).
 \end{array}\right.                                      \tag{10}
\]

Similarly,

\[
 e_b\notin\operatorname{span}(L_x,S_x)
 \Longleftrightarrow
 \left\{
 \begin{array}{l}
 D_x=0,\\
 (l_a,s_a)\ne(0,0)\ \text{or}\ (L_x,S_x)=(0,0).
 \end{array}\right.                                      \tag{11}
\]

Equations (10)--(11) include the rank-zero fibre correctly.  The
three-by-three determinant (3) loses precisely this rank information.

For a complementary four-set \(U\), define the projective rank-drop locus

\[
 \mathscr R_U=
 \{([\xi],[\eta]):\xi^{\mathsf T}C\eta=0,
                  \ D_x(\xi,\eta)=0\text{ for all }x\in U\}. \tag{12}
\]

A target-visible curvature-bearing selector must lie in \(\mathscr R_U\),
outside the curvature hyperplane, the target-coordinate divisor, and the
coordinate-line loci in (10) or (11).  This is a necessary-and-sufficient
test for the local visibility part of the dark-cut theorem.

## 3. Invertible compression: one gcd of four binary quadratics

Sections 3--4 assume that the compression is the full missing square
\(A=B=\{a,b\}\).  Rectangular \(1\times2\) and \(2\times1\) compressions
have rank-one functionals but not the conic/ruling geometry below.

Assume \(C\in\operatorname{Mat}_{2\times2}\) is invertible.  The isotropic
section

\[
 \mathscr Q_C=\{([\xi],[\eta])\in\mathbf P^1\times\mathbf P^1:
                       \xi^{\mathsf T}C\eta=0\}             \tag{13}
\]

is an irreducible \((1,1)\)-conic.  It has the parametrization

\[
                [\xi]\longmapsto
                ([\xi],[J C^{\mathsf T}\xi]).              \tag{14}
\]

Restricting (6) to (14) gives one binary quadratic per site,

\[
 d_x(\xi)=\xi^{\mathsf T}N_xJ C^{\mathsf T}\xi.           \tag{15}
\]

The linear map \(N\mapsto d_N\) has kernel exactly \(\mathbb C C\).
Indeed, multiplication by \(JC^{\mathsf T}\) is invertible and a
quadratic form vanishes identically exactly when its matrix is
skew-symmetric.  That kernel has dimension one, and \(CJC^{\mathsf T}\)
is skew-symmetric.  Therefore

\[
                         d_x\equiv0
              \quad\Longleftrightarrow\quad N_x\in\mathbb C C. \tag{16}
\]

Let \(g_U\) be the homogeneous gcd of the nonzero quadratics \(d_x\), with
the convention that \(g_U=0\) when all four vanish.  Then:

* if some \(d_x\ne0\), \(\deg g_U\le2\), so \(\mathscr R_U\) has at most
  two projective points, counted without multiplicity;
* if three distinct points of \(\mathscr Q_C\) satisfy all four rank-drop
  equations, then every \(d_x\) is zero and
  \(N_x\in\mathbb C C\) for all \(x\in U\);
* at each point of \(\mathscr R_U\), one still has to check
  \(\xi^{\mathsf T}K\eta\ne0\), \(\xi_e\eta_e\ne0\), and (10) or (11).

When \(K\notin\mathbb C C\), its restriction to \(\mathscr Q_C\) is a
nonzero binary quadratic, so curvature detection removes only finitely
many points.  The same is true of either target product
\(\xi_e\eta_e\).  These open conditions do not change the common-zero
requirement (8).

The quantifier correction is important.  If no selector is visible at all
four sites, it does **not** follow that some \(N_x\) is proportional to
\(C\).  For example take \(C=I\), write
\(\xi=(x,y)\), \(\eta=(-y,x)\), and choose

\[
 N_0=\begin{pmatrix}0&0\\0&1\end{pmatrix},\qquad
 N_1=J.
\]

Then

\[
                         d_0=xy,qquad d_1=x^2+y^2,         \tag{17}
\]

which have no common projective zero over \(\mathbb C\), while neither
matrix is proportional to \(C\).  Every \(N\) is realizable as a local
wedge matrix: take \(P_x=I\) and \(S_x=-JN\), so
\(P_x^{\mathsf T}JS_x=N\).  The first local \(P\)-map and a second local
\(S\)-map already make the two aggregate missing-label stars injective.
Thus injectivity of those two endpoint maps supplies no missing
finite-cover implication.

## 4. Rank-one full-square compression: two ruling gcds

Let

\[
                         C=a b^{\mathsf T}\ne0,             \tag{18}
\]

and choose nonzero \(\xi_0,\eta_0\) with

\[
                         \xi_0^{\mathsf T}a=0,qquad
                         b^{\mathsf T}\eta_0=0.
\]

The isotropic section is the union of two ruling lines

\[
 \mathscr Q_\xi=\{([\xi_0],[\eta]):[\eta]\in\mathbf P^1\},
 \qquad
 \mathscr Q_\eta=\{([\xi],[\eta_0]):[\xi]\in\mathbf P^1\}. \tag{19}
\]

On them, the local rank-drop equations are respectively

\[
 \xi_0^{\mathsf T}N_x\eta=0,qquad
 \xi^{\mathsf T}N_x\eta_0=0.                              \tag{20}
\]

Each is linear in the moving projective coordinate, and

\[
\begin{aligned}
 \xi_0^{\mathsf T}N_x=0
   &\Longleftrightarrow N_x=a w_x^{\mathsf T}
      \text{ for some }w_x,\\
 N_x\eta_0=0
   &\Longleftrightarrow N_x=w_x b^{\mathsf T}
      \text{ for some }w_x.                               \tag{21}
\end{aligned}
\]

Consequently, on either ruling, the common rank-drop locus is:

1. the whole ruling if all four corresponding linear forms vanish;
2. one projective point if all nonzero forms have the same kernel; or
3. empty if two forms have different kernels.

Two distinct common rank-drop points on \(\mathscr Q_\xi\) force
\(N_x=a w_x^{\mathsf T}\) for every \(x\); two on
\(\mathscr Q_\eta\) force \(N_x=w_x b^{\mathsf T}\) for every \(x\).

Not every ruling is eligible for a prescribed target and curvature.  For
target \(e\), the first ruling has a dense eligible open exactly when

\[
                         (\xi_0)_e\ne0,qquad
                         \xi_0^{\mathsf T}K\ne0,             \tag{22}
\]

and the second exactly when

\[
                         (\eta_0)_e\ne0,qquad
                         K\eta_0\ne0.                        \tag{23}
\]

On an eligible ruling, its zero, one, or infinite common rank-drop
candidates must again be filtered by (10)--(11).  This is the complete
singular classification for a full \(2\times2\) compression; a blanket
irreducible-conic argument would miss both the component eligibility and
the one-point common-kernel case.

## 5. An exact target-blocked dark-complement guard

The rank-drop obstruction is compatible with the positive inputs available
before the unused full-nine rows are invoked.  Work on sites
\(W=\{0,1,2,3,4,5\}\), use missing colours \(a=0,b=1\), and let
\(\delta=2\).  Put

\[
\begin{aligned}
 L&=x_{0,a}+x_{2,a}+x_{4,a},\\
 S&=x_{1,a}+x_{2,b}+x_{4,b},\\
 q&=x_{2,a}x_{3,a}+x_{4,a}x_{5,a},\\
 \beta&=LS.
\end{aligned}                                             \tag{24}
\]

Only the \(01\)-edge of \(\beta\) is disjoint from both supported edges of
\(q\).  Hence, with divided matching powers,

\[
                         \boxed{\beta q^{[2]}=X_a}.         \tag{25}
\]

At sites \(2\) and \(4\), the two local cap factors span the whole missing
plane:

\[
 H_2=H_4=\operatorname{span}(e_a,e_b),                    \tag{26}
\]

so the active target \(a\) is blocked there.  Their dark spaces are the
single \(\delta\)-covector lines.  Therefore the physical blocks
\(q_{23}=e_a\otimes e_a\) and \(q_{45}=e_a\otimes e_a\) both vanish on
the corresponding dark products.  Every other block of \(q\) is zero, so

\[
 q_{xy}|_{K_x\times K_y}=0
       \qquad(x\ne y\in\{2,3,4,5\}).                       \tag{27}
\]

The distinguished decorated coefficient is
\(\beta_{01}(a,a)=1\).  Thus (24)--(27) realize exact failure of the
physical dark-cut graph for that nonzero cap edge, with the target-blocked
alternative occurring exactly as predicted.

The same data fit the \(T=0\) curvature-bearing selector algebra.  On the
full missing square take

\[
 C=E_{bb},\qquad \ell=E_{aa},\qquad
 R=Q=e_a,\qquad U=0,qquad T=0,qquad
 K=UC-RQ^{\mathsf T}=-E_{aa}.                             \tag{28}
\]

Then

\[
 \ell(C)=0,qquad \ell(E_{aa})=1,qquad \ell(K)=-1,qquad
 [\beta]_{01;a,a}=-\ell(K)=1.                             \tag{29}
\]

The local values also have the required triangular orientation:
\(S_0=0\) and \(L_1=0\), so the reverse assignment vanishes.  Finally,
both selected endpoint stars extend injectively to three rows, for example

\[
 (p_a,p_b,p_\delta)=(L,x_{3,b},x_{5,\delta}),\qquad
 (s_a,s_b,s_\delta)=(S,x_{3,b},x_{5,\delta}).              \tag{30}
\]

This guard includes one literal diagonal full-nine row (25), the selected
curvature coefficient, pure-\(\delta\) darkness, and good-star extensions.
It is not an eight-site full-nine source: the other eight pair rows are not
asserted.  Therefore it does not refute a theorem that uses those rows.
It proves that neither goodness of these two displayed endpoint maps,
rank-one selection, the diagonal cap row, nor nonradial curvature can
separately eliminate the target-blocked incidence.  The omitted rows, the
other two good endpoint maps, and the two-chart overlap remain possible
additional inputs; the guard does not decide which of them is essential.

## 6. Exact scope and next usable statement

The target-blocked branch can now be stated without an incorrect genericity
heuristic:

For a full \(2\times2\) compression:

* for invertible \(C\), compute the gcd of the four binary quadratics
  (15); there are at most two candidate selectors unless all four wedge
  matrices lie in \(\mathbb C C\);
* for rank-one \(C\), compute one gcd of linear forms on each eligible
  ruling; there is at most one candidate per ruling unless the corresponding
  left or right alignments (21) hold;
* at those candidates apply the curvature, target, and coordinate-line
  filters exactly.

This is a finite **candidate** reduction on the full-square branch, not a
proof by avoiding finitely many bad points.  The rectangular branches need
their own one-parameter formulation.  A natural positive lemma would have
to show that additional full-nine/overlap identities force a common root
of the wedge forms, or force all of the alignments in (16) or (21) and then
exclude the coordinate-line residues.  Without such an identity, the
selector-conic variation runs in the wrong dimension.

The dependency-free checker
[`verify_target_blocked_incidence_rank_drop.py`](../computations/verify_target_blocked_incidence_rank_drop.py)
exhausts the local rank predicate over \(\mathbb F_3\), audits the
invertible and rank-one kernel classifications over \(\mathbb F_3\), and
replays all \(3^6\) decorated coefficients of the exact guard (24)--(30).
