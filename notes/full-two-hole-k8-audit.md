# Full two-hole audit of the K8 witness-incidence model

## 1. Outcome

The compressed K8 model from
[`witness-incidence-k8-countermodel.md`](witness-incidence-k8-countermodel.md)
passes much more of the uncompressed annihilation system than its
construction requires:

* all `168` one-hole vector systems, equivalently all `504` scalar
  equations, hold identically;
* `407` of the `420` full two-hole matrix identities hold identically;
* every two-hole identity for each of the four rank-three paired edges
  `01,23,45,67` holds; and
* the remaining `13` failures split into eight target-term failures, four
  hole-correction failures, and one genuinely cofactor-coupled failure.

The model has trivial automorphism group even if one permits one global
permutation of the three colors.  Thus its thirteen failures are literally
thirteen singleton symmetry orbits.  The useful compression is instead the
algebraic `8+4+1` classification above.

The unique cofactor-type failure gives a particularly small obstruction.
One scalar coefficient of one two-hole identity is already nonzero.  On the
same weighted support chart that coefficient factors as a product of eleven
supported entries.  Hence the condition forces an explicit eleven-way
coordinate-boundary alternative.  Exact deletion tests show that every one
of those eleven branches still has active forced anchors and linearly
independent same-star contribution atoms.  The coefficient kills the open
K8 support chart, but forced anchors plus the entry-minimality shadow do not
close its boundary branches.

## 2. The matrix identity being audited

Fix deleted vertices `p,q`, put

\[
 R=B\setminus\{p,q\},\qquad
 \gamma_u=(A_{pu}^Tx)\mathbin{\times}(A_{qu}^Ty),\qquad
 g=x^TA_{pq}y.
\]

For holes `w,z in R`, put `S=R\setminus\{w,z\}` and let `Q_{wz}` be the
two-site partial contraction of the complementary matching tensor on `R`
against the four covectors `gamma_u`, `u in S`.  Also set

\[
 h_S=\left\langle H_S,\bigotimes_{u\in S}\gamma_u\right\rangle,
 \qquad
 x_t=A_{pt}^Tx,\quad y_t=A_{qt}^Ty,
\]

and

\[
 B_{wz}=x_wy_z^T+y_wx_z^T.
\]

The exact target identity is

\[
 D_{pq}^{wz}:=
 \operatorname{diag}\!\left(
 x_ry_r\prod_{u\in S}\gamma_{u,r}
 \right)_{r=0}^2
 -gQ_{wz}-h_SB_{wz}=0.                         \tag{1}
\]

All calculations below are exact polynomial calculations over the integers.

## 3. Complete failure classification

At a nonzero residual cell, record which of the three summands in (1)
survives.  The thirteen failing hole configurations are as follows.

| class | deleted pair and holes `(p,q;w,z)` | nonzero residual cells |
|---|---|---:|
| target | `(0,3;5,7)`, `(0,5;2,3)`, `(1,3;5,7)`, `(1,4;6,7)`, `(2,4;1,6)`, `(2,5;1,6)`, `(3,4;1,6)`, `(3,5;1,6)` | one each |
| correction | `(0,4;1,5)`, `(0,5;1,4)`, `(1,4;0,5)`, `(1,5;0,4)` | nine each |
| cofactor | `(1,5;2,3)` | two |

In the target class every nonzero residual cell has nonzero diagonal target
term and zero `gQ` and `hB` terms.  In the correction class the target term
is zero and the nonzero residual cells all contain `hB`; some also contain
`gQ`.  In the cofactor class both the target and correction terms vanish,
while `gQ` is nonzero.  Thus the eight one-cell target failures are the
smallest failures by residual support, while `(1,5;2,3)` is the smallest
failure that actually sees the complementary cofactor.

Representative factorizations of `D` are

\[
\begin{array}{c|c|c}
\text{class}&(p,q;w,z;i,j)&D_{ij}\\ \hline
\text{target}&(0,3;5,7;1,1)&
 -x_1^3x_2^2y_0y_1^2y_2^2\\
\text{correction}&(0,4;1,5;0,0)&
 -x_0x_1^2x_2^2y_0^3y_2^2\\
\text{cofactor}&(1,5;2,3;1,1)&x_0^5y_1^5.
\end{array}                                             \tag{2}
\]

There is no hidden symmetry identification in this table.  Any
automorphism must permute the four rank-three edges, so it lies in
`(S_2)^4 semidirect S_4` on vertices.  Testing those `384` vertex
permutations together with all six global color permutations leaves only
the identity.  Consequently the literal automorphism-orbit decomposition
has thirteen singleton orbits; the three rows above are polynomial types,
not symmetry orbits.

## 4. The weakest genuinely cofactor-coupled condition

Take

\[
                  (p,q;w,z)=(1,5;2,3),\qquad S=\{0,4,6,7\}.
\]

Here `A_15=E_01`, so `g=x_0y_1`.  The four contracted cross covectors are

\[
\begin{aligned}
 \gamma_0&=(-x_2y_1,0,x_0y_1),&
 \gamma_4&=(0,-x_0y_2,x_0y_1),\\
 \gamma_6&=(0,x_0y_1,0),&
 \gamma_7&=(0,-x_0y_1,0).
\end{aligned}                                             \tag{3}
\]

Direct contraction gives

\[
 \operatorname{diag}(t_0,t_1,t_2)=0,
 \qquad h_S=0,
 \qquad B_{23}=x_0y_1\operatorname{diag}(0,1,1),           \tag{4}
\]

but

\[
 Q_{23}=-x_0^4y_1^4\operatorname{diag}(0,1,1).             \tag{5}
\]

Thus (1) forces `Q_23=0` because `g` is a nonzero polynomial.  The single
scalar coefficient condition

\[
                  [x_0^4y_1^4](Q_{23})_{11}=0             \tag{6}
\]

already kills the model: its actual value is `-1`.  This is weaker than
requiring the full `3 by 3` two-hole identity, or even the full polynomial
entry `(Q_23)_11=0`.  The coefficient has exactly one perfect-matching
source,

\[
                        (03)(24)(67),                      \tag{7}
\]

so (6) is not hiding a cancellation among matching terms.  The analogous
`(2,2)` coefficient comes uniquely from `(02)(34)(67)`.

## 5. Weighted support factorization and the local boundary alternative

Replace every `1` in the support array by its own weight
`a_{uv}^{ij}`.  The zero pattern, singleton anchors, and paired diagonal
blocks are unchanged.  Equations (4) remain structural identities on this
whole weighted chart.  Exact coefficient extraction gives

\[
\begin{aligned}
 [x_0^4y_1^4](Q_{23})_{11}
 ={}-&a_{01}^{00}a_{03}^{21}a_{05}^{11}a_{14}^{00}
      a_{16}^{02}a_{17}^{00}a_{24}^{12}\\
    &\mathrel{}\cdot a_{45}^{11}a_{56}^{10}a_{57}^{12}a_{67}^{11}.
                                                               \tag{8}
\end{aligned}
\]

The full residual coefficient also has the nonzero deleted-edge factor
`a_15^{01}`.  Dividing by it gives (8), which is the sharper statement on
the chart where `A_15` remains present.

Consequently (6) gives an exact finite local alternative: at least one of
the eleven factors in (8) must vanish.  Three branches delete one diagonal
cell from one of the paired edges `01,45,67`; the other eight branches
delete the sole cell of a singleton edge.  This is the strongest support
conclusion available from this coefficient alone.

To test whether forced anchors or entry-minimality close those branches,
set one factor at a time to zero and keep every other supported weight equal
to one.  In all eleven resulting arrays the checker verifies:

1. every complementary six-site matching tensor remains nonzero;
2. every one of the `24` ordered vertex/color ports still has an active
   forced-anchor-form edge;
3. at each vertex the contribution atoms of all remaining nonzero incident
   cells have rank equal to their number.

For a singleton-cell deletion the two affected stars have eight atoms and
the other six have nine; the minimum anchor multiplicity is one.  For a
paired diagonal-cell deletion the two affected stars again have eight
atoms, all other stars have nine, and the minimum anchor multiplicity is
two.  Thus all eleven branches retain precisely the active-anchor and
same-star irredundancy properties forced by entry-minimality.

These deletion arrays are not asserted to satisfy the other target
identities.  Their role is diagnostic: the cofactor coefficient supplies a
finite eleven-way boundary split on this support chart, but neither forced
anchors nor the local entry-minimality lemma eliminates any branch.  A
continuation must combine several cofactor-coupled equations across
different deleted pairs, or control how the boundary branches intersect.

## 6. Exact checker

Run

```text
python computations/verify_witness_incidence_k8_full_two_hole.py
```

The script expands all one-hole and full two-hole systems, verifies the
`407/13` split and the `8+4+1` classification, enumerates the exact
automorphism group, proves the unique-source factorization (8), and checks
active cofactors, forced anchors, and exact star ranks on all eleven
coordinate-boundary branches.
