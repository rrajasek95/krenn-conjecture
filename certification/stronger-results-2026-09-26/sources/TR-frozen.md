# Cubic scalar triangles are impossible at every order

**Status:** new all-order research proof, 2026-09-20, by
`/root/scalar_pencil_coupling`, following `/root`'s triangle cofactor
observation. Independent audit pending. No existing frozen or canonical
file was changed. The general Krenn--Gu conjecture remains open.

## 1. Actual scalar hypothesis and conclusions

Let M be a complex symmetric zero-diagonal matrix on an even vertex set
V. Let C be its ACTUAL zero-diagonal hafnian cofactor matrix:

    tau = haf(M) != 0,
    C[u,v] = haf(M[V without {u,v}])  if u!=v,
    C[u,u] = 0.

Assume the exact scalar identity

    M C = tau I.                                             (1)

The graph G has edge uv precisely when M[u,v]!=0. Graphs are simple;
there are no loops. Hafnians are unsigned matching sums, with value one
on the empty set and zero on odd sets. All cancellations are retained.
Every use of a cofactor below refers to this one actual M.

**Theorem.** No triangle of G can have all three of its vertices of
degree exactly three. Consequently every cubic component of G is
triangle-free, at every order.

There is a stronger intermediate conclusion. If two adjacent cubic
vertices p,q have a common neighbor r, then

    M[p,q] C[p,q] = tau,

and the cofactors on their other four incident edges are zero. This
does not assert that those four original edge weights vanish. It is
a statement about actual cofactor values, not termwise matching support.

These scalar conclusions require no other color, positivity, minimum
source, or restriction on the degrees of vertices not specified.

## 2. Any cubic vertex annihilates all cofactors between its neighbors

Let p have exactly the neighbors r,s,t, with corresponding nonzero
weights a,b,c. Put

    H_p=haf(M[V without {p,r,s,t}]).

In C[s,r], the retained p has only t available, so C[s,r]=c H_p.
In C[t,r], it has only s available, so C[t,r]=b H_p. The r-th entry
of row p in (1), using C[r,r]=0, is therefore

    0=(M C)[p,r]=b C[s,r]+c C[t,r]=2bc H_p.                   (2)

Both b,c are nonzero, so H_p=0. Expanding the three cofactors between
neighbors at their retained vertex p now gives

    C[r,s]=c H_p=0,
    C[r,t]=b H_p=0,
    C[s,t]=a H_p=0.                                         (3)

This includes the four-vertex boundary: then H_p=haf(empty)=1, so
(2) already excludes a scalar cubic vertex under (1). No negative-order
hafnian or limiting argument is used.

## 3. Two adjacent cubic vertices on a triangle have one nonzero incident cofactor

Let p,q be adjacent cubic vertices and r a common neighbor. Write

    N(p)={q,r,s},       N(q)={p,r,t},
    a=M[p,q], b=M[p,r], c=M[p,s],
    d=M[q,r], e=M[q,t].                                    (4)

The vertices s,t lie outside {p,q,r}. They may coincide. All five
displayed weights are nonzero. Equation (3) at p and q gives

    C[q,r]=C[q,s]=C[r,s]=0,
    C[p,r]=C[p,t]=C[r,t]=0.                                 (5)

If s=t, (5) already makes the cofactors on all four edges other than
pq zero. The diagonal p equation of (1) then gives a C[p,q]=tau.

Suppose next that s!=t. The following identity holds for actual
cofactors from ANY matrix with the two specified cubic rows, even
without (1):

    (M C)[p,t] = 2a C[q,t].                                (6)

To check it, define

    H_1=haf(M[V without {p,q,r,t}]),
    H_2=haf(M[V without {p,q,s,t}]).

In C[r,t], the retained q must match p, giving C[r,t]=a H_1.
In C[q,t], the retained p can match r or s, giving

    C[q,t]=b H_1+c H_2.

Finally C[s,t]=a H_2. Indeed, after deleting s,t the vertices p,q
each have only the other one and r available. If p matches r, q has
no available partner; thus p and q must match each other. This argument
does not restrict the other neighbors or degree of r. Therefore

    (M C)[p,t]
       =a C[q,t]+b C[r,t]+c C[s,t]
       =a(b H_1+c H_2)+ab H_1+ac H_2
       =2a C[q,t],

proving (6), with the exact unsigned factor two.

Since p!=t, (1) and a!=0 imply C[q,t]=0. Interchanging p,q in the
same argument gives C[p,s]=0. Together with (5), all four cofactors
on incident edges other than pq vanish. The diagonal equation at p
now reads

    tau=a C[p,q].                                          (7)

The diagonal equation at q gives the same value. In particular the
shared edge pq has a nonzero actual cofactor even though the other
incident edges remain present in M.

## 4. A third cubic vertex gives an immediate contradiction

If the common neighbor r is also cubic, both p and q belong to N(r).
Equation (3) applied at r gives C[p,q]=0. This contradicts (7) because
tau!=0. It proves the theorem for any triangle all of whose vertices
are cubic, irrespective of every other degree or edge in the graph.

Equivalently, a triangle in such a scalar matrix must have at least
one vertex of degree different from three. The previously reviewed
scalar degree lemma says that degree two is impossible and a degree-one
vertex belongs to an isolated edge. Thus every possible triangle must
contain a vertex of degree AT LEAST FOUR.

## 5. Consequence for the actual full ternary problem

The reviewed global theorem supplies hypothesis (1) for each original
same-color matrix M_h of a full ternary source. The reviewed strict
degree bound says deg_h(v)<=n/2-2 for every n>=6. The reviewed scalar
degree lemma gives only degree one or degree at least three, with
degree-one vertices confined to isolated matching edges.

Thus at n=10 every individual color graph is a disjoint union of
isolated matching edges and TRIANGLE-FREE cubic components. More
generally every cubic color component at any source order is
triangle-free. The conclusion concerns one color graph at a time;
it does not assert that the physical union of the three color graphs
has no triangles.

No bipartiteness conclusion follows here: an odd cycle of length at
least five has not been excluded by this argument. Nor is a degree-four
vertex on a triangle excluded. No source reduction, universal useful
configuration, or general nonexistence result is claimed.

## 6. Verification and provenance

The cubic-triangle proof in Sections 2--4 is self-contained given the
actual scalar hypothesis. The degree-at-least-four corollary also uses
the reviewed scalar degree lemma. The inventory
`cubic_scalar_triangle_dependencies.json` records the exact reviewed
source and audit hashes for that corollary and Section 5.

The bounded standard-library checker `verify_cubic_scalar_triangle.py`
checks the cofactor expansions (2), (3), and (6) as exact integer
identities on deterministic matrices at orders 6,8,10,12. It also
checks the elementary forced-matching expansion of a triangle with
three distinct exterior neighbors. These examples do not satisfy (1)
and are not claimed to be sources; they test the expansion conventions
and factor two. They are not a census or a proof by finite enumeration.

The existing eight-vertex scalar conference example remains a valid
cubic scalar control: it is triangle-free. This theorem does not
contradict that reviewed exact example.
