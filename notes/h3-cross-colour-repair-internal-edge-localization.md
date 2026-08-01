# Where a cross-colour star-sector repair would have to put its mass

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.

## 1. Outcome

The [star-sector trade](h3-star-sector-anchor-terminal-class-trade.md) closes
the star-sector repair of the audited seven-row guard for **monochromatic**
internal quadratics, and records the cross-colour case as open.  This note
does not close it either, but cuts it down to a named place.

Free, on top of the frozen colour-2 slice: nine direct scalars, seventy-two
colour-0/1 star entries, thirty monochromatic colour-0/1 internal edges, and
the ninety cross-colour internal edges — \(201\) unknowns, \(6438\) nonzero
equations of the \(9\times729\).  Write \(q(x@a,y@b)\) for the internal edge
\(\{x,y\}\) carrying colour \(a\) at \(x\) and \(b\) at \(y\).

Three results, all proved by formal identity or exhaustive split:

**C1.  The trade note's "only eight unknowns" is an artefact of its
propagation rule, not of the system.**  That rule absorbs only equations
reducing to a single repeated variable.  Full elimination of the degree-one
equations forces **twenty** cross-colour edges to zero and leaves exactly two
relations,
\[
 q(2@2,4@c)+q(3@2,4@c)=0\qquad(c=0,1).
\]
The twelve extra zeros are \(q(x@c,2@2)\) and \(q(x@c,3@2)\) for
\(x\in\{0,1\}\), and \(q(2@2,5@c)\), \(q(3@2,5@c)\), for \(c\in\{0,1\}\).

**C2.  The trade survives, as a fifteen-word family in each sign.**
Exhaustively over all \(729\) words,
\(\operatorname{Row}(0,1,w)+\lambda\operatorname{Row}(0,2,w)
=(d_{01}+\lambda d_{02})\operatorname{haf}_w(q)\)
holds for exactly fifteen words at \(\lambda=+2\) and fifteen at
\(\lambda=-2\).  Since a nonzero \(\chi\) on either admissible cap forces
\((d_{01},d_{02})\neq(0,0)\), at least one of \(d_{01}\pm2d_{02}\) is nonzero and the whole corresponding family of
hafnians must vanish.  Reduced by C1, each family is six single monomials:

* \(d_{01}+2d_{02}\neq0\ \Longrightarrow\ q(2@c,3@2)=0\) and
  \(q(2@c,5@2)\,q(2@2,4@{c'})=0\);
* \(d_{01}-2d_{02}\neq0\ \Longrightarrow\ q(2@2,3@c)=0\) and
  \(q(3@c,5@2)\,q(2@2,4@{c'})=0\),

for all \(c,c'\in\{0,1\}\).  In particular a cross-colour completion keeping
the edge \(\{2,3\}\) live in **both** orientations has \(\chi=0\).

**C3.  Localization.**  An exhaustive branch search closes the whole
\(9\times729\) cross-colour system under one hypothesis: *every internal edge
carrying colour 0 or 1 at site 2 or at site 3 against a colour-2 partner
vanishes* — twenty of the ninety cross unknowns, none of them already forced
by C1.  So

> any cross-colour completion of this slice must put **some** of its
> \(2\)-mixed internal mass on an edge whose non-\(2\) colour sits at site
> \(2\) or site \(3\) — at least one of those twenty edges is nonzero.

Those are exactly the two sites carrying no colour-2 internal edge and
carrying the guard's stars \(p_2=z_2+z_3\), \(s_1=z_2-z_3\).  The
monochromatic infeasibility is the special case where all ninety vanish; the
intermediate hypotheses "all sixty \(2\)-mixed vanish" and "all thirty-six
\(2\)-mixed incident to \(\{2,3\}\) vanish" also close and are implied.

## 2. What remains open, and what defeated it

The unconditional cross-colour case.  The methods tried and their failure
modes, recorded so they are not repeated:

* **Branch search** with full Gaussian closure, monomial-factor splitting and
  nonzero propagation: over \(300{,}000\) nodes, no solution leaf, but tens of
  thousands of *undecided* leaves at depth \(40\)–\(55\) where every remaining
  variable has been declared nonzero and \(10\)–\(60\) polynomial equations
  remain.  The method is not a decision procedure there.
* **Linearization** (monomials in the linear span, plus degree-raised
  products): \(88\) forced monomials at the root, no leaf closed.
* **Gröbner bases** over a finite field: no termination within twenty minutes
  on the full system or on the two-colour subsystems.
* **Two-colour restrictions** \(\{0,2\}\), \(\{1,2\}\), \(\{0,1\}\), which are
  necessary sub-conditions: none decided.  The \(\{0,1\}\) restriction carries
  no frozen data at all and linearization finds no forced monomial in it.  So
  **no single two-colour restriction can carry the obstruction** — any
  obstruction here is genuinely three-colour.

The specific sub-case that defeated the search: all four \(q(2@\cdot,3@\cdot)\)
orientations dead, so that C2 says nothing about the edge \(\{2,3\}\), but
\(2\)-mixed edges from sites \(2,3\) to \(\{0,1,4,5\}\) live, with
\(d_{01}\neq0\).  Its residual is \(5800\) equations in \(155\) unknowns.

The figures in this section come from exploratory runs and are **not**
reproduced by the checker; of them only the \(5800/155\) residual is
recomputable from the shipped model.  No search at any point returned a
feasible point.

## 3. Audit

The dependency-free checker
[`verify_h3_cross_colour_repair_internal_edge_localization.py`](../computations/verify_h3_cross_colour_repair_internal_edge_localization.py)
validates its model two ways — it reproduces the committed guard ledger at the
guard point, and specialized to monochromatic edges it reproduces the
committed thirty-two forced zeros and the collapse to
\(\{04,05,14,15,23\}\) — and then verifies C1 by exact elimination, C2 by
exhaustion over all \(729\) words in both signs, and C3 by an exhaustive
branch search over \(106\) nodes, with no solution leaf and no undecided leaf.
Node counts depend on the branch ordering and are regression tripwires, not
invariants: an independently written implementation closes the same system in
\(64\), \(98\) or \(3217\) nodes depending on the rule, always with no
surviving leaf.  Standard library only, exact
arithmetic, about six seconds, passing normal, `-O` and `-I -S`,
byte-identical across five hash seeds.

C1 was independently re-derived: the cross-colour system has exactly twenty-two
homogeneous degree-one equations in twenty-four variables, of full rank
twenty-two, giving twenty eliminated variables and the two displayed
relations.
