# Full-row square obstruction on the `011166` boundary

## 1. Outcome

Fix an invertible pair `p,q` in the eight-site problem, and suppose its six
outside zero-cross masks are exactly the union-five residual row

\[
                         (0,1,1,1,6,6)                  \tag{1}
\]

with the three `1` sites hard for colour `0` and the two `6` sites hard for
colours `1,2`.  This branch cannot occur in a realization of the ternary
diagonal.  The proof uses the full row at the unique nonwitness site, not a
covering argument on a partial diagonal.

Write the three exact singleton-`0` sites as `a,b,c`, the two exact
`{1,2}` sites as `u,v`, and the nonwitness as `k`.  At a generic point of
the incidence quadric, the contraction at `p,q` has the exact six-site
form

\[
 \sum_{r=0}^2\lambda_r e_r^{\otimes6}
       =\left[XY{Q^2\over2}\right]_{1^6},\qquad
 \lambda_r\ne0.                                        \tag{2}
\]

Here `X=sum_i x_i`, `Y=sum_i y_i`, and
`Q=sum_(i<j)A_ij` in the site-square-free algebra.  Equivalently, (2) is
the arbitrary-`z` five-hole identity of
[`n8-union-five-full-hole-response.md`](n8-union-five-full-hole-response.md)
before its nonwitness slot is contracted.

The proof has two ingredients.

1. All scalar four-site hafnians except the one complementary to `u,v`
   vanish.  A square-free factor calculation then forces the scalar edge
   `uv` to vanish and makes the two scalar edge rows into `u,v` have zero
   product.
2. Contracting `u,v` in their missing color turns (2) into a four-factor
   permanent equal to a pure fourth power.  A three-site injectivity lemma
   and a square-permanent obstruction force both scalar edge rows to be
   supported only at `k`.  Their common-core annihilation then forces the
   one supposedly nonzero four-site hafnian to vanish.

The singleton normal form used below is completely general.  The two
oppositely directed anchors are consequences of the putative full-row
identity, rather than extra hypotheses.  In particular, the third singleton
may be mixed or may carry an additional `p`- or `q`-anchor.  The two
UFD/staircase models in
[`n8-011166-factor-allocation-boundary.md`](n8-011166-factor-allocation-boundary.md)
are special cases, so neither has an extension to the full row.

## 2. The unique nonzero scalar four-cofactor

For every outside site put

\[
 n_i=x_i\mathbin\times y_i,
 \qquad q_{ij}=n_i^TA_{ij}n_j.                          \tag{3}
\]

All six sites are nontriple, so every `x_i,y_i` is independent and every
pair response

\[
              R_{ij}=x_iy_j^T+y_ix_j^T                 \tag{4}
\]

has rank two.  The hard sets are

\[
 H_0=\{a,b,c\},\qquad H_1=H_2=\{u,v\}.                \tag{5}
\]

Leave two outside sites open and contract the other four by their `n_i`.
Only the hole pair `u,v` retains target colors: it retains colors `1,2`.
Its two-hole identity has a nonzero binary target and hence a nonzero
residual scalar.  Every other hole pair retains no color, and rank two of
(4) forces its residual scalar to vanish.

Let `C={k,a,b,c}` and use square-free scalar variables `t_i`.  Define

\[
\begin{aligned}
 q_C&=\sum_{i<j\in C}q_{ij}t_it_j,\\
 \ell&=\sum_{i\in C}q_{iu}t_i,\qquad
 m=\sum_{i\in C}q_{iv}t_i,\qquad
 d=q_{uv}.
\end{aligned}                                           \tag{6}
\]

The complete set of fifteen scalar two-hole conclusions is exactly

\[
 {q_C^2\over2}=h\,t_kt_at_bt_c,\quad h\ne0,
 \qquad q_C\ell=q_Cm=0,
 \qquad \ell m+dq_C=0.                                 \tag{7}
\]

Indeed, expand

\[
 q=q_C+t_u\ell+t_vm+d\,t_ut_v
\]

and compare the four-site coefficients of `q^2/2`.

The last three equations already force

\[
                         \boxed{d=0,\qquad \ell m=0.}   \tag{8}
\]

If `d` were nonzero, then `q_C=-d^{-1}\ell m`.  Multiplying
`q_C ell=0` by `m` would give

\[
              0=q_C\ell m=-d q_C^2,
\]

contrary to \(h\ne0\).  Equation (8) follows.

## 3. The four-factor equation

Because `u,v` are exact-double sites and their binary two-hole target is
nonzero, both star pairs span the active coordinate plane.  Thus

\[
 \operatorname {span}\{x_u,y_u\}
 =\operatorname {span}\{x_v,y_v\}=\langle e_1,e_2\rangle,
 \qquad n_u,n_v\in\mathbb C^*e_0.                        \tag{9}
\]

Contract the two sites `u,v` in (2) by `n_u,n_v`, but leave all four sites
of `C` open.  For \(i\in C\), put

\[
 L_i=A_{iu}n_u,\qquad M_i=A_{iv}n_v.                   \tag{10}
\]

Orienting an edge in the other direction only transposes this notation.
The scalar transverse coordinates are

\[
 n_i^TL_i=\ell_i,\qquad n_i^TM_i=m_i.                  \tag{11}
\]

Since both deleted stars vanish in color `0` at `u,v`, the two star
factors in (2) must lie in `C`.  The two internal edges either use `uv`,
giving `dQ_C`, or connect `u,v` separately into `C`, giving the two new
linear factors `L,M`.  By (8), the first case is zero.  Thus (2) gives the
exact four-site identity

\[
          \boxed{\operatorname {Per}_C(X,Y,L,M)
                        =\Lambda e_0^{\otimes C},\qquad\Lambda\ne0,} \tag{12}
\]

together with `ell m=0`.

## 4. Two elementary permanent lemmas

The first lemma will be used repeatedly.

**Lemma 4.1 (injective triangle response).**  At three sites let each
`x_i,y_i` be independent.  Then

\[
 (v_1,v_2,v_3)\longmapsto
 R_{12}\otimes v_3+R_{13}\otimes v_2+R_{23}\otimes v_1 \tag{13}
\]

is injective.

**Proof.**  Extend `x_i,y_i` to a local basis.  A component of `v_i`
outside their span occurs only in the term \(R_{jk}\otimes v_i\), so it must
vanish.  Write `v_i=s_ix_i+t_iy_i`.  The six remaining coefficient
equations split into

\[
 s_1+s_2=s_1+s_3=s_2+s_3=0,
 \qquad
 t_1+t_2=t_1+t_3=t_2+t_3=0.                            \tag{14}
\]

Each coefficient matrix has determinant `2`; hence every `s_i,t_i` is
zero. `QED`

The next lemma is the only place where the singleton anchor geometry is
used.

Its two directed-anchor hypotheses are forced in the present row.  Contract
(2) at `k,u,v` by their common annihilators.  The two exact-double sites
kill target colors `1,2`, whereas all three contracted covectors retain
color `0`.  On the three singleton holes the result is therefore a
nonzero pure-color triangle response of the form (10) in
[`n8-union-five-full-hole-response.md`](n8-union-five-full-hole-response.md).
Lemma 2 of that note forces a `p`-side `0`-anchor and a `q`-side `0`-anchor
at distinct singleton sites.  Relabel those sites as `a,b`; the remaining
singleton is `c`.

**Lemma 4.2 (no square fourth power).**  Suppose `a,b,c` are exact
singleton-`0` sites and `k` is a nonwitness.  There is no vector family
`Z_i` on
`C={k,a,b,c}` for which

\[
                 \operatorname {Per}_C(X,Y,Z,Z)
                           =\rho e_0^{\otimes C},qquad\rho\ne0.     \tag{15}
\]

**Proof.**  Since `k` is a nonwitness, `x_k,y_k` are independent and
\(e_0\notin\operatorname {span}\{x_k,y_k\}\).  Thus
\(n_k(e_0)\ne0\) for \(n_k=x_k\mathbin\times y_k\).  Contract (15) at
`k` by `n_k`.  The two star factors are killed there, whereas the right
side is nonzero.  Consequently `n_k(Z_k)` is nonzero and

\[
                 \operatorname {Per}_{abc}(X,Y,Z)
                              =\nu e_0^{\otimes3},\qquad\nu\ne0.     \tag{16}
\]

At each singleton write \(e_0=a_ix_i+b_iy_i\).  In the local `X,Y`
bases, the left side of (16) has zero `XXX` and `YYY` coefficients.  The
corresponding target coefficients are \(\nu\prod_i a_i\) and
\(\nu\prod_i b_i\).  Thus one singleton is a `q`-side anchor and a
distinct singleton is a `p`-side anchor.  Relabel them as `b` and `a`,
respectively.

Make independent local changes of basis which preserve the target line.
The resulting completely general normal form is

\[
\begin{array}{c|cc}
 &x_i&y_i\\ \hline
 a&e_0&Ae_0+w_a\\
 b&Be_0+w_b&e_0\\
 c&Ce_0+Uw_c&De_0+Vw_c,
\end{array}                                             \tag{17}
\]

where

\[
                  \delta=CV-DU\ne0.                    \tag{18}
\]

The cases `U=0` and `V=0` allow an extra directed anchor at `c`; the mixed
case has \(UV\ne0\).

Direct coefficient comparison, or Lemma 2 of the full-hole-response note,
gives the unique solution

\[
\begin{aligned}
 Z_a&={\nu\over2\delta}\bigl((AU+V)e_0+Uw_a\bigr),\\
 Z_b&=-{\nu\over2\delta}\bigl((BV+U)e_0+Vw_b\bigr),\\
 Z_c&={\nu\over2}e_0.                                  \tag{19}
\end{aligned}
\]

Assume first \(UV\ne0\).  In the coefficient with singleton word
`w_aw_bw_c`, the term having `Z_k` is zero by (16), while the terms having
`x_k` and `y_k` have respective coefficients

\[
 -{UV^2\nu^2\over2\delta^2},qquad
 -{U^2V\nu^2\over2\delta^2}.                           \tag{20}
\]

Equation (15) would therefore force

\[
                         Vx_k+Uy_k=0,
\]

contrary to independence.  If `U=0`, the coefficient at
`w_aw_be_0` is \(-\nu^2x_k/(2C)\), which is nonzero.  If `V=0`, the same
coefficient is \(-\nu^2y_k/(2D)\).  These cover all possibilities allowed by
(18), and prove the lemma. `QED`

## 5. Zero-product support and the contradiction

Write `ell_i=n_i^TL_i` and `m_i=n_i^TM_i`.  We first show

\[
       \ell_a=\ell_b=\ell_c=m_a=m_b=m_c=0.             \tag{21}
\]

For linear forms in four square-free variables, `ell m=0` has the following
elementary classification.  If both forms are nonzero, their common
support has size at most two.  On a two-element support `{i,j}`, all four
entries are nonzero and

\[
                    {\ell_i\over\ell_j}
                         =-{m_i\over m_j}.              \tag{22}
\]

This follows immediately from the equations
`ell_i m_j+ell_j m_i=0`.  If one support had at least three elements, those
pair equations would force the other form to be zero.

Contract (12) at `k` by `n_k`.  Its right side is nonzero, so at least one
of `ell_k,m_k` is nonzero.

Suppose first that `m=0`.  The `k` contraction says

\[
 \ell_k\operatorname {Per}_{abc}(X,Y,M)
                         =\Lambda n_k(e_0)e_0^{\otimes3}.             \tag{23}
\]

Thus `ell_k ne 0`, and the unique triangle response has a nonzero vector at
each of `a,b,c`.  If, say, `ell_j ne 0` at a singleton, contracting (12) at
`j` gives

\[
                  \operatorname {Per}_{C\setminus j}(X,Y,M)=0.
\]

Lemma 4.1 makes all three displayed residual vectors zero, contradicting
(23).  Hence `ell` is supported only at `k`.  The case `ell=0` is
symmetric.

It remains to consider `ell,m` both nonzero.  Their common support contains
`k`.  A one-element support already proves (21).  Otherwise it is
`{k,j}` for one singleton `j`.  Put

\[
       R_i=\ell_kM_i+m_kL_i,qquad
       S_i=\ell_kM_i-m_kL_i.                            \tag{24}
\]

By (22), contraction of (12) at `j` is a nonzero scalar multiple of

\[
                   \operatorname {Per}_{C\setminus j}(X,Y,S)=0.
\]

Lemma 4.1 gives `S_i=0` at all three sites different from `j`.  Hence the
square-free square `S^2` is zero.  Solving (24) for `L,M` now rewrites
(12), up to a nonzero scalar, as

\[
                    \operatorname {Per}_C(X,Y,R,R)
                              =\rho e_0^{\otimes C},\qquad\rho\ne0,
\]

contradicting Lemma 4.2.  This proves (21).

Consequently `ell=ell_k t_k` and `m=m_k t_k`, with at least one of the two
coefficients nonzero.  If `ell_k ne 0`, the equation `q_C ell=0` forces

\[
                         q_{ab}=q_{ac}=q_{bc}=0.         \tag{25}
\]

The same conclusion follows from `q_Cm=0` when `m_k ne 0`.  But then

\[
 h=q_{ka}q_{bc}+q_{kb}q_{ac}+q_{kc}q_{ab}=0,           \tag{26}
\]

contradicting (7).  Therefore the residual row (1) is impossible. `QED`

## 6. Exact audit

Run

```text
.venv/bin/python computations/verify_n8_011166_square_obstruction.py
```

The checker verifies the general triangle solution (19), the three
off-diagonal coefficients used in Lemma 4.2, injectivity of (13), the
square-free decomposition (7), and the final hafnian implication (25)--
(26) symbolically over the rational function field.
