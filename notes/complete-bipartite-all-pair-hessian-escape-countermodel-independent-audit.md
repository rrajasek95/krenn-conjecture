# Independent audit: complete-bipartite all-pair escape family

## 1. Verdict

The construction in
[complete-bipartite-all-pair-hessian-escape-countermodel.md](complete-bipartite-all-pair-hessian-escape-countermodel.md)
is correct, uniformly for every even order $N=2s\ge6$.  It is a valid
endpoint-ordered aggregate source whose every pair-deleted chart has two
injective stars and connected bipartite rank-three graph.  Its pure
constant-colour coefficients are exactly one, and all pair responses are
literal cofactor expansions of the same quadratic.

The scope statement is also correct and essential.  This family is **not**
a source for the ternary GHZ tensor and hence is **not** a counterexample to
Krenn's conjecture.  The word with colour $0$ at site $0$ and colour $1$ at
every other site has coefficient $2^{s-1}$ instead of zero.  The family is
only a countermodel to structural arguments which omit the mixed GHZ
vanishing equations.

## 2. Matrix and endpoint-order audit

Let

\[
 D=\begin{pmatrix}1&1&1\\1&2&4\\1&3&9\end{pmatrix}.
\]

A direct Leibniz expansion gives

\[
 \det D=(18-12)-(9-4)+(3-2)=2.
\]

For $d=(1,2,9)$ and

\[
 \sigma_c=\frac1{s!d_c^s},\qquad
 S=\operatorname{diag}(\sigma_0,\sigma_1,\sigma_2),
\]

the scaled block $SD$ is invertible because
$\det(SD)=\sigma_0\sigma_1\sigma_2\det D\ne0$.  Every cross-shore
block whose left endpoint is site $0$ is $SD$, every other cross-shore
block is $D$, and same-shore blocks vanish.

This is genuinely endpoint oriented.  From a right-shore endpoint the
blocks are $(SD)^T$ or $D^T$; one must not reuse their left-oriented
matrices.  Thus the special site-$0$ row scale becomes the corresponding
column scale on reversal.  The independent checker constructs every
oriented block this way and computes the star ranks from the concatenated
oriented rows.

Each nonzero matrix cell can be realized by one decorated source with the
two displayed endpoint colours and its rational weight.  Splitting a cell
among parallel sources changes nothing provided their weights sum to the
same entry.  Hence the aggregate matrices are legitimate source data, not
abstract pair responses.

## 3. Exact normalization and the mixed residual

Every perfect matching of $K_{s,s}$ is a bijection between the shores, so
there are $s!$ matchings.  For the constant word $c^{2s}$, each matching
has one scaled edge incident to site $0$ and $s-1$ unscaled edges.  Its
weight is

\[
    \sigma_c d_c^s=\frac1{s!}.
\]

The coefficient is therefore exactly one for each $c=0,1,2$.  This
calculation includes the special scaling exactly once and does not depend
on cancellation.

Now give site $0$ colour $0$ and every other site colour $1$.  Again every
left-right bijection contributes.  Its site-$0$ edge contributes
$\sigma_0D_{01}=1/s!$, while the other $s-1$ edges contribute
$D_{11}^{s-1}=2^{s-1}$.  Therefore

\[
 [e_0\otimes e_1^{\otimes(2s-1)}]H_B(A)
   =s!\frac{2^{s-1}}{s!}=2^{s-1}\ne0.                 \tag{1}
\]

For the named pair $p=0,q=1$, the direct same-shore block is zero, so all
of (1) lies in the two-star cofactor term.  Equivalently, its $s!$ terms
come from choosing ordered distinct right neighbors for $0$ and $1$ and
then a bijection on the remaining vertices:
$s(s-1)(s-2)!=s!$.  Since the GHZ target vanishes on every nonconstant
word, (1) proves both the stated residual and the claimed limitation.

## 4. Stars, deletion graphs, and global support

For any deleted pair $\{p,q\}$, a star at either endpoint retains at least
one cross-shore block.  More precisely, it retains $s$ such blocks when
$p,q$ share a shore and $s-1$ when they lie on opposite shores.  Every
retained block is $D$, $SD$, or the transpose of one of them, and is
invertible.  Its three rows already have rank three inside the direct sum
of neighbor spaces, so both aggregate stars are injective.

The rank-three graph is exactly $K_{s,s}$.  Deleting a same-shore pair
gives $K_{s-2,s}$, while deleting an opposite-shore pair gives
$K_{s-1,s-1}$.  For $s\ge3$ both are spanning, connected, and bipartite.
All entries of $D$ and $SD$ are nonzero, as are all entries of their
transposes.  Consequently every endpoint-colour row reaches exactly the
$s$ vertices on the opposite shore.

The vertex connectivity is exactly $s$.  Deleting fewer than $s$ vertices
leaves at least one vertex on each shore, and the remaining complete
bipartite graph is connected.  Deleting a whole shore leaves the other
shore as an independent set of size $s$.  Every vertex has rank-three
degree $s$, so no vertex is cubic once $s\ge4$.  (At the boundary $s=3$,
the graph is $K_{3,3}$ and every vertex is cubic; the primary note states
the no-cubic conclusion only for $s\ge4$.)

## 5. Literal common-source cofactor identity

Fix any pair $p,q$, endpoint colours $c,d$, and a colour assignment on the
other sites $W$.  Partition the perfect matchings of the one physical
quadratic into two disjoint classes.

1. A matching containing $\{p,q\}$ contributes the direct entry
   $a_{cd}$ times a perfect matching on $W$.
2. Every other matching has unique distinct sites $r,t\in W$ paired with
   $p,q$, respectively, followed by a perfect matching of
   $W\setminus\{r,t\}$.

Coefficientwise, this is exactly

\[
       a_{cd}x^{[s-1]}+p_cs_dx^{[s-2]}.                \tag{2}
\]

The divided-power convention removes permutation multiplicities, while
the ordered roles of $p$ and $q$ retain endpoint asymmetry.  The partition
proves (2) for every order and every pair without a genericity assumption.
It also explains why pair-chart exchange identities alone cannot exclude
this family: all charts are merely different partitions of matchings from
the same source.

The independent checker reconstructs both sides separately.  It exhausts
all $3^6$ colour words and all 15 pairs at $N=6$, then checks all pairs,
all nine endpoint-colour choices, and structured internal assignments at
$N=8,10$.  Thus the common-source claim is tested as a coefficient
identity, not inferred from the primary implementation.

## 6. Independent exact checker and frozen inputs

Frozen primary artifacts:

```text
778e7a04ed5e0af0d69cac5b92fb0833a3903fe5e00c239d3a29715674dcb779  notes/complete-bipartite-all-pair-hessian-escape-countermodel.md
a807dc8ab7198b4cbe730ea33f58f87062cddb804c9a8b8de3928949ebc3a191  computations/verify_complete_bipartite_all_pair_hessian_escape_countermodel.py
d48d831e7a6d2645b785a8582deec407c6219e86d57b5cfce0bbd4c3932169c8  computations/audit_complete_bipartite_all_pair_hessian_escape_countermodel_independent.py
```

The clean-room checker
[audit_complete_bipartite_all_pair_hessian_escape_countermodel_independent.py](../computations/audit_complete_bipartite_all_pair_hessian_escape_countermodel_independent.py)

* verifies the two frozen primary hashes before doing mathematics;
* uses a Leibniz determinant computation and independent rational row
  reduction;
* reconstructs the special row scaling and all reversed endpoint blocks;
* checks the normalization and mixed formulas uniformly through $N=60$
  and enumerates permanents through $N=14$;
* computes both star maps and every deletion graph for all pairs through
  $N=20$;
* exhausts the vertex-connectivity lower bound for $K_{s,s}$ through
  $s=7$; and
* verifies (2) by an independent perfect-matching recursion.

These finite calculations audit the implementation and boundary cases.
The bijection, invertible-block, graph, and matching-partition arguments
above prove the statements uniformly for all even $N\ge6$.

## 7. Final scope

The audit supports exactly the primary note's negative conclusion.  Pure
normalization, aggregate-star injectivity, connected-bipartite rank data,
and literal overlap of physical pair cofactors do not by themselves force
a bounded separator, sparse row, or cubic vertex.  Any successful escape
elimination must use genuinely mixed GHZ vanishing (or equivalent
information carried by the distinguished polarized kernel vectors).

Because equation (1) violates that mixed vanishing, none of this weakens
the conjecture itself.
