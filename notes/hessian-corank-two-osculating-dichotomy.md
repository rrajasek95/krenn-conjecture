# The two-excess Hessian stratum has an osculating/common-line dichotomy

## 1. Outcome

This note continues
[`extra-hessian-corank-two-propagation.md`](extra-hessian-corank-two-propagation.md)
on the first surviving singular stratum

\[
                 \dim E_q=2,
 \qquad E_q:=\ker\mathcal H_q/\mathcal G_q.              \tag{1}
\]

On the connected spanning nonbipartite rank-three chart, with all six
deleted-star rows reaching at least three internal sites, the six
off-diagonal pair directions have a rigid projective configuration:
the two directions in every row and every column form a basis of `E_q`.
This has two consequences.

1. If the internal matching power is a nonzero pure target line, the
   second fundamental form on `E_q` cannot be injective.  Thus the
   Veronese-faithful curvature branch excludes that order-reduction
   boundary.
2. After quotienting lower osculating terms, the directed six-cycle
   identity gives one cubic relation.  If the third osculating map is
   injective, unique factorization forces
   
   \[
                         [K_{cd}]\parallel[K_{dc}]
                         \qquad(c\ne d).                 \tag{2}
   \]

   The proportionalities can be normalized simultaneously.  On every
   rank-three internal edge the resulting alternating star pencil either
   vanishes or has a common colour-kernel line at both endpoints.  This is
   an exact `3 by 3` singular-pencil classification, not a genericity
   assertion.

On the local-full branch the zero pencils propagate.  If the three-row
matrices of one star are invertible at every internal site, the two stars
become globally proportional and **every** internal block has the single
explicit form

\[
 q_{ij}={1\over\alpha_i+\alpha_j-b}\,
             P_iHP_j^{\mathsf T},                        \tag{3}
\]

where `H` is one fixed invertible symmetric zero-diagonal matrix.  A
zero-pencil edge whose endpoints have no common killed colour direction
already forces both local star pairs to be proportional invertible
matrices, with the same proportionality ratio.  Hence connectedness
reduces the entire no-common-line branch to this local-full form.  The
simultaneous orthogonal colour symmetry of this common matrix then makes
the off-diagonal equations kill every symmetric colour direction modulo
the common-power line.  The diagonal equations would put all three pure
targets on that line, a contradiction.  Thus corank exactly two is reduced
to two concrete exceptional loci:

* a kernel in the second or third osculating map;
* a common colour line killed by both deleted stars at one internal site.

These loci are not excluded here.  An exact local model below shows
that the common-line alternative is genuine: an alternating pencil can
have one-dimensional image spanned by an invertible matrix.  Globally, the
common line produces a common nonneighbor of the deleted pair in the
rank-three graph; on a triple shore it produces a pure three-cross selector
unless one explicit direct bilinear scalar is nonzero.

## 2. Pair equations and the six quotient directions

Retain the notation and normalization of the preceding note.  Thus `W`
has `2r` sites,

\[
 Q={q^r\over r!},\qquad
 \mathcal H_q(Z)={Zq^{r-1}\over(r-1)!},                  \tag{4}
\]

and the actual pair equations are

\[
 \mathcal H_q(p_cs_d)+a_{cd}Q=\delta_{cd}X_c.            \tag{5}
\]

Put

\[
 \lambda_{cd}=a_{cd}/r,
 \qquad K_{cd}=p_cs_d+\lambda_{cd}q.                    \tag{6}
\]

Then

\[
 \mathcal H_q(K_{cd})=\delta_{cd}X_c.                   \tag{7}
\]

For `c!=d`, let

\[
                              u_{cd}=[K_{cd}]\in E_q.     \tag{8}
\]

Assume throughout Sections 2--7 that

1. `G_3(q)` is connected, spanning, and nonbipartite;
2. every `p_c` and every `s_d` reaches at least three internal sites; and
3. `dim E_q=2`.

The one-product gauge lemma of the preceding note immediately sharpens.

**Lemma 2.1 (row-column basis lemma).**  For every fixed `d`, the two
vectors

\[
                         \{u_{cd}:c\ne d\}               \tag{9}
\]

form a basis of `E_q`.  For every fixed `c`, the two vectors
`{u_cd:d!=c}` also form a basis.

**Proof.**  Suppose, for a fixed `d`, that the two classes in (9) are
dependent.  A nonzero linear combination of the corresponding `K_cd`
is a vertex gauge.  It has the form

\[
 \left(\mu_cp_c+\mu_ep_e\right)s_d+bq\in\mathcal G_q,
 \qquad \{c,e,d\}=\{0,1,2\}.                             \tag{10}
\]

Since `s_d` reaches three sites, Lemma 3.1 of the preceding note gives
`mu_cp_c+mu_ep_e=0`.  Both rows are nonzero, so

\[
                              p_e=t p_c                  \tag{11}
\]

for a nonzero scalar `t`.

Use first the `c`-th column of (5).  Its diagonal and `e,c`
off-diagonal equations give

\[
 \mathcal H_q(p_cs_c)+a_{cc}Q=X_c,
 \qquad
 t\mathcal H_q(p_cs_c)+a_{ec}Q=0.                        \tag{12}
\]

Hence `X_c in C Q`.  The same calculation in column `e` gives
`X_e in C Q`.  This is impossible because `X_c,X_e` are independent
(and if `Q=0`, (12) already says `X_c=0`).  Thus (9) is independent and,
by (1), is a basis.  Interchanging the deleted endpoints proves the row
statement. `QED`

In particular all six `u_cd` are nonzero.  No two entries sharing a row
or sharing a column are projectively equal.

There is also an exact link to the three-hole exceptional branch.  The
canonical injection

\[
 {\ker\Psi_{j,r}\over\operatorname {im}\mathcal G_{j,r}}
 \hookrightarrow
 \operatorname {Hom}(\bar V_j^*,E_q)                    \tag{12a}
\]

from
[`three-hole-to-pair-hessian-injection.md`](three-hole-to-pair-hessian-injection.md)
is in fact an isomorphism.

**Proposition 2.2 (three-hole/Hessian quotient equivalence).**  Under the
connected nonbipartite graph hypothesis,

\[
 {\ker\Psi_{j,r}\over\operatorname {im}\mathcal G_{j,r}}
 \simeq \bar V_j\otimes E_q
 \simeq\operatorname {Hom}(\bar V_j^*,E_q).              \tag{12b}
\]

The displayed injection is this isomorphism.  In particular

\[
 \dim {\ker\Psi_{j,r}\over\operatorname {im}\mathcal G_{j,r}}
       =2\dim E_q.                                       \tag{12c}
\]

**Proof.**  Put

\[
 \mathcal M:\mathbb C\oplus(\mathcal R_W)_2
       \longrightarrow(\mathcal R_W)_{2r},
 \qquad \mathcal M(a,Z)=aC_j+\mathcal H_q(Z).            \tag{12d}
\]

After moving the unique barred `j` factor to the front, the definition of
the three-hole map is literally

\[
                         \Psi_{j,r}=I_{\bar V_j}\otimes\mathcal M.      \tag{12e}
\]

Euler's identity `H_q(q)=rC_j` gives an isomorphism

\[
 \ker\mathcal M\longrightarrow\mathbb C\oplus\ker\mathcal H_q,
 \qquad (a,Z)\longmapsto
          \left(a,Z+{a\over r}q\right).                 \tag{12f}
\]

For a scalar expansion tuple `(alpha_i)`, put `a=sum_i alpha_i` and
`beta_i=-alpha_i+a/(2r)`.  Since `|W|=2r`, this is an isomorphism

\[
 \mathbb C^W\longrightarrow
       \mathbb C\oplus\{(\beta_i):\sum_i\beta_i=0\}.     \tag{12g}
\]

Under (12f), the scalar expansion gauge is exactly `(a,Z^beta)`.
Tensoring (12g) with `bar V_j` therefore identifies the full expansion-
gauge image with

\[
 \bar V_j\otimes(\mathbb C\oplus\mathcal G_q)
       \subseteq\bar V_j\otimes
                   (\mathbb C\oplus\ker\mathcal H_q).   \tag{12h}
\]

The graph hypothesis makes the Hessian gauge parametrization injective,
so quotienting (12h) proves (12b).  Contracting the first tensor factor is
exactly the map `Theta` in (12a), proving that the earlier injection is the
same isomorphism. `QED`

Thus three-hole excess and pair-Hessian excess are not merely linked; at a
fixed `j` they are the same quotient tensored by the two-dimensional
barred slot.  In particular, an intrinsic dimension bound or comparison
of the three colours cannot by itself contradict Hessian corank two.

There is nevertheless extra information in the distinguished star class.

**Corollary 2.3 (maximal distinguished orbit at corank two).**  Suppose
the pair data come from an actual full source, with deleted vertices the
fixed star centre and `j`.  Under the assumptions of Section 2,

\[
 \dim {\ker\Psi_{j,r}\over\operatorname {im}\mathcal G_{j,r}}=4
                                                        \tag{12i}
\]

for every colour `r`.  The quotient is spanned by the barred-slot
endomorphism orbit of the distinguished kernel vector supplied by the
colour-`r` star equation.

**Proof.**  Under (12a), the distinguished vector is sent to the map whose
two coordinate contractions are

\[
                         e_d^*\longmapsto u_{rd}
                         \qquad(d\ne r).                 \tag{12j}
\]

The row part of Lemma 2.1 says that these two images form a basis of the
two-space `E_q`.  Hence (12j) is an isomorphism
`bar V_j^* -> E_q`.

Every endomorphism `L` of the unique barred `j` slot preserves
`ker Psi_(j,r)` and preserves its expansion-gauge subspace.  Contraction
shows that its image under (12a) is right composition by `L^*`:

\[
                         \Theta(Lv)=\Theta(v)\circ L^*.  \tag{12k}
\]

Since `Theta(v)` is invertible, the four matrix units in
`End(bar V_j)` give all four dimensions of
`Hom(bar V_j^*,E_q)`.  Their quotient classes are independent by the
injection (12a).  The same injection gives the opposite upper bound four,
proving (12i). `QED`

Thus quotient Hessian corank exactly two does not merely make the
three-hole map singular: it puts every actual row-derived three-hole map
on its maximal possible four-dimensional excess locus.

## 3. Second curvature: line, secant, or Veronese

The gauge-descended second fundamental form is

\[
 \mathrm {II}_q:\operatorname {Sym}^2E_q\longrightarrow
   \operatorname {coker}\mathcal H_q,
 \qquad
 [U][V]\longmapsto
 \left[{UVq^{r-2}\over(r-2)!}\right].                  \tag{13}
\]

For a two-dimensional `E_q`, its possibilities have a literal binary-
quadratic classification.

* If `rank II_q=3`, it is injective; projectively it retains the full
  quadratic Veronese conic.
* If `rank II_q=2`, its one-dimensional kernel is generated by a binary
  quadratic `ell_1 ell_2`.  For distinct factors this is a secant relation
  `II(ell_1,ell_2)=0`; for a repeated factor it is a tangent relation
  `II(ell,ell)=0`.
* If `rank II_q<=1`, every second-curvature value lies on one common
  output line (or is zero).

This is just factorization of a binary quadratic over `C`; it is recorded
because the first case has an exact consequence for the pair system.

**Theorem 3.1 (pure internal power forces second degeneracy).**  Suppose

\[
                              Q=\kappa X_h,
 \qquad \kappa\ne0                                      \tag{14}
\]

for one colour `h`.  Then `II_q` is not injective.

**Proof.**  Since `H_q(q)=rQ`, the quadratic

\[
                    L_{hh}=K_{hh}-{1\over r\kappa}q      \tag{15}
\]

lies in `ker H_q`; let `u_hh` be its class in `E_q`.
Let `{h,c,d}={0,1,2}`.  The physical rank-one identity

\[
                         (p_hs_h)(p_cs_d)
                            =(p_hs_d)(p_cs_h)             \tag{16}
\]

and (15) give, modulo `im H_q`,

\[
                    \mathrm {II}_q(u_{hh},u_{cd})
                       =\mathrm {II}_q(u_{hd},u_{ch}).   \tag{17}
\]

All terms introduced by adding a multiple of `q` disappear in the
cokernel: `S_q(q,U)=(r-1)H_q(U)` for a kernel vector `U`, and
`S_q(q,q)=r(r-1)Q` lies in the Hessian image.

If `II_q` were injective, (17) would be the equality

\[
                         u_{hh}u_{cd}=u_{hd}u_{ch}        \tag{18}
\]

in the polynomial ring `Sym(E_q)`.  Its right side is nonzero by
Lemma 2.1, so `u_hh` is nonzero.  Unique factorization says that the factor
`u_cd` is proportional to either `u_hd` or `u_ch`.  The first pair shares
column `d`, and the second pair shares row `c`; both proportionalities are
forbidden by Lemma 2.1.  This contradiction proves the theorem. `QED`

Thus the exceptional branch `Q in C X_h`, which otherwise prevents a
simple quotient-flattening argument, is already forced off the Veronese-
faithful second-curvature chart.

## 4. The third osculating symbol and the six-cycle

Assume `r>=3`; the omitted case has four internal sites and belongs to the
already-complete six-vertex theorem.  Write

\[
 \mathsf S_q(U,V)={UVq^{r-2}\over(r-2)!},\qquad
 \mathsf T_q(U,V,Z)={UVZq^{r-3}\over(r-3)!}.             \tag{19}
\]

To remove choices of kernel representatives and all lower osculating
corrections, let `L_q^(3)` be the span in the top-support space of

\[
 \operatorname {im}\mathcal H_q,
 \quad \mathsf S_q(\ker\mathcal H_q,(\mathcal R_W)_2),
 \quad \mathsf T_q(\mathcal G_q,\ker\mathcal H_q,
                                    \ker\mathcal H_q).   \tag{20}
\]

By construction, the symmetric trilinear map descends to

\[
 \mathrm {III}_q:\operatorname {Sym}^3E_q
       \longrightarrow (\mathcal R_W)_{2r}/L_q^{(3)}.   \tag{21}
\]

Call the third symbol **faithful** when (21) is injective.  This is an
explicit finite-rank condition on the actual common powers, not an
assumption that a kernel direction integrates.

The off-diagonal products form the six-cycle toric configuration.  Their
unique primitive binomial is

\[
 (p_0s_1)(p_1s_2)(p_2s_0)
       =(p_0s_2)(p_2s_1)(p_1s_0).                        \tag{22}
\]

Equation (26) of the preceding note expands (22).  Its lower terms lie in
(20), so

\[
 \mathrm {III}_q(u_{01}u_{12}u_{20})
       =\mathrm {III}_q(u_{02}u_{21}u_{10}).             \tag{23}
\]

**Theorem 4.1 (faithful cubic gives the symmetric triangle).**  If
`III_q` is faithful, then

\[
 u_{01}\parallel u_{10},\qquad
 u_{12}\parallel u_{21},\qquad
 u_{20}\parallel u_{02}.                                \tag{24}
\]

Moreover the three proportionality constants have product one in the
orientation of (22), so they can be removed simultaneously by nonzero
diagonal rescalings of the two deleted colour spaces.

**Proof.**  Faithfulness turns (23) into equality of two products of three
linear forms in the UFD `Sym(E_q)=C[x,y]`.  Consider the factor `u_01`.
It cannot be proportional to `u_02`, because those two share row zero, and
it cannot be proportional to `u_21`, because those two share column one.
Lemma 2.1 therefore forces `u_01 parallel u_10`.  The same argument
cyclically gives the other two statements.

Substitution in (23) shows that the product of the three scalars is one.
Consequently there are nonzero `rho_0,rho_1,rho_2` such that, after
replacing `s_d` and `a_cd` by `s_d/rho_d` and `a_cd/rho_d`, the normalized
classes satisfy

\[
                              u_{cd}=u_{dc}\quad(c\ne d). \tag{25}
\]

The right side of the `d,d` equation is merely rescaled by the nonzero
factor `rho_d`; its purity and independence are unchanged. `QED`

If (21) is not faithful, its nonzero kernel is an explicit binary cubic,
which over `C` factors into one, two, or three projective directions with
multiplicity.  Thus failure is itself a concrete third-osculating
degeneracy, rather than an unspecified “higher compatibility” branch.

## 5. A rank-one alternating pencil with invertible image

Under the normalization (25), each difference `K_cd-K_dc` is a vertex
gauge.  At an internal site `i`, package the three local row vectors as
the columns of matrices

\[
 P_i=(p_{0,i}\ p_{1,i}\ p_{2,i}),\qquad
 S_i=(s_{0,i}\ s_{1,i}\ s_{2,i}).                       \tag{26}
\]

For an edge `ij`, define the alternating pencil

\[
 \mathcal L_{ij}:\Lambda^2\mathbb C^3\longrightarrow
                    V_i\otimes V_j,
 \qquad
 \mathcal L_{ij}(M)=P_iMS_j^{\mathsf T}
                         -S_iMP_j^{\mathsf T}.           \tag{27}
\]

The three basis values are exactly the blocks of
`p_cs_d-p_ds_c`.  Since each difference is a gauge plus a scalar multiple
of `q`, on every edge of `G_3(q)` one has

\[
                         \operatorname {im}\mathcal L_{ij}
                                  \subseteq\mathbb Cq_{ij}.             \tag{28}
\]

The following elementary classification is the local boundary.

**Lemma 5.1 (invertible one-line alternating pencil).**  Let
`A,B,C,D` be `3 by 3` matrices and define

\[
 \mathcal L(M)=AMB^{\mathsf T}-CMD^{\mathsf T}
                  \qquad(M\in\Lambda^2\mathbb C^3).     \tag{29}
\]

If `im L` is one-dimensional and is spanned by an invertible matrix, then
there is a nonzero vector `ell` such that

\[
                         A\ell=C\ell=B\ell=D\ell=0.      \tag{30}
\]

**Proof.**  The kernel of `L` is a two-plane in `Lambda^2 C^3`.  Every
such plane has the form `ell wedge C^3`; choose coordinates with
`ell=e_3`.  Write the columns of the four matrices as
`a_i,b_i,c_i,d_i`.  Vanishing on `e_2 wedge e_3` and
`e_3 wedge e_1` says

\[
\begin{aligned}
 a_2b_3^{\mathsf T}-a_3b_2^{\mathsf T}
   -c_2d_3^{\mathsf T}+c_3d_2^{\mathsf T}&=0,\\
 a_3b_1^{\mathsf T}-a_1b_3^{\mathsf T}
   -c_3d_1^{\mathsf T}+c_1d_3^{\mathsf T}&=0.           \tag{31}
\end{aligned}
\]

Passing first to the quotient by `span(a_3,c_3)` shows that if
`b_3,d_3` were independent, all four of `a_1,a_2,c_1,c_2` would lie in a
two-space; the remaining value of `L` would have rank at most two.
Thus `b_3,d_3` are dependent.  Transposing the argument shows that
`a_3,c_3` are dependent.

Suppose both spans are nonzero.  The expression (29) has the elementary
`GL_2` freedom which changes the two summands on the left and makes the
inverse change on the two right summands.  If the two coefficient lines
have nonzero pairing under this freedom, they may be normalized so that
`a_3,b_3` are nonzero.  Write
`c_3=kappa a_3`, `d_3=mu b_3`.  Equations (31) give scalars `t_1,t_2`
with

\[
\begin{array}{ll}
 a_1=\mu c_1-t_1a_3,&b_1=\kappa d_1-t_1b_3,\\
 a_2=\mu c_2+t_2a_3,&b_2=\kappa d_2+t_2b_3.
\end{array}                                               \tag{32}
\]

Relative to the left vectors `(c_1,c_2,a_3)` and right vectors
`(d_1,d_2,b_3)`, the remaining value
`L(e_1 wedge e_2)` has coefficient matrix

\[
 \begin{pmatrix}
 0&\mu\kappa-1&\mu t_2\\
 1-\mu\kappa&0&\mu t_1\\
 -\kappa t_2&-\kappa t_1&0
 \end{pmatrix},                                         \tag{33}
\]

whose determinant is zero.  It therefore cannot be invertible.  If one
of the two spans is zero, (31) gives the same rank-at-most-two conclusion
unless the other span is also zero.  In the remaining zero-pairing case,
the same `GL_2` freedom gives

\[
 a_3=a,\quad c_3=0,\qquad b_3=0,\quad d_3=b.
\]

Equations (31) then put `b_1,b_2` on the line `C b` and put
`c_1,c_2` on the line `C a`.  The remaining value of `L` is a sum of a
matrix with one-dimensional row space `C b^T` and a matrix with
one-dimensional column space `C a`; it again has rank at most two.
Hence
`a_3=c_3=b_3=d_3=0`, which is exactly (30). `QED`

The conclusion is sharp.  Take all four matrices to have third column
zero and choose their first two columns so that the sole value on
`e_1 wedge e_2` is the identity.  Section 8 gives an exact integer model.

Applied to (27)--(28), Lemma 5.1 says:

\[
 \boxed{\quad
 \mathcal L_{ij}\ne0
 \Longrightarrow
 \ker P_i\cap\ker S_i\cap\ker P_j\cap\ker S_j\ne0
 \quad(ij\in G_3(q)).                                    \tag{34}
\]

Thus every nonzero alternating response on a rank-three edge propagates a
literal common colour direction killed by both stars at both endpoints.

The zero response has the same conclusion unless both local star pairs
are invertibly proportional.

**Lemma 5.2 (zero pencil without a common kernel).**  Suppose
`L_ij=0` and

\[
 \ker P_i\cap\ker S_i=0,
 \qquad
 \ker P_j\cap\ker S_j=0.                               \tag{34a}
\]

Then there are invertible matrices `R_i,R_j` and nonzero coefficient
pairs `(a_i,b_i),(a_j,b_j)` such that

\[
 P_i=a_iR_i,\quad S_i=b_iR_i,
 \qquad
 P_j=a_jR_j,\quad S_j=b_jR_j,                           \tag{34b}
\]

and

\[
                         a_i b_j-b_i a_j=0.             \tag{34c}
\]

**Proof.**  Let `U=C^3` be the colour space.  Contract (27) by arbitrary
covectors `phi in V_i^*` and `psi in V_j^*`, and put

\[
 x=\phi P_i,\quad y=\phi S_i,
 \qquad x'=\psi P_j,\quad y'=\psi S_j\in U^*.
\]

Vanishing for every alternating matrix `M` is exactly

\[
                              x\wedge y'=y\wedge x'.    \tag{34d}
\]

If `x,y` were independent, wedging (34d) first with `x` and then with
`y` would put both `x'` and `y'` in `span(x,y)`.  As `psi` varies, the
combined row space of `P_j,S_j` would have dimension at most two.  This is
equivalent to a nonzero vector in `ker P_j intersect ker S_j`, contrary to
(34a).  Hence `phi P_i` and `phi S_i` are dependent for every `phi`.
The symmetric argument gives the analogous statement at `j`.

We use the elementary two-operator local-dependence fact: if linear maps
`A,B:X->Y` have `Ax,Bx` dependent for every `x`, and
`im A+im B` has dimension at least three, then `A,B` are linearly
dependent.  Indeed, if `rank A>=2`, choose `x_1,x_2` with independent
images.  Dependence at `x_1,x_2,x_1+x_2` gives one scalar `t` on their
span; comparison with these two vectors shows `B=tA` on every other
vector, including `ker A`.  If `rank A<=1`, then `rank B>=2` and the same
argument is applied with the maps interchanged.

Apply this fact to `P_i^T,S_i^T`.  Condition (34a) says that their combined
image is all of `U^*`, so `P_i,S_i` are linearly dependent.  Their nonzero
common matrix must have rank three, again by (34a).  This proves the first
half of (34b), and the other endpoint is identical.  Finally (27) becomes

\[
             (a_i b_j-b_i a_j)R_iMR_j^{\mathsf T}=0
             \qquad(M\in\Lambda^2U).
\]

The two `R` matrices are invertible and some `M` is nonzero, which gives
(34c). `QED`

## 6. The zero-pencil and local-full branch

There is an equally rigid zero case.

**Lemma 6.1 (zero alternating pencil).**  If `P_i,P_j` are invertible and
`L_ij=0`, then there is a scalar `t_ij` such that

\[
                         S_i=t_{ij}P_i,
 \qquad                  S_j=t_{ij}P_j.                  \tag{35}
\]

**Proof.**  Put `A_i=P_i^(-1)S_i` and `A_j=P_j^(-1)S_j`.
Equation (27) becomes

\[
                         MA_j^{\mathsf T}=A_iM
                  \quad(M\in\Lambda^2\mathbb C^3).      \tag{36}
\]

Using successively the three elementary skew matrices shows that all
off-diagonal entries of `A_i,A_j` vanish and their three diagonal entries
are equal to one common scalar.  This gives (35). `QED`

Return now to the faithful-third-symbol normalization (25), and suppose
that no internal site has a common colour-kernel line:

\[
                         \ker P_i\cap\ker S_i=0
                         \qquad(i\in W).                 \tag{36a}
\]

Equation (34) makes every pencil (27) zero on `G_3(q)`.  Lemma 5.2 says
that at every endpoint the two local matrices are proportional to an
invertible matrix, and that their projective proportionality ratio is the
same across an edge.  Connectedness gives one global ratio.  Neither
coordinate of that ratio can vanish: otherwise every `P_i`, or every
`S_i`, would vanish, contrary to the row-support assumptions of Section 2.
Consequently every `P_i` is invertible and there is one nonzero scalar `t`
with

\[
                              s_c=t p_c\qquad(c=0,1,2).   \tag{37}
\]

The three unordered classes `u_01,u_12,u_20` have kernel representatives
of the form `t p_cp_d+lambda_cd q`.  They are pairwise distinct by
Lemma 2.1 but lie in the two-space `E_q`.  Their unique linear relation
has all coefficients nonzero.  Expanding that relation and absorbing its
`q` coefficient gives an invertible symmetric zero-diagonal matrix

\[
 H=\begin{pmatrix}0&h_{01}&h_{20}\\h_{01}&0&h_{12}\\
                    h_{20}&h_{12}&0\end{pmatrix},
 \qquad h_{01}h_{12}h_{20}\ne0,                         \tag{38}
\]

and a gauge `Z^alpha` such that

\[
                         \sum_{c<d}h_{cd}p_cp_d+bq
                              =Z^\alpha.                 \tag{39}
\]

On every pair `ij`, (39) reads

\[
                         P_iHP_j^{\mathsf T}
                         =(\alpha_i+\alpha_j-b)q_{ij}.   \tag{40}
\]

The left side is invertible for every pair.  Hence

\[
 \alpha_i+\alpha_j-b\ne0,
 \qquad \operatorname {rank}q_{ij}=3                    \tag{41}
\]

for every `i<j`, not merely for the pairs originally in `G_3(q)`.  Thus
`G_3(q)` is complete and (40) is exactly (3) on every pair.

The full pair equations exclude this residual form.

**Theorem 6.2 (common-matrix diagonal obstruction).**  Equations (5)
cannot hold on the local-full branch above.

**Proof.**  Apply `P_i^(-1)` at each internal site.  The local columns of
the three `p_c` become the standard colour basis, while (3) becomes

\[
             q_{ij}=w_{ij}H,
 \qquad      p_c=\sum_i e_c^{(i)},
 \qquad      s_c=t p_c,                                 \tag{42}
\]

where `w_ij=(alpha_i+alpha_j-b)^(-1)` and `t!=0`.  These invertible site
changes preserve the nonzeroness and linear independence of the three
targets.

Let `V=C^3`, let `p(u)=sum_i u^(i)`, and define

\[
 \Phi:\operatorname {Sym}^2V\longrightarrow
             \bigotimes_{i\in W}V_i,
 \qquad
 \Phi(u\mathbin\odot v)=\mathcal H_q(p(u)p(v)).         \tag{43}
\]

The group

\[
        G=\{g\in\operatorname {SL}(V):gHg^{\mathsf T}=H\}
          \simeq SO_3(\mathbb C)                        \tag{44}
\]

fixes `q` and `Q`, and `Phi` is equivariant for its congruence action.
Consequently the kernel of the induced map

\[
 \overline\Phi:\operatorname {Sym}^2V\longrightarrow
       \left(\bigotimes_{i\in W}V_i\right)/\mathbb C Q \tag{45}
\]

is `G`-invariant.  The off-diagonal equations in (5), together with
`t!=0`, put the three matrices `E_cd+E_dc`, `c<d`, in this kernel.

Their span `K` is the full zero-diagonal symmetric subspace.  Since `H`
is zero-diagonal, `H in K`.  Under `G`,

\[
 \operatorname {Sym}^2V=\mathbb C H\oplus
   \{U:\operatorname {tr}(H^{-1}U)=0\}.                \tag{46}
\]

The second summand is the irreducible five-dimensional traceless
symmetric representation of `SO_3(C)`.  The invariant trace is nonzero on
`K` (indeed its value on `H` is three), so `K` also contains a nonzero
trace-free vector.  Its invariant span is therefore both summands in
(46), hence all of `Sym^2 V`.  Thus `bar Phi=0`.

The three diagonal equations in (5), reduced modulo `C Q`, now give
`[X_c]=0` for every `c`.  This puts three independent nonzero target
tensors in one line, a contradiction. `QED`

A detailed independent proof and exact irreducibility audit appear in
[`cauchy-shared-matrix-diagonal-obstruction.md`](cauchy-shared-matrix-diagonal-obstruction.md).

**Theorem 6.3 (corank-two osculating dichotomy).**  Under the hypotheses
of Section 2, at least one of the following holds.

1. `III_q` has a nonzero cubic kernel.
2. After the harmless diagonal normalization in Theorem 4.1, there are an
   internal site `i` and a nonzero colour vector `ell` such that

   \[
                              P_i\ell=S_i\ell=0.          \tag{46a}
   \]

**Proof.**  If the first alternative fails, Theorem 4.1 supplies the
normalization (25).  A nonzero pencil on `G_3(q)` gives (46a) directly by
Lemma 5.1.  If every pencil is zero and (46a) never occurs, Lemma 5.2 and
connectedness give (36a)--(37), hence the local-full common-matrix chart
(40).  Theorem 6.2 excludes that chart. `QED`

If additionally `Q` is a nonzero pure target tensor, then either
alternative 1 or 2 occurs together with a nonzero kernel of `II_q`, by
Theorem 3.1.

## 7. Global rank-graph and triple-shore footprint

Return to the original full source and write `A_xy` for its aggregate
endpoint-oriented blocks.  The common line in (46a) is a relation among
the rows at each deleted endpoint.  Undoing the nonzero diagonal colour
rescaling used in Theorem 4.1 gives covectors `xi in V_p^*` and
`eta in V_q^*` with the same coordinate support and

\[
                    \xi^{\mathsf T}A_{pi}=0,
 \qquad             \eta^{\mathsf T}A_{qi}=0.           \tag{46b}
\]

In particular both incident blocks have rank at most two.

**Corollary 7.1 (common nonneighbor in the rank-three graph).**  Let

\[
                  R=\{xy:\operatorname {rank}A_{xy}=3\}.
\]

If `III_q` is faithful in the pair chart obtained by deleting `p,q`, then
some internal site `i` obeys

\[
                              pi,qi\notin R.             \tag{46c}
\]

Consequently, if the hypotheses of Section 2 and third-symbol faithfulness
hold after every deletion of two vertices, then every pair `p,q` has a
common neighbor in the complement graph `bar R`.  In particular `bar R`
has minimum degree at least two, has diameter at most two, and every one of
its edges lies in a triangle.

**Proof.**  Theorem 6.3 gives (46b), which proves (46c).  Apply this to
every pair.  The common-nonneighbor statement is precisely the assertion
that every two vertices have a common neighbor in `bar R`; it gives the
diameter and triangle claims.  A vertex of complement degree zero is
immediately impossible.  If `p` had the unique complement neighbor `q`,
applying the assertion to the pair `p,q` would produce a second complement
neighbor of `p`. `QED`

There is also a direct bridge to the triple-shore selector normal form.
Put `C={p,q,i}`, `U=B\setminus C`, and split the matching tensor as
`T_1+T_3` according to whether a matching crosses the cut `C|U` once or
three times.

**Proposition 7.2 (common-line selector or direct obstruction).**  Suppose
(46b) holds.  If

\[
                          \xi^{\mathsf T}A_{pq}\eta=0,   \tag{46d}
\]

then the triple shore `C` has a pure three-cross selector: for every colour
`r` in the common coordinate support of `xi,eta`, there is a product
covector `Theta in V_C^*` such that

\[
 \Theta(e_s^{\otimes C})=\delta_{rs},qquad
 (\Theta\otimes I)T_1=0,qquad
 (\Theta\otimes I)T_3=e_r^{\otimes U}.                 \tag{46e}
\]

Thus a common-kernel site either gives the explicit selector (46e), or it
lies on the equally explicit nonisotropic boundary
`xi^T A_pq eta != 0`.

**Proof.**  Choose `r` with `xi_r eta_r!=0`, which is possible because the
two covectors have the same nonempty coordinate support, and let

\[
 \theta_s=\begin{cases}(\xi_r\eta_r)^{-1},&s=r,\\0,&s\ne r,
             \end{cases}
 \qquad \Theta=\xi\otimes\eta\otimes\theta.            \tag{46f}
\]

The one-crossing expansion is

\[
                T_1=A_{qi}\otimes R_p+A_{pi}\otimes R_q
                                  +A_{pq}\otimes R_i,    \tag{46g}
\]

with tensor slots restored to the order `p,q,i,U`.  The first summand is
killed by `eta^T A_qi=0`, the second by `xi^T A_pi=0`, and the third by
(46d).  Hence `Theta` kills `T_1`.  Formula (46f) gives its displayed
values on the three constant tensors.  Applying it to
`T_1+T_3=Delta_(B,3)` proves the last identity in (46e). `QED`

The implication (46e) is exactly the row-degenerate alternative of
[`five-set-contamination-normal-form.md`](five-set-contamination-normal-form.md),
but here its covector is constructed from the corank-two Hessian geometry.

When the deleted block is invertible, the three-shore normal form makes
this boundary substantially sharper.

**Proposition 7.3 (invertible-pair selector/coordinate-row dichotomy).**
Assume `A_pq` is invertible and that (46b) comes from alternative 2 of
Theorem 6.3.  Then at least one of the following holds for the shore
`C={p,q,i}`.

1. A constant one-crossing row is in the mixed-row span.  Consequently
   `C` carries a pure three-cross selector as in Corollary 2.3 of
   [`five-set-contamination-normal-form.md`](five-set-contamination-normal-form.md).
2. The common coordinate support of `xi,eta` is a singleton `{r}`.  Thus
   row `r` of both `A_pi` and `A_qi` is zero, while

   \[
                               (A_{pq})_{rr}\ne0.         \tag{46h}
   \]

**Proof.**  Suppose the first alternative fails.  All three constant
one-crossing residues are then nonzero.  Since `A_pq` is invertible while
the two matrices in (46b) are singular, Corollary 3.2 of the cited note
puts this shore in the cyclic staircase form.  Relabel the vertices so
that `x=p,y=q,z=i`; after a simultaneous colour permutation and harmless
nonzero scalar divisions, the three matrices are

\[
\begin{aligned}
 A_{qi}&=E_{00}+b_0^{-1}(e_1u^{\mathsf T}+ve_2^{\mathsf T}),\\
 A_{pi}&=E_{11}+b_1^{-1}(-e_0u^{\mathsf T}+we_2^{\mathsf T}),\\
 A_{pq}&=E_{22}+b_2^{-1}(-e_0v^{\mathsf T}-we_1^{\mathsf T}).
                                                               \tag{46i}
\end{aligned}
\]

Write `xi=(x_0,x_1,x_2)^T` and `eta=(y_0,y_1,y_2)^T`.  The first two
columns of the two left-kernel equations in (46b) give

\[
 x_0u_0=0,qquad x_1=b_1^{-1}x_0u_1,
 \qquad
 y_0=-b_0^{-1}y_1u_0,qquad y_1u_1=0.                  \tag{46j}
\]

If `x_0!=0`, then `u_0=0`, and (46j) gives `y_0=0`, contrary to equality
of the two coordinate supports.  Hence `x_0=0`, and then `x_1=0`.
The common nonempty support is therefore `{2}`, so `y_0=y_1=0` as well.
The `(2,2)` entry of the last matrix in (46i) is one.  Restoring the
nonzero scalar and undoing the simultaneous colour permutation gives
(46h). `QED`

Thus, at an invertible pair, the common-line branch is not an arbitrary
rank-two incident-block locus: it is either an exact triple-shore selector
or a named coordinate row missing simultaneously from both incident
blocks.  This is the form suited to overlap with zero-row propagation and
selector identities.

## 8. What remains

The theorem does not close quotient corank exactly two unconditionally.
It replaces that locus by an explicit lower-rank condition at the third
osculating level or a common-line condition on the physical star matrices.
Neither is an arbitrary Hessian-matrix condition:

* `II_q` and `III_q` use `q^(r-2)` and `q^(r-3)` from the same common
  power;
* the six-cycle comes from the actual factorization `p_cs_d`;
* (34) and (46a) are literal common kernels of endpoint-ordered `3 by 3`
  star matrices; and
* the only all-local-full escape has been excluded using the exact
  off-diagonal and diagonal pair equations.

The next useful attack is correspondingly narrow: propagate the coordinate
row in Proposition 7.3 through an overlapping deleted-pair chart, or
combine its alternative selector with another triple shore.
Merely assuming that an excess direction integrates is still invalid by
`source-hessian-nonintegrability-countermodel.md`.

## 9. Exact audit and sharp local model

[`verify_hessian_corank_two_osculation.py`](../computations/verify_hessian_corank_two_osculation.py)
checks the UFD projective classification, the determinant-zero matrix in
(33), both zero-pencil classifications (including the contracted wedge and
local-dependence calculations in Lemma 5.2), and the blockwise Cauchy
identity (39)--(40) over the rationals.  The companion verifier
[`verify_cauchy_shared_matrix_diagonal_obstruction.py`](../computations/verify_cauchy_shared_matrix_diagonal_obstruction.py)
checks the invariant trace decomposition and exact irreducibility input in
Theorem 6.2.  The first verifier also checks a rational rank-two common-line
site and its product selector from Proposition 7.2.

It also checks the following sharp integer model for Lemma 5.1.  With
`E_ab=e_a e_b^T`, take

\[
\begin{array}{ll}
 A=(-e_1\ e_0\ 0),&B=(e_0\ e_1\ 0),\\
 C=(e_2\ 0\ 0),&D=(0\ e_2\ 0).
\end{array}                                               \tag{47}
\]

Then `L(e_2 wedge e_3)=L(e_3 wedge e_1)=0` while

\[
                         \mathcal L(e_1\wedge e_2)=I_3.  \tag{48}
\]

All four matrices have the common kernel `Ce_3`.  Thus a rank-three
internal block does not by itself eliminate the one-line pencil; the
common-line alternative in Theorem 6.3 is necessary.
