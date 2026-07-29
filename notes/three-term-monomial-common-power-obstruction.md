# Three monomials in one colour still have no common-power lift

## 1. Result

Let \(U\) be a six-set.  At every site \(u\), let \(V_u\) contain
distinguished independent vectors

\[
 e_0^{(u)},e_1^{(u)},e_2^{(u)}.
\]

For a pair \(P\subset U\), put

\[
 E_i(P)=\bigotimes_{u\notin P}e_i^{(u)},\qquad
 X_i=\bigotimes_{u\in U}e_i^{(u)}.
\]

Choose three distinct pairs \(A_1,A_2,A_3\), two initially arbitrary pairs
\(C,D\), and nonzero complex coefficients
\(\lambda_1,\lambda_2,\lambda_3,\gamma,\delta\).  Set

\[
 F=\sum_{r=1}^3\lambda_rE_0(A_r)
      +\gamma E_1(C)+\delta E_2(D).                    \tag{1}
\]

Allow six completely arbitrary star rows

\[
 p_0,p_1,p_2,s_0,s_1,s_2\in\bigoplus_{u\in U}V_u
\]

and retain all nine exact products

\[
                         p_i s_jF=\delta_{ij}X_i.       \tag{2}
\]

**Theorem 1.1 (three-term monomial obstruction).**  Equations (1)--(2)
admit no six-site quadratic \(q\) satisfying

\[
                         q^{[2]}=F,\qquad q^{[3]}=0.    \tag{3}
\]

The bracket powers are unordered matching sums.  The star rows may have
arbitrary multi-site support, arbitrary directions outside the three
displayed axes, arbitrary endpoint order, and arbitrary complex
cancellation.

The proof has three exact parts.

1. The product table forces all five missing pairs
   \(A_1,A_2,A_3,C,D\) to be distinct.
2. The equation \(qF=0\), forced by (3), is a weighted graph-incidence
   kernel.  Its dimensions are computed by hand for all five three-edge
   graph shapes.  A local diagonal torus then normalizes every nonzero
   coefficient in (1); no weight modulus survives, including for the
   \(3K_2\) shape.
3. The \(60{,}060\) labelled supports form 70 exact orbits.  After
   substituting the complete \(qF\) kernel, every full affine ideal of
   coefficients of \(q^{[2]}-F\) is the unit ideal over \(\mathbb Q\).

The standalone checker
[verify_three_term_monomial_common_power_obstruction.py](../computations/verify_three_term_monomial_common_power_obstruction.py)
audits the support census, torus-character ranks, complete \(qF\) kernels,
frozen ledgers, and all 70 unit ideals.

## 2. The products force five distinct supports

Work in the site-square-zero algebra

\[
 \mathcal R_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u),
 \qquad V_uV_u=0.                                      \tag{4}
\]

For \(P=\{a,b\}\), multiplication by \(E_k(P)\) retains exactly the
two endpoint orders

\[
 B_{ij}(P)=p_{i,a}\otimes s_{j,b}
              +s_{j,a}\otimes p_{i,b}\in V_a\otimes V_b. \tag{5}
\]

Extend the three displayed local vectors to bases.  The response space of
\(E_k(P)\) is spanned by the coordinate words which are fixed to colour
\(k\) outside \(P\) and arbitrary on \(P\).  Response spaces belonging to
different colours have disjoint coordinate-word supports: two pairs cover
at most four of the six sites, leaving a site fixed to two distinct
coordinate colours.

Apply (2) to row \((1,1)\).  Its colour-one part gives

\[
 B_{11}(C)=\gamma^{-1}e_1^{\otimes C}\ne0.             \tag{6}
\]

If \(C=D\), the colour-two component of the same row requires the identical
tensor \(B_{11}(C)\) to vanish, a contradiction.

Suppose instead that \(C=A_r\).  In the colour-zero part of this row, the
term from \(A_r\) contains the coordinate word which is \(e_1\) at both
sites of \(A_r\) and \(e_0\) elsewhere.  A response from another distinct
pair \(A_s\) cannot contain this word: both sites carrying the nonzero
deviation from \(e_0\) would have to lie in \(A_s\), forcing
\(A_s=A_r\).  Thus this nonzero word cannot cancel, again a contradiction.
Hence \(C\) differs from all three \(A_r\)'s and from \(D\).

The same argument applied to row \((2,2)\) shows that \(D\) differs from
every \(A_r\).  Therefore

\[
                         A_1,A_2,A_3,C,D
                         \quad\text{are all distinct}. \tag{7}
\]

This is the only use of the product table in the rest of the proof.
Equation (5) shows explicitly that no endpoint orientation was suppressed.

## 3. The full weighted \(qF=0\) incidence kernel

Choose projections

\[
 V_u\longrightarrow
 \langle e_0^{(u)},e_1^{(u)},e_2^{(u)}\rangle
\]

fixing the displayed axes.  They induce an algebra homomorphism of (4).
Any solution in larger local spaces would project to a solution with
three-dimensional local spaces, so this reduction is lossless.

The elementary matching identity

\[
                         q q^{[2]}=3q^{[3]}             \tag{8}
\]

counts the three choices of a distinguished edge in every three-edge
matching.  Thus (3) implies the necessary equation

\[
                              qF=0.                    \tag{9}
\]

Only \(q_P\) can multiply \(E_i(P)\) without repeating a site.  Disjoint
coordinate-word supports first give

\[
                              q_C=q_D=0.               \tag{10}
\]

For the colour-zero part, decompose

\[
 V_u=\mathbb C e_0^{(u)}\oplus W_u
\]

and, for an edge \(e=\{u,v\}\) of the three-edge graph
\(G=\{A_1,A_2,A_3\}\), write

\[
\begin{aligned}
 q_e={}&x_e\,e_0^{(u)}e_0^{(v)}
       +a_{e,u}e_0^{(v)}
       +e_0^{(u)}a_{e,v}
       +Z_e,                                           \tag{11}\\
 &a_{e,u}\in W_u,\quad a_{e,v}\in W_v,\quad
 Z_e\in W_u\otimes W_v .
\end{aligned}
\]

Projecting (9) transversely at both endpoints of \(e\) isolates the term
from that edge, so

\[
                              Z_e=0\qquad(e\in G).      \tag{12}
\]

A word transverse only at a vertex \(u\) can arise precisely from the
edges incident with \(u\).  The all-\(e_0\) word receives every scalar
term.  Consequently (9) is exactly

\[
 \boxed{
 \sum_{\substack{e\in G\\u\in e}}\lambda_e a_{e,u}=0
       \quad(u\in U),\qquad
 \sum_{e\in G}\lambda_e x_e=0,\qquad Z_e=0.}           \tag{13}
\]

There are no other equations on the three colour-zero blocks.  Every
weight is nonzero, so at a used vertex of degree \(d\) each of the two
transverse coordinates has a \((d-1)\)-dimensional incidence kernel.
If \(v(G)\) is the number of used vertices, the transverse dimension is

\[
                   2\sum_{u:\deg u>0}(\deg u-1)
                   =2(6-v(G)),                         \tag{14}
\]

and the scalar kernel has dimension two.  Ten physical pairs lie outside
the five target supports and contribute \(10\cdot9=90\) free coordinates.
This gives the complete dimensions:

| zero-edge graph \(G\) | labelled \(G\)'s | \(v(G)\) | colour-zero kernel | full \(qF\) rank | full kernel |
|---|---:|---:|---:|---:|---:|
| three-edge star | 60 | 4 | 6 | 39 | 96 |
| triangle | 20 | 3 | 8 | 37 | 98 |
| three-edge path | 180 | 4 | 6 | 39 | 96 |
| two-edge path plus a disjoint edge | 180 | 5 | 4 | 41 | 94 |
| three-edge matching \(3K_2\) | 15 | 6 | 2 | 43 | 92 |

The checker independently constructs the 135-column coefficient matrix of
\(qF\), verifies these ranks over \(\mathbb Q\), and checks that the actual
parameterization later sent to Singular is a basis of its full kernel.

## 4. All five weights normalize exactly

After (7), the product table has done its job.  We may therefore use a local
diagonal automorphism which need not fix the tensors \(X_i\).  For colour
zero, scale

\[
                         e_0^{(u)}\longmapsto t_u e_0^{(u)},
 \qquad t_u\in\mathbb C^*.
\]

The coefficient of \(E_0(e)\) is multiplied by the character

\[
                         \chi_e(t)=\prod_{u\notin e}t_u. \tag{15}
\]

Let \(c_e\in\{0,1\}^6\) be the exponent vector of this character.  For
distinct edges \(e,f\),

\[
 c_e\cdot c_f=
 \begin{cases}
 3,&e\cap f\ne\varnothing,\\
 2,&e\cap f=\varnothing,
 \end{cases}
 \qquad c_e\cdot c_e=4.                                \tag{16}
\]

For the five graph shapes, the determinant of the \(3\times3\) Gram matrix
of \(c_{A_1},c_{A_2},c_{A_3}\) is:

| shape | star | triangle | path | path plus edge | \(3K_2\) |
|---|---:|---:|---:|---:|---:|
| determinant | 10 | 10 | 12 | 20 | 32 |

Thus the three exponent rows have rank three over \(\mathbb Q\).  The
associated map of complex tori

\[
 (\mathbb C^*)^6\longrightarrow(\mathbb C^*)^3,\qquad
 t\longmapsto(\chi_{A_1}(t),\chi_{A_2}(t),\chi_{A_3}(t)) \tag{17}
\]

is surjective on complex points.  Indeed, Smith normal form changes the
source and target by invertible monomial coordinates and turns the map into
\((z_1,z_2,z_3)\mapsto(z_1^{d_1},z_2^{d_2},z_3^{d_3})\) with nonzero
\(d_i\); every nonzero complex number has a \(d_i\)-th root.

For the potentially deceptive \(3K_2\) case, write the pairs as
\(01,23,45\), set

\[
 x=t_0t_1,\qquad y=t_2t_3,\qquad z=t_4t_5,
\]

and let \(b_r=\lambda_r^{-1}\).  The required equations are

\[
                         yz=b_1,\qquad xz=b_2,\qquad xy=b_3. \tag{18}
\]

Choose \(x\in\mathbb C^*\) with \(x^2=b_2b_3/b_1\), then put
\(y=b_3/x\) and \(z=b_2/x\).  Hence even \(3K_2\) has no residual weight
invariant.

The colour-one and colour-two axes scale independently, and each single
coefficient is normalized by scaling any site in its four-site complement.
Applying these algebra automorphisms to \(q\) preserves both equations in
(3).  We may therefore assume

\[
                   \lambda_1=\lambda_2=\lambda_3=\gamma=\delta=1. \tag{19}
\]

## 5. Seventy complete affine unit ideals

There are 15 pairs on six labelled sites.  After (7), the number of labelled
supports is

\[
                         \binom{15}{3}\,12\,11=60{,}060. \tag{20}
\]

The three colour-zero pairs are unordered, while \(C,D\) are exchanged only
together with the colour swap \(1\leftrightarrow2\).  Quotienting by these
symmetries and \(S_6\) gives exactly 70 orbits:

| zero graph | orbit numbers | number of orbits | labelled supports |
|---|---|---:|---:|
| three-edge star | 1--13 | 13 | 7,920 |
| triangle | 14--19 | 6 | 2,640 |
| three-edge path | 20--41 | 22 | 23,760 |
| path plus edge | 42--66 | 25 | 23,760 |
| \(3K_2\) | 67--70 | 4 | 1,980 |

The labelled counts sum to \(60{,}060\).  The checker independently forms
every orbit from all site permutations and the colour-\(1/2\) swap, proves
that the orbits are disjoint and exhaustive, and freezes the ordered
representative-and-size ledger with SHA-256

    bf78ec80a487610252f80a447cb7092019c15464b4729ba49af095461b7702f3

For each representative, substitute the complete normalized kernel
(10)--(13).  For every four-set
\(S=\{u_0,u_1,u_2,u_3\}\) and every word
\(c\in\{0,1,2\}^S\), impose

\[
\begin{aligned}
 &(q_{u_0u_1})_{c_0c_1}(q_{u_2u_3})_{c_2c_3}
 +(q_{u_0u_2})_{c_0c_2}(q_{u_1u_3})_{c_1c_3}\\
 &\hspace{30mm}
 +(q_{u_0u_3})_{c_0c_3}(q_{u_1u_2})_{c_1c_2}
 -[F]_{S,c}=0.                                        \tag{21}
\end{aligned}
\]

The endpoint convention is
\((q_{vu})_{ba}=(q_{uv})_{ab}\), so both endpoint orders are retained.
Equation (21) is the complete coefficient list of \(q^{[2]}-F\), not a
projection or selected support.  Depending on the zero graph, the affine
ring has 92, 94, 96, or 98 variables; after identically zero equations are
removed, there are between 813 and 1,215 generators.

These ideals have no saturation, auxiliary inverse, nonzero-variable
declaration, or generic stratum.  Singular computes the unit basis \([1]\)
over \(\mathbb Q\) for every one of the 70 ideals.  Thus there is no complex
solution, including every degenerate and cancellation stratum.  The 70
individual ordered-generator hashes are frozen in the checker; the combined
orbit/support/hash ledger has SHA-256

    17ffabc76022262f0ffc2866ccc179e8b7fec5d96ceace239418c24341fcf216

The ideals impose only the necessary consequence \(qF=0\), rather than
adding \(q^{[3]}=0\) again.  They are therefore weaker than (3); their
emptiness is sufficient.  This completes the proof of Theorem 1.1.

## 6. Exact scope

This theorem closes the pure-monomial multiplicity profile \((3,1,1)\)
with arbitrary nonzero complex weights and arbitrary star rows.  It does
not cover profile \((2,2,1)\), four or more same-colour monomials, a
non-pure four-site lift, or the general cyclic/diagonal direct-block
problem.  It is not a global six-site descent and does not prove Krenn's
conjecture.  The next genuinely different bounded profile is \((2,2,1)\):
two separate weighted incidence kernels then coexist, and their torus
characters and second-power equations must be treated simultaneously.
