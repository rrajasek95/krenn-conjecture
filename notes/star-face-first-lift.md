# The first two-adic lift on the residual-supported two-edge star face

## Outcome

The two-edge-star valuation from
`valuation-filtered-laurent-circuit.md` admits a complete order-zero
description and an exact first-lift system.

Let every colored cell on `01` and `02` have valuation `-nu(2)` and every
other cell valuation zero.  After writing

\[
 U_{01}=2A_{01},\qquad U_{02}=2A_{02},\qquad
 Z_{uv}=A_{uv}\quad(uv\ne01,02),                           \tag{1}
\]

all entries are units.  In every coefficient there are six star-containing
minimum terms and nine other terms.  Write their sums as `L_c(U,Z)` and
`G_c(Z)`.  The exact target equation is

\[
                         L_c+2G_c=2\delta_c,               \tag{2}
\]

where `delta_c=1` for a constant colouring and zero otherwise.

There are three new conclusions.

1. Every torus-valued solution of the initial system `bar L=0` is either on
   a precisely described rank-one-factor branch or on the degenerate branch
   where two overlapping four-site matching tensors both vanish.
2. If the residue field is exactly `F_2`, four coefficient equations rule
   out (2) modulo the first target digit for **every ramification index**.
   This extends the old rank-`45/46` calculation, which treated only the
   unramified all-ones expansion.
3. Over an arbitrary residue extension, the complete system is still
   impossible.  Exact row-wise annihilators kill `L`, before reduction and
   independently of ramification.  The two overlapping four-site cofactors
   then force the projection of `G` to have flattening rank one, whereas the
   projected diagonal target has rank three.  The branch `B=C=0` is ruled
   out separately by the same shared-cofactor pencil.

The four-equation proof itself does not extend to arbitrary residue
extensions.  An exact calculation in the unramified ring with residue `F_4`
gives a unit-valued solution of that abstract matrix pattern.  The universal
argument therefore genuinely needs the shared cofactor identities in the
complete system.

The finite matching decomposition, truncated-ramified-ring identities, and
the `F_4` boundary matrix are checked by
`computations/verify_star_face_first_lift.py`.  The exact annihilator,
common-pencil permanent identity, projected target minor, and degenerate
incidence contradiction are checked independently by
`computations/verify_star_cofactor_projection.py`.

## 1. Complete initial equations

For a colouring

\[
                 c=(a,b,c,d,e,f),\qquad S=(d,e,f),         \tag{3}
\]

put

\[
\begin{aligned}
 X_{ab}&=\overline U_{01}^{ab},&
 Y_{ac}&=\overline U_{02}^{ac},\\
 B_{cS}&=H_{\{2,3,4,5\}}(\overline Z)_{cdef},&
 C_{bS}&=H_{\{1,3,4,5\}}(\overline Z)_{bdef}.
\end{aligned}                                             \tag{4}
\]

The six minimum matchings are the three completions of `01` and the three
completions of `02`.  Consequently

\[
                    \overline L_{abcS}
                       =X_{ab}B_{cS}+Y_{ac}C_{bS}.         \tag{5}
\]

All `X_ab,Y_ac` are nonzero.

**Lemma 1.1 (initial-star dichotomy).**  A torus-valued solution of (5) has
exactly one of the following forms.

* `B=C=0` as complete `3 by 27` tensors; or
* there are nonzero vectors `u=(u_a)`, `x=(x_b)`, `y=(y_c)` and a nonzero
  `27`-vector `h=(h_S)` such that

\[
 \begin{aligned}
 X_{ab}&=u_ax_b,&Y_{ac}&=u_ay_c,\\
 C_{bS}&=x_bh_S,&B_{cS}&=y_ch_S.                           \tag{6}
 \end{aligned}
\]

Here entries of `h` may vanish, but `u,x,y` are torus-valued.

**Proof.**  Suppose some `B_(cS)` is nonzero.  Equation (5) and nonvanishing
of `X,Y` then show that, at this `S`, every coordinate of both `B` and `C`
is nonzero.  Ratios in (5), first with `a` fixed and then with `a` varied,
show respectively that the `b`-dependence is a common vector `x`, the
`c`-dependence is a common vector `y`, and the two star matrices have the
same row factor `u`.  Substitution gives (6) at this `S`.  Repeating the
same ratio calculation at every other nonzero column gives the same
`u,x,y`; a zero coordinate in one of `B,C` forces the entire corresponding
column of both to vanish.  This defines `h` and proves (6).  If no entry of
`B` is nonzero, (5) forces `C=0`, giving the other branch. `QED`

On the nondegenerate branch, arbitrary endpoint-colour gauges normalize
`X` and `Y` to all ones and make both four-site tensors independent of their
distinguished first colour.  Such a gauge need not preserve the normalized
six-site target; the factors in (6) therefore cannot simply be discarded in
the first-lift equation.

## 2. The exact Bockstein system

Let `O` be the valuation ring, `pi` a uniformizer, and `e=nu(2)`.  Suppose a
choice `q_<` of unit entries has already solved

\[
                         L(q_<)\equiv0\pmod {2}.           \tag{7}
\]

For `e>1`, this notation includes all compatible lower `pi`-digits through
order `e-1`; it is not determined by the residue point alone.  Define the
first-output Bockstein

\[
               \beta(q_<)=\frac{L(q_<)}2\bmod\pi.         \tag{8}
\]

Make the final multiplicative correction

\[
                         q=q_<(1+2z).                      \tag{9}
\]

Reducing (2) after division by two gives the linear system over the residue
field

\[
 D_{\log}L_{\bar q}(z)
       =\overline\delta-\overline G(\bar q)-\beta(q_<).   \tag{10}
\]

Thus the exact first-lift invariant is the cokernel class

\[
 [\overline\delta-\overline G-\beta]
       \in\operatorname {coker}D_{\log}L_{\bar q}.        \tag{11}
\]

Equivalently, every left-kernel vector `lambda` of the logarithmic Jacobian
must annihilate the right side of (10).  Formula (11) is gauge-covariant:
an invertible endpoint-colour change only applies invertible row and column
scalings to the linearized system.  It is also the reason an order-zero
minimum-face invariant is insufficient.  In a ramified field, `beta`
depends on the intervening jet, not only on `bar q`.

For an unramified field, one may choose Teichmuller lifts of the residue
entries in (8).  The old four-row rank-`45/46` witness is one left-kernel
evaluation of (10) at the all-ones `F_2` point.

## 3. A ramification-independent obstruction over `F_2`

Assume now that the residue field is exactly `F_2`; every displayed unit
has residue one.  Use only the four colourings

\[
 022220,\qquad222220,\qquad022222,\qquad222222.            \tag{12}
\]

In each fibre, the nine nonminimum terms have unit residue, so their sum has
residue `9=1`.  Modulo `pi^(e+1)`, equation (2) therefore says that the
six-term minimum sum is `2` for the first three mixed colourings and zero
for the last pure colouring.

Group the three `01` completions and the three `02` completions.  For
`a,t in {0,2}` the minimum sum has the form

\[
                         p_{at}=x_ar_t+y_as_t,             \tag{13}
\]

where all eight quantities `x_a,y_a,r_t,s_t` are units.  Equations (12)
would require

\[
                 p_{00}=p_{20}=p_{02}=2,qquad p_{22}=0
                         \pmod {\pi^{e+1}}.                \tag{14}

The following elementary observation is uniform in `e`.

**Lemma 3.1.**  If the residue field is `F_2` and `v,w` are units, then

\[
 v+w\equiv2\pmod {\pi^{e+1}}
          \quad\Longleftrightarrow\quad
 v\equiv w\pmod {\pi^{e+1}}.                             \tag{15}
\]

Indeed, every unit is `1 mod pi`.  If `v+w=2`, then
`w-v=2(1-v)` modulo `pi^(e+1)`, which vanishes; the converse is the same
calculation in reverse.

Apply (15) to the first three equations of (14).  They give

\[
 x_0r_0=y_0s_0,\qquad x_2r_0=y_2s_0,
 \qquad x_0r_2=y_0s_2.                                  \tag{16}
\]

Division by units yields `x_2r_2=y_2s_2`.  Applying (15) once more makes
`p_22=2`, contradicting the last equation of (14).  Hence:

**Theorem 3.2.**  The two-edge-star valuation has no lift through the first
target digit over any mixed-characteristic DVR with residue field `F_2`,
regardless of its ramification index.

This is an actual filtration-level contradiction, but not yet the one
needed for a hypothetical number-field point: a place above two may have a
larger finite residue field.

## 4. Why four fibres do not handle residue extensions

Let `R=GR(4,2)=Z/4[omega]/(omega^2+omega+1)`.  Its residue field is `F_4`.
In `R`, put

\[
 M=\begin{pmatrix}1&1\\ \omega&\omega+2\end{pmatrix},
 \qquad
 T=\begin{pmatrix}1&1\\1&0\end{pmatrix}.                 \tag{17}
\]

The determinant of `M` is two.  Set `V=adj(M)T`.  Direct multiplication
gives

\[
                         MV=2T,                            \tag{18}
\]

and all eight entries of `M,V` are units.  Interpreting the rows of `M` as
`(x_a,y_a)` and the columns of `V` as `(r_t,s_t)` realizes exactly (14).
Thus Lemma 3.1, and therefore the four-fibre proof, is special to residue
field `F_2`.

Thus a residue solution of the abstract four-equation quotient is not a lift
of all 729 equations; (17)--(18) only proves that a universal argument must
retain more of that system.  The next sections do so without enumerating
lower jets.

## 5. Exact annihilation before taking the Bockstein

The key point is that the relevant cokernel projection can be lifted to the
valuation ring and applied to (2) itself.  For a fixed colour `a` at vertex
zero, regard

\[
 \widetilde X_a=(U_{01}^{ab})_b,\qquad
 \widetilde Y_a=(U_{02}^{ac})_c                            \tag{19}
\]

as primitive rows over the valuation ring.  Choose rank-two matrices
`Pi^X_a,Pi^Y_a` over that ring such that

\[
                 \Pi^X_a\widetilde X_a=0,\qquad
                 \Pi^Y_a\widetilde Y_a=0.                \tag{20}
\]

Contract the `b,c` indices of (2) by their tensor product.  Formula (5),
which is an integral identity before reduction, gives

\[
  (\Pi^X_a\otimes\Pi^Y_a)L_a=0.
\]

The valuation ring has characteristic zero, so the remaining factor of two
can be cancelled exactly:

\[
 (\Pi^X_a\otimes\Pi^Y_a)G_a
       =(\Pi^X_a\otimes\Pi^Y_a)\delta_a.                 \tag{21}
\]

This removes both the logarithmic Jacobian and every lower-jet contribution
to `beta`; in particular, (21) is uniform in the ramification index.

On the nondegenerate branch of Lemma 1.1, the reductions of the kernels in
(20) are the fixed lines `kx` and `ky`.  The matrices in (20) may be chosen
so that their reductions are fixed quotient maps

\[
                 \pi_x:k^3\longrightarrow k^3/kx,
                 \qquad
                 \pi_y:k^3\longrightarrow k^3/ky        \tag{22}
\]

for every `a`.  Indeed, lift any two rows annihilating `x` and correct one
coefficient using a unit coordinate of `widetilde X_a`; the correction is
divisible by the uniformizer.  Do the same for `widetilde Y_a`.

## 6. The shared-cofactor pencil

Put `V_i=k^3` for `i=3,4,5`, and abbreviate the three internal edge tensors
by `R_34,R_35,R_45`.  For a triple `p=(p_3,p_4,p_5)` of one-site forms set

\[
 F(p)=p_3R_{45}+p_4R_{35}+p_5R_{34},\qquad K=\ker F.      \tag{23}
\]

Tensor placements in (23) are the evident ones.  Let
`per(r,p,q)` be the six-term permanent obtained by assigning the three rows
`r,p,q` bijectively to the sites `3,4,5`.  In characteristic two it is also
the determinant.

**Lemma 6.1 (shared-cofactor pencil).**  Suppose all three `R_ij` are
nonzero.  Exactly one of the following descriptions applies after extending
the residue field algebraically.

* `dim K<=1`; or
* `dim K=2`, and there are one-site forms `l_i,m_i` such that

\[
 R_{ij}=l_i m_j+m_i l_j,\qquad
 K=\{(\alpha l_i+\beta m_i)_{i=3}^5:(\alpha,\beta)\in k^2\}. \tag{24}
\]

In either case, for arbitrary linear families `p_alpha,q_beta in K`, the
matrix-valued tensor

\[
                    (\operatorname {per}(r,p_\alpha,q_\beta))_{\alpha\beta}
                                                                    \tag{25}
\]

is a fixed matrix times `F(r)`.  In the first case it is zero.

**Proof.**  If `K` contains a vector whose three components are nonzero,
choose each component as the first basis vector in its one-site space.
The coefficients off those three first rows and columns vanish, while the
remaining row and column coefficients agree in pairs.  Equivalently, there
are `m_i` for which

\[
                         R_{ij}=l_i m_j+m_i l_j.
\]

Projecting any other kernel vector modulo `span(l_i,m_i)` at site `i`, and
using the nonzero opposite edge, shows that all its components lie in these
two-dimensional spans.  If all three spans have dimension two, the six
coefficients containing both an `l` and an `m` say directly that its three
`l`-coefficients agree and its three `m`-coefficients agree.  If a span is a
line, write `m_i=c_i l_i`; the same conclusion follows after deleting that
redundant coordinate, and `R_ij != 0` says that the relevant `c_i+c_j` does
not vanish.  This gives the common pair `(alpha,beta)` in (24).  The two
global triples `(l_i)` and `(m_i)` are independent, since otherwise every
`R_ij` would vanish.  Thus `K` has dimension two.  Multilinearity gives the
exact identity

\[
 \operatorname {per}\bigl(r,k(\alpha,\beta),k(\gamma,\eta)\bigr)
       =(\alpha\eta+\beta\gamma)F(r).                    \tag{26}
\]

If there is no kernel vector with three nonzero components, then over the
infinite algebraic closure the vector space `K` is contained in one of the
three coordinate hyperplanes, say `p_3=0`.  A nonzero identity
`p_4R_35+p_5R_34=0` makes `R_35,R_34` rank-one tensors with fixed factors,
so its solution space is a line.  Finally the permanent is alternating in
characteristic two, hence vanishes on two vectors in that line. `QED`

For later use, write the remaining incident rows as

\[
\begin{aligned}
 r_a&=(Z_{03}^{a,*},Z_{04}^{a,*},Z_{05}^{a,*}),\\
 s_b&=(Z_{13}^{b,*},Z_{14}^{b,*},Z_{15}^{b,*}),\\
 t_c&=(Z_{23}^{c,*},Z_{24}^{c,*},Z_{25}^{c,*}).           \tag{27}
\end{aligned}
\]

Then `C_b=F(s_b)`, `B_c=F(t_c)`, and the nine-term tensor is exactly

\[
            G_{abcS}=Z_{12}^{bc}F(r_a)_S
                         +\operatorname {per}(r_a,s_b,t_c)_S. \tag{28}
\]

## 7. The nondegenerate branch has rank one, not three

Reduce (21) and use the fixed quotients (22).  Equations (6) and (27) imply

\[
 p_\alpha=\sum_b(\pi_x)_{\alpha b}s_b\in K,\qquad
 q_\beta=\sum_c(\pi_y)_{\beta c}t_c\in K.                \tag{29}
\]

Lemma 6.1 applied to (28) now shows that the entire left side of (21) is

\[
                         M\otimes (F(r_a)_S)              \tag{30}
\]

for one fixed `2 by 2` matrix `M`.  Its flattening across
`(bar V_1 tensor bar V_2)|(V_0 tensor V_3 tensor V_4 tensor V_5)` has rank
at most one.

The projected target has the three left factors

\[
                 \pi_x(e_i)\otimes\pi_y(e_i),\qquad i=0,1,2. \tag{31}
\]

They are linearly independent.  To see this, use `e_0,e_1` as quotient
bases and eliminate `e_2` with the relations supplied by the torus vectors
`x,y`; the two cross coefficients in a putative relation force the
coefficient of the third tensor to vanish, and then the other two vanish.
The right factors are supported at the three distinct pure words
`(a,S)=(i,i,i,i)`.  Hence the right side of (21) has flattening rank three,
contradicting (30).

## 8. The branch `B=C=0`

Here every `s_b,t_c` belongs to `K`.  Each one has three nonzero components,
because every edge cell is a unit.  Lemma 6.1 therefore gives the pencil
(24).  Put `W_i=span(l_i,m_i)`.

For each fixed `a`, reduce the exact annihilators (20), now without assuming
their kernels are independent of `a`.  Their linear combinations of the
`s_b,t_c` still lie in `K`, so (26)--(28) make the projected left side of
(21) a simple tensor

\[
                              M_a\otimes F(r_a).           \tag{32}
\]

The projected target is

\[
 (\bar\Pi^X_a e_a)\otimes(\bar\Pi^Y_a e_a)
                       \otimes e_a\otimes e_a\otimes e_a. \tag{33}
\]

Its first factor is nonzero: a coordinate vector cannot span a row whose
three entries are nonzero.  Equality of the two nonzero simple tensors in
(32)--(33) forces

\[
                           F(r_a)=\lambda_a e_a^{\otimes3}
                           \quad(\lambda_a\ne0).           \tag{34}
\]

But `R_ij in W_i tensor W_j`.  Quotienting any two of the sites `3,4,5` by
their `W_i` kills every summand of `F(r)`.  Applying such a double quotient
to (34) says that, for each colour `a`, the coordinate vector `e_a` belongs
to at least two of `W_3,W_4,W_5`.

No `W_i` can contain two coordinate vectors.  If it did, its dimension at
most two would make it the corresponding coordinate plane, and every
incident `R_ij in W_i tensor W_j` would have a zero row, contrary to the
unit-valued edge cells.  The three colours therefore yield at least six
required incidences with the `W_i`, while the three spaces admit at most
three.  This contradiction finishes the second branch.

**Theorem 8.1.**  The two-edge-star valuation has no characteristic-zero
lift over any mixed-characteristic valuation ring, for every ramification
index and every residue-field extension.
