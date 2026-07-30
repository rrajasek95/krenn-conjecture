# Parallel proof attack board after the flat-to-cubic collapse

Audit date: 2026-07-29.

## 1. Current trunk

The conjecture is still open in this workspace, but the uniform structural
frontier is now smaller.  For an exact ternary aggregate source on even
(N\ge8), bad-pair degeneracy and the canonical transition theorem give
one of two outcomes.

1. A physical transition is nonzero.  It supplies a literal curvature
   minor and a generically active cap line.
2. The selected fan is flat.  Every active edge at its low-degree centre
   is bad, hence has a monochromatic pure complementary cofactor.  The
   resulting pure ports can be merged by colour without changing the full
   matching tensor, producing an exact source of the same order with a
   literal cubic centre.

Thus degree four, five, and six are no longer separate flat endpoints.  The
main proof split is

\[
                 \text{curved cap line}\qquad\text{or}\qquad
                 \text{exact cubic source}.                       \tag{1}
\]

The exact clean-pair theorem finishes the conjecture once an active clean
cap is found.  The six-site obstruction finishes an order descent.  Every
attack below is therefore judged by whether it produces a clean cap, an
exact smaller source, or an outright contradiction.

## 2. Highest-value parallel attacks

### A. Couple two curved cap lines

An inactive clean root is no longer an arbitrary bad point.  It exports
either an exact lower-colour effective quadratic or a nonzero nilpotent
packet, with explicit higher jets at a repeated root.  The target theorem
is:

> Two physical curvature lines sharing the complete transverse pair rows
> cannot support only mutually compatible lower-colour or nilpotent root
> packets.

A proof may use a four-site curvature square, a resultant after retaining
the transverse diagonal rows, or incompatibility of the two osculating
ledgers.  Curvature, Bianchi, and good-star injectivity alone are known to
be insufficient, so a valid argument must visibly use the full target
rows absent from the guard.

### B. Close the cubic Hessian packets

For two nonneighbours of a cubic centre, the audited exact dichotomy is:

1. two faithful nullity-at-least-two spaces are visible on the same common
   exterior star and all their cross-Hessian responses land in one tensor
   line; or
2. one colour has the pure (3\times3) two-crossing packet: eight Hessian
   responses vanish and the ninth is a nonzero decomposable target.

The natural theorem-sized targets are a classification of tensor-valued
Hessians with a one-dimensional cross-image, or propagation of two pure
packets across overlapping residual pairs.  Either should force a shared
kernel, a literal sparse star, or a clean selector.  Raw nullity counting
is already guarded and should not be repeated.

### C. Reduce the globally flat cubic network to its boundary core

Choose an entry-minimal exact source and assume every relevant fan is flat.
Every vertex having at least three good neighbours is cubic.  Since the bad
graph is (4)-degenerate, the set (X) of vertices having at most two good
neighbours has size at most seven: inside (X), every vertex has bad degree
at least (|X|-3), whereas an induced subgraph has a vertex of degree at
most four.

Outside (X), each vertex has exactly one diagonal edge of each colour.
The nonzero constant-colour coefficients force those edges to form three
partial one-factors.  An alternating two-colour cycle disjoint from (X)
could be flipped while retaining the same nonzero residual constant-colour
coefficient, producing an uncancellable mixed word.  Hence every such
cycle meets (X).

The next deliverable is to compress the remaining properly three-coloured
cubic multipole to an exact response on the at-most-seven-site boundary,
or to use a boundary-avoiding alternating structure to obtain a mixed
coefficient directly.  The prism-to-Petersen guard excludes scalar
three-edge-colouring invariants; the proof must retain the exact boundary
tensor or the pure complementary cofactors.

### D. Finish the E2 plane-packet boundary

On the dense defect-three chart, a diagonally live rank-two block is now
one of:

1. a glued physical two-plane packet;
2. a complement-sum block;
3. an endpoint-hole collapse.

The complement-sum locus is empty when all three defect components are
imbalanced and equals the constrained universal inactive core when all
three are balanced.  The remaining targets are therefore exact: propagate
an endpoint hole to a sparse row, glue differently labelled plane packets
across their rank-one intersection, or eliminate the one-/two-imbalance
component signatures.  Rank-zero/rank-one blocks and zero diagonals must be
handled separately rather than silently absorbed.

## 3. Independent backup routes

### E. Zero-shore apolar ladder

A growing aggregate-zero shore forces linearly many full internal stars on
its complement and an (O(h))-sparse cross-interface unless curvature
returns.  More strongly, three coordinate monomials lie in one hafnian
ideal with all mixed permanent syzygies, and the common matching power
obeys an exact multiaffine apolar ladder.  A useful next theorem would turn
those syzygies into a multigraded degree or Betti-number contradiction, or
show that one full internal star supplies an active clean cap.  This route
is independent of the cubic classification and becomes stronger with
(N).

### F. Filtered acyclicity of pair-cap overlaps

Physical annihilator corrections on overlapping pair charts satisfy a
literal Koszul-type lift equation before multiplication by the common
power.  Prove that the kernel of this overlap complex is gauge, or else
forces one of the registered sparse/low-rank alternatives.  This would
turn chartwise E1/E2 data into one global cap family.  Mere Bianchi flatness
is not enough; the target is filtered injectivity on the actual Hessian
annihilator module.

### G. Matching-compatible Segre circuits

Kruskal uniqueness already excludes every decorated Wick expansion in its
visible range.  Outside that range, every tripartition forces a short exact
linear circuit among grouped Segre products.  The missing theorem is to
show that a circuit whose terms come from decorated perfect matchings has a
shared physical edge, a tight cut, or a selector cap.  A classification of
arbitrary Segre circuits would be excessive; only circuits stable under the
matching deletion/exchange operations are relevant.

### H. Multi-pair cap incidence

For one pair, cap-space dimension and intersection theory are guarded by
exact dirty root-cover models.  A viable algebraic-geometric version must
use two or more overlapping physical pair-cap spaces and the transverse
target equations on their intersection.  The exact deliverable is a
proper saturated common-zero statement for the joint clean-error ideal,
not a dimension count on one projective cap space.

## 4. Work to deprioritize

The following may still falsify a proposed lemma, but they are not natural
main-line proof work:

* another fixed-order collision census;
* a larger support enumeration around one polarized seed;
* bare curvature/Bianchi identities without transverse target rows;
* raw kernel-dimension or graph-density counts without physical response
  provenance;
* isolated generic-rank computations whose exceptional strata are not
  closed exactly.

The dependency order is therefore (A/B/C) first, (D) as the closest
independent backstop, and (E/F/G/H) in parallel when capacity permits.
