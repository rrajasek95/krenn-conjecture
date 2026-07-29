# The exposed-grid obstruction for the path and triangle equality cases

## 1. Result

The three-edge-path and triangle geometries in the rank-budget equality
frontier are impossible. This leaves only the wedge-plus-disjoint geometry
at rank budget twelve, together with rank budget strictly greater than
twelve.

The proof uses the whole typed double-quotient grid supplied by
[the full-rank-site response frontier](full-rank-site-response-invisibility-countermodel.md),
not only its nonzero target corner. It is support-independent: no individual
perfect-matching term is set to zero, and no coordinate ansatz is made for
the blocks of \(q\). Once the quotient identities are available, the proof
does not use \(q^{[3]}=0\).

More precisely, let the equality omission pairs be \(B_0,B_1,B_2\). The
following two configurations cannot occur:

\[
 B_0=AB,\quad B_1=BC,\quad B_2=CD,                    \tag{1a}
\]

or

\[
 B_0=AB,\quad B_1=BC,\quad B_2=CA.                    \tag{1b}
\]

The first is the three-edge path and has local ranks
\((2,1,1,2,3,3)\); the second is the triangle and has ranks
\((1,1,1,3,3,3)\).

## 2. Every omission pair exposes a complete grid

Write

\[
 {\cal M}_u=\{c:u\in B_c\}.
\]

At rank-budget equality, \(W_u\) is exactly the span of the target axes
whose colours are not in \({\cal M}_u\). Consequently the quotient axes

\[
 \{\bar e_c^{(u)}:c\in{\cal M}_u\}\subseteq V_u/W_u
\]

are nonzero and independent. Choose coefficient functionals
\(\lambda_{u,c}\in(V_u/W_u)^*\) satisfying

\[
 \lambda_{u,c}(\bar e_d^{(u)})=\delta_{cd}
       \qquad(c,d\in{\cal M}_u).                       \tag{2}
\]

For every exposed site-colour label \(u_c\), define

\[
\begin{aligned}
 P_{u,c}&=
 \bigl(\lambda_{u,c}(\bar p_{0,u}),
       \lambda_{u,c}(\bar p_{1,u}),
       \lambda_{u,c}(\bar p_{2,u})\bigr)^t,\\
 S_{u,c}&=
 \bigl(\lambda_{u,c}(\bar s_{0,u}),
       \lambda_{u,c}(\bar s_{1,u}),
       \lambda_{u,c}(\bar s_{2,u})\bigr)^t,\\
 x_{u,c}&=(P_{u,c},S_{u,c})\in\mathbb C^3\oplus\mathbb C^3.
                                                               \tag{3}
\end{aligned}
\]

For \(x=(P,S)\) and \(y=(P',S')\), put

\[
                       \Phi(x,y)=P(S')^t+P'S^t.         \tag{4}
\]

Suppose \(B_c=uv\). Equation (31) of the full-rank-site frontier says that
the entire quotient tensor \(N_{uv}\), not merely one of its coordinates,
equals

\[
 \theta_c E_{cc}\otimes\bar e_c^{(u)}\otimes
                    \bar e_c^{(v)},\qquad\theta_c\ne0. \tag{5}
\]

Applying the functionals (2) gives the exposed-grid rule

\[
 \Phi(x_{u,d},x_{v,e})=
 \begin{cases}
   \theta_cE_{cc},&d=e=c,\\
   0,&\text{otherwise},
 \end{cases}
 \quad d\in{\cal M}_u,\ e\in{\cal M}_v.               \tag{6}
\]

In particular, the two points at the target corner of every grid are
nonzero. All of (6) is a consequence of the nine tensor response equations
and uniqueness of the simple quotient tensor. It does not split
\(F=q^{[2]}\) into individual matching terms.

## 3. The crossed-target lemma

Call a nonzero point \((P,S)\) **\(P\)-pure** if \(S=0\), **\(S\)-pure** if
\(P=0\), and **mixed** otherwise.

**Lemma 3.1 (zero-pair classification).** If \(x,y\ne0\) and
\(\Phi(x,y)=0\), then either \(x,y\) are pure of the same type or there are
nonzero \(P,S\) and \(\rho\) such that

\[
                         x=(P,S),\qquad y=\rho(P,-S).   \tag{7}
\]

**Proof.** Write \(x=(P,S)\), \(y=(P',S')\). If \(S=0\), then
\(P(S')^t=0\), so \(S'=0\); the \(S\)-pure case is symmetric. If \(x\) is
mixed, then

\[
                         P(S')^t=-P'S^t.                \tag{8}
\]

Neither side can vanish, since that would make \(y=0\). Equality of the two
nonzero rank-one matrices makes \(P'\) proportional to \(P\) and \(S'\)
proportional to \(S\), with opposite proportionality constants. This is
(7). \(\square\)

**Lemma 3.2 (crossed-target purity).** Let \(i\ne j\), and suppose

\[
\begin{aligned}
 \Phi(x,y)&=\alpha E_{ii},&\Phi(z,w)&=\beta E_{jj},\\
 \Phi(x,z)&=0,&\Phi(y,w)&=0,
                                                        \tag{9}
\end{aligned}
\]

where \(\alpha,\beta\ne0\). Then all four points are pure. Moreover, \(x,z\)
have the same pure type, \(y,w\) have the same pure type, and those two types
are opposite.

**Proof.** Apply Lemma 3.1 to the two zero pairs. Suppose first that \(x,z\)
are mixed antipodes. If \(y,w\) are mixed antipodes too, the two nonzero
matrices in the first line of (9) are proportional. This is impossible for
\(E_{ii}\) and \(E_{jj}\).

If \(y,w\) are \(P\)-pure, the two target matrices have a common right
factor: they are \(R S^t\) and \(R'S^t\), up to nonzero scalars. If they are
\(S\)-pure, the two targets have a common left factor instead. Distinct
diagonal matrix units have distinct one-dimensional row and column spaces,
so both alternatives are impossible. Hence \(x,z\) are pure of the same
type. The symmetric argument makes \(y,w\) pure of the same type. A nonzero
value of \(\Phi\) between pure points is possible only for opposite types.
\(\square\)

Thus two target corners of different colours, together with the two crossed
zero corners, turn four a priori arbitrary points of
\(\mathbb C^3\oplus\mathbb C^3\) into typed pure points.

## 4. The three-edge path is impossible

For (1a), the missing-colour sets are

\[
 {\cal M}_A=\{0\},\quad
 {\cal M}_B=\{0,1\},\quad
 {\cal M}_C=\{1,2\},\quad
 {\cal M}_D=\{2\}.                                    \tag{10}
\]

Rule (6) gives the following complete exposed grids. A displayed target has
an arbitrary nonzero scalar coefficient.

| pair | target corner | zero corners |
|---|---|---|
| \(AB\) | \(\Phi(A_0,B_0)=E_{00}\) | \(\Phi(A_0,B_1)=0\) |
| \(BC\) | \(\Phi(B_1,C_1)=E_{11}\) | \(\Phi(B_0,C_1)=\Phi(B_0,C_2)=\Phi(B_1,C_2)=0\) |
| \(CD\) | \(\Phi(C_2,D_2)=E_{22}\) | \(\Phi(C_1,D_2)=0\) |

Apply Lemma 3.2 first to the \(AB\) and \(BC\) targets, using the crossed
zeros \(A_0B_1\) and \(B_0C_1\). Apply it again to the \(BC\) and \(CD\)
targets, using \(B_1C_2\) and \(C_1D_2\). All six target points are now pure,
and their types obey

\[
 A_0\sim B_1\sim C_2,\qquad
 B_0\sim C_1\sim D_2,                                  \tag{11}
\]

with the two chains having opposite types. But the middle grid also gives

\[
                              \Phi(B_0,C_2)=0.           \tag{12}
\]

The two nonzero pure points in (12) have opposite types, so their outer
product cannot vanish. This contradicts (12).

## 5. The triangle is impossible

For (1b),

\[
 {\cal M}_A=\{0,2\},\qquad
 {\cal M}_B=\{0,1\},\qquad
 {\cal M}_C=\{1,2\}.                                   \tag{13}
\]

Every omission pair now exposes a \(2\times2\) grid:

| pair | target corner | zero corners |
|---|---|---|
| \(AB\) | \(\Phi(A_0,B_0)=E_{00}\) | \(A_0B_1,A_2B_0,A_2B_1\) |
| \(BC\) | \(\Phi(B_1,C_1)=E_{11}\) | \(B_0C_1,B_0C_2,B_1C_2\) |
| \(CA\) | \(\Phi(C_2,A_2)=E_{22}\) | \(C_1A_0,C_1A_2,C_2A_0\) |

Here a bare corner label means that its \(\Phi\)-value is zero. The crossed
zeros \(A_0B_1,B_0C_1\) purify the \(AB/BC\) targets. The crossed zeros
\(B_1C_2,C_1A_2\) then purify the \(BC/CA\) targets. Consequently

\[
 A_0\sim B_1\sim C_2,\qquad
 B_0\sim C_1\sim A_2,                                  \tag{14}
\]

again with opposite types. The zero middle corner
\(\Phi(B_0,C_2)=0\) gives the same contradiction as in (12). Cyclically,
the \(CA/AB\) crossed pair supplies a third redundant purity check.

This proves that no exact rational, complex, or symbolic common-power
response model with local ranks \((1,1,1,3,3,3)\) can realize the triangle
geometry.

## 6. Exact checker and remaining scope

The standalone checker
[verify_rank_budget_path_triangle_exposed_grid_obstruction.py](../computations/verify_rank_budget_path_triangle_exposed_grid_obstruction.py)

* verifies symbolically the proportional-target branch of Lemma 3.2 and the
  row-space/column-space obstruction in both pure branches;
* constructs every target and zero corner directly from (6);
* checks the path census \(3\) targets plus \(5\) zeros and the triangle
  census \(3\) targets plus \(9\) zeros; and
* exhausts all \(2^6\) pure endpoint-type assignments in each case, finding
  none.

For comparison, the wedge-plus-disjoint geometry has only two exposed zero
corners. Even after declaring all six target points pure, its type clauses
have four solutions. Its disconnected third omission pair cannot supply the
second crossed-target propagation used above. Therefore this argument does
not close that geometry. It also says nothing about rank budget above
twelve.
