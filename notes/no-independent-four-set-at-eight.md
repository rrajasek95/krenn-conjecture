# The live graph has no independent four-set

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.  This does **not** decide
\((8,3)\).

## 1. The theorem

> In any solution of `EqSystemN 8 3`, the live support graph \(L\) — edges
> whose matrix is nonzero — has **no independent set of size four**.
> Equivalently, every \(4\)-subset of the eight vertices contains a live edge.

## 2. Proof

**Step 1, E/O parity.**  For a balanced split \(V=S\sqcup S^c\), every perfect
matching of \(K_8\) uses exactly as many \(S\)-internal as \(S^c\)-internal
edges: \(k\) internal edges consume \(2k\) vertices, leaving \(4-2k\) to cross,
and the cross count read from either side is the same.  Verified with zero
violations over all \(35\) splits and \(105\) matchings, together with the
sharper identity \(\text{cross}=4-2k\).

**Step 2, invisibility.**  If \(S\) is independent, only \(k=0\) matchings
survive, so none uses an \(S^c\)-internal edge either.  Proved through the
general invariant rather than the special case: **dead pair = free edge** is
the edge expansion \(T=A_{uv}C_{uv}+(\text{terms free of }A_{uv})\) with
\(C_{uv}=H_{V\setminus\{u,v\}}(A)\), verified as a formal monomial identity on
all \(6561\) colourings.  Zeroing those cells therefore preserves the tensor
exactly, and the support collapses into a bipartite \(4+4\) graph.

**Step 3, exclusion of bipartite \(4+4\).**  Two independent routes.

*Route A, dependency-free, for any support with at least one dead cross edge.*
Minimum degree three — from the forced incident-edge theorem of
[`slice-cover.md`](slice-cover.md) — makes both endpoints of a dead cross edge
cubic, so every live edge there is an anchor with a distinct far label.  A
one-match colouring collapses a row and column to one live edge each and the
permanent reduces to a \(2\times2\) minor, checked on all \(65536\) support
patterns.  Non-constant fibres then force \(141\) rectangle conditions, and in
all eight constant-fibre cases the rectangle closure fills **all \(36\)** cells
— so no core edge can be an anchor.  Anti-monotonicity of the anchor test is
proved exhaustively, so testing the closure is complete.

*Route B, for the complete \(K_{4,4}\).*
[`k44-coordinate-complement-obstruction.md`](../proofs/k44-coordinate-complement-obstruction.md)
Theorem 2, re-run and UNSAT after 38 CEGAR rounds.  This is the one sub-case
Route A does not cover: at degree four the one-match colouring isolates the
*free* edge rather than an anchor.

## 3. Where \(d=3\) enters, and why the eight-cycle survives

Route A uses \(d=3\) through **minimum degree three**.  The alternating
eight-cycle is a genuine \((8,2)\) solution with independence number \(4\),
bipartite between evens and odds — and minimum degree \(2\).  So the argument
correctly fails to fire at \(d=2\), and the checker verifies that every
necessary condition it uses is *satisfied* there.  That is the sharp boundary
case: the theorem is false at \(d=2\) and the proof knows it.

## 4. A third route, and an honest gap

A parallel study reports \(Q(\mathrm{Per}_4)=2\), which would exclude every
bipartite \(4+4\) support at once, subgraphs included.  Its bridge —
**Proposition 3′**: contracting the right shore of \(H(A)\) with all-ones gives
\((\bigotimes_iM_i)\mathrm{Per}_m\) with \(M_i(e_j)\) the row-sum vector of
\(A_{ij}\) — is **confirmed** here as a formal identity for \(m=3,4\) with
arbitrary non-rank-one matrices and dead edges allowed.  The note's own
Proposition 3, as literally stated, covers only rank-one matrices.

\(Q(\mathrm{Per}_4)\leq2\) itself is **not verified here**.  What was
established independently: each \(M_i\) is surjective; a rank-three restriction
forces every \((2,2)\)-flattening to rank exactly three; and \(\rho=7-c\) with
\(\rho\geq5\) whenever a pair has no shared zero coordinate, over all \(1294\)
conjugacy types.  So a subrank-three restriction needs shared zero coordinates
in each pairing.  That is an audit, not a proof.

**The theorem does not depend on it.**  Steps 3A and 3B suffice, and
\(Q(\mathrm{Per}_m)\leq2\) is strictly stronger than the incidence statement
the chain actually consumes.

## 5. What this does not say

1. Nothing about whether \((8,3)\) has a solution.
2. Route B is cited, not re-proved here, and its audit needs a SAT solver.  A
   dependency-free \(m=0\) proof looks reachable by counting but was not done.
3. The forced incident-edge theorem is taken as proved; only its support-level
   consequence was verified.
4. It says nothing at \(n\neq8\): both the parity count and the subrank input
   are size-specific.

## 6. Audit

[`verify_no_independent_four_set_at_eight.py`](../computations/verify_no_independent_four_set_at_eight.py)
— stdlib only, exact integer and `Fraction` arithmetic, zero bare asserts,
about two seconds, passing `python3`, `-O` and `-I -S`.  **All fifteen injected
mutations raise under both `python3` and `python3 -O`.**  Cross-checked on the
one-dead-edge sub-case by a disjoint code path, with a positive control
confirming the rectangle condition genuinely fires on a configuration that
passes anchors and all constant fibres.

Steps 1 and 2 were independently verified a second time, before this checker
existed, directly from the literal matching tensor.
