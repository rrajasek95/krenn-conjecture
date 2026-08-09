# An adjacent cubic pair gives an exact two-site descent

## 1. Outcome

Let an exact ternary matching source on an even set `B` have two adjacent
literal cubic sites `p,q`.  Suppose their common edge has colour `c`.
Then there is an exact ternary matching source on

\[
                         B\setminus\{p,q\}.                 \tag{1}
\]

The construction is algebraic, preserves endpoint order, and allows
arbitrary complex aggregate blocks and cancellations.  It does not divide
by a residual tensor or require a genericity hypothesis.

Consequently an order-minimal counterexample of order at least eight cannot
contain an adjacent cubic pair.  At order eight the descent lands at order
six, which is excluded by
[`the arbitrary-complex six-site obstruction`](../proofs/six-site-arbitrary-complex-obstruction.md).
Combined with the majority-cubic reduction in
[`n8-oriented-rankone-curvature-full-nine-frontier.md`](n8-oriented-rankone-curvature-full-nine-frontier.md),
this closes the majority-cubic branch of the uniform rank-one/essential-star
dichotomy.  The curved rank-one full-nine overlap remains the other branch.

## 2. The adjacent packet

Write `d,e` for the two colours different from `c`.  Cubic rigidity makes
the direct block and the four other port rows literal coordinate cells:

\[
\begin{aligned}
 A_{pq}&=\lambda E_{cc},\\
 p_d&=\alpha_d e_d^{(u_d)},&s_d&=\beta_d e_d^{(v_d)},\\
 p_e&=\alpha_e e_e^{(u_e)},&s_e&=\beta_e e_e^{(v_e)} .
\end{aligned}                                                \tag{2}
\]

All five displayed scalars are nonzero.  At either cubic endpoint the
three physical neighbours are distinct, so `u_d != u_e` and
`v_d != v_e`.  The nonzero diagonal target rows also force
`u_d != v_d` and `u_e != v_e`; otherwise the corresponding star product
would be zero in the square-free site algebra.

Put `W=B\setminus{p,q}`, `|W|=2h`, and let `q` denote the aggregate
quadratic on `W`.  The nine pair equations give

\[
\begin{aligned}
 q^{[h]}&=\lambda^{-1}X_c,\\
 q^{[h-1]}_{W\setminus\{u_d,v_d\}}
     &=(\alpha_d\beta_d)^{-1}X_d,\\
 q^{[h-1]}_{W\setminus\{u_e,v_e\}}
     &=(\alpha_e\beta_e)^{-1}X_e.                         \tag{3}
\end{aligned}
\]

When their two sites are distinct, the crossed zero rows also give

\[
 q^{[h-1]}_{W\setminus\{u_d,v_e\}}=0,
 \qquad
 q^{[h-1]}_{W\setminus\{u_e,v_d\}}=0.                    \tag{4}
\]

The subscript notation in (3)--(4) is literal deletion of the displayed
physical sites.  If a crossed pair collides at one site, its star product
is zero before a cofactor is formed, and (4) is not asserted or needed.

## 3. Four distinct ports

First suppose `u_d,v_d,u_e,v_e` are four distinct sites.  In the aggregate
edge spaces on `W`, add the four endpoint-ordered coordinate cells

\[
\begin{array}{c|c|c}
\text{pair}&\text{endpoint colours}&\text{weight}\\ \hline
u_dv_d&(d,d)&\alpha_d\beta_d\\
u_ev_e&(e,e)&\alpha_e\beta_e\\
u_dv_e&(d,e)&\alpha_d\beta_e\\
u_ev_d&(e,d)&-\alpha_e\beta_d .
\end{array}                                                 \tag{5}
\]

Call their sum `r` and put `q'=q+r`.  Multiaffinity of the matching
polynomial is especially sparse here.  The first two linear insertion
terms are `X_d,X_e` by (3), and the last two vanish by (4).  Among pairs of
inserted cells, only the first two and the last two are vertex-disjoint.
They occupy the same four sites with the same endpoint-colour word, while
their weights add to

\[
 (\alpha_d\beta_d)(\alpha_e\beta_e)
 +(\alpha_d\beta_e)(-\alpha_e\beta_d)=0.                  \tag{6}
\]

No three inserted cells are pairwise disjoint.  Therefore, coefficient by
coefficient and for every `h`,

\[
                       (q')^{[h]}
            =\lambda^{-1}X_c+X_d+X_e.                     \tag{7}
\]

Notice that the sign in the final endpoint-ordered cell is essential.  It
is available because source weights are arbitrary complex numbers.

## 4. Port collisions

The inequalities following (2) leave only two possible cross
identifications: `u_d=v_e` and `u_e=v_d`, separately or together.  If
either occurs, the two same-colour pairs `u_dv_d` and `u_ev_e` share a
physical site.  Add only the first two cells in (5).  Their product is zero
in the square-free site algebra, so there is no quadratic insertion term;
their two linear terms are again `X_d,X_e`.  Equation (7) follows without
using either crossed zero row.  This also covers the double collision, in
which the two different coordinate cells lie in the same aggregate
physical block.

## 5. Inductive consequence and scope

All three coefficients in (7) are nonzero.  A diagonal colour rescaling at
one residual site normalizes `lambda^-1` to one and preserves the aggregate
matching-source model.  Thus `q'` is an exact ternary source on `N-2`
sites.

This is a genuine source construction, not merely a cut or output-tensor
identity.  It closes an adjacent literal cubic pair by minimal-order
descent.  It does **not** close the separate branch in which the structural
count selects two overlapping doubly-injective rank-one charts: those
sites need not be cubic, and their unresolved full-nine coupling remains
source-provenant.

## 6. Exact audit

Run

```sh
python3 computations/verify_adjacent_cubic_pair_descent.py
python3 -O computations/verify_adjacent_cubic_pair_descent.py
```

The checker enumerates every allowed equality pattern of the four physical
ports, retains endpoint colours, and performs the formal monomial-weight
calculation in (5)--(6).  In the four-distinct stratum it independently
checks that the two displayed opposite pairings are the only compatible
insertions and that no triple can occur.  In every collision stratum it
checks that the two same-colour insertions overlap.
