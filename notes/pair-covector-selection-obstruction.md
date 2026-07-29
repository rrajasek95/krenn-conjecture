# A general-covector obstruction to cleaning an active pair

## 1. The candidate selection principle

Let \(H_B(X)=\Delta_{B,q}\), delete a pair \(p,q\), and cap its two slots by
an arbitrary bilinear covector \(K\).  With
\(U=B\setminus\{p,q\}\), write

\[
 s(K)=\langle K,X_{pq}\rangle
\]

and let `R_K=(R_ab(K))` be the first-jet edge family

\[
 R_{ab}(K)=K\mathbin{\lrcorner}
 \left(X_{pa}\otimes X_{qb}+X_{pb}\otimes X_{qa}\right).     \tag{1}
\]

The exact cap formula is

\[
 K\mathbin{\lrcorner}H_B(X)
     =s(K)H_U(X)+DH_U(X)[R_K].                                \tag{2}
\]

If `s(K)!=0`, replacing the old edges by `X+R_K/s` creates higher terms.
When `|U|=4`, the entire correction is

\[
                       s(K)^{-1}H_U(R_K).                     \tag{3}
\]

The target cap is

\[
 K\mathbin{\lrcorner}\Delta_{B,q}
       =\sum_i\kappa_i(K)e_i^{\otimes U},\qquad
 \kappa_i(K)=K(e_i,e_i).                                    \tag{4}
\]

A natural strengthening of the desired existential pair-selection lemma
would be:

> **Active-edge covector-cleaning principle.**  For every tensor-active
> edge \(pq\) of an exact realization, some arbitrary covector \(K\)
> satisfies
> \(s(K)\prod_i\kappa_i(K)\ne0\) and kills the higher correction.

This would make any active edge, and in particular any forced coordinate
anchor, available for an order-two induction.  It is false even for two
colors.  The counterexample below varies all four entries of `K`; it is not
the already-falsified ansatz which only rescales `X` and `R` by two global
scalars.

## 2. An exact binary counterexample

Use the rational realization of `Delta_(6,2)` from
`notes/induction-route.md`, on vertices `1,...,6`:

\[
\begin{array}{c|c}
12&(e_0+e_1)e_0\\
34,56,24&e_0e_0\\
13&-e_1e_0\\
16,23&e_1e_1\\
45&\frac34e_1e_1\\
15,46&\frac12e_1e_1.
\end{array}                                                   \tag{5}
\]

Its four supported perfect matchings give exactly
\(e_0^{\otimes6}+e_1^{\otimes6}\), and every displayed edge has a nonzero
four-site cofactor.  In particular \(13\) is a tensor-active rank-one basis
edge.

Cap `p=1,q=3`.  Write the completely general covector as

\[
 K=\sum_{a,b=0}^1 k_{ab}e_a^*\otimes e_b^*.
\]

Since `X_13=-e_1e_0`,

\[
 s(K)=-k_{10},\qquad \kappa_0(K)=k_{00},\qquad
 \kappa_1(K)=k_{11}.                                      \tag{6}
\]

On `U=(2,4,5,6)`, direct use of (1) gives the only nonzero effective
entries

\[
\begin{array}{c|c}
R_{24}&(k_{00}+k_{10})e_0e_0\\
R_{25}&\frac12k_{11}e_1e_1\\
R_{26}&k_{11}e_1e_1\\
R_{45}&\frac12k_{10}e_0e_1\\
R_{46}&k_{10}e_0e_1.
\end{array}                                                   \tag{7}
\]

Only the pairings `25|46` and `26|45` contribute to `H_U(R_K)`, and they
have the same mixed coloring.  Hence

\[
 H_U(R_K)=k_{10}k_{11}\,
 e_1^{(2)}e_0^{(4)}e_1^{(5)}e_1^{(6)}
 =-s(K)\kappa_1(K)\,
 e_1^{(2)}e_0^{(4)}e_1^{(5)}e_1^{(6)}.                      \tag{8}
\]

Equation (8) is an all-covector polynomial identity.  If the cap sees the
active edge and retains both target colors, then
\(s(K)\kappa_0(K)\kappa_1(K)\ne0\), so (8), and therefore the correction
(3), is nonzero.  Neither \(k_{01}\) nor any choice of the other off-diagonal
entry can change it.

**Proposition 2.1.**  A tensor-active coordinate rank-one edge of an exact
binary GHZ realization need not admit any nondegenerate clean covector cap.

This rules out choosing a pair merely because it is active, rank one, or a
coordinate anchor.  It does **not** refute the weaker statement that every
exact realization has *some other* pair admitting a clean cap: the source
(5) has other clean pairs.  A proof of monotonicity must therefore contain
a genuinely global pair-selection argument.  The color-sensitive
stabilizer identities can help rank candidate edges, but activity or anchor
status alone cannot supply the selection criterion.

The exact symbolic audit is

```sh
uv run python computations/verify_general_covector_pair_cap_obstruction.py
```
