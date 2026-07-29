# Synchronized E2 responses factor on dense overlaps, but inactive edges retain the diagonal targets

## 1. Outcome

The factorization half of the proposed synchronization-or-cap theorem has
an exact positive answer on the dense fixed-row branch.

Fix a good fan centre `r`.  Suppose one selected family of physical E2
responses uses the same centre colour row `P`, its defect primitives
synchronize, and hence the response-fork descent gives one global
quadratic `Z`.  If, after deleting any two fan neighbours, `P` is still
supported at three physical sites, then the chartwise physical
factorizations glue literally:

\[
                    \boxed{Z=PS}                                      \tag{1}
\]

for one global linear form `S`.  Consequently

\[
                  L_i=\operatorname {span}\{P_i,S_i\}\subseteq V_i  \tag{2}
\]

is a common sitewise colour subbundle of rank at most two through which
every block of `Z` factors.  In particular, global site support at least
five is sufficient for (1).  The proof is coordinate-free and uses only
injectivity of multiplication by a linear form supported at three sites.

This is a real factorization theorem, but it does **not** close the full
synchronized E2 branch.  Two minimal exact guards locate both remaining
issues.

1. With only three fan charts and a two-site centre row, synchronized
   primitives and literal endpoint-ordered physical star products need not
   have a global physical factor.  Section 5 gives a five-site rational
   model.
2. Even when `Z=PS` is nonzero, all three normalized diagonal pair rows
   can hold.  Section 6 gives a four-site integral model.  Its diagonal
   targets are carried by edges on which
   `alpha_i+alpha_j=0`, so those source blocks are invisible in
   `Z=Gamma_q(alpha)`.

Thus the exact missing hypotheses are no longer “some rank-two argument.”
One must derive overlap density (or kill the sparse holonomy directly) and
control the **inactive graph**

\[
             G_0(\alpha)=\{ij:q_{ij}\ne0,
                                  \ \alpha_i+\alpha_j=0\}.           \tag{3}
\]

Every rank-three edge lies in this graph.  Factorization of the response
section says nothing about the source blocks on (3), and the three diagonal
targets can live there.  The synchronized branch therefore remains open
exactly on the sparse/inactive-edge boundary.

## 2. Synchronized physical response data

Put `U=B\setminus{r}` and let `F subset U` be a set of fan neighbours.
For `u in F`, write

\[
                         W_u=U\setminus\{u\}.                       \tag{4}
\]

Fix a centre colour `c`.  The row of the global `r`-star is a linear form

\[
                         P=\sum_{i\in U}P_i,
 \qquad                  P^{(u)}=P|_{W_u}.                         \tag{5}
\]

For each `u`, fix an endpoint colour `d_u` and let
`S^(u)` be that endpoint-oriented row of the `u`-star into `W_u`.
Suppose the chosen E2 primitives synchronize to
`alpha in mathfrak t_U`.  The positive descent in
[`good-pair-response-fork-and-exact-overlap-flatness.md`](good-pair-response-fork-and-exact-overlap-flatness.md)
gives

\[
 Z=\Gamma_{q_U}(\alpha),
 \qquad
 Z|_{W_u}=P^{(u)}S^{(u)}.                              \tag{6}
\]

The second equality is not an abstract rank bound.  It is the literal
physical block identity from the selected off-diagonal response, with
endpoint order retained.  The accompanying direct entry is

\[
 A_{r\mid u}(c,d_u)=-\sum_{i\in W_u}\alpha_i.                       \tag{7}
\]

Nothing below divides by this scalar or by a component of a star.

## 3. Dense-overlap factorization theorem

We use the elementary site-square-zero annihilator fact:

**Lemma 3.1 (linear multiplication).**  If a linear form `P_T` is nonzero
at at least three sites of `T`, then

\[
 \mathcal R_1(T)\longrightarrow\mathcal R_2(T),
 \qquad R\longmapsto P_TR                                      \tag{8}
\]

is injective over characteristic different from two.

For completeness, if `P_TR=0`, then on three nonzero sites the simple
tensor equations make `R_i=lambda_i P_i` and
`lambda_i+lambda_j=0` for every pair.  The three equations give every
`lambda_i=0`; pairing any remaining site with an anchor then gives its
component of `R` equal to zero.

**Theorem 3.2 (synchronized factorization).**  Assume `|F|>=3` and

\[
 |\operatorname {supp}_s(P)\setminus\{u,v\}|\ge3
                    \qquad(u\ne v\text{ in }F).                     \tag{9}
\]

Then there is a unique `S in mathcal R_1(U)` such that

\[
                         S|_{W_u}=S^{(u)}\quad(u\in F),
 \qquad                  Z=PS.                                    \tag{10}
\]

In particular, (9) holds whenever
`|supp_s(P)|>=5`.

**Proof.**  On the common complement
`K_uv=U\setminus\{u,v}`, equations (6) give

\[
 P|_{K_{uv}}\bigl(S^{(u)}|_{K_{uv}}-S^{(v)}|_{K_{uv}}\bigr)=0.      \tag{11}
\]

Condition (9) and Lemma 3.1 make the parenthesized difference zero.
Therefore the `S^(u)` glue coordinate by coordinate to one `S` on `U`.
Every pair of sites `i,j` is contained in some `W_u`, because at least
three fan neighbours are available.  Restricting (6) to that block gives
`Z_ij=(PS)_ij`.  This proves existence.  If `PS=PS'`, Lemma 3.1 on any
chart and overlap gives `S=S'`.  \(\square\)

The theorem produces the promised exterior-power structure without a
choice of bases.  With `L_i` as in (2),

\[
 Z_{ij}\in L_i\otimes L_j,
 \qquad \dim L_i\le2,
 \qquad \bigwedge^3L_i=0.                              \tag{12}
\]

Moreover, if `alpha_i+alpha_j != 0`, then (6) gives

\[
                         q_{ij}={Z_{ij}\over\alpha_i+\alpha_j}
                                  \in L_i\otimes L_j.               \tag{13}
\]

Thus every **active** source block factors through the same planes.  The
only uncontrolled blocks are precisely those in `G_0(alpha)`.

## 4. What the rank-three components add

Every rank-three edge belongs to `G_0(alpha)`, since
`alpha in ker B_3(q_U)`.  Nevertheless the zero response on such an edge
does constrain the physical factors.

**Lemma 4.1 (line field on a nonvanishing component).**  Let `C` be a
connected component of `G_3(q_U)`.  Suppose `P_i` and `S_i` are nonzero
at every vertex of `C`.  Then there are nonzero scalars `lambda_i` with

\[
                         S_i=\lambda_iP_i,
 \qquad                  \lambda_i=-\lambda_j\quad(ij\in E(C)).    \tag{14}
\]

In particular `C` must be bipartite.  On a nonbipartite component some
`P_i` or `S_i` is zero.

**Proof.**  Equations (1) and `Z_ij=0` give

\[
                 P_i\otimes S_j=-S_i\otimes P_j.                    \tag{15}
\]

Equality of two nonzero simple tensors makes the two factors at each
endpoint proportional, and substitution gives the sign change in (14).
Propagation around an odd cycle returns `lambda_i=-lambda_i`, impossible
in characteristic zero.  \(\square\)

This recovers the familiar antipodal line on a dense bipartite component,
now inside the globally glued planes (2).  It does not control a component
at a zero of `P` or `S`, nor any rank-one/rank-two edge joining different
components.  Those are exactly the sparse and cross-component terms left
by Theorem 3.2.

## 5. Minimal three-chart physical holonomy

The overlap hypothesis (9) cannot simply be omitted.  This example is a
response model, not a complete pair chart or a Krenn source.

Let

\[
 U=\{0,1,2,3,4\},\qquad F=\{0,1,2\},
\]

and use ternary local spaces with displayed vectors in their standard
bases.  Put

\[
 P_0=e_1^{(0)},\qquad P_1=e_0^{(1)},\qquad P_2=P_3=P_4=0,            \tag{16}
\]

\[
 q_{02}=e_1^{(0)}\otimes e_0^{(2)},\qquad
 q_{12}=-e_0^{(1)}\otimes e_0^{(2)},
 \qquad
 \alpha=(1/2,-1/2,-1/2,0,0).                             \tag{17}
\]

Then `sum alpha=-1/2`; the `02` block is inactive while the coefficient
on the `12` block is `-1`, so

\[
 Z=\Gamma_q(\alpha)=e_0^{(1)}\otimes e_0^{(2)}.           \tag{18}
\]

Choose the endpoint colour `d=1` in all three charts.  The physical block
`A_(0|2)=q_02` has row `d` equal to `e_0^(2)` at endpoint `0`, while its
transpose has row `d` zero at endpoint `2`.  The block `A_(1|2)=q_12` has
row `d` zero at both endpoints.  Consequently the three endpoint rows are

\[
 S^{(0)}=e_0^{(2)},\qquad S^{(1)}=S^{(2)}=0.                        \tag{20}
\]

The centre direct entries in endpoint order are

\[
 A_{r\mid0}(c,1)=1,qquad A_{r\mid1}(c,1)=A_{r\mid2}(c,1)=0.        \tag{21}
\]

They agree with the actual components (16), and

\[
 \sum_{W_0}\alpha=-1,qquad
 \sum_{W_1}\alpha=\sum_{W_2}\alpha=0.                           \tag{22}
\]

Thus (6)--(7) hold literally in all three charts.  In chart `0` the
restricted source is `-e_0^(1)e_0^(2)`, and its response is
`(e_0^(1)e_0^(2),-1)=delta_(q|W_0)(alpha|W_0)`.  In chart `1` the
remaining `02` source block is inactive, and in chart `2` the source is
zero; both responses and scalar components vanish.  The primitive is one
synchronized global vector, not three independently selected coordinates.

There is no global `S` with `Z=PS`.  The `02` block would read

\[
                0=Z_{02}=P_0\otimes S_2
\]

and hence force `S_2=0`, while the `12` block would read

\[
       e_0^{(1)}\otimes e_0^{(2)}=Z_{12}=P_1\otimes S_2,            \tag{23}
\]

a contradiction.  The obstruction is exactly that the overlap of charts
`0` and `1` sees only one site of `supp(P)`, so multiplication by `P` is
not injective there.

This model retains endpoint order and the scalar component of the response.
Its internal Hessians are not gauge-rigid and it supplies no diagonal
targets.  It therefore does not refute the desired theorem on exact E2
charts; it proves that synchronization and physical off-diagonal products
alone are insufficient.

## 6. Three normalized diagonals can live on the inactive graph

The normalized diagonal rows do not, by themselves, force (9) or make a
factorized response contradict the target.  Here is a smallest exact
pair-chart guard.

On `W={0,1,2,3}`, write `[ij]_(ab)` for
`e_a^(i)e_b^(j)` in the displayed endpoint order and put

\[
 q=[23]_{00}+[13]_{11}+[12]_{22}+[03]_{01}.                       \tag{24}
\]

Take

\[
 \begin{array}{lll}
 p_0=e_0^{(0)},&p_1=e_1^{(2)},&p_2=e_2^{(0)},\\
 s_0=e_0^{(1)},&s_1=e_1^{(0)}+e_1^{(3)},&s_2=e_2^{(3)}.
 \end{array}                                                       \tag{25}
\]

Both triples are linearly independent.  The three triangle edges in
(24) intersect pairwise, and the last edge is disjoint only from `12`.
Therefore

\[
 q^{[2]}=[03]_{01}[12]_{22},                                      \tag{26}
\]

and direct multiplication gives all three normalized diagonal rows

\[
                         p_cs_cq=X_c^W\qquad(c=0,1,2).              \tag{27}
\]

Set

\[
                         \alpha=(1,0,0,0).                          \tag{28}
\]

Then

\[
 p_0s_1=[03]_{01}=\Gamma_q(\alpha),
 \qquad \sum_i\alpha_i=1,                                       \tag{29}
\]

and the selected off-diagonal equation is exact with direct entry `-1`:

\[
                   -q^{[2]}+p_0s_1q=0.                             \tag{30}
\]

Thus the E2 response section is nonzero and already factors through the
planes `span(P_i,S_i)`, while every diagonal target in (27) is normalized.
There is no contradiction because the triangle `12,13,23` lies in
`G_0(alpha)` and carries the three pure complementary cells.  The active
edge `03` carries the response but not the missing third-colour geometry.

Again, this is a pair-chart response guard, not a hypothetical exact source:
its rank-three graph is empty and its Hessian is not gauge-rigid.  Its
logical force is precise.  Even after factorization, the three diagonal
rows cannot exclude the synchronized branch without a theorem controlling
the inactive blocks.

## 7. Exact remaining gate

The dense fixed-row synchronized subbranch is closed at the factorization
level by Theorem 3.2.  It is not yet a contradiction to the three target
colours, because (12)--(13) constrain `Gamma_q(alpha)`, not all of `q` or
all six physical star rows.

A complete synchronized-branch theorem now needs one of the following
genuinely additional inputs.

1. Prove from gauge rigidity, goodness, and the complete diagonal rows
   that a selected centre row satisfies (9), then control the source blocks
   on `G_0(alpha)` inside the same planes `L_i`; or
2. show that failure of (9), or a diagonal matching carried by
   `G_0(alpha)`, exports an active clean cap.

The first requirement is sharp against Section 5; the second is sharp
against Section 6.  Merely knowing blockwise rank at most two, merely
having a global defect vector, or merely imposing the three normalized
diagonal products does not bridge either gap.

The dependency-free checker
[`verify_synchronized_e2_factorization_and_inactive_edge_boundary.py`](../computations/verify_synchronized_e2_factorization_and_inactive_edge_boundary.py)
audits both exact guards, including endpoint reversal, primitive sums,
all three diagonal tensors, the nonzero off-diagonal response, and the
failure of the global factor equation in (23).  It also checks the overlap
support threshold behind Theorem 3.2.  The uniform theorem is the proof in
Section 3, not a finite computation.
