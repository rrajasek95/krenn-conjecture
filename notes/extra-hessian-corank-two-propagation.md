# A dense pair needs at least two excess Hessian directions

## 1. Outcome

The first singular stratum in the source-Hessian escape is still
impossible.  Delete two vertices and let `q` be the quadratic on the
remaining even set.  Assume that the rank-three graph of `q` is connected,
spanning, and nonbipartite.  If the three rows of one deleted star reach at
least three internal sites and the three rows of the other star are
nonzero, then the nine pair equations force

\[
 \boxed{\quad
 \dim\bigl(\ker\mathcal H_q/\mathcal G_q\bigr)\ge2.
 \quad}                                                   \tag{1}
\]

Here `G_q` is the unavoidable vertex-expansion gauge.  Thus a single
non-gauge Hessian direction cannot be the dense escape from the
gauge-rigid pair theorem.  In particular, if all six deleted-star rows
meet at least three sites, Hessian corank must exceed the gauge corank by
at least two.

The proof uses the complete three-colour pair system and the fact that its
off-diagonal kernel vectors are polarized products of the *same two
stars*.  It is false for an arbitrary collection of Hessian-kernel
vectors.  A second part records the exact second- and third-order
rank-one identities obeyed by these distinguished directions.  Those
identities give a concrete integrability hierarchy on the remaining
excess-at-least-two locus, but they do not yet exclude that locus.

## 2. Normalized pair equations

Let `W` have `2r` sites, `r>=2`, and work in the site-square-zero algebra

\[
 \mathcal R_W=\bigotimes_{i\in W}(\mathbb C\oplus V_i),
 \qquad V_i^2=0,
 \qquad \dim V_i=3.
\]

Put

\[
 Q={q^r\over r!},\qquad
 \mathcal H_q(Z)={Zq^{r-1}\over(r-1)!}.                  \tag{2}
\]

For two deleted vertices, orient their incident blocks toward the deleted
endpoints and write their colour rows as linear elements
`p_0,p_1,p_2` and `s_0,s_1,s_2` on `W`.  Let `a_cd` be the direct-edge
matrix.  The exact two-deletion equations are

\[
 \boxed{\quad
 \mathcal H_q(p_cs_d)+a_{cd}Q=\delta_{cd}X_c,
 \qquad 0\le c,d\le2,
 \quad}                                                   \tag{3}
\]

where `X_c=otimes_(i in W)e_c^(i)`.  These equations retain arbitrary
asymmetric endpoint matrices and all complex cancellation.

For scalars `alpha_i` of sum zero, define

\[
 (Z^\alpha)_{ij}=(\alpha_i+\alpha_j)q_{ij},
 \qquad
 \mathcal G_q=\{Z^\alpha:\sum_i\alpha_i=0\}.            \tag{4}
\]

Every such vector lies in `ker H_q`.  Let

\[
 E_q=\ker\mathcal H_q/\mathcal G_q                       \tag{5}
\]

be the excess Hessian space.  Finally put

\[
 \lambda_{cd}={a_{cd}\over r},\qquad
 K_{cd}=p_cs_d+\lambda_{cd}q.                            \tag{6}
\]

Since `H_q(q)=rQ`, equation (3) becomes

\[
                         \mathcal H_q(K_{cd})
                              =\delta_{cd}X_c.            \tag{7}
\]

In particular, the six `K_cd` with `c!=d` are distinguished elements of
the actual source Hessian kernel.

## 3. A gauge polarized product must vanish

Let `G_3(q)` be the graph whose edge `ij` is present when the matrix
`q_ij` has rank three.  For a linear element `t=sum_i t_i`, let
`supp_s(t)={i:t_i!=0}`.

**Lemma 3.1 (one-product gauge rigidity).**  Suppose `G_3(q)` is
connected, spanning, and nonbipartite.  If

\[
                         pt+bq\in\mathcal G_q             \tag{8}
\]

and `|supp_s(t)|>=3`, then `p=0` and `b=0`.

**Proof.**  Write the right side of (8) as `Z^alpha`, with
`sum_i alpha_i=0`.  On the block `ij`,

\[
 p_i\otimes t_j+t_i\otimes p_j
       =(\alpha_i+\alpha_j-b)q_{ij}.                     \tag{9}
\]

On an edge of `G_3(q)`, the left side has matrix rank at most two while a
nonzero scalar multiple of the right-side matrix has rank three.  Hence

\[
 \alpha_i+\alpha_j=b,
 \qquad
 p_i\otimes t_j+t_i\otimes p_j=0                         \tag{10}
\]

on every rank-three edge.  Put `beta_i=alpha_i-b/2`.
Connectedness and an odd cycle force `beta_i=0` for every `i`.  The
zero-sum condition then gives `b=0`, hence `alpha=0`.  Equation (8) is
therefore the equality `pt=0` in every block, not merely on the
rank-three graph.

Multiplication by a linear element supported at three or more sites is
injective on linear elements in characteristic different from two.  For
completeness, if `pt=0`, then on three active sites the equality of two
simple tensors gives `p_i=mu_i t_i` and `mu_i+mu_j=0` for every pair.
The three equations force all `mu_i=0`; pairing any remaining site with an
active one then gives its component of `p` equal to zero.  Thus `p=0`.
`QED`

The lemma is where the physical block ranks and the site grading enter.
It would not follow in the abstract two-step annihilator quotient.

## 4. Corank-one propagation and contradiction

**Theorem 4.1 (excess-corank-two theorem).**  Suppose the nine equations
(3) hold and `G_3(q)` is connected, spanning, and nonbipartite.  Assume,
in one of the two endpoint orientations, that

\[
 |\operatorname {supp}_s(s_d)|\ge3\quad(d=0,1,2),
 \qquad p_c\ne0\quad(c=0,1,2).                           \tag{11}
\]

Then `dim E_q>=2`.

**Proof.**  Suppose instead that `dim E_q<=1`.  Fix a colour `d`.  The
two vectors

\[
                         K_{cd}\qquad(c\ne d)             \tag{12}
\]

lie in `ker H_q` by (7), so their two classes in the at-most-one-
dimensional space `E_q` are linearly dependent.  There are scalars
`mu_c`, not both zero, such that

\[
 \sum_{c\ne d}\mu_cK_{cd}
   =\left(\sum_{c\ne d}\mu_cp_c\right)s_d
      +\left(\sum_{c\ne d}\mu_c\lambda_{cd}\right)q
       \in\mathcal G_q.                                  \tag{13}
\]

Lemma 3.1 and (11) imply

\[
                         \sum_{c\ne d}\mu_cp_c=0.        \tag{14}
\]

Thus the two rows `p_c` with `c!=d` are linearly dependent.  Doing this
for `d=0,1,2` shows that every pair among `p_0,p_1,p_2` is dependent, and
hence their total span has dimension at most one.  Since none is zero,
there are a nonzero linear element `p` and nonzero scalars `t_c` such that

\[
                              p_c=t_cp.                   \tag{15}
\]

Put `R_d=H_q(ps_d)`.  The pair equations now read

\[
                         a_{cd}Q+t_cR_d=\delta_{cd}X_c.   \tag{16}
\]

For fixed `d`, choose either `c!=d`.  Since `t_c!=0`, the off-diagonal
equation in (16) gives `R_d in C Q` (with the literal conclusion
`R_d=0` if `Q=0`).  The diagonal equation then gives

\[
                              X_d\in\mathbb C Q.          \tag{17}
\]

This holds for all three `d`, which is impossible because
`X_0,X_1,X_2` are linearly independent.  The assumption
`dim E_q<=1` was false. `QED`

Interchanging the deleted endpoints gives the symmetric version: it is
enough that all `p_c` reach three sites and all `s_d` are nonzero.  In
particular, if all six rows reach at least three internal sites, the
conclusion (1) follows in either orientation.

**Corollary 4.2 (refined dense-pair trichotomy).**  For every deleted pair
in a hypothetical ternary source, at least one of the following occurs.

1. `dim(ker H_q/G_q)>=2`;
2. `G_3(q)` is disconnected, nonspanning, or bipartite;
3. in each endpoint orientation, either one row of the first star is zero
   or one row of the second star reaches at most two internal sites.

Consequently a fully dense source whose internal rank-three graph remains
connected and nonbipartite after the deletion cannot lie on the first
Hessian determinantal stratum: it lies at least two ranks below the
gauge-rigid maximum.

## 5. The exact curvature identities on the surviving locus

The six kernel vectors in (7) carry more structure than the dimension
argument uses.  Define

\[
 \mathsf S_q(U,V)={UVq^{r-2}\over(r-2)!}.                \tag{18}
\]

For kernel vectors, its class modulo `im H_q` descends through the gauge
quotient:

\[
 \mathrm {II}_q:E_q\times E_q\longrightarrow
       \operatorname {coker}\mathcal H_q,
 \qquad
 \mathrm {II}_q([U],[V])=[\mathsf S_q(U,V)].             \tag{19}
\]

Indeed, let `D_alpha` be the site-weight derivation and let
`G=D_alpha q` be a gauge, with `sum alpha_i=0`.  For `V in ker H_q`,
differentiating `Vq^(r-1)=0` gives the exact identity

\[
             \mathsf S_q(G,V)=-\mathcal H_q(D_\alpha V), \tag{20}
\]

so changing either representative by a gauge changes (18) by a Hessian
image.  Thus (19) is the genuine second fundamental form of the matching-
power fibre after quotienting its integrable vertex torus.

The polarized products

\[
                         B_{cd}:=p_cs_d=K_{cd}-\lambda_{cd}q             \tag{21}
\]

obey every rank-one minor identity

\[
                         B_{cd}B_{ef}=B_{cf}B_{ed}.       \tag{22}
\]

Substitution of (21), followed by multiplication by
`q^(r-2)/(r-2)!`, gives

\[
\begin{aligned}
 &\mathsf S_q(K_{cd},K_{ef})-\mathsf S_q(K_{cf},K_{ed})\\
 &=(r-1)(
    \lambda_{ef}\delta_{cd}X_c+
    \lambda_{cd}\delta_{ef}X_e-
    \lambda_{ed}\delta_{cf}X_c-
    \lambda_{cf}\delta_{ed}X_e)\\
 &\qquad-r(r-1)(\lambda_{cd}\lambda_{ef}
                    -\lambda_{cf}\lambda_{ed})Q.        \tag{23}
\end{aligned}
\]

This is an exact second-order integrability identity forced by the actual
common power.  It is not an identity of arbitrary Hessian matrices.

There is a genuinely ternary next member.  For distinct `c,d,e`,
commutativity gives

\[
                         B_{cd}B_{de}B_{ec}
                            =B_{ce}B_{ed}B_{dc}.          \tag{24}
\]

When `r>=3`, put

\[
 \mathsf T_q(U,V,Z)={UVZq^{r-3}\over(r-3)!}.             \tag{25}
\]

All six `K`'s in (24) are off diagonal and hence lie in the Hessian
kernel.  Expanding (24) gives

\[
\begin{aligned}
 &\mathsf T_q(K_{cd},K_{de},K_{ec})
   -\mathsf T_q(K_{ce},K_{ed},K_{dc})\\
 &=(r-2)\Bigl[
   \lambda_{cd}\mathsf S_q(K_{de},K_{ec})
  +\lambda_{de}\mathsf S_q(K_{cd},K_{ec})
  +\lambda_{ec}\mathsf S_q(K_{cd},K_{de})\\
 &\hspace{37mm}
  -\lambda_{ce}\mathsf S_q(K_{ed},K_{dc})
  -\lambda_{ed}\mathsf S_q(K_{ce},K_{dc})
  -\lambda_{dc}\mathsf S_q(K_{ce},K_{ed})\Bigr]\\
 &\quad+r(r-1)(r-2)
   (\lambda_{cd}\lambda_{de}\lambda_{ec}
    -\lambda_{ce}\lambda_{ed}\lambda_{dc})Q.           \tag{26}
\end{aligned}
\]

The possible terms containing `q^2K_ab` vanish precisely because every
index pair in (24) is off diagonal and (7) sends those `K_ab` to zero.
Equation (26) is the first closed three-colour cycle relation among the
six excess directions.

## 6. Scope and audit

Theorem 4.1 closes the gauge-plus-one stratum, not the full singular
locus.  The Hamilton countermodel in
`source-hessian-nonintegrability-countermodel.md` already proves that an
individual extra direction can have nonzero second obstruction, so one
cannot replace (23)--(26) by an assumption that every kernel vector
integrates.  What remains is now sharper: on the dense connected
nonbipartite chart, an actual solution needs at least a two-dimensional
excess space carrying six polarized kernel vectors satisfying (23) and
(26).

No positivity, endpoint symmetry, rank-one edge decomposition, or
termwise cancellation was used.  Parallel decorated sources have already
been aggregated into arbitrary `3 by 3` blocks.  Zero and rank-deficient
internal blocks are retained literally and appear only through alternative
2 of Corollary 4.2.

[`verify_extra_hessian_corank_two.py`](../computations/verify_extra_hessian_corank_two.py)
checks the factorial normalizations in (20), (23), and the general form of
(26) over the rationals in the square-free site algebra.  It also checks
(20) on a genuine nongauge Hamilton Hessian-kernel vector, rather than
only on two gauge vectors.
