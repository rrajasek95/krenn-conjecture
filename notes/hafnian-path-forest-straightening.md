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

For a spanning edge multigraph \(F\), put

\[
 d(F)=\left(
  \sum_e(m_e-1),\quad
  |E(F)_{\rm simple}|-|V(F)|+c(F),\quad
  \sum_v\max(0,\deg_F(v)-2),\quad
  c(F)
 \right),                                                \tag{4}
\]

where \(c(F)\) is its number of connected components.  The first three
entries measure parallel excess, cycle rank, and branching excess.  On the
zero-defect stratum, a legal endpoint join changes only
\(c(F)\mapsto c(F)-1\).

Starting with a perfect matching, at most \(h-1\) legal joins are possible:

\[
 hP_2\longrightarrow P_4+(h-2)P_2\longrightarrow\cdots
 \longrightarrow P_{2h}.                                \tag{5}
\]

Therefore any straightening system which always chooses a zero-defect join
terminates by homogeneous degree \(2h-1\).  This is a genuine well-founded
statistic, rather than a guessed degree cap.  It is only the combinatorial
part of the desired theorem: a single additive term order must still orient
all simultaneously active algebraic cells toward those legal joins.

## 5. Why Pluecker and Bianchi are the expected complete overlap list

Two legal component joins are either disjoint or share a path component.
Disjoint joins commute.  Joins using the same star give the already proved
Pluecker/Eagon--Northcott relations, and changing a colour row gives the
three-colour Koszul relation.  Joins based at two different vertices give
the cross-star Bianchi square.  These are exactly the local diamonds in the
poset of spanning path forests.

This suggests a cellular straightening complex whose cells are decorated
path forests, with boundary given by deleting join edges.  The formal
identity \(\partial^2=0\) is the Bianchi cancellation.  The geometric split
at a repeated coordinate is then the deletion--localization analogue of the
ordinary deletion--contraction recurrence for a graphic matroid.

The useful uniform theorem to prove is now precise:

> **Path-forest straightening target.**  After normalizing a support chart,
> the mixed hafnian ideal has a source-labelled Groebner/Morse completion
> indexed by decorated spanning linear forests.  Every new leading monomial
> is the squarefree product of the forest edges; every critical pair reduces
> by a disjoint-commutation, Pluecker/Koszul, or cross-star Bianchi cell; and
> the component count in (4) bounds the completion at degree \(2h-1\).

Such a theorem would give a finite squarefree degeneration uniformly in
\(h\).  It would still have to be followed by the terminal pure-target
normal-form calculation; radicality alone is not the conjecture.  The open
algebraic point is simultaneous orientability: the degree-six example proves
that a good forest term exists in one cell and is compatible with every
earlier lead, not that all cells admit one common refinement.
