# The common power excludes the minimal cyclic three-zero boundary

## 1. Outcome

Continue from the cyclic port orbit in
[live-three-zero-uncontracted-port-normal-form.md](live-three-zero-uncontracted-port-normal-form.md).
Let \(a,b\) be the two type-\(22\) rank-one centres, let
\(z_0,z_1,z_2\) be the three literal zero sites, and suppose the residual
nonzero shore is minimal: it consists of three live sites and the two
type-\(10\) rank-two centres. Thus, after the ports at \(a,b\) use
\(z_1,z_2\), the residual cap is on

\[
 R=\{0,1,2,3,4,z_0\},
 \qquad P_0,P_1,P_2\text{ invertible},
 \qquad \operatorname {rank}P_3=\operatorname {rank}P_4=2.       \tag{1}
\]

The preceding note proves that the complete residual response at \(z_0\)
vanishes:

\[
                            {\cal D}_0(x,z)=0.                     \tag{2}
\]

The actual common-power origin of this response now gives the missing
contradiction.

**Theorem 1.1 (minimal residual star injectivity).** Under (1)--(2),

\[
                         q_{i z_0}=0\qquad(0\le i\le4).            \tag{3}
\]

The two blocks from \(z_0\) to \(a,b\) are singular coordinate-port
blocks, while the two zero--zero blocks from \(z_0\) vanish. Hence (3)
makes \(z_0\) an isolated vertex of the spanning rank-three graph
\(G_3(q)\), a contradiction.

Consequently the **two-coordinate-factor rank-two direct-quadratic
pattern** has no cyclic three-zero lift when the live shore has three
sites and there are no additional nonzero singular sites. This statement
does not concern the coordinate-rank-one direct-quadratic pattern, whose
four centres have different types. The proof here is uniform over
arbitrary complex blocks incident with the zero sites, arbitrary gauges of
the two residual type-\(10\) centres, and every admissible invertible
zero-diagonal \(H\); it is not only a calculation at the normalized
rational example. Larger live shores, additional singular sites, and
\(s>3\) still require a descent to this minimal residual. The restriction
on the live-shore size is removed when all live beta values equal \(\mu\)
in
[live-three-zero-common-beta-all-orders.md](live-three-zero-common-beta-all-orders.md).

## 2. The cyclic ports synchronize the beta values

In the cyclic orbit the two rank-one centre stars have the form

\[
\begin{array}{c|ccc}
 &z_0&z_1&z_2\\ \hline
a&e_0\alpha&e_1\gamma&F\\
b&e_1\delta&G&e_0\beta,
\end{array}                                                     \tag{4}
\]

where every displayed map is nonzero and \(F,G\) are injective. Since
\(P_{z_j}=0\), the structural relation

\[
 P_iHP_j^{\mathsf T}=(\beta_i+\beta_j)q_{ij}                     \tag{5}
\]

says that the beta values at the ends of every nonzero centre--zero block
are opposite. Each row of (4) meets all three zero sites. It follows that

\[
 \beta_a=\beta_b=\mu\ne0,
 \qquad \beta_{z_0}=\beta_{z_1}=\beta_{z_2}=-\mu.                 \tag{6}
\]

The two type-\(10\) centres jointly miss colour \(2\). The coordinate-port
theorem supplies a nonzero colour-\(2\) port from each of them to a zero
site, so (5)--(6) give

\[
                         \beta_3=\beta_4=\mu.                     \tag{7}
\]

For a live site \(i\), equation (5) at \(i z_0\) reduces to

\[
                         (\beta_i-\mu)q_{i z_0}=0.                 \tag{8}
\]

Thus only a live site with \(\beta_i=\mu\) can have a nonzero block to
\(z_0\). Let \(k\in\{0,1,2,3\}\) be the number of such live sites and
relabel them \(0,\ldots,k-1\). The only initially unknown star blocks in
(3) are then those at

\[
                              J_k=\{0,\ldots,k-1,3,4\}.             \tag{9}
\]

All internal denominators used below are nonzero. Indeed, between two
live sites the left side of (5) is invertible; between a live site and a
type-\(10\) centre it has rank two; and between the two type-\(10\) centres
it is the nonzero rank-two matrix obtained by restricting \(H\) to the
\(01\)-plane.

## 3. Arbitrary centre gauges reduce to one normal form

Apply independent invertible changes of basis at the five nonzero local
factors. At a live site use \(P_i^{-1}\). At a type-\(10\) centre, the
component incidence says that its kernel is \(\mathbb C e_2\), while its
restrictions to \(\mathbb C e_0\) and \(\mathbb C e_1\) have independent
images. An invertible left factor therefore takes that map to
\(D=\operatorname {diag}(1,1,0)\). These independent local changes put

\[
 P_0=P_1=P_2=I,
 \qquad P_3=P_4=D.                                             \tag{10}
\]

They transform every incident \(q\)-block by the same invertible local
factor. Thus they preserve the vanishing of the cap, every block rank,
whether a zero-star block vanishes, and the fact that the zero-star blocks
are otherwise arbitrary. No simultaneous gauge or equality of the two
original type-\(10\) matrices is assumed.

The common source matrix remains

\[
 H=\begin{pmatrix}
 0&h_{01}&h_{02}\\
 h_{01}&0&h_{12}\\
 h_{02}&h_{12}&0
 \end{pmatrix},
 \qquad h_{01}h_{02}h_{12}\ne0.                                \tag{11}
\]

On the five nonzero sites,

\[
 q_{ij}=s_{ij}P_iHP_j^{\mathsf T},
 \qquad s_{ij}={1\over\beta_i+\beta_j}\ne0.                     \tag{12}
\]

Fix a coordinate \(b\) at \(z_0\), and write
\(Z_{i,r}=q_{i z_0}[r,b]\). The three choices of \(b\) do not mix. For a
word \(w=(w_0,\ldots,w_4)\) and a diagonal source colour \(c\), the
coefficient of \(w\otimes e_b\) in the residual cap is

\[
 E_{w,c}^{(b)}=
 \sum_{\{u,v\}\subseteq\{0,\ldots,4\}}
  2(P_u)_{w_u c}(P_v)_{w_v c}
  \sum_{\substack{i\notin\{u,v\}\\
                  \{i,j,l\}=\{0,\ldots,4\}\setminus\{u,v\}}}
       Z_{i,w_i}\,(q_{jl})_{w_jw_l}.                              \tag{13}
\]

There is no direct contribution in (13), because the rank-two coordinate
factor has \(B_{cc}=0\). Formula (13) is simply the exact matching
expansion of
\(p(e_c)^2q_R^2/2!\): the marked factors occupy \(u,v\), \(i\) is paired
to \(z_0\), and the last two sites use their internal \(q\)-edge.
Equation (2) says that every expression (13) is zero.

## 4. The four beta strata are injective

First suppose \(k\le2\). Restrict to words for which exactly two sites
can carry the marked colour \(c\). The marked pair in (13) is then unique,
so every nonzero matrix entry is one monomial

\[
                   2s_{jl}h_{w_jw_l},                              \tag{14}
\]

possibly with one harmless diagonal entry of \(D\). In particular it is
nonzero. Successive use of the following coefficient rows is triangular;
an entry named earlier in a row has already been proved zero. Here
\(Z_{ir}\) denotes the variable at site \(i\), local colour \(r\), for the
fixed zero colour \(b\).

\[
\begin{array}{c|l}
k&\text{successive pivots }Z_{ir}:\ (w;c)\\ \hline
0&
 Z_{42}:(00212;0),\ Z_{32}:(00221;0),\
 Z_{41}:(01201;0),\ Z_{31}:(00211;0),\
 Z_{30}:(01201;1),\ Z_{40}:(01210;1)\\[1mm]
1&
 Z_{00}:(00211;1),\ Z_{42}:(00212;0),\ Z_{32}:(00221;0),\
 Z_{41}:(01201;0),\ Z_{31}:(00211;0),\
 Z_{30}:(01201;1),\ Z_{40}:(01210;1),\
 Z_{01}:(10201;0),\ Z_{02}:(20201;0)\\[1mm]
2&
 Z_{42}:(00212;0),\ Z_{32}:(00221;0),\
 Z_{00}:(02011;1),\ Z_{10}:(00211;1),\
 Z_{30}:(01201;1),\ Z_{40}:(01210;1),\
 Z_{41}:(02101;0),\ Z_{31}:(00211;0),\
 Z_{11}:(01201;0),\ Z_{12}:(02201;0),\
 Z_{01}:(10201;0),\ Z_{02}:(20201;0).
\end{array}                                                     \tag{15}
\]

Substitution in (13) verifies that each displayed pivot has coefficient
of the form (14). Thus all \(3(k+2)\) variables vanish when \(k\le2\).

It remains to take \(k=3\). Now all five nonzero sites have beta value
\(\mu\), so \(s_{ij}=1/(2\mu)\) for every internal pair. Order the fifteen
variables by

\[
 (Z_{00},Z_{01},Z_{02},Z_{10},\ldots,Z_{42}),                      \tag{16}
\]

and select the following fifteen rows of (13):

\[
\begin{gathered}
 (00211;0),(00211;1),(00212;0),(00221;0),(01201;0),\\
 (01201;1),(01210;0),(01210;1),(02011;1),(02101;0),\\
 (02201;0),(10201;0),(10201;1),(20201;0),(22001;0).
                                                                    \tag{17}
\end{gathered}
\]

Direct fraction-free elimination, using (11)--(13), gives the determinant

\[
                   \det M={8h_{02}^{\,5}h_{12}^{\,10}\over\mu^{15}}
                         \ne0.                                    \tag{18}
\]

Hence the \(k=3\) star map is injective as well. Repeating the argument
for \(b=0,1,2\) proves (3).

## 5. Why zeroing the residual star violates the global graph hypothesis

Equation (6) gives

\[
 (\beta_{z_0}+\beta_{z_j})q_{z_0z_j}
       =-2\mu q_{z_0z_j}=0\qquad(j=1,2),                         \tag{19}
\]

so both zero--zero blocks at \(z_0\) vanish. The only remaining incident
blocks are \(q_{a z_0},q_{b z_0}\). They are coordinate ports of rank-one
centres. Their annihilator spaces have dimension two, while the port
restriction has nonzero one-dimensional image; an invertible block would
restrict injectively and have two-dimensional image. Thus both port
blocks are singular.

There are no other sites in the minimal chart. Together, (3) and (19)
show that no rank-three edge is incident with \(z_0\). This does not claim
that \(z_0\) is isolated in the full support graph: its two port blocks are
nonzero. It is isolated specifically in \(G_3(q)\), contradicting the
global hypothesis that this rank-three graph is connected and spanning.
This proves Theorem 1.1.

## 6. Exact audit

[verify_live_three_zero_common_power_star_injectivity.py](../computations/verify_live_three_zero_common_power_star_injectivity.py)
constructs the normalized rational cap with

\[
 H=\begin{pmatrix}0&1&2\\1&0&3\\2&3&0\end{pmatrix},
 \qquad B={1\over2}(E_{01}+E_{10}),                              \tag{20}
\]

and arbitrary \(3\times3\) blocks on the five edges to \(z_0\). After
zero rows are deleted, the exact coefficient matrix has size
\(2718\times45\). The rows (17), repeated for the three zero-site
coordinates, form a \(45\times45\) minor of determinant

\[
                              2^{24}3^{30}.                         \tag{21}
\]

The same checker treats the four beta strata symbolically. For
\(k=0,1,2\) it verifies every triangular pivot in (15) as a single nonzero
monomial in the internal edge scalars and the entries of \(H\). For
\(k=3\) it reconstructs (18) over
\(\mathbb Q(h_{01},h_{02},h_{12},\mu)\).
