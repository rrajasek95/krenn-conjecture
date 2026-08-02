# The Buchberger cells have a path-forest skeleton

## 1. Structural result

The squarefree terms found in normalized chart 26 are governed by a much
smaller uncoloured object.  Forget the endpoint colours of a decorated edge
variable, but retain its two vertices and its multiplicity.  The leading
skeletons through the first compatibility cell are

\[
 \begin{array}{c|c|c}
 \text{homogeneous degree}&\text{skeleton}&\text{components}\\ \hline
 h=4&P_2+P_2+P_2+P_2&4,\\
 h+1=5&P_4+P_2+P_2&3,\\
 h+2=6&P_6+P_2\ \text{or}\ P_4+P_4&2.
 \end{array}
\]

Thus a new Buchberger layer joins two components of a spanning linear
forest.  The bad old degree-six lexicographic lead does not do this: it
repeats one decorated coordinate.  The feasible weighted lead is a
component-joining term of type \(P_6+P_2\).

This is not merely a pattern in the selected degree-five leads.  The
path-forest shape of every top-degree term in each universal degree-five
transport follows formally from the Laplace identities.

## 2. Universal degree-five forest lemma

Let \(|B|=2h\), and use the notation of
[`hafnian-star-minor-buchberger-identity.md`](hafnian-star-minor-buchberger-identity.md).
Every top-degree monomial on the right side of the one-end transport

\[
 B_uH_a-A_uH_b
   =\sum_{w\ne u,v}(B_uA_w-A_uB_w)
       H_{B\setminus\{v,w\}}
\tag{1}
\]
has an uncoloured skeleton

\[
                         P_4+(h-2)P_2.                 \tag{2}
\]

Indeed, a term in the summand indexed by \(w\) contains the two distinct
star edges \(vu,vw\).  In the perfect matching supplied by the smaller
hafnian, \(u\) is paired with some \(z\notin\{v,w\}\).  These three edges
form the path

\[
                             z-u-v-w.
\]

The remaining \(2h-4\) vertices are paired disjointly.  Hence all edge
variables are distinct, the graph is spanning and acyclic, and (2) follows.
The two terms of the star minor have the same conclusion.

The direct-double transport has the same skeleton.  Its displayed
coefficient contains the distinct edges \(uv,vw,uz\), forming

\[
                             w-v-u-z,
\]

and its smaller cofactor matches every remaining vertex.  Consequently the
entire first Buchberger layer, before any term-order choice, is supported on
decorated spanning linear forests of type (2).  This proof works at every
even order and uses neither the chart nor the eight-site census.

For chart 26 at eight sites, the exhaustive calculation sharpens the lemma:
all 84,005 reduced degree-five cells have distinct leads, and all their
leads retain this same skeleton.

## 3. What the first compatibility cell is measuring

Suppose a transport cell is already indexed by a spanning linear forest
\(F\).  Multiplication by one new edge has three qualitatively different
effects.

1. If its endpoints lie in different components and are endpoints of their
   paths, it joins those components and produces another spanning linear
   forest.
2. If the endpoints lie in one component, it closes a cycle.
3. If it repeats an underlying edge, it produces a parallel edge; it may
   even repeat the identical decorated coordinate.

The first exact degree-six cell displays precisely this split.  Among its
372 top-degree terms there are

\[
 \begin{array}{c|r}
 P_6+P_2&200\\
 P_4+P_4&100\\
 \text{parallel underlying edge, different decorations}&44\\
 \text{repeated decorated coordinate}&22\\
 \text{underlying cycle}&6.
 \end{array}                                             \tag{3}
\]

The weighted order selects one of the 300 genuine component joins.  The old
lexicographic order selects one of the 22 repeated-coordinate terms.  Thus
the weight repair has a combinatorial meaning: it orients the compatibility
cell toward the graphic-matroid independent stratum.

There is a complementary circuit description on the input side.  If two
perfect matchings share all but two of their edges, delete the common edges.
On the four remaining vertices their union is the alternating cycle
\(C_4\).  The only decorated exception is that the two monomials can use the
same underlying matching edge with different endpoint colours; after
forgetting colours this is a parallel-edge two-circuit.  Hence every
degree-\(h+2\) critical LCM between original matching leads is supported on
an alternating four-cycle or on a decorated parallel pair.  Its reduction
is literally a circuit-breaking operation.  The same circuit skeleton
persists when one input has already been replaced by a one-join path forest.

This puts the computation close to broken-circuit straightening for a
graphic matroid, but with a crucial twist: the circuit coefficients are
smaller, source-labelled hafnians rather than scalars.  Same-star Pluecker
identities say that this coefficient system is flat along one star.  The
cross-star Bianchi cells measure its curvature.  A useful description of
the desired algebra is therefore a **hafnian-twisted broken-circuit
algebra**: the ordinary no-broken-circuit termination is already visible,
and the remaining task is to prove that its coefficient curvature is exact
in the literal mixed source complex.

The exact audit is

```text
python3 computations/verify_n8_chart26_path_forest_skeleton.py
```

It reconstructs all 6,558 original leads, all 84,005 degree-five cells, and
the 546-term compatibility remainder before forgetting any decoration.

## 4. Candidate uniform termination statistic

There is a canonical **output base** on every forest occurring above.  Let
\(F\) be a spanning linear forest all of whose path components have even
order.  On each component, start at either endpoint and take the first,
third, fifth, and so on edges.  Because the component has an odd number of
edges, reversing the path selects the same set.  The union \(M(F)\) of these
alternating edges is therefore a uniquely determined perfect matching.
The complementary edges

\[
                         J(F)=E(F)\setminus M(F)           \tag{4}
\]

are the joins between the matching components.  If \(F\) has \(c(F)\)
components, then \(|J(F)|=h-c(F)\).  Conversely, starting from \(M(F)\) and
adding the joins in any order reconstructs \(F\), provided each join uses
two current path endpoints in different components.

For a fixed forest, different orders on \(J(F)\) form a Boolean cube.  This
does not say that its output base \(M(F)\) is the matching of the input
hafnian term; the two matchings can differ by an alternating \(C_4\) flip.
Thus the Boolean cube stores join order only after its base is fixed.

In fact \(J(F)\) is itself a matching.  Along an even path, the edges not in
the odd-position matching occupy the even positions and are pairwise
vertex-disjoint.  Thus the same forests have the equivalent description

\[
 F=M\cup J,\qquad M\text{ a perfect matching},\quad
 J\text{ a partial matching},
 \tag{5}
\]

where \(M\cup J\) has no alternating cycle.  Conversely these conditions
make every component an even alternating path and recover \(M=M(F)\).
After contracting the edges of \(M\), the join matching is an acyclic
port-labelled path forest on the matching blocks.

More precisely, let \({\cal E}(V)\) be the poset of all such forests under
edge inclusion.  Then

\[
 {\cal E}(V)=\coprod_{M\text{ a perfect matching}}{\cal E}_M(V),
 \qquad {\cal E}_M(V)=\{F:M(F)=M\}.                       \tag{5a}
\]

If \(F\subseteq G\), every added edge joins endpoints of two even paths;
the alternating matching of the joined path is the union of the two old
alternating matchings.  Hence comparable forests have the same base.  For
every \(F\), its principal interval is exactly

\[
 [M(F),F]=\{M(F)\cup S:S\subseteq J(F)\}
          \cong\mathsf B_{|J(F)|}.                       \tag{5b}
\]

Deleting any subset of the even-position join edges cuts an even path only
into even paths, proving (5b).  The whole fibre \({\cal E}_M(V)\) is a
down-set of endpoint-capacitated acyclic join matchings, not generally one
Boolean cube.

The distinction between input and output bases already occurs in the first
universal transport.  If the cancelled input matching contains \(uv,wz\),
the output path \(z-u-v-w\) has alternating base \(uz,vw\); their symmetric
difference is the cycle \(uv,vw,wz,zu\).  In chart 26 the first source base
is \((02)(13)(45)(67)\), while the lead `0948cfebf5` has output base
\((02)(13)(46)(57)\).  This is why the coproduct (5a) must be glued by
base-exchange operators rather than treated as one cubical complex.

At the terminal rank \(|J|=h-1\), the forest is connected and hence is an
alternating Hamilton path.  The join matching \(J\) leaves exactly its two
endpoints \(p,q\) unmatched, so

\[
                         J\text{ is a perfect matching of }
                         B\setminus\{p,q\}.               \tag{6}
\]

This is the combinatorial interface with clean-pair descent.  A
source-faithful contraction which carries the pure readout to terminal
forest cells automatically produces both a candidate clean pair \(p,q\)
and the smaller support matching (6).  The still-missing statement is that
the physical coefficient attached to some terminal endpoint pair is active
and has zero lift indeterminacy.

For a spanning edge multigraph \(F\), put

\[
 d(F)=\left(
  \sum_e(m_e-1),\quad
  |E(F)_{\rm simple}|-|V(F)|+c(F),\quad
  \sum_v\max(0,\deg_F(v)-2),\quad
  c(F)
 \right),                                                \tag{7}
\]

where \(c(F)\) is its number of connected components.  The first three
entries measure parallel excess, cycle rank, and branching excess.  On the
zero-defect stratum, a legal endpoint join changes only
\(c(F)\mapsto c(F)-1\).

Starting with a perfect matching, at most \(h-1\) legal joins are possible:

\[
 hP_2\longrightarrow P_4+(h-2)P_2\longrightarrow\cdots
 \longrightarrow P_{2h}.                                \tag{8}
\]

Therefore any straightening system which always chooses a zero-defect join
terminates by homogeneous degree \(2h-1\).  This is a genuine well-founded
statistic, rather than a guessed degree cap.  It is only the combinatorial
part of the desired theorem: a single additive term order must still orient
all simultaneously active algebraic cells toward those legal joins.

## 5. Fixed-base Koszul coherences and the base-exchange gap

There is an exact all-orders source identity behind the first local cells.
Fix a perfect matching \(M\), and for a colour word \(c\) write

\[
             \mu_M(c)=\prod_{uv\in M}X_{uv}(c_u,c_v).
\]

For two mixed words define the literal source syzygy

\[
 R^M_{cd}=\mu_M(d)H_c-\mu_M(c)H_d.                       \tag{K2}
\]

The distinguished \(M\)-matching term cancels.  These relations are the
two-by-two minors of the matrix with columns
\((\mu_M(c),H_c)^{\mathsf T}\), so their higher coherences are automatic.
For three words, let \(E^M_{cd}\) denote the formal source cell whose image
is (K2), and put

\[
 T^M_{cde}=\mu_M(e)E^M_{cd}-\mu_M(d)E^M_{ce}
       +\mu_M(c)E^M_{de}.                                \tag{K3}
\]

Its boundary is zero by direct cancellation.  For four words the four
instances of (K3) satisfy the tetrahedral
identity

\[
 \mu_M(f)T^M_{cde}-\mu_M(e)T^M_{cdf}
       +\mu_M(d)T^M_{cef}-\mu_M(c)T^M_{def}=0.           \tag{K4}
\]

The same alternating Koszul formula supplies every higher simplex.  These
are identities in the labelled source module, not only polynomial
equalities after taking its image.

The star and direct-double cells are primitive factors of (K2).  If \(c,d\)
differ at one endpoint of an edge of \(M\), their matching monomials share
the product on the other \(h-1\) edges, and (K2) is that common product
times the one-end star transport.  If the two changed endpoints form one
edge of \(M\), the same statement gives the direct-double transport.
Consequently (K3)--(K4) prove all higher coherence *before* this common
factor is cancelled.  Passing to the primitive low-degree cells is a colon
or localization step; proving that the Koszul simplices survive that step is
exactly a source-saturation problem.

Two legal component joins are either disjoint or share a path component.
Disjoint joins commute.  Joins using the same star give the already proved
Pluecker/Eagon--Northcott relations, and changing a colour row gives the
three-colour Koszul relation.  Joins based at two different vertices give
the cross-star Bianchi square.  These are exactly the local diamonds in the
fixed-\(M\) poset of spanning path forests.  They are the primitive images
of faces of the Koszul simplices above.

This suggests a cellular straightening complex whose cells are decorated
path forests, with boundary given by deleting join edges.  The formal
identity \(\partial^2=0\) is the Bianchi cancellation.  The geometric split
at a repeated coordinate is then the deletion--localization analogue of the
ordinary deletion--contraction recurrence for a graphic matroid.

The completed degree-six census shows that fixed-base cubes are not the
whole complex.  Some compatibility remainders have path-forest terms, but
their canonical alternating matchings differ from every input source
matching.  They are **base-matching exchange curvature**.  The appropriate
global object must therefore glue the fixed-\(M\) Koszul complexes along
alternating-cycle flips \(M\leftrightarrow M'\).  Other compatibility cells
contain no simple path-forest term at all and require a
deletion--localization split before entering this complex.

### 5.1 Exact alternating-C4 exchange and its three-cell

The first nontrivial gluing is also determinantal.  Fix matchings \(M,N\)
and abbreviate

\[
 a_c=\mu_M(c),\qquad b_c=\mu_N(c),\qquad
 P^M_{cd}=a_cH_d-a_dH_c,qquad
 \Delta^{MN}_{cd}=a_cb_d-a_db_c.                         \tag{E1}
\]

The columns \((a_c,b_c,H_c)^{\mathsf T}\) form a three-row matrix.  Its
two-column Pluecker identities give the endpoint exchange formulas

\[
 \boxed{
 b_cP^M_{cd}-a_cP^N_{cd}=\Delta^{MN}_{cd}H_c,
 \qquad
 b_dP^M_{cd}-a_dP^N_{cd}=\Delta^{MN}_{cd}H_d.}           \tag{E2}
\]

For three states, the matching-exchange Bianchi determinant is

\[
\begin{aligned}
 C^{MN}_{cde}
 &=b_cP^M_{de}-b_dP^M_{ce}+b_eP^M_{cd}\\
 &=-a_cP^N_{de}+a_dP^N_{ce}-a_eP^N_{cd}\\
 &=-\bigl(\Delta^{MN}_{de}H_c-
          \Delta^{MN}_{ce}H_d+
          \Delta^{MN}_{cd}H_e\bigr).                   \tag{E3}
\end{aligned}
\]

This cell has an exact support property: if the \(H\)-row is expanded by
perfect matchings, the contributions of \(M\) and \(N\) vanish separately
because each repeats one of the first two determinant rows.  Thus (E3)
lives away from both input bases, exactly as in the two weighted bad
representatives having 238 and 264 simple path terms but zero terms on an
input source matching.

There is a literal higher coherence beyond the Bianchi squares.  For four
states \(c<d<e<f\), the maximal minors of the same three-by-four matrix
satisfy

\[
 \boxed{
 a_cC^{MN}_{def}-a_dC^{MN}_{cef}
 +a_eC^{MN}_{cdf}-a_fC^{MN}_{cde}=0,}                  \tag{E4a}
\]

\[
 \boxed{
 b_cC^{MN}_{def}-b_dC^{MN}_{cef}
 +b_eC^{MN}_{cdf}-b_fC^{MN}_{cde}=0.}                  \tag{E4b}
\]

These are the two row-Laplace boundaries of a source-labelled tetrahedral
three-cell.  When \(M\mathbin\triangle N=C_4\), the exchange minors in (E1)
are supported on that alternating four-cycle, times the common matching
core.  Therefore an alternating-\(C_4\) exchange does supply the missing
local three-cell.  Adding more matching rows gives the analogous higher
coherences as ordinary minors, although determinantal boundary identities
alone do not prove acyclicity after the label diagonal is imposed.

The exact eight-site audit uses

\[
 M=(02)(13)(45)(67),\qquad N=(02)(13)(47)(56)
\]

and source codes \(1,2,10,11\).  It verifies all twelve endpoint instances
of (E2), four 498-term determinants (E3), separate cancellation of the two
base matching terms, and both tetrahedral identities (E4).  The primitive
boundary transports have 180 terms whenever the two words differ at one
endpoint.  Run

```text
python3 computations/verify_n8_chart26_c4_exchange_3cell.py
```

with ledger digest
`64b1f89a760ae8268e0ab4fe9712cb9b289a3b540f9c0a370a3554f754ade287`.

This is the exact local answer to the base-exchange part of the degree-six
frontier, not yet its reduction theorem.  The remaining algebraic step is
to prove that cancelling the state-dependent common monomial factors in
(E2)--(E4) preserves the tetrahedral coherence in each refined source
class.  That is a source-saturation question.  The two bad representatives
with no simple path term still require vertex splitting before these cells
apply.

### 5.2 Primitive factorization exposes a colon obstruction

The un-divided three-cell is coherent, but the weighted degree-six problem
uses its primitive factors.  An exact normalization/reduction audit gives a
sharp negative answer for the two path-bearing bad representatives.

For the class of size 42,754, with sources (H_1) and the transport
((1,10)), each endpoint instance of (E2) has full common factor

```text
09094848d9f4
```

and primitive homogeneous degree six.  Its three summands have respectively
180, 180, and 210 terms.  All three reduce separately to zero against the
complete degree-four/degree-five basis.  Thus this degree-six exchange face
is already lower-exact and supplies no reducer for the 504-term normal form
with lead `0951acc6f4f4`.

For the class of size 38,702, with sources (H_1) and ((1,37)), the common
factor is only

```text
09094848f4
```

so the primitive endpoint cells have degree seven.  At endpoint 1 their
three normal forms have 330, 552, and 714 terms; the middle one is exactly
`c6` times the 552-term bad degree-six remainder.  At endpoint 37 the first
normal form is zero and the other two are exactly plus and minus `ca` times
that remainder.  The exchange identity therefore transports the curvature
to a colon multiple instead of contracting it.

This failure is not repaired by another decorated edge of the same (C_4).
For the first remainder, multiplication by any of

```text
c6 c7 d9 e4 e7 f4
```

leaves all 504 terms unchanged and uses zero reduction steps.  For the
second, the same is true for

```text
c6 ca d9 dc e4 e7 f4.
```

The four (E3) determinants share the factor `09094848`; after division they
are 498-term homogeneous degree-eight cells, and both (E4) tetrahedra remain
literal identities.  Degree eight cannot reduce either homogeneous
degree-six remainder.  Hence the exact conclusion is:

> Alternating-(C_4) exchange supplies the coherent three-cell, but the
> complete lower basis has a nonzero primitive (C_4)-colon class on both
> path-bearing representatives.

Run

```text
python3 computations/verify_n8_chart26_c4_primitive_colon.py
```

with digest
`a5c14aff114eb4dc43e4b10e223d6bcb4571d06fffa8f31190d1821b53f8de36`.

There is an exact cross-chart shadow of the same boundary.  After removing
the eight-variable common factor from the chart-25 four-row integral dual,
the residual monomials

```text
4c62bce5  4d62b8e6  4f5ebce8  5e62b8bc
```

live on vertices ({1,3,5,6}).  The first three use every edge of the
alternating cycle (13,36,56,15); the last is the parallel-pair degeneration
((15)^2(36)^2).  A primitive matching-exchange minor
(Delta^{MN}_{cd}), after its common matching core is removed, has exactly
the first (C_4) skeleton.  The essential parallel term in the chart-25
functional, with coefficient vector ((-2,-1,-1,+1)), is therefore the
diagonal/colon correction not supplied by a genuine (C_4) exchange
minor.  This identifies the same local support mechanism; it does not yet
identify the two chart complexes by a chain isomorphism.

The useful uniform theorem to prove is now precise:

> **Path-forest straightening target.**  After normalizing a support chart,
> the mixed hafnian ideal has a source-labelled Groebner/Morse completion
> indexed by decorated spanning linear forests.  Every new leading monomial
> is the squarefree product of the forest edges; every critical pair reduces
> by fixed-base Koszul simplices and coherent alternating-cycle
> base-exchange cells; collision-only cells admit a terminating exact vertex
> split; and the component count in (7) bounds each forest branch at degree
> \(2h-1\).

Such a theorem would give a finite squarefree degeneration uniformly in
\(h\).  It would still have to be followed by the terminal pure-target
normal-form calculation; radicality alone is not the conjecture.  The open
algebraic point is simultaneous orientability: the degree-six example proves
that a good forest term exists in one cell and is compatible with every
earlier lead, not that all cells admit one common refinement.

## 6. Polarization explains why source labels and Bocksteins are unavoidable

A repeated physical coordinate in a compatibility cell comes from two
different occurrences in the source construction.  Before those occurrences
are identified, replace them by variables \(x_{e,\sigma}\) and
\(x_{e,\tau}\), labelled by their matching/transport slots.  The offending
factor \(x_e^2\) becomes the squarefree product
\(x_{e,\sigma}x_{e,\tau}\).  More generally, the fully source-labelled
straightening complex lives naturally in a polarized ring

\[
 \widetilde R=\mathbb Q[x_{e,\sigma}],
 \qquad
 R=\widetilde R/(x_{e,\sigma}-x_{e,\tau}).                \tag{9}
\]

Upstairs, the path-forest cellular complex can remain squarefree even when
its physical image has collisions.  The difficult step is the diagonal
specialization (9).  A squarefree polarized ideal does not by itself make
that specialization reduced: the elementary polarization
\((x_1x_2,x_1-x_2)\mapsto(x^2)\) is the warning example.  What is needed is
a transverse, source-compatible diagonal specialization, not merely a
squarefree calculation before provenance is forgotten.

The Rees filtration by the differences
\(x_{e,\sigma}-x_{e,\tau}\) records precisely this issue.  Its successive
connecting maps are the Schur--Bockstein transfers computed in chart 25;
cross-star Bianchi identities are candidate null-homotopies for the same
collision classes in chart 26.  If a class is not null-homotopic, splitting
at the physical coordinate gives the exact closed/open alternatives
\(x_e=0\) and \(x_e\ne0\).

The exact homological target is **derived diagonal transversality**.  Write
\(L\) for the sequence of all label-identification differences, let
\(\widetilde M\) be the polarized source module, and let
\(\widetilde C\to\widetilde M\) be its proposed path-forest resolution.  It
is enough for source exactness after depolarization to prove

\[
 \operatorname {Tor}^{\widetilde R}_i
   (\widetilde M,\widetilde R/(L))=0\quad(i>0)             \tag{10}
\]

and to identify
\(\widetilde C\otimes_{\widetilde R}\widetilde R/(L)\)
with the literal physical source complex.  Equivalently, the total complex

\[
       \operatorname {Tot}(\widetilde C\otimes K(L))       \tag{11}
\]

must be acyclic away from degree zero.  Bianchi identities give proposed
homotopies on two-dimensional faces of this Koszul cube; (8) requires
compatible homotopies in every dimension.

There is a minimal warning against stopping at the Bianchi squares.  In
\(S=k[x,y,z]\), the ideal

\[
                         (xy,xz)=x(y,z)                   \tag{12}
\]

is squarefree and has the cellular resolution

\[
 0\longrightarrow S\mathop{\longrightarrow}^{(z,-y)}S^2
 \mathop{\longrightarrow}^{(xy,xz)}S\longrightarrow S/(xy,xz)
 \longrightarrow0.                                      \tag{13}
\]

The overlap closes by the Bianchi cancellation \(xyz-xyz=0\).  Moreover
each of \(x-y\) and \(x-z\) is individually regular on \(S/(xy,xz)\):
neither lies in either associated prime \((x)\) or \((y,z)\).  The pair is
not a regular sequence.  After imposing \(x=y\), the ring is
\(k[x,z]/(x^2,xz)\), where \(x(x-z)=0\) with \(x\ne0\).  After the full
diagonal specialization, (13) becomes

\[
 0\longrightarrow k[x]\mathop{\longrightarrow}^{(x,-x)}k[x]^2
 \mathop{\longrightarrow}^{(x^2,x^2)}k[x],               \tag{14}
\]

whose first homology is \(k[x]/(x)\).  Thus pairwise regularity and every
local boundary square can coexist with higher Tor and a nonreduced physical
quotient \(k[x]/(x^2)\).  Even when (10) holds, it certifies exact source base
change rather than reducedness; radicality or transverse reduced
intersection remains a separate assertion.

This separates the prospective proof into three concrete theorems:

1. construct the polarized path-forest cellular resolution;
2. prove derived diagonal transversality by a coherent contraction of (11),
   using exact vertex splits wherever such a contraction fails; and
3. reduce the pure target in the resulting terminal critical complex.

The first part is graphic broken-circuit combinatorics, the second is the
new source-relative geometry, and the third is the conjecture-specific
normal-form calculation.  This decomposition explains why output-level
hafnian identities alone repeatedly lose exactly the information needed at
higher order.
