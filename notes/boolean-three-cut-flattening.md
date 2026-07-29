# The Boolean `3 | (n-3)` flattening and a dense cap countermodel

This note isolates exactly what the rank-three flattening of the Boolean
Fourier shadow says, and also what it does **not** say.  Across three sites
the target has an exact rank-three residue factorization.  A general matching
source has an equally exact decomposition into its one-cross and three-cross
sectors, but equality constrains only their sum.  In particular, rank three
does not turn a six-site cap into a six-site Wick minor.

The last point has a fully algebraic countermodel.  A complete bipartite
`K_(6,6)` cap, with every cross edge nonzero in both Boolean coordinates,
contracts exactly to the six-bit `MOD_3` tensor even though all internal
edges among the six surviving sites vanish.  This is not a counterexample to
Krenn's conjecture: it does not satisfy the full twelve-site zero-sum
identity.  It is a counterexample only to the proposed rank/cap reduction.

## 1. Coefficient convention

For an oriented edge `i<j`, write

\[
 E_{ij}(z_i,z_j)=a_{ij}+b_{ij}z_i+c_{ij}z_j+d_{ij}z_i z_j
                =\sum_{s,t\in\{0,1\}}e_{ij}^{st}z_i^s z_j^t .
\tag{1}
\]

Thus `e_ij^(00)=a_ij`, `e_ij^(10)=b_ij`,
`e_ij^(01)=c_ij`, and `e_ij^(11)=d_ij`.  The coefficient of
`z^epsilon` in the hafnian polynomial is

\[
 [z^\epsilon]H_n(E)
 =\operatorname {haf}\bigl(e_{ij}^{\epsilon_i\epsilon_j}\bigr).
\tag{2}
\]

It is important here to select a coefficient as in (2), rather than to
evaluate (1) at `z_i=epsilon_i`.

The Boolean Fourier target is

\[
 Z_n(z)=\sum_{\substack{S\subseteq[n]\\|S|=0\pmod3}}z^S.
\tag{3}
\]

## 2. Exact rank-three target factorization

Let `L={1,2,3}` and `R=[n]\L`.  For `r in Z/3`, put

\[
 V_r(z_R)=\sum_{\substack{B\subseteq R\\|B|=r\pmod3}}z^B
\tag{4}
\]

and put

\[
 \begin{aligned}
 U_0&=1+z_1z_2z_3,\\
 U_1&=z_1+z_2+z_3,\\
 U_2&=z_1z_2+z_1z_3+z_2z_3.
 \end{aligned}
\tag{5}
\]

Sorting a monomial by its left and right cardinalities gives the exact
factorization

\[
 \boxed{Z_n=U_0V_0+U_1V_2+U_2V_1.}
\tag{6}
\]

For `n>=6`, the three `U_r` are nonzero with disjoint monomial supports,
and so are the three `V_r`.  Hence the `2^3 by 2^(n-3)` coefficient
flattening has rank exactly three.  Equivalently, with a primitive cube root
`omega`,

\[
 {f1}_{|A|+|B|=0\pmod3}
 ={1\over3}\sum_{q=0}^2\omega^{q|A|}\omega^{q|B|}.
\tag{7}
\]

If `F_alpha(z_R)` denotes the coefficient row of a putative source after
selecting the left state `alpha in {0,1}^3`, equality with (3) says exactly

\[
 \begin{array}{c|c}
 \alpha&F_\alpha\\ \hline
 000,111&V_0\\
 100,010,001&V_2\\
 110,101,011&V_1.
 \end{array}
\tag{8}
\]

These are five row-equality relations, in addition to the choice of the
three common rows.  They are relations on the **total** matching sum.

## 3. Exact one-cross/three-cross source formula

For an even subset `T subseteq R`, let `H_T(z_T)` be the hafnian polynomial
of the source induced on `T`, with `H_emptyset=1`.  After selecting the left
state `s` at vertex `i`, retain the right endpoint of a cross edge as the
linear polynomial

\[
             E_{ir}^{,s}(z_r)=e_{ir}^{s0}+e_{ir}^{s1}z_r.
\tag{9}
\]

Define the one-cross boundary row

\[
 G_{i,s}=\sum_{r\in R}E_{ir}^{,s}(z_r)H_{R\setminus\{r\}}
\tag{10}
\]

and, for `alpha in {0,1}^L`, the three-cross boundary row

\[
 Q_\alpha=
 \sum_{\phi:L\hookrightarrow R}
   \left(\prod_{i\in L}E_{i,\phi(i)}^{\,\alpha_i}(z_{\phi(i)})\right)
   H_{R\setminus\operatorname {im}\phi}.
\tag{11}
\]

The injections in (11) have labeled domain `L`; there is no factorial in
the formula.  Every perfect matching crosses the odd cut in either one or
three edges.  Partitioning the matchings by that number gives

\[
 \boxed{
 \begin{aligned}
 F_\alpha={}&e_{23}^{\alpha_2\alpha_3}G_{1,\alpha_1}
             +e_{13}^{\alpha_1\alpha_3}G_{2,\alpha_2}
             +e_{12}^{\alpha_1\alpha_2}G_{3,\alpha_3}
             +Q_\alpha .
 \end{aligned}}
\tag{12}
\]

Formula (12) is the exact source-side companion to (6).  Substituting (12)
in (8) does not separate `Q_alpha` from the three one-cross summands.  A
rank argument that discards either sector is therefore making an additional
claim, not reading off a consequence of flattening rank.

## 4. An exact dense cap with the same six-bit flattening

Here is a sharp countermodel to that additional claim.  Take six surviving
Boolean sites `U={1,...,6}` and six capped sites `W={1',...,6'}`.  Keep only
the complete bipartite cross block `U x W`; in particular, every internal
edge in `U` is zero.  Contract each site in `W` with one fixed coordinate.

Choose nonzero algebraic numbers `a,b,omega` satisfying

\[
             ab=1,\qquad a^3+b^3=20,\qquad
             \omega^2+\omega+1=0.
\tag{13}
\]

For example, take `a^3=10+3sqrt(11)`, `b=a^(-1)`, and a primitive cube
root `omega`.  Set

\[
 (x_1,\ldots,x_6)=
 (a,a\omega,a\omega^2,b,b\omega,b\omega^2).
\tag{14}
\]

Choose nonzero row scalars `c_i` with

\[
                         \prod_{i=1}^6c_i={1\over6!}.
\tag{15}
\]

On the cross edge `i j'`, after contracting `j'`, put the two-entry vector

\[
                         c_i(e_0+x_j e_1).
\tag{16}
\]

Every one of the 36 cross edges is present, and both of its Boolean entries
are nonzero.  This is therefore dense on the entire boundary-cap block.
The elementary-symmetric generating polynomial of (14) is

\[
 \begin{aligned}
 \prod_{j=1}^6(1+x_jt)
  &=(1+a^3t^3)(1+b^3t^3)\\
  &=1+20t^3+t^6.
 \end{aligned}
\tag{17}
\]

If `S subseteq U` is the set of boundary sites in state one and `|S|=k`,
the contracted matching sum is the permanent of the corresponding `6 by 6`
scalar cross matrix.  For each chosen `k`-set of columns, there are
`k!(6-k)!` permutations, so it is exactly

\[
 \begin{aligned}
 \operatorname {per}M_S
 &=\left(\prod_i c_i\right)k!(6-k)!
       e_k(x_1,\ldots,x_6)\\
 &={e_k(x_1,\ldots,x_6)\over {6\choose k}}
  ={f1}_{k=0\pmod3}.
 \end{aligned}
\tag{18}
\]

Thus the cap output is **exactly** `Z_6`.  In particular its `3|3`
flattening is exactly the rank-three tensor (6).  Nevertheless the principal
six-site Wick minor on `U` is zero, because there is not a single internal
edge on `U`; all of (18) comes from the six-cross sector of the cap.

This example proves the precise negative conclusion:

**Proposition.**  Exact agreement with the rank-three Boolean flattening,
even exact agreement of an entire six-boundary cap with `Z_6`, does not force
the principal six-site Wick minor or a termwise one-cross/three-cross
identification.  The failure persists with a fully dense, nonzero
boundary-cap cross block.

The example does not obey the unconstrained twelve-site target equations at
the capped vertices.  Therefore it closes only the flattening-to-minor
shortcut.  A successful use of (6)--(12) must bring in equations involving
the complementary states, or a new invariant that controls the crossing
sector rather than merely the total row space.

The exact finite audit is
`computations/verify_boolean_three_cut_countermodel.py`.
