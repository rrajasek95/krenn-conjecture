# Centered deletion defects force a low rank-three degree

## 1. Outcome

For a finite simple graph \(J\), define

\[
 b(J)=\#\{\text{nontrivial bipartite connected components of }J\}
      +\#\{\text{isolated vertices of }J\}.             \tag{1}
\]

Thus \(b(J)\) is simply the number of connected components of \(J\)
which are bipartite, with isolated vertices explicitly included.  Call a
vertex \(v\) of \(J\) **deletion-defective** when

\[
                         b(J-v)\ge2,                    \tag{2}
\]

and **safe** otherwise.

**Theorem 1.1 (centered defect stability).**  Let \(H\) be a graph on
\(n\ge7\) vertices with \(b(H)\le1\).  If at least \(n-6\) vertices of
\(H\) are deletion-defective, then

\[
                              \delta(H)\le2.             \tag{3}
\]

Equivalently, if \(\delta(H)\ge3\) and \(b(H)\le1\), then \(H\) has at
least seven safe vertices.

This is a graph theorem.  In the Krenn reduction, let \(R\) be the global
rank-three block graph and fix the center \(r\) of a good-pair fan.  Put

\[
                         H=R-r,\qquad n=N-1.             \tag{4}
\]

For a fan neighbor \(u\), the internal rank-three graph of the pair
\(\{r,u\}\) is exactly \(H-u\), and its chart defect is \(b(H-u)\).
Consequently, if at least \(N-7=n-6\) fan pairs are in escape class (E2),
then

\[
             b(R-r)\ge2\quad\text{or}\quad\delta(R-r)\le2. \tag{5}
\]

After the uniform elimination of (E3), a good fan has at least \(N-7\)
pairs, each in (E1) or (E2).  The contrapositive gives the useful
three-way export

\[
 \boxed{\ b(R-r)\ge2,\quad \delta(R-r)\le2,\quad
         \text{or the fan contains an (E1) pair}.\ }     \tag{6}
\]

The alternatives in (5)--(6) are centered: a vertex of degree two in
\(R-r\) may still have global rank-three degree three through its edge to
\(r\).

## 2. Block-cut preliminaries

A vertex of a connected graph is a **cut vertex** if deleting it
disconnects that graph; all other vertices are **non-cut**.  We use the
standard block-cut tree, whose block nodes are the maximal 2-connected
subgraphs together with bridge blocks, and whose other nodes are cut
vertices.  A leaf block has a unique attachment cut vertex.

**Lemma 2.1 (non-cut supply).**  A connected graph \(C\) of minimum
degree at least three has at least four non-cut vertices.  If \(C\) has a
cut vertex, it has at least six non-cut vertices.

**Proof.**  If \(C\) has no cut vertex, every vertex is non-cut and
\(|C|\ge4\).  Suppose it has a cut vertex.  Its block-cut tree has at
least two leaf blocks.  A leaf block cannot be a bridge: the endpoint
other than its attachment would have global degree one.  Hence a leaf
block \(L\) is 2-connected.  Every vertex of \(L\) other than its
attachment is globally non-cut, has no incident edge outside \(L\), and
therefore has degree at least three inside \(L\).  Thus \(L\) has at
least four vertices and supplies at least three non-cut vertices.
Two distinct leaf blocks have disjoint sets of such internal vertices,
giving at least six. \(\square\)

The equality case will be needed rather than hidden in the count.

**Lemma 2.2 (the six-non-cut equality case).**  If a connected graph
\(C\) has minimum degree at least three, has a cut vertex, and has exactly
six non-cut vertices, then its block-cut tree has exactly two leaf
blocks.  Both leaf blocks are copies of \(K_4\).  Every cut vertex \(x\)
is safe in the strong sense that every component of \(C-x\) which meets
an end of the block-cut tree is nonbipartite.

**Proof.**  Equality in Lemma 2.1 permits exactly two leaf blocks and
exactly three non-cut vertices in each.  Such a leaf block has four
vertices.  Each of its three internal vertices has degree at least three
inside the four-vertex block, so the block is \(K_4\).

A tree with exactly two leaves is a path.  An internal nonbridge block
would either contain a non-cut vertex, increasing the total beyond six,
or contain at least three cut vertices, making its block node branch.
Thus every block between the two \(K_4\)'s is a bridge.  Minimum degree
also rules out a chain with a cut vertex incident only to two consecutive
bridges; the two end \(K_4\)'s therefore either share their attachment or
their attachments are joined by one bridge.  Deleting any cut vertex
leaves a full \(K_4\), or the triangle obtained by deleting its attachment,
on each surviving end.  Those components are nonbipartite. \(\square\)

For a bipartite component the supply is larger.

**Lemma 2.3 (bipartite supply).**  Let \(B\) be a connected bipartite
graph of minimum degree at least three.

1. If \(B\) has a cut vertex, it has at least ten non-cut vertices.
2. If \(B\) has no cut vertex, then \(|B|\ge6\), and equality forces
   \(B=K_{3,3}\).

**Proof.**  Consider a leaf block \(L\) with attachment \(a\), and write
its shores as \(X\sqcup Y\) with \(a\in X\).  As in Lemma 2.1, it is not
a bridge.  Every \(y\in Y\) is internal and has degree at least three in
\(L\), so \(|X|\ge3\).  There is an internal vertex in \(X\setminus
\{a\}\), and its degree gives \(|Y|\ge3\).  Thus \(L\) has at least six
vertices and supplies at least five non-cut vertices.  Two leaf blocks
supply ten.

If \(B\) has no cut vertex, all its vertices are non-cut.  Each shore has
at least three vertices because the minimum degree is three, so
\(|B|\ge6\).  At equality the shores have size three and every vertex is
adjacent to the entire opposite shore, giving \(K_{3,3}\). \(\square\)

We also need one deletion which preserves an odd cycle.

**Lemma 2.4 (odd-cycle-preserving deletion).**  A connected
nonbipartite graph \(C\) of minimum degree at least three has a non-cut
vertex \(v\) for which \(C-v\) is connected and nonbipartite.

**Proof.**  If \(C\) has a cut vertex, choose a block containing an odd
cycle.  The block-cut tree has at least two leaf blocks, so choose a leaf
block different from that odd-cycle block and take an internal vertex
\(v\) of it.  The vertex \(v\) is non-cut and the chosen odd cycle
survives in \(C-v\).

If \(C\) has no cut vertex, take a shortest odd cycle \(Q\).  It cannot
span \(C\): otherwise minimum degree three gives \(Q\) a chord, and the
two cycles cut off by the chord include a shorter odd one.  Choose
\(v\notin Q\).  The graph \(C-v\) is connected because \(v\) is non-cut,
and it still contains \(Q\). \(\square\)

## 3. Seven safe vertices

Assume throughout this section that \(\delta(H)\ge3\) and \(b(H)\le1\).
There are two cases.

### 3.1 No bipartite component

Suppose \(b(H)=0\), so every connected component is nonbipartite.  A
non-cut vertex of any component is safe: deleting it leaves that component
connected, either nonbipartite or the sole new bipartite component.

If \(H\) has at least two components, Lemma 2.1 supplies at least four
non-cut vertices in each of two components, hence at least eight safe
vertices.  If \(H\) is connected and has no cut vertex, all \(n\ge7\)
vertices are safe.  Finally suppose \(H\) is connected and has a cut
vertex.  Lemma 2.1 gives at least six safe non-cut vertices.  If it gives
seven, we are done.  In the equality case Lemma 2.2 shows that any cut
vertex is also safe: deleting it leaves nonbipartite \(K_4\) or triangle
ends and therefore creates no bipartite component.  This is the seventh
safe vertex.

### 3.2 One bipartite component

Suppose \(b(H)=1\), and denote the unique bipartite component by \(B\).
Minimum degree three excludes an isolated vertex.  Every non-cut vertex
of \(B\) is safe, since deleting it leaves one connected bipartite
component and does not change any nonbipartite component.

If \(B\) has a cut vertex, Lemma 2.3 supplies at least ten safe vertices.
If it has no cut vertex and \(|B|\ge7\), all vertices of \(B\) give the
required seven.  The only remaining case is \(B=K_{3,3}\), of order six.
Because \(n\ge7\), \(H\) then has a nonbipartite component \(C\).
Lemma 2.4 supplies a vertex \(v\in C\) for which \(C-v\) remains connected
and nonbipartite.  The six vertices of \(B\), together with \(v\), are
seven safe vertices.

This proves the contrapositive of Theorem 1.1. \(\square\)

## 4. Translation to the E2 fan

Let \(R\) have the physical sites of an exact projected source as vertices,
with \(xy\in E(R)\) precisely when the aggregate block \(A_{xy}\) has
rank three.  Fix a fan center \(r\).  Deleting a fan neighbor \(u\) from
\(H=R-r\) gives

\[
                    H-u=R-\{r,u\}=G_3(q_{r,u}),        \tag{7}
\]

the internal rank-three graph of that pair chart.  Definition (1) agrees
exactly with the defect \(\nu\) used by the escape-chart theorem: a
nontrivial bipartite component contributes one, and an isolated vertex
contributes one.  Hence an (E2) fan pair is precisely a deletion-defective
fan vertex.

The target-flattening theorem gives a good fan \(F\) with

\[
                         |F|\ge N-7=n-6.                \tag{8}
\]

If every member of \(F\) is (E2), Theorem 1.1 yields (5).  More generally,
when \(b(H)\le1\) and \(\delta(H)\ge3\), at most \(n-7=N-8\) vertices of
all of \(H\) are deletion-defective.  Thus \(F\) contains at least

\[
                         |F|-(N-8)\ge1                 \tag{9}
\]

pair outside (E2), which is (E1) after the uniform (E3) exclusion.  This
proves (6).

Two tensor exports remain, and the graph theorem does not silently claim
either one.

1. **Centered low-degree export.**  From \(\delta(R-r)\le2\), derive a
   contradiction or a support-reducing mixed-equation normal form.  The
   selected site can still have global rank-three degree three via its
   block to \(r\), so an uncentered degree-two lemma is insufficient.
2. **Defect-vector synchronization.**  When \(b(R-r)\ge2\), synchronize
   the defect coefficient vectors across the overlapping pair charts
   \(R-\{r,u\}\).  Component counts alone do not identify their shore
   signs, isolated directions, or the corresponding mixed-cell
   coefficients.

These are algebraic/tensor tasks; neither follows from block-cut
combinatorics.

## 5. Sharp guards

All three hypotheses and constants have simple exact guards.

* **The order threshold:** \(K_{3,3}\) has \(n=6\), \(b=1\), and
  \(\delta=3\).  Since \(n-6=0\), the premise would be vacuous at order
  six.  Thus \(n\ge7\) is necessary as stated.
* **The degree conclusion:** \(C_6\sqcup K_3\) has \(n=9\), \(b=1\), and
  \(\delta=2\).  Deleting any of the three triangle vertices leaves two
  bipartite components, while deleting a cycle vertex leaves only one.
  It has exactly \(3=n-6\) deletion defects, so (3) cannot be strengthened
  to \(\delta\le1\).
* **The initial defect bound:** for \(s\ge3\), two disjoint copies of
  \(K_{s,s}\) have \(b=2\), minimum degree \(s\), and every vertex is
  deletion-defective.  The condition \(b(H)\le1\) is essential.

## 6. Exact audit

The dependency-free checker
[verify_centered_defect_stability.py](../computations/verify_centered_defect_stability.py)
verifies the three sharp guards, both six-non-cut \(K_4\) equality shapes,
the ten-non-cut bipartite leaf boundary, the centered fan arithmetic, and
deterministic graph samples.  Its default run also exhausts all \(2^{15}\)
labelled graphs on six vertices, locating the \(K_{3,3}\) order boundary.

The optional command

    uv run python computations/verify_centered_defect_stability.py --full

additionally exhausts all \(2^{21}\) labelled graphs on seven vertices.
This is an audit of the finite boundary, not the proof of the uniform
theorem; Sections 2--3 supply the latter.
