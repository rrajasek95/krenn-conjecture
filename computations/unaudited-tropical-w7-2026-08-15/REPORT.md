# W7 — Route T.1 symmetric-cone closure — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 31cefe2 at start (repo moved to a419499 mid-run; lanes
committing). Exact Fraction/integer arithmetic except two labelled
numerical probes (one re-verified at 60 digits). Agent's report
transcribed here (its write was policy-blocked). Scripts/JSON in this
directory.

## Verdict: Route T falsified as a closing route; retire/re-scope
1. BRIEF PREMISE CORRECTED: the repo does NOT prove the diagonal
   PENCIL system insoluble — notes/diagonal-termwise-census-and-
   pencil-guard.md proves the pencil is soluble for every k>=2. The
   committed insolubility is the TERMWISE system T(k) (proofs/
   diagonal-hafnian-recurrence-obstruction.md, insoluble at n=6,8,10).
   W7's chamber reduction lands on the termwise system verbatim
   (f(c,c)=0 chamber; 1638/1638 splits at N=8) — corroboration.
2. RESIDUAL FAMILY IS 3-DIM (g_ab = f(a,b) - (f(aa)+f(bb))/2) x 27
   diagonal sign patterns. Fan fully enumerated: 183 faces at N=6,
   795 at N=8 (products with sign patterns: 4941 / 21465 cells).
   Independent control reproduces W4's 21-dim no-singleton locus;
   non-symmetric colour forms carry singletons 60/60 (symmetry
   hypothesis load-bearing).
3. SINGLETON CERTIFICATE WORTH NOTHING AT N=8 ON THIS FAMILY: 0/795
   faces (31/183 at N=6). Sharp reason: N=6 content (2,2,2) has
   multiplicity 1; at N=8 no content does (closest (2,2,4) gives 3).
   This is exactly why six sites was tractable.
4. KILL TABLE: 4733/4941 cells closed at N=6, 19907/21465 at N=8
   (751/795 g-faces at gauge-normalised f(c,c)=0). New hand-proved
   torus lemmas: H4 (W symmetric zero-diagonal, N>=6, ALL
   off-diagonal entries nonzero, char != 2,3 => some 4-subset
   hafnian nonzero; Groebner-verified at N=6; char-3 sharpness
   witness), P2 (2+2 permanents), A (anchor collapse). Residue
   concentrated where all three anchors degenerate to 0.
5. FALSIFICATION: at N=6, Theorem A makes T.1 true at EVERY weight,
   yet four residual cones (all f(c,c)<0) carry genuine torus
   solutions of the GENERATOR-LEVEL initial system (60-digit
   verification; box constraint is the discriminating control — the
   singleton cone and w=0 correctly fail). So the GHZ generators are
   NOT a tropical basis: in_w(generators) is strictly smaller than
   in_w(I), and cone-by-cone certificates can never close T.1 at
   generator level. Closing it needs Groebner bases of I itself in
   135/252 variables — not a route.
6. PAYOFF CORRECTED: gauge preserves I on a subtorus of dim 3N-3, so
   Trop(I) contains the lineality L_0 if a full-support solution
   exists; T.1 at w=0 is circular, and T.1 off L_0 yields only
   Trop(I) subset L_0 => V(I) cap T is EMPTY OR A FINITE UNION OF
   GAUGE ORBITS (Bieri-Groves). RIGIDITY, NOT EMPTINESS — a
   full-support counterexample would be isolated mod gauge (useful:
   collides with any positive-dimensional deformation family, e.g.
   trichotomy branch (iii)); the plan's "T.1 empties the stratum" is
   wrong as written.
7. RECONCILIATION WITH CEILING FRONT: "support 28" there counts
   EDGES; densest tested configuration is 51 of 252 CELLS. T.1's
   dense-cell stratum is complementary, untouched. Honest open gap:
   edge-supports {19..27} (no dedicated N=8 notes; floor trail
   reaches 18) + the >=4-off-diagonal-cell and reduced-diagonal
   sub-cases of 28 + the dense-cell interior.
8. SUPPORT RESTRICTION: fan restricts verbatim and singletons get
   STRONGER on smaller supports, but H4/P2 need full support — the
   engine does not compose into a band argument.

## Soft spots
Negative controls numerical; N=8 falsifier analogue untested (dense
6561 x ~690k design flaw, killed); "no solution found" = solver
failure, only the 4 positives count; tied-argmin contents discarded
(sound, lossy); char != 2,3; repo moved mid-run.

## Keep
The exact fan; the termwise-reduction corroboration (with the
pencil/termwise correction); LEMMA H4 (self-contained full-support
obstruction killing the monochrome-favouring chamber at every
N >= 6); the rigidity statement of T.1's true payoff.
