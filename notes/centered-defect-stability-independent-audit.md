# Independent audit of centered defect stability

## 1. Verdict and statement reconstructed

For a graph \(J\), let \(b(J)\) count its bipartite connected components,
including isolated vertices.  A deletion \(v\) is defective when
\(b(J-v)\ge2\), and safe when \(b(J-v)\le1\).

The audited claim is:

> If \(|H|=n\ge7\), \(b(H)\le1\), and \(\delta(H)\ge3\), then at least
> seven vertices of \(H\) are safe.

The claim is **confirmed**.  The reconstruction below does not use the
proof in the primary note.  It also checks the two potentially tight
boundaries: exactly six ordinary non-cut vertices in a nonbipartite
component, and a unique six-vertex bipartite component.

## 2. Independent block accounting

Work first in one connected component \(C\) of minimum degree at least
three.  If \(C\) is 2-connected, all of its at least four vertices are
non-cut.

Otherwise use its block-cut tree.  A leaf block cannot be a bridge,
because the endpoint away from its articulation would have degree one in
the whole graph.  It is therefore a 2-connected block \(L\) with one
attachment \(a\).  Every vertex of \(L-a\)

* has no incident edge outside \(L\);
* has degree at least three in \(L\); and
* remains globally non-cut.

Thus \(|L|\ge4\), and every leaf block contributes at least three distinct
non-cut vertices.  There are at least two leaves, so a connected cut graph
contributes at least six.

Suppose equality is attained.  There are exactly two leaf blocks, each
with three internal vertices.  Those internal vertices have degree three
inside a four-vertex block, so both leaves are \(K_4\)'s.  The block-cut
tree has two leaves and is a path.  An internal 2-connected block would
either add a non-cut vertex or have at least three articulation vertices
and branch the tree.  Hence only bridge blocks can lie between the two
ends.  Moreover, two consecutive internal bridge blocks would give their
common articulation degree two, so minimum degree three permits only the
following equality shapes:

1. the two \(K_4\)'s share their attachment; or
2. their two attachments are joined by one bridge.

Deleting any articulation in either shape leaves a triangle or \(K_4\)
at both ends.  In particular, every resulting side containing an end is
nonbipartite.  Hence an articulation supplies a seventh safe vertex when
the six ordinary non-cut vertices are the only ones available.

This verifies the delicate equality step; merely saying that there are
two leaf blocks would not by itself justify the seventh deletion.

## 3. Bipartite boundary reconstructed

Now let \(B\) be a connected bipartite component of minimum degree at
least three.  In a leaf block, put its unique attachment \(a\) in shore
\(X\).  All vertices of the other shore \(Y\) are internal and have degree
at least three, so \(|X|\ge3\).  A 2-connected bipartite block has a vertex
in \(X-\{a\}\); its degree gives \(|Y|\ge3\).  The leaf therefore has at
least six vertices and contributes at least five non-cut vertices.
A cut bipartite component has two leaves and at least ten non-cut vertices.

If \(B\) has no cut, every vertex is non-cut and each shore has at least
three vertices.  Hence \(|B|\ge6\).  At equality the shores are \(3+3\);
minimum degree three forces every cross edge, so \(B=K_{3,3}\).

It remains to check that one extra safe vertex exists when this unique
bipartite component has exactly six vertices.  Any other component \(C\)
is nonbipartite.  There is a non-cut \(v\in C\) which preserves an odd
cycle:

* if \(C\) has a cut, take an internal vertex of a leaf block different
  from a block containing a fixed odd cycle;
* if \(C\) has no cut, a shortest odd cycle is not spanning, since a
  spanning one has a chord under minimum degree three and that chord cuts
  off a shorter odd cycle.  Take a vertex outside it.

Then \(C-v\) stays connected and nonbipartite.  Deleting \(v\) leaves the
original \(K_{3,3}\) as the sole bipartite component, so \(v\) is safe.
Together with the six vertices of \(K_{3,3}\), this gives seven.

## 4. Global component audit

There are only two possibilities under \(b(H)\le1\).

* If \(b(H)=0\), every component is nonbipartite.  A non-cut deletion can
  make its component bipartite, but it remains connected, so it creates
  at most one bipartite component.  It is safe.  Two or more components
  provide at least \(4+4\) such vertices.  One component provides all
  \(n\ge7\) vertices when 2-connected, at least seven non-cuts when the
  block bound is not tight, and the articulation just constructed when it
  is tight.
* If \(b(H)=1\), minimum degree three rules out an isolated component.
  Let \(B\) be the unique nontrivial bipartite component.  Every non-cut
  deletion in \(B\) leaves exactly one connected bipartite component and
  is safe.  The preceding section gives ten, seven, or the
  \(K_{3,3}\)-plus-one count according to the three possible cases.

Thus at least seven of the \(n\) deletions have \(b(H-v)\le1\), so at most
\(n-7\) are defective.  This is exactly the contrapositive required:
\(n-6\) defective deletions force \(\delta(H)\le2\).

## 5. Translation and quantifier audit

For the global rank-three graph \(R\), a fixed center \(r\), and
\(H=R-r\), the internal graph after deleting the pair \(\{r,u\}\) is
literally \(H-u\).  No edge ranks are recomputed after deletion; this is
an induced-subgraph identity.  The chart defect counts the same objects
as \(b\): nontrivial bipartite components and isolated vertices.  Hence
an (E2) pair in the \(r\)-fan is exactly a defective deletion of \(H\).

With \(n=N-1\), the fan lower bound \(N-7\) is exactly \(n-6\), not
\(n-7\).  Therefore, if all those fan pairs are (E2), either the theorem's
hypothesis \(b(H)\le1\) fails or \(\delta(H)\le2\).  If instead
\(b(H)\le1\) and \(\delta(H)\ge3\), at most \(N-8\) fan vertices can be
(E2), so any good fan of size at least \(N-7\) contains an (E1) pair once
(E3) has been excluded.

Two limitations are genuine and correctly retained:

1. degree at most two is only inside \(R-r\); the selected vertex can
   have degree three in \(R\) through \(r\);
2. when \(b(R-r)\ge2\), graph components alone do not synchronize the
   shore-sign or isolated defect vectors of the overlapping pair charts.

Thus the theorem supplies a centered low-degree/defect synchronization
dichotomy, not by itself a tensor contradiction.

## 6. Sharpness audit

The three guards compute exactly.

* \(K_{3,3}\): \(n=6\), \(b=1\), \(\delta=3\), and all six deletions are
  safe.  The implication would be false at \(n=6\) because the required
  number \(n-6\) of defects is zero.
* \(C_6\sqcup K_3\): \(n=9\), \(b=1\), and \(\delta=2\).  Its six cycle
  deletions are safe, while its three triangle deletions are defective.
  Thus it has exactly \(n-6\) defects at degree two.
* \(K_{s,s}\sqcup K_{s,s}\), \(s\ge3\): \(b=2\), minimum degree \(s\),
  and every deletion is defective.  The initial bound \(b(H)\le1\)
  cannot be omitted.

The independent checker exhausts the full labelled six-vertex boundary
by default and the full labelled seven-vertex case only under the
optional full flag.  Those enumerations audit definitions and constants;
the uniform conclusion is supplied by the argument above.
