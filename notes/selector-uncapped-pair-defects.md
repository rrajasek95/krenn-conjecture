# What termwise selectors do not see: the uncapped pair defect

## 1. Outcome

The all-complement bridge leaves a termwise-selector branch.  An exact
diagnostic shows precisely what is missing there.  There is an integral
eight-site block system with

* an invertible block `A_pq`;
* twelve exact termwise selector declarations, covering every outside site
  and all three target colours; and
* matching tensor equal to `Delta_(8,3)` plus exactly eight mixed basis
  tensors, each with coefficient one.

Thus neither a missing target colour nor a one-coordinate defect is the
essential gap.  The first invisible coefficients can be three positions
away from a constant word.  Six of the eight defects use the edge `pq` and
the two perfect matchings of the internal six-cycle; the other two are the
extra mixed perfect matchings in the union of the three selected
one-factors.

This separation gives a general exact identity.  For every colouring `x`
of the six outside sites, the entire uncapped `p,q` coefficient matrix is

\[
 D_x=h_xA_{pq}+\sum_{\{u,v\}\subset R}h_{uv,x}
       (P_u(x_u)Q_v(x_v)^T+P_v(x_v)Q_u(x_u)^T).          \tag{1}
\]

Here `h_x` and `h_(uv,x)` are internal six- and four-site hafnian
coefficients, while `P_u(c)=A_pu e_c` and `Q_u(c)=A_qu e_c`.  In a genuine
solution, `D_x` is `E_rr` for `x=r^R` and zero for every nonconstant `x`.
Consequently every nonconstant internal coefficient `h_x ne0` forces the
avoiding-`pq` correction in (1) to have rank three.  In particular at least
three participating `p`-star columns and at least three participating
`q`-star columns must span their full endpoint spaces.  This closes the
subbranch in which a nonconstant internal monomial has only a two-dimensional
extension star.

Termwise selectors interact with (1) in a transparent but limited way.
Writing a selector as three `p,q` matrix functionals, its fibrewise
contraction kills exactly the `pq`-used terms and the terms in which `p` or
`q` is paired to the selector site.  It tests only the remaining
three-cross correction.  The full identity, however, requires cancellation
of the two matrices before that projection.  This is the precise uncapped
compatibility still needed to close the termwise branch.

## 2. The uncapped pair-cap matrix

Let `B={p,q} disjoint-union R`, with `|R|=6`.  For a word
`x:R -> {0,1,2}`, put

\[
\begin{aligned}
 h_x&=[e_x]H_R(A),\\
 h_{uv,x}&=[e_{x|R\setminus\{u,v\}}]
                         H_{R\setminus\{u,v\}}(A),\\
 P_u(x_u)&=A_{pu}e_{x_u}\in V_p,\qquad
 Q_u(x_u)=A_{qu}e_{x_u}\in V_q.                         \tag{2}
\end{aligned}
\]

Let `D_x in V_p tensor V_q` be the coefficient of `e_x` in the full
matching tensor, leaving `p,q` open.

**Lemma 2.1 (uncapped pair identity).**  For arbitrary edge matrices,

\[
\boxed{
 D_x=h_xA_{pq}+\sum_{\{u,v\}\subset R}h_{uv,x}
       \big(P_u(x_u)Q_v(x_v)^T+P_v(x_v)Q_u(x_u)^T\big).} \tag{3}
\]

If `H_B(A)=Delta_(B,3)`, then

\[
 D_x=\begin{cases}
 E_{rr},&x=r^R,\\
 0,&x\text{ nonconstant}.
 \end{cases}                                             \tag{4}
\]

**Proof.**  A matching either uses `pq`, giving `A_pq` times an internal
matching of `R`, or avoids `pq`.  In the second case `p,q` have two distinct
partners `u,v`; the two possible assignments give the two outer products
in (3), and the other four outside sites contribute `h_(uv,x)`.  These
cases are disjoint and exhaustive.  Equation (4) is the corresponding
coefficient slice of the target. `QED`

The formula is coefficientwise and therefore retains arbitrary complex
cancellation.  In particular, `h_x ne0` means the complete internal
coefficient is nonzero; it does not select an individual internal matching.

## 3. A rank-three extension requirement

Let

\[
 X_x=\sum_{\{u,v\}\subset R}h_{uv,x}
       \big(P_u(x_u)Q_v(x_v)^T+P_v(x_v)Q_u(x_u)^T\big). \tag{5}
\]

For a word `x`, call a `p`-column `P_u(x_u)` participating if it occurs in
a nonzero outer-product summand of (5), and define participating `q`
columns similarly.

**Corollary 3.1 (uncapped rank coverage).**  Suppose `A_pq` is invertible
and (4) holds.

1. If `x` is nonconstant and `h_x ne0`, then
   \[
                         X_x=-h_xA_{pq}                  \tag{6}
   \]
   has rank three.  The participating `p`-columns span `V_p`, and the
   participating `q`-columns span `V_q`.  In particular there are at least
   three participating sites on each endpoint.
2. If `x=r^R` and `h_x ne0`, then
   \[
                         X_x=E_{rr}-h_xA_{pq}             \tag{7}
   \]
   has rank at least two, so both participating endpoint-column spans have
   dimension at least two.

**Proof.**  Equation (6) follows from (3)--(4), and its right side is
invertible.  The column space of (5) is contained in the span of its
participating `P` vectors, while its row space is contained in the span of
its participating `Q` vectors.  Both spans must therefore have dimension
three.  For (7), the rank inequality gives
`rank(E_rr-h_xA_pq)>=3-1=2`, and the same span argument applies. `QED`

Thus a nonconstant monomial in `H_R` cannot merely be cancelled in the
aggregate.  It needs a word-aligned, full-rank system of extensions through
both deleted stars.  This is substantially stronger than ordinary support
or matching-coveredness.

## 4. Exact coupling to a termwise selector

Fix a selector site `s` of colour `r`, and expand

\[
 \Theta_s=\sum_{k=0}^2\Phi_{s,k}\otimes e_k^{*(s)},
 \qquad \Phi_{s,k}\in(V_p\otimes V_q)^*.                 \tag{8}
\]

For a word `y` on `U_s=R\setminus\{s\}`, let `x(k)` extend `y` by
`x(k)_s=k`.  Applying the selector to the uncapped fibres gives

\[
 \boxed{
 \sum_{k=0}^2\langle\Phi_{s,k},D_{x(k)}\rangle
       =\begin{cases}1,&y=r^{U_s},\\0,&\text{otherwise.}\end{cases}} \tag{9}
\]

Split (3), relative to `s`, as

\[
\begin{aligned}
 D_x^{(1,s)}={}&h_xA_{pq}
   +\sum_{u\in U_s}h_{su,x}
       \big(P_s(x_s)Q_u(x_u)^T+P_u(x_u)Q_s(x_s)^T\big),\tag{10}\\
 D_x^{(3,s)}={}&\sum_{\{u,v\}\subset U_s}h_{uv,x}
       \big(P_u(x_u)Q_v(x_v)^T+P_v(x_v)Q_u(x_u)^T\big).\tag{11}
\end{aligned}
\]

The superscripts are the crossing numbers of the triple shore `pqs`.
Recall the termwise one-cross vector

\[
 L_u^s=\Theta_s\mathbin{\lrcorner}
   (A_{pq}\otimes A_{su}+A_{ps}\otimes A_{qu}
                              +A_{qs}\otimes A_{pu})\in V_u. \tag{12}
\]

**Lemma 4.1 (selector/pair-fibre coupling).**  For every `y`,

\[
 \sum_k\langle\Phi_{s,k},D_{x(k)}^{(1,s)}\rangle
   =\sum_{u\in U_s}h_{su,y}\,(L_u^s)_{y_u}.             \tag{13}
\]

Consequently, if the selector is termwise, then

\[
 \sum_k\langle\Phi_{s,k},D_{x(k)}^{(1,s)}\rangle=0,
 \qquad
 \sum_k\langle\Phi_{s,k},D_{x(k)}^{(3,s)}\rangle
       =\mathbf1_{y=r^{U_s}}.                            \tag{14}
\]

**Proof.**  Expand the internal coefficient in the first term of (10) by
the partner of `s`:

\[
 h_{x(k)}=\sum_{u\in U_s}(A_{su})_{k,y_u}h_{su,y}.       \tag{15}
\]

Substitute (15) in (10), contract by `Phi_(s,k)`, and sum over `k`.
For fixed `u`, the three resulting contractions are respectively the three
terms in (12), evaluated at the coordinate `y_u`.  This proves (13).
Equation (14) follows from termwise vanishing and (9). `QED`

Equation (14) explains the countermodel below.  A termwise selector can be
perfect on every exposed word while being completely blind, after its one
functional projection, to the matrix cancellation required between
`D^(1,s)` and `D^(3,s)`.  The actual target equation (4) retains all nine
entries of every `D_x`; this is the additional compatibility a successful
continuation must exploit.

## 5. A balanced twelve-selector countermodel

Label the outside sites `0,...,5` and take the three edge-disjoint perfect
matchings

\[
\begin{aligned}
 M_0&=\{p0,q1,23,45\},\\
 M_1&=\{p2,q3,04,15\},\\
 M_2&=\{p4,q5,02,13\}.                                  \tag{16}
\end{aligned}
\]

Put `E_rr` on every edge of `M_r`, put

\[
 A_{pq}=\begin{pmatrix}0&1&0\\0&0&1\\1&0&0\end{pmatrix}, \tag{17}
\]

and set every other block to zero.  For each colour `r`, every site except
the `p`- and `q`-partners in `M_r` carries the coordinate selector

\[
                         \Theta_{s,r}=(e_r^*)^{\otimes\{p,q,s\}}. \tag{18}
\]

There are four declarations per colour, twelve total.  Every outside site
carries two colours.  As in the preceding selector-sector model,
`A_pq` has zero diagonal, the chosen `s` is not a `p/q` partner, and the
three-cross matching is forced to be `M_r`.  Hence all twelve identities

\[
 (\Theta_{s,r}\otimes\operatorname{id})T_1=0,
 \qquad
 (\Theta_{s,r}\otimes\operatorname{id})T_3=e_r^{\otimes5} \tag{19}
\]

hold, and all their `L_u^(s,r)` vanish separately.

The internal support on `R` is the six-cycle

\[
                         02,23,31,15,54,40.               \tag{20}
\]

It has two perfect matchings.  Tensor expansion gives exactly

\[
                         H_B=\Delta_{B,3}+\sum_{j=1}^8e_{z_j}, \tag{21}
\]

where, in the vertex order `(p,q,0,1,2,3,4,5)`,

\[
\begin{array}{c|c}
\text{uses }pq&z_j\\ \hline
\text{yes}&01110011, 01222200, 12110011,\\
          &12222200, 20110011, 20222200\\ \hline
\text{no}&12121212, 21212121.
\end{array}                                               \tag{22}
\]

The first six words are the three cells of `A_pq` times the two internal
perfect matchings.  The last two are the two additional perfect matchings
of the cubic graph `M_0 union M_1 union M_2`.  Every coefficient is one,
and no other defect occurs.  Four words in (22) have Hamming distance three
from the nearest constant word and four have distance four.  Thus all
constant, one-defect, and two-defect coefficients are already correct.

For each of the two nonconstant internal words `x` with `h_x=1`, the model
has `X_x=0`, so (6) fails by the full invertible matrix `A_pq`.  This is the
lowest-complexity uncapped obstruction: the selector projections (19) are
all exact, but the word-aligned rank-three extensions demanded by
Corollary 3.1 are absent.

The example is a diagnostic sector countermodel, not a realization of the
target.  Its role is to show sharply which uncapped equations are new.

## 6. Exact audit

Run

```text
.venv/bin/python computations/verify_selector_uncapped_pair_defects.py
```

The checker verifies (3) on a dense deterministic integer specialization,
audits all twelve selector equations and all sixty termwise vectors in the
balanced model, enumerates the complete `3^8` coefficient table, certifies
the eight-word residual (22) and its `6+2` matching-channel split, and
checks the two failed rank-three extensions exactly.
