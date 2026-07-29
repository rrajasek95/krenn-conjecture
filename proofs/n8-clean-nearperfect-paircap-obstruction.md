# A site-graded pair-cap obstruction for every clean near-perfect core

## 1. Outcome

The full nine two-deletion caps retain more than the abstract quotient
algebra: in a catalectically exposed physical edge they recover every
individual product cell.  This gives a uniform obstruction whenever the
three colours expose a connected three-edge multigraph.

As a finite application, consider a six-site internal quadratic `q` with
exactly two nonzero monochromatic cells of each colour.  Suppose the two
colour-`c` cells match four sites and omit an edge `e_c`, and suppose none
of the three omitted physical edges occurs anywhere in the support of
`q`.  Then the full nine-cap equations are impossible over `C`, for every
choice of the six nonzero cell weights.

There are exactly 43,245 ordered supports in this clean near-perfect
chart.  The uniform connected-edge theorem excludes 36,045.  The other
7,200 supports form six orbits under site and colour permutations.  Three
orbits already fail the necessary condition `X_0 in im(H_q)` by a
two-coordinate left functional.  Singleton catalecticant rows and the
same crossed-target lemma exclude the other three.

This is a strict extension of the one sparse fixed-`q` chart in
`n8-full-pair-suspension-subchart-obstruction.md`.  It remains a sparse
six-site theorem: an arbitrary `q` need not have clean exposed edges.

## 2. Normalized nine-cap equations

Let `W` have `N=2r` sites and work in

\[
  \mathcal R_W=\bigotimes_{i\in W}(\mathbb C\oplus V_i),
  \qquad V_iV_i=0.
\]

For `q in (R_W)_2`, linear elements `p,s`, and a quadratic `Z`, put

\[
 Q(q)={q^r\over r!},\qquad
 B_q(p,s)={psq^{r-1}\over(r-1)!},\qquad
 H_q(Z)={Zq^{r-1}\over(r-1)!}.                         \tag{1}
\]

Delete two sites from a putative ternary source.  If `p_c,s_d` are its
two star rows and `a_cd` is its direct-edge matrix, coefficient extraction
at the deleted sites gives all nine equations

\[
 \boxed{\quad
 B_q(p_c,s_d)+a_{cd}Q(q)=\delta_{cd}X_c,
 \qquad 0\le c,d\le2,
 \quad}                                                  \tag{2}
\]

where `X_c=product_(i in W)x_(i,c)`.  This is the factorial-normalized
form of the equations in `two-deletion-quotient-level-algebra.md`.

Package all cap indices at a site-coordinate label `xi=(i,alpha)` as

\[
 P_\xi=(p_{0,i,\alpha},p_{1,i,\alpha},p_{2,i,\alpha})^t,
 \qquad
 S_\xi=(s_{0,i,\alpha},s_{1,i,\alpha},s_{2,i,\alpha})^t,
 \qquad x_\xi=(P_\xi,S_\xi).                            \tag{3}
\]

For two labels define the matrix

\[
 \Phi(x_\xi,x_\eta)=P_\xi S_\eta^t+P_\eta S_\xi^t.   \tag{4}
\]

Its `(c,d)` entry is exactly the cell of `p_cs_d` on the corresponding
physical edge.

## 3. Clean catalecticant exposure

Fix a physical edge `e={i,j}` and a colour `t`.  For colours
`alpha,beta`, let `gamma_(e,t)^(alpha,beta)` be the word which is `t` off
`e` and is `alpha,beta` at `i,j`.

Call `(e,t)` **exposed** by `q` if there is a nonzero scalar `lambda` such
that, for every quadratic `Z` and all `alpha,beta`,

\[
 [\gamma_{e,t}^{\alpha,\beta}]H_q(Z)
       =\lambda Z_e(\alpha,\beta).                       \tag{5}
\]

Call it **clean** when in addition the entire matrix `q_e` is zero.  Since

\[
                         H_q(q)=rQ(q),                   \tag{6}
\]

the direct-edge term in (2) vanishes in every row (5) of a clean exposed
edge.  Taking all nine cap indices at once yields

\[
 \boxed{\quad
 \Phi(x_{i,\alpha},x_{j,\beta})
   =\lambda^{-1}\delta_{\alpha t}\delta_{\beta t}E_{tt}.
 \quad}                                                   \tag{7}
\]

Thus one clean exposed edge gives a full `3 by 3` block of physical
relations, not merely a product class modulo `ker(H_q)`.

## 4. The crossed-target lemma

We need one elementary classification.  Call a nonzero point `(P,S)`
`P`-pure if `S=0`, `S`-pure if `P=0`, and mixed otherwise.

**Lemma 4.1 (zero-pair classification).**  If nonzero `x=(P,S)` and
`y=(P',S')` satisfy `Phi(x,y)=0`, then either both are `P`-pure, both are
`S`-pure, or both are mixed and

\[
                         y=\rho(P,-S)                    \tag{8}
\]

for some nonzero `rho`.

**Proof.**  If one component of `x` is zero, the equation immediately
forces the same component of `y` to be zero.  In the mixed case both sides
of

\[
                         PS'^t=-P'S^t
\]

are nonzero decomposable tensors.  Equality of their two factors gives
`P'=rho P` and `S'=-rho S`.  `QED`

**Lemma 4.2 (crossed targets force purity).**  Let `c ne d` and let
`A,B,C,D` be nonzero.  If

\[
 \Phi(A,B)=uE_{cc},\qquad \Phi(C,D)=vE_{dd},
 \qquad \Phi(A,D)=\Phi(C,B)=0,                           \tag{9}
\]

with `uv ne 0`, then all four points are pure.  The zero pairs `(A,D)` and
`(C,B)` have one common purity type, while the other pair has the opposite
type.

**Proof.**  Apply Lemma 4.1 to the two zero pairs.  If one is `P`-pure and
the other `S`-pure, (9) has precisely the asserted form.  They cannot be
pure of the same type because one target would vanish.

If one zero pair is mixed and the other pure, the two target equations
force proportional nonzero components of the mixed antipodal pair to lie
on the distinct coordinate lines `Ce_c` and `Ce_d`, a contradiction.  If
both zero pairs are mixed, write

\[
 D=\rho(P_A,-S_A),\qquad B=\sigma(P_C,-S_C).
\]

Direct substitution gives

\[
                         \Phi(C,D)=-{\rho\over\sigma}\Phi(A,B),
\]

which would make `E_cc` proportional to `E_dd`.  This is impossible for
`c ne d`.  `QED`

## 5. Uniform connected exposed-edge obstruction

**Theorem 5.1.**  Suppose `(e_c,c)` is clean and exposed by `q` for each
`c=0,1,2`.  Regard `(e_0,e_1,e_2)` as a three-edge multigraph, retaining
parallel edges.  If this multigraph is connected, the nine equations (2)
have no solution.

**Proof.**  Equation (7) supplies one nonzero target pair on each `e_c`
and zero for every crossed coordinate pair on that edge.

If some vertex is incident to all three edges, apply Lemma 4.2 to every
pair of colours at that vertex.  The three nonzero special points at the
vertex would have to be pairwise of opposite purity types, impossible for
two types.  This also covers a parallel pair with an adjacent third edge
and three parallel edges.

It remains to consider connected three-edge multigraphs of maximum degree
two.  They are a three-edge path and a triangle.

For a path, write the successive edges as colours `0,1,2`.  Lemma 4.2 on
the first two targets makes the two special points at their common vertex
pure of opposite types.  The target relation makes the two endpoints of
each edge opposite.  Apply the same argument to the last two targets.
On the middle edge, the colour-`0` point at one endpoint and the colour-`2`
point at the other endpoint are now nonzero pure points of opposite types.
Their `Phi` is a nonzero decomposable matrix, whereas (7) says it is zero.

For a triangle, propagate purity around the three target edges in the
same way.  On any one edge, the two special points belonging to the other
two colours end with opposite purity types.  Again their `Phi` is nonzero
but (7) requires zero.  `QED`

The theorem is uniform in the number of internal sites.  Its hypothesis
is a concrete source-catalecticant condition, not a property of an
abstract level algebra.

## 6. Every clean six-site near-perfect core

Now take six internal sites.  For each colour `c`, choose a matching `M_c`
of two physical edges, color both cells `(c,c)`, and let `e_c` be the
omitted pair.  Give the six cells arbitrary nonzero weights and include no
other cells in `q`.  Assume

\[
                   \{e_0,e_1,e_2\}\cap
                   \bigcup_c M_c=\varnothing.            \tag{10}
\]

For a word which is colour `c` off `e_c`, the only compatible pair of
`q`-cells is `M_c`.  Consequently `(e_c,c)` is clean and exposed.  If the
omitted-edge multigraph is connected, Theorem 5.1 applies immediately.

There are 43,245 ordered choices satisfying (10), of which 36,045 are
connected.  The 7,200 disconnected choices have the following six support
orbits under `S_6 times S_3`.  An entry

\[
                         e_c:M_c
\]

records the omitted edge and its two-cell matching.

| orbit | size | `(e_0:M_0; e_1:M_1; e_2:M_2)` | certificate |
|---|---:|---|---|
| `R0` | 1080 | `01:23,45; 01:23,45; 24:03,15` | two-word image witness |
| `R1` | 1080 | `01:23,45; 01:24,35; 25:03,14` | two-word image witness |
| `R2` | 2160 | `01:23,45; 02:13,45; 34:05,12` | two-word image witness |
| `R3` | 2160 | `01:23,45; 02:14,35; 34:05,12` | crossed singleton rows |
| `R4` | 360 | `01:23,45; 24:03,15; 35:02,14` | crossed singleton rows |
| `R5` | 360 | `01:23,45; 24:03,15; 35:04,12` | crossed singleton rows |

For unit cell weights, the following functionals annihilate the complete
image of `H_q` in `R0,R1,R2`, respectively:

\[
 [000000]-[000011],\qquad
 [000000]-[001111],\qquad
 [000000]-[000011].                                     \tag{11}
\]

Each takes value one on `X_0`, so the diagonal `(0,0)` cap is impossible.
For arbitrary nonzero cell weights, multiply the two coefficients in each
functional by the opposite nonzero matching products; the same two-row
cancellation holds.

For `R3,R4,R5`, label the two special endpoint points of `e_c` by
`z_(2c),z_(2c+1)`.  Singleton rows give the three targets

\[
             \Phi(z_0,z_1)\sim E_{00},\quad
             \Phi(z_2,z_3)\sim E_{11},\quad
             \Phi(z_4,z_5)\sim E_{22}.                  \tag{12}
\]

The following pairs are singleton zero rows; only five per orbit are
needed:

\[
\begin{array}{c|c}
R3&(03),(12),(04),(15),(24)\\
R4&(03),(12),(05),(14),(25)\\
R5&(03),(12),(04),(15),(24).
\end{array}                                               \tag{13}
\]

In every row of (13), the first two pairs cross the targets of colours
zero and one.  The next two cross the targets of colours zero and two
(with the second target reversed when necessary).  Lemma 4.2 therefore
makes all six points pure.  Target pairs must have opposite types and zero
pairs the same type.  The fifth zero pair in each row then joins opposite
types, a contradiction.

This excludes all six disconnected orbits and completes the clean
near-perfect chart theorem.

## 7. Exact audit

Run

```text
uv run python computations/verify_n8_clean_nearperfect_paircap_obstruction.py
```

The script uses integer support arithmetic.  It enumerates all clean
supports, checks the connected degree distribution, canonicalizes the
7,200 disconnected supports into the six displayed orbits, verifies every
column identity in (11), and reconstructs the singleton target and zero
rows in (12)--(13).
