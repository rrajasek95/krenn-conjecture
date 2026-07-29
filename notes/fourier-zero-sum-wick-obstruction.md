# Fourier zero-sum and Wick-cycle obstructions

This note records two exact consequences of Fourier transforming the three
color modes.  They do not assume positivity, symmetry of endpoint colors, or
rank-one aggregate edges.  The first excludes every Gaussian/Wick ansatz
which preserves the visible `Z/3` symmetry.  The second excludes the much
larger chart in which the charge-zero covariance is supported on one isolated
perfect matching.

Neither statement by itself is a reduction of the general problem: a general
source can break the target symmetry, and its charge-zero scalar graph can
have many perfect matchings with complex cancellation.

## 1. The exact zero-sum form

Let `omega` be a primitive cube root of unity and apply at every mode the
invertible Fourier map

\[
                 e_r\longmapsto \sum_{s=0}^2\omega^{rs}f_s.
\tag{1}
\]

Then

\[
 \sum_{r=0}^2 e_r^{\otimes n}
 \longmapsto
 \sum_{s_1,\ldots,s_n}\left(\sum_{r=0}^2
       \omega^{r(s_1+\cdots+s_n)}\right)
       f_{s_1}\otimes\cdots\otimes f_{s_n}
 =3\sum_{\sum s_v=0}f_{s_1}\otimes\cdots\otimes f_{s_n}.
\tag{2}
\]

Absorb the harmless scalar `3` into one local mode.  Thus a putative
three-color source gives arbitrary two-site matrices `C_uv` whose scalar
Wick moments obey

\[
 \operatorname {haf}\bigl(C_{uv}(s_u,s_v)\bigr)_{u,v\in B}
       ={f1}_{\sum_vs_v=0\pmod3}.                            \tag{3}
\]

Equivalently, introduce formal centered Gaussian variables `X_(v,s)` with
bilinear covariance

\[
 \mathbb E[X_{u,a}X_{v,b}]=C_{uv}(a,b),\qquad u\ne v.
\tag{4}
\]

No positivity or genuine probability distribution is meant: Wick's rule is
the algebraic definition of the displayed moments over `C`.  Equation (3)
is exactly

\[
 \mathbb E\prod_vX_{v,s_v}={\bf1}_{\sum_vs_v=0}.              \tag{5}
\]

Restricting every mode to charges `0,1` gives the useful Boolean shadow

\[
 \mathbb E\prod_vX_{v,\epsilon_v}
             ={f1}_{|\epsilon|=0\pmod3}.                    \tag{6}
\]

## 2. An invariant Gaussian cannot work

Suppose the covariance itself respects the global charge action

\[
                         X_{v,s}\longmapsto\omega^sX_{v,s}.
\tag{7}
\]

Then invariance of (4) forces

\[
 C_{uv}(a,b)=0\quad\hbox{unless}\quad a+b=0\pmod3.           \tag{8}
\]

Every nonzero Wick pairing therefore pairs a charge `1` with a charge `2`
and pairs charge `0` with charge `0`.  In particular its charge counts must
satisfy

\[
                         n_1=n_2,\qquad n_0\text{ even}.       \tag{9}
\]

For any `n>=4`, put `k` zeros and `n-k` ones, where `k` is the residue of
`n` in `{0,1,2}`.  The total charge is zero because `n-k` is divisible by
three, so (5) requires the moment to be one.  But `n-k>0` and there are no
charge-two variables, contradicting (9).  We have proved:

**Proposition 2.1.**  For every `n>=4`, the zero-sum tensor (2) is not the
degree-`n` Wick tensor of a `Z/3`-invariant covariance.  Consequently one
cannot average a hypothetical source covariance to the target symmetry;
any exact source must break that symmetry at the two-point level.

### Why the Reynolds twirl does not preserve the target

This last warning can be made exact.  Let `g=diag(1,omega,omega^2)` in the
charge basis.  The edgewise Reynolds projection is

\[
 \Pi(C_{uv})={1\over3}\sum_{k=0}^2
                    (g^k\otimes g^k)C_{uv}.                  \tag{9a}
\]

It is the projection onto (8), so for every coloring `s`

\[
 \Pi(C_{uv})(s_u,s_v)=
 \begin{cases}C_{uv}(s_u,s_v),&s_u+s_v=0,\\0,&\text{otherwise.}\end{cases}
\tag{9b}
\]

The hafnian of the twirled covariance therefore performs the charge
projection independently on every matched edge.  The target projection is
only the single global condition `sum_v s_v=0`.  Proposition 2.1 says these
can never agree for `n>=4`.

In particular

\[
             H(C)=Z_n\quad\Longrightarrow\quad H(\Pi C)\ne Z_n. \tag{9c}
\]

Thus the ordinary finite-group averaging argument cannot be a global bridge:
the matching map is degree `n/2`, and edgewise averaging creates mixed orbit
choices independently on its `n/2` factors.  Averaging the *output* does
preserve `Z_n`, but it is not the hafnian of the averaged covariance.

Nor does target invariance force source invariance up to a target-preserving
gauge in general.  At `n=4`, Fourier-transform the exact three-one-factor
construction on `K_4`.  It maps to `Z_4`.  If a target-preserving local gauge
made its covariance `Z/3`-invariant, that gauged covariance would contradict
Proposition 2.1.  Hence symmetry lifting already fails for an exact source at
the first nontrivial order.  Any lifting theorem for `n>=6` would need a new
order-dependent rigidity hypothesis; it cannot follow from equivariance or
Reynolds averaging alone.

## 3. Four vacuum-closed pairs are impossible

Retain only charges `0,1`.  Suppose there are `m` designated pairs and a
remaining vertex set `R` such that

\[
 M=\{a_ib_i:1\le i\le m\}:
 \quad C_{a_i v}(0,0)=C_{b_i v}(0,0)=0
       \quad\bigl(v\notin\{a_i,b_i\}\bigr),
 \qquad C_{a_i v}(1,0)=0\quad(v\in R),
 \qquad b_i:=C_{a_ib_i}(0,0)\ne0.                             \tag{10}
\]

All remaining vertices form an even set `R`.  (If `R` were odd, the
all-zero hafnian would vanish.)  Put `h=haf C[R](0,0)`.  The all-zero
coefficient in (6) factors as

\[
                              h\prod_i b_i=1.                 \tag{10a}
\]

In particular `h` and every `b_i` are nonzero.  No condition is imposed on
the covariance inside `R`; it may support arbitrarily many perfect matchings
and arbitrary complex cancellation.  The last vanishing in (10) is
essential: charge-zero isolation alone would not prevent a flipped `a_i`
from opening an alternating path through `R`.

For `i,j` define

\[
                         d_{ij}:={C_{a_ib_j}(1,0)\over b_j}.  \tag{11}
\]

Here and below the arguments of `C` are placed at the displayed endpoints;
this convention retains asymmetric endpoint data.

For `I subseteq [m]`, flip precisely the vertices `a_i`, `i in I`, from
charge zero to charge one.  The vertices in `R` must still match wholly
inside `R`: at charge zero they have no covariance edge to a designated
pair.  A simple defect count then forces every unflipped pair `a_kb_k`,
`k notin I`, to use its base edge.  Indeed, if `r` unflipped pairs were
opened, the opened pairs would contain `|I|+2r` charge-zero vertices but
only `|I|` charge-one vertices.  Since (10) permits no edge between zero
vertices from different designated pairs, these vertices cannot all be
matched.  The same count rules out an edge between two flipped vertices.
Consequently a nonzero matching sends each flipped `a_i` to one of the zero
vertices `b_j`, `j in I`.  Hence these matchings are in bijection with
permutations of `I`.  Their weights, together with (10a), give the exact
identity

\[
 \mathbb E\left(\prod_{i\in I}X_{a_i,1}
          \prod_{v\notin\{a_i:i\in I\}}X_{v,0}\right)
   =h\left(\prod_{k\notin I}b_k\right)
      \operatorname {per}\bigl(C_{a_ib_j}(1,0)\bigr)_{i,j\in I}
   =\operatorname {per}D[I].                                 \tag{12}
\]

Combining (6) and (12),

\[
             \operatorname {per}D[I]={\bf1}_{|I|=0\pmod3}.  \tag{13}
\]

Singleton and two-element sets imply

\[
                 d_{ii}=0,\qquad d_{ij}d_{ji}=0.             \tag{14}
\]

For distinct `i,j,k`, the principal `3 by 3` permanent is

\[
              d_{ij}d_{jk}d_{ki}+d_{ik}d_{kj}d_{ji}=1.       \tag{15}
\]

By (14), at most one of the two products in (15) is nonzero.  Therefore
exactly one is nonzero, and every triple is a directed three-cycle in the
tournament whose edge `i -> j` means `d_ij != 0`.  This is impossible on
four vertices: a vertex with at least two out-neighbors, together with any
two such neighbors, forms a transitive triple.  Restricting to any four
indices gives the contradiction for every `m>=4`.

**Theorem 3.1 (vacuum-closed-pair obstruction).**  No collection of arbitrary
complex `2 by 2` edge covariance blocks with Boolean Wick moments (6) can
have four or more designated pairs satisfying (10).  In particular, at
every even order `n>=8`, the all-zero scalar covariance of a three-color
realization cannot be supported on a single perfect matching (take `R`
empty).

The threshold in the tournament argument is sharp.  For `m=3`, the matrix

\[
 D=\begin{pmatrix}0&1&0\\0&0&1\\1&0&0\end{pmatrix}           \tag{16}
\]

has principal permanents `1,0,0,1` in sizes `0,1,2,3`.  Thus the obstruction
is genuinely the incompatibility among overlapping triples at four base
pairs, not a hidden positivity claim or a termwise assertion at six
vertices.

The exact combinatorial audit is
`computations/verify_fourier_isolated_vacuum_obstruction.py`.

## 4. A uniform exact one-shore construction

The Boolean shadow (6) cannot by itself be used after fixing half the
vertices of a bipartite source.  In fact the resulting one-shore condition
has an exact solution at every order.

Let `K_(m,m)` have left vertices `1,...,m` and right vertices `1,...,m`.
Keep every right charge equal to zero.  Define

\[
 R_m(t)=\sum_{\substack{0\le k\le m\\k=0\pmod3}}
                  {m\choose k}t^k.                           \tag{17}
\]

Its constant coefficient is one, so over `C` it has a factorization

\[
                         R_m(t)=\prod_{j=1}^m(1+x_jt),        \tag{18}
\]

where zero values `x_j=0` pad the factorization if `deg R_m<m`.  On the edge
from left vertex `i` to right vertex `j`, set

\[
 C_{ij}(0,0)=c_i,\qquad C_{ij}(1,0)=c_i x_j,
 \qquad\prod_{i=1}^m c_i={1\over m!}.                        \tag{19}
\]

If the set `I` of left charge-one vertices has size `k`, summing over the
`m!` bipartite perfect matchings gives

\[
 \begin{aligned}
 \sum_{\sigma\in S_m}\prod_iC_{i,\sigma(i)}({\bf1}_{i\in I},0)
 &= {1\over m!}\sum_{\sigma\in S_m}
                   \prod_{i\in I}x_{\sigma(i)}\\
 &= {k!(m-k)!\over m!}\,e_k(x_1,\ldots,x_m)\\
 &= {e_k(x_1,\ldots,x_m)\over {m\choose k}}
  ={f1}_{k=0\pmod3}.                                      \tag{20}
 \end{aligned}
\]

The penultimate equality uses (18), whose `t^k` coefficient is
`e_k(x)`.  This is precisely the restriction of the zero-sum target with
all right charges fixed to zero.

For the first relevant case `m=4`, take `a^3=4` and

\[
                       (x_1,x_2,x_3,x_4)=(a,a\omega,a\omega^2,0), \tag{21}
\]

because `product_j(1+x_jt)=1+4t^3`.  Thus (19)--(20) are an
explicit algebraic certificate, not a dimension count or a numerical fit.

**Proposition 4.1 (one-shore MOD3 realization).**  For every `m`, the
restriction of the `2m`-party zero-sum tensor obtained by fixing one shore
to charge zero is an exact restriction of the `K_(m,m)` perfect-matching
tensor.  Therefore any Fourier proof must couple equations from both shores;
no obstruction based only on one-shore Boolean flips can succeed.

This does not lift to a Krenn counterexample: when right charges are allowed
to vary, (19) supplies none of the required mixed-shore equations.  It is the
same logical gap as contracting one shore of the incidence tensor to the
ordinary permanent tensor.
