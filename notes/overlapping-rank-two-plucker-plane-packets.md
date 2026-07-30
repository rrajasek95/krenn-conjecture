# Overlapping rank-two Plücker blocks form physical plane packets

## 1. Outcome

The genuinely overlapping part of the differential-Plücker problem has a
coordinate-free local reduction.  Work on the dense gauge-rigid
defect-three chart on which the six off-diagonal E2 primitives span the
defect space.  Let `ij` be a rank-two block, and suppose the three physical
diagonal blocks

\[
                         (p_b s_b)_{ij}\qquad(b=0,1,2)
\]

are nonzero.  Then one of the following happens.

1. The block belongs to a physical two-plane packet.  Its two endpoint
   image planes are generated either by two same-colour physical pairs, or
   by one mixed physical response.  Packets of the same type glue
   automatically across overlapping blocks.
2. Every differential-Plücker operator is blind on the block:

   \[
       \sigma(\alpha)-\alpha_i-\alpha_j=0
                         \qquad(\alpha\in D).          \tag{1}
   \]

3. Two reverse-response spaces have a proper sum `P` in `D`, `sigma`
   vanishes on `P`, and the remaining colour has an endpoint hole: one of
   its two `p` components or two `s` components is zero.

Consequently, on the fully transverse locus, where those four components
are nonzero for every colour, every diagonally live rank-two block is
either planar or lies on the exact complement-sum locus (1).  There is no
additional diffuse ``overlapping rows'' case.

The reduction also isolates the reverse-plane boundary.  If two escaped
diagonals have reverse spaces whose sum is proper but `sigma` is nonzero on
that sum, a single literal mixed response generates the rank-two planes on
every such block.  If `sigma` vanishes there, the four mixed products
through the omitted colour vanish; away from an endpoint hole, their
reciprocal-line relation forces (1).

This is a structural reduction, not the final E2 contradiction.  The
remaining exact targets are now the complement-sum blocks, endpoint-hole
propagation, and rank-one intersections between differently labelled plane
packets.  No graph subcase enumeration or computational checker is used.

The Hessian input is the diagonal-escape lemma from
[`differential-plucker-diagonal-escape-and-separated-packet.md`](differential-plucker-diagonal-escape-and-separated-packet.md).
That note eliminates the fully separated reciprocal-line model by a Hall
deficit.  The argument below treats its complementary, genuinely
overlapping locus.

The complement-sum locus itself has a short component description.  A
pair on that locus must meet every imbalanced bipartite component of the
rank-three graph.  Hence it is empty when all three defect components are
imbalanced.  If all three are balanced, it is exactly the universal
inactive core `K(D)` constrained by the multiresponse theorem; that
identification does not by itself eliminate the core.

## 2. Setup and the two tensor lemmas

Let `q` be the internal quadratic on the chart, let

\[
                         D=\ker B_3(q),\qquad \dim D=3,
\]

and write the six exact off-diagonal responses as

\[
 Z_{cd}=p_cs_d=\Gamma_q(\alpha_{cd}),qquad
 \alpha_{cd}\in D\quad(c\ne d).                       \tag{2}
\]

Assume that the six primitives span `D`.  Put

\[
 \ell_{ij}(\alpha)=\alpha_i+\alpha_j,qquad
 \sigma(\alpha)=\sum_k\alpha_k,qquad
 h_{ij}=\sigma-\ell_{ij}.                              \tag{3}
\]

For a colour `b`, if `{a,d}` is its complement, define its reverse-response
space

\[
                   R_b=\operatorname {span}
                    \{\alpha_{ad},\alpha_{da}\}\subseteq D.      \tag{4}
\]

Gauge rigidity and differential-Plucker closure give the diagonal-escape
implication

\[
 (Z_{bb})_{ij}\notin\mathbb Cq_{ij}
                   \quad\Longrightarrow\quad
             h_{ij}|_{R_b}=0.                          \tag{5}
\]

This is the only Hessian input used below.

For an oriented block `ij`, let `I_i(T)` and `I_j(T)` denote the two
flattening image spaces of a tensor `T in V_i tensor V_j`.

**Lemma 2.1 (a live rank-two product exposes both factor planes).**  If

\[
 T=x_i\otimes y_j+y_i\otimes x_j
\]

has matrix rank two, then

\[
 I_i(T)=\operatorname {span}\{x_i,y_i\},\qquad
 I_j(T)=\operatorname {span}\{x_j,y_j\},                \tag{6}
\]

and both displayed spans have dimension two.

**Proof.**  The two flattening ranks are bounded by the dimensions of the
displayed spans.  Rank two forces both pairs of simple-tensor factors to
be independent, and then the inclusions are equalities.  \(\square\)

The zero version records the only way a mixed physical product can
disappear without an endpoint hole.

**Lemma 2.2 (reciprocal zero pair).**  Fix colours `a!=b`.  Suppose all
four vectors

\[
 p_{a,i},p_{a,j},s_{a,i},s_{a,j}
\]

are nonzero, and

\[
                         (Z_{ab})_{ij}=(Z_{ba})_{ij}=0.             \tag{7}
\]

If `(Z_bb)_ij` is nonzero, then

\[
                         (Z_{bb})_{ij}\in
                         \mathbb C^*(Z_{aa})_{ij}.                  \tag{8}
\]

**Proof.**  The first equality in (7) is

\[
 p_{a,i}\otimes s_{b,j}+s_{b,i}\otimes p_{a,j}=0.
\]

If one component of `s_b` were zero, both would be zero, contradicting
the nonvanishing of `(Z_bb)_ij`.  Uniqueness of a nonzero simple tensor
therefore gives a nonzero scalar `gamma` with

\[
                   s_{b,i}=\gamma p_{a,i},\qquad
                   s_{b,j}=-\gamma p_{a,j}.             \tag{9}
\]

The reverse equality gives a nonzero `beta` with

\[
                   p_{b,i}=\beta s_{a,i},\qquad
                   p_{b,j}=-\beta s_{a,j}.              \tag{10}
\]

Substitution yields

\[
                         (Z_{bb})_{ij}
                    =-\beta\gamma (Z_{aa})_{ij},        \tag{11}
\]

which proves (8).  \(\square\)

## 3. The block trichotomy

Call a nonzero diagonal `(Z_bb)_ij` **aligned** if it belongs to
`C q_ij`, and **escaped** otherwise.

**Theorem 3.1 (rank-two Plücker packet reduction).**  Suppose

\[
                         \operatorname {rank}q_{ij}=2              \tag{12}
\]

and all three diagonal blocks `(Z_bb)_ij` are nonzero.  At least one of
the following holds.

1. **Two-diagonal plane.**  Two colours `b,c` are aligned.  For each of
   them,

   \[
     I_i(q_{ij})=\operatorname {span}\{p_{b,i},s_{b,i}\},
     \qquad
     I_j(q_{ij})=\operatorname {span}\{p_{b,j},s_{b,j}\},         \tag{13}
   \]

   and the same identities hold with `c` in place of `b`.
2. **Complement-sum block.**  Equation (1) holds, equivalently
   `h_ij|D=0`.
3. **Mixed-response plane.**  For two escaped colours `b,c`, the proper
   space

   \[
                              P=R_b+R_c\subsetneq D                 \tag{14}
   \]

   satisfies `sigma|P!=0`.  One of the four primitives through the third
   colour `a` has nonzero `sigma`; for that ordered pair `(r,s)`,

   \[
                 (Z_{rs})_{ij}=\sigma(\alpha_{rs})q_{ij},          \tag{15}
   \]

   and Lemma 2.1 gives its two physical endpoint planes.
4. **Endpoint-hole boundary.**  For two escaped colours `b,c`, (14)
   holds, `sigma|P=0`, and at least one of

   \[
                    p_{a,i},p_{a,j},s_{a,i},s_{a,j}                 \tag{16}
   \]

   is zero, where `a` is the remaining colour.

**Proof.**  If at least two diagonals are aligned, their nonzero scalar
multiples of the rank-two block `q_ij` have rank two.  Lemma 2.1 gives
(13), proving alternative 1.

Otherwise at least two diagonals, say `b,c`, escape.  By (5), `h_ij`
annihilates `P=R_b+R_c`.  If `P=D`, alternative 2 follows.

Suppose `P` is proper.  It is spanned by the four primitives

\[
       \alpha_{ab},\alpha_{ba},\alpha_{ac},\alpha_{ca}.            \tag{17}
\]

If `sigma|P` is nonzero, one of these four generators has nonzero
`sigma`.  Since `h_ij` vanishes on `P`, its block coefficient satisfies

\[
                   \ell_{ij}(\alpha_{rs})
                                =\sigma(\alpha_{rs})\ne0.
\]

Equation (2) gives (15), and this is alternative 3.

It remains that `sigma|P=0`.  Now `ell_ij|P=0`, so all four physical
blocks in (17) vanish at `ij`.  If (16) holds, we are in alternative 4.
Otherwise apply Lemma 2.2 to `a,b`.  The nonzero escaped block
`(Z_bb)_ij` is a nonzero multiple of `(Z_aa)_ij`; hence the latter also
escapes.  Equation (5) now makes `h_ij` vanish on `R_a`.  The six
primitives span `D`, so

\[
                              P+R_a=D.
\]

Thus `h_ij|D=0`, which is alternative 2.  \(\square\)

Two useful specializations are immediate.

**Corollary 3.2 (fully transverse blocks).**  If all twelve physical row
components at `i,j` are nonzero, alternatives 1--3 hold; the endpoint-hole
boundary is absent.  Thus every
fully transverse, diagonally live rank-two block is a physical plane block
or a complement-sum block.

The following propagation fact supplies the quantifier needed in the next
corollary.

**Lemma 3.3 (one aligned diagonal aligns all three).**  On a rank-two block
on which all six off-diagonal responses are scalar multiples of `q_ij`, if
one nonzero diagonal `(Z_aa)_ij` is a scalar multiple of `q_ij`, then all
three diagonals are scalar multiples of `q_ij`.

**Proof.**  Rescale and choose bases of the two endpoint image planes so
that

\[
       (p_{a,i},s_{a,i}),\qquad(s_{a,j},p_{a,j}),\qquad
                         q_{ij}=I_2.                              \tag{18a}
\]

For another colour `b`, quotienting the two mixed identities `Z_ab` and
`Z_ba` by these endpoint planes first places all four colour-`b` vectors
in the same planes.  In the displayed bases, the condition that both
mixed tensors are scalar matrices has the form

\[
\begin{aligned}
 s_{b,i}&=(t,\lambda), &s_{b,j}&=(\lambda,-t),\\
 p_{b,i}&=(\mu,u),     &p_{b,j}&=(-u,\mu).
\end{aligned}                                                    \tag{18b}
\]

Direct multiplication gives

\[
                         (Z_{bb})_{ij}
                    =(\lambda\mu-tu)I_2.                         \tag{18c}
\]

Diagonal liveness makes this scalar nonzero.  The same argument applies
to the third colour.  \(\square\)

**Corollary 3.3 (reverse spaces in general position).**  If

\[
                         R_b+R_c=D\qquad(b\ne c),                  \tag{18}
\]

then every diagonally live rank-two block is either a two-diagonal plane
or a complement-sum block.  No collapsed reverse-plane alternative is
available.

**Proof.**  By Lemma 3.3 either all three diagonals align, giving the plane
alternative, or all three escape.  In the latter case the displayed pair
is a pair of escaped colours, so (5) makes `h_ij` vanish on their sum,
which is `D`.  \(\square\)

The endpoint-hole alternative is more rigid than the name suggests.

**Corollary 3.4 (one hole kills an opposite star pair).**  In alternative
4, let `a` be the remaining colour and `{b,c}` the two escaped colours.
At least one of the following holds:

1. `p_(a,i)=p_(a,j)=0`;
2. `s_(a,i)=s_(a,j)=0`;
3. at one endpoint `v in {i,j}`,

   \[
                         p_{a,v}=s_{b,v}=s_{c,v}=0;
   \]

4. at one endpoint `v in {i,j}`,

   \[
                         s_{a,v}=p_{b,v}=p_{c,v}=0.
   \]

**Proof.**  All four mixed blocks in (17) vanish.  If, say,
`p_(a,i)=0`, then either `p_(a,j)=0`, giving the first alternative, or

\[
 (Z_{ab})_{ij}=s_{b,i}\otimes p_{a,j}=0,\qquad
 (Z_{ac})_{ij}=s_{c,i}\otimes p_{a,j}=0,
\]

which gives the third alternative.  The other endpoint is symmetric.
Starting from a zero component of `s_a` and using
`(Z_ba)_ij=(Z_ca)_ij=0` gives the second or fourth alternative.
\(\square\)

## 4. Plane packets glue without coordinates

The local planes above are compatible on genuine overlaps.

**Theorem 4.1 (automatic gluing).**

1. Let `E_diag` be any family of rank-two blocks in alternative 1.  On an
   edge `e`, let `C_e` be its set of aligned colours; `|C_e|>=2`.  If two
   edges `ij,ik` of `E_diag` meet at `i`, then

   \[
                          I_i(q_{ij})=I_i(q_{ik}).                  \tag{19}
   \]

   Consequently every connected component of `E_diag` carries a
   canonical sitewise plane bundle `L_i` with
   `q_ij in L_i tensor L_j` on every one of its edges.
2. Fix a proper reverse space `P` and one physical generator
   `alpha_rs in P` with `sigma(alpha_rs)!=0`.  On every rank-two block
   with `h_ij|P=0`, equation (15) holds.  These blocks likewise carry the
   plane bundle

   \[
                L_i=\operatorname {span}\{p_{r,i},s_{s,i}\}.      \tag{20}
   \]

**Proof.**  In the first statement, two subsets of a three-colour set,
each of order at least two, intersect.  Choose `b in C_ij intersect C_ik`.
Equation (13) identifies both planes with
`span{p_(b,i),s_(b,i)}`, proving (19).

For the second statement, `h_ij(alpha_rs)=0` changes the response
coefficient into the fixed nonzero scalar `sigma(alpha_rs)`.  Lemma 2.1
identifies the endpoint plane with (20).  At two incident blocks the same
two independent physical vectors occur, so the planes agree.  \(\square\)

More generally, two differently labelled packets glue whenever the span
of their common physical generators has dimension two at the shared site.
If they do not glue, that physical overlap has rank at most one.  Thus the
only packet-incidence obstruction is a literal line overlap, not an
uncontrolled rank-two configuration.

## 5. The complement-sum locus meets at most two imbalanced components

There is a useful exact description of alternative 2 which does not refer
to physical row coordinates.  Let `G_3(q)` be the graph of rank-three
blocks.  For each connected bipartite component `C`, choose shores
`C^+,C^-` and write

\[
 \zeta_C=1_{C^+}-1_{C^-},\qquad
 \Delta_C=\sigma(\zeta_C)=|C^+|-|C^-|.                \tag{21}
\]

An isolated vertex is allowed here: it is a bipartite component with one
shore empty and `|Delta_C|=1`.  The vectors `zeta_C` over the bipartite
components form a basis of `D`; nonbipartite components contribute no
defect direction.

**Proposition 5.1 (component signature).**  A site pair `ij` satisfies
`h_ij|D=0` if and only if, for every bipartite component `C`,

\[
                    \Delta_C=\zeta_C(i)+\zeta_C(j),                \tag{22}
\]

where `zeta_C` is zero off `C`.  Consequently:

1. every component disjoint from `{i,j}` is balanced;
2. a component containing exactly one endpoint has imbalance `+1` or
   `-1`, with the sign of that endpoint;
3. a component containing both endpoints has imbalance `0` when they are
   on opposite shores and `+2` or `-2` when they are on the same shore.

In defect three, a complement-sum pair therefore meets every imbalanced
defect component, so there are at most two such components.  At least one
of the three defect components is balanced and nontrivial.  If all three
components are imbalanced, the complement-sum locus is empty.  If all are
balanced, then

\[
             h_{ij}|D=0\quad\Longleftrightarrow\quad
             \ell_{ij}|D=0\quad\Longleftrightarrow\quad ij\in K(D).
                                                                    \tag{23}
\]

**Proof.**  Evaluate `h_ij=sigma-ell_ij` on the component basis
`zeta_C`; this gives exactly (22).  The three listed cases are the possible
values of `zeta_C(i)+zeta_C(j)`.  A nonzero `Delta_C` forces the pair to
meet `C`, and two sites can meet at most two disjoint components.  A
balanced component cannot be an isolated vertex.  Finally, when all
component imbalances vanish, `sigma|D=0`, so `h_ij=-ell_ij` on `D`; the
last condition in (23) is the definition of the universal inactive core.
\(\square\)

Thus complement-sum blocks are identified with the constrained
inactive-core route on the all-balanced stratum, and do not exist on the
all-imbalanced stratum.  This is not a closure of `K(D)`.  Only the mixed
imbalance signatures in (22) remain independent.

Those mixed signatures are also explicit.  With two imbalanced
components, `i,j` lie one in each and both shore imbalances are `+1` or
`-1`, with the corresponding endpoint signs.  With one imbalanced
component, either both endpoints lie on one of its shores and its
imbalance is `+2` or `-2`, or exactly one endpoint lies there, its
imbalance is `+1` or `-1`, and the other endpoint lies in a nonbipartite
component.  An endpoint cannot lie alone in a balanced bipartite
component by (22).  Thus the unresolved complement-sum locus has only an
imbalance-one cross-component form and an imbalance-two same-shore form.

## 6. Exact remaining gate

The theorem removes the broad overlapping-row case from the local
differential-Plücker frontier.  A completion can now target three explicit
objects.

* **Complement-sum:** exclude rank-two source blocks satisfying (1), or
  show that their normalized diagonal matching terms export an active cap.
* **Holes and zero diagonals:** propagate endpoint holes (and the analogous
  zero-diagonal reciprocal-line boundary) across the good fan until a
  physical row becomes sparse or a zero shore appears.
* **Packet incidence:** use one third-site source equation to glue two
  differently labelled plane packets across their remaining rank-one
  intersection.  Once they glue, the multiresponse inactive-core theorem
  applies to the resulting common sitewise planes.

No finite search is attached: every assertion is a two-tensor rank
argument plus the already audited diagonal-escape implication (5).
