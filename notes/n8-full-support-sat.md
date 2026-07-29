# Full support-only SAT encoding at `n=8`

`computations/search_n8_binomial_support_full_sat.py` complements the lazy
search by installing every mixed-fibre structural condition before the first
SAT call.  For target orbit 39 it uses

```text
M0 = 01|23|45|67
M1 = 02|13|46|57
M2 = 03|14|27|56.
```

There are \(3^8-3=6558\) mixed colourings and 105 perfect matchings per
colouring, hence 688,590 term variables.  Every term variable is equivalent
to the conjunction of its four decorated-cell support bits.  Unit-true
target cells are removed from these conjunctions during construction, which
is logically equivalent and improves propagation.  Each mixed fibre is then
constrained to contain zero or exactly two true terms.

## Cardinality encodings

The default `native` encoding introduces two equal activation bits `p,q` per
fibre and posts

```text
atmost(terms + [-p, -q], 2)
atmost([-term for term in terms] + [p, q], 105).
```

If `p=q=0`, the first constraint forces zero terms.  If `p=q=1`, the two
constraints force at most and at least two terms.  The two cases therefore
give exactly the allowed set `{0,2}`.  This encoding was exhaustively checked
on all assignments of six inputs with MiniCard, Gluecard4, CaDiCaL 1.9.5,
and CaDiCaL 3.0.0.

The portable `state` encoding is pure CNF.  Exact prefix predicates record
whether at least one and at least two terms have appeared, and a third term
is forbidden.  It uses 206 auxiliary variables, 825 clauses, and 2,061
clause literals per 105-term fibre.  Exhaustive truth-table testing likewise
confirms that its projections are exactly the assignments of weight zero or
two.

## Cap-24 orbit-39 benchmark

With `--max-cells 24 --symmetry-lex`, the full native formula has:

```text
mixed fibres                 6,558
term variables             688,590
all variables              703,638
ordinary CNF clauses     3,335,423
ordinary clause literals 8,617,759
native at-most constraints   13,117
native at-most literals    1,403,664
```

The seven lex leaders use the full eight-element coloured automorphism group
of the orbit-39 targets and compare only the 252 support bits.  A support
orbit always has a lexicographically least member, so this does not remove a
possible signed or complex-phase solution.

On the current machine, construction took 2.8 seconds and 1.27 GiB peak RSS
with CaDiCaL 1.9.5's BooleanEngine.  The identical MiniCard build took 1.7
seconds and 217.5 MiB peak RSS.  A later uniform characteristic-two parity
argument rules out every structural 0/2 support with pure-fibre sizes
`(1,1,1)`.  The remaining CaDiCaL `at most 24` validation run was therefore
stopped without a solver result so resources could move to the unrestricted
extra-pure chart.

For comparison, the same cap and symmetry with the portable CNF counter has
the exactly calculated size

```text
variables                2,042,492
clauses                  8,736,024
clause literals         22,117,390
```

Clauses are streamed into the backend and never retained as one large Python
list.

## Extra pure matchings and the orbit-40 frontier

`--allow-extra-constants` still forces the chosen target matching in each
pure fibre but no longer forbids the other 104 pure matchings.  This option
requires `--toric` (or the coefficient-free `--structural-only` mode).  For a
consistent mixed Laurent lattice, the full quotient reduction of the product
of the three pure-fibre polynomials decides exactly whether some complex
torus point makes all three constants nonzero.  A zero quotient product
is first minimized to a sufficient subset of mixed exponent rows and pure
colours, then learns a term-level nogood guarding only those mixed pairs and
the exact present/absent state of the retained pure-colour indicators.
Retaining those pairs cannot create a third term under the full 0/2 formula,
and retaining those pure indicators preserves the minimized zero product, so
the obstruction persists.  A nonzero product is reported as
`SURVIVOR TORIC EXACT` and can be normalized to constant coefficients one by
a vertex-zero endpoint-colour gauge.

`--monomial-seed` phases orbit 40 toward its 28-cell diagonal boundary.  The
independent boundary checker finds 38 mixed binomials and 48 odd three-row
integer circuits, each supported on ten cells.  Their guards are installed
before the first SAT call.  Under the full target-independent
\(S_8\mathbin{\times}S_3\) vertex/colour action, they occupy two disjoint
orbits of 30,240 guards each.  Three subsequently discovered and independently
reconstructed schemas add disjoint orbits of sizes 30,240, 60,480, and
30,240; one is genuinely off-diagonal.  All 181,440 ten-cell clauses are
preloaded.  Independent checkers reconstruct the three binomial fibres and
odd relation behind every representative, re-expand and deduplicate all five
orbits, and confirm exact equality with the production preload.

The first dense global checkpoint exposed a further twelve-cell unit
triangle.  Its full `S8 x S3` orbit has 241,920 guards and is disjoint from
the preceding 181,440.  Intersecting those guards with the twelve forced
target cells gives counts `{0:55680, 1:95616, 2:61824, 3:23808, 4:4608,
5:384}`.  The full encoder preloads the complete intersection-at-least-three
slice: 28,800 clauses which reduce distinctly to lengths
`{7:384, 8:4608, 9:23808}`.  This includes the 48 target-automorphism images.
Together with the earlier families, 210,240 triangle guards are present
before solving.  The independent checker reconstructs the three stated
fibres, verifies signs `(-1,+1,+1)` columnwise, and audits the full orbit,
disjointness, overlap histogram, and exact production slice.

A second exact preload couples support bits to pure-term status.  One mixed
exponent row can force the corresponding pure polynomial to vanish on every
mixed-lattice torus point.  The target-pair subfamily has 9,408 schemas:
8,640 guards of size six and 768 of size seven, with 9,264 absent from the
original single-orbit preload.  A four-cycle row actually has three matched
cancellation pairs.  The exact zero pure fibre can be any nonempty union
containing the pair with the forced target term, so its size can be two, four,
or six.  Adding all such unions gives the complete fixed-target one-row
family of 35,328 schemas, with pure-size histogram
`{2:9408, 4:17280, 6:8640}`.

After forced target cells are removed, all 35,328 schema conditions stay
distinct and their guard sizes are `{2:96, 3:3840, 4:31392}`.  The target
pure indicator is itself unit true, so removing its false negative literal
leaves an exact unfactored clause of length 106--108.  The clauses share only
204 exact-pure-fibre conditions: 132 of size two, 36 of size four, and 36 of
size six.  Each is represented once by a 105-literal implication to an
auxiliary trigger, after which every schema clause has length only 3--5,
with histogram `{3:96, 4:3840, 5:31392}`.  Existentially eliminating the
trigger recovers the unfactored clause exactly; exhaustive Boolean truth
tables check this projection.  The independent inverse enumeration starts
from every pair of mixed matchings, proves equality with the production
family, reconstructs all allowed cancellation-pair unions, audits every
exponent-row identity, and independently verifies that each of the 204
exact pure fibres has zero reduced quotient product.

The preserved pre-classification checkpoint
`computations/n8_orbit40_pre_target9408_round6_structural.json` makes the
gain concrete: it has 83 cells, 3,687 exact mixed binomials and pure sizes
`(2,2,2)`.  It hits none of the formerly effective target-compatible old
schemas but hits five of the 9,408-schema target-pair subfamily, with all five exponent
identities independently reconstructed.  `--phase-support` can reuse such a
saved structural JSON only as a solver phase preference while the upgraded
clauses repair its violations.

```text
.venv/bin/python computations/verify_n8_toric_diagonal_triangle_orbits.py
.venv/bin/python computations/verify_n8_toric_additional_triangle_orbits.py
.venv/bin/python computations/verify_n8_full_triangle_orbits.py
.venv/bin/python computations/verify_n8_toric_dense_target_triangle.py
.venv/bin/python computations/verify_n8_toric_one_row_pure_zero_orbit.py
.venv/bin/python computations/verify_n8_toric_all_target_one_row.py
.venv/bin/python computations/verify_n8_sparse_first_triangle.py
```

`--phase-consistent-seed` replaces the 28-cell boundary phase preference by
an independently checked 36-cell support with 94 mixed binomials, pure-fibre
sizes `(24,2,2)`, and a consistent mixed lattice.  Its quotient pure product
is zero; the minimizer finds mixed row 75 alone together with pure colour one,
yielding a 107-literal simplified clause.  In fact the seed contains two hits
from the preloaded one-row orbit, so it is excluded before solving and serves
only as a structural phase preference.  This seed is canonicalized under
target automorphisms when lex leaders are enabled.

## Structural cell ceilings

An uncapped exact 0/2 support automatically has at most 189 cells.  For each
vertex colouring, view the selected decorated cells as the edges of a graph
on eight vertices.  A graph with at least 22 of the 28 possible edges has
more than two perfect matchings: `K8` has 105 perfect matchings, each missing
edge can destroy only the 15 matchings containing it, and six missing edges
leave at least `105 - 6*15 = 15` by the union bound.  Hence every mixed
colouring contributes at most 21 graph edges.

Write `O,D` for the numbers of selected off-diagonal and diagonal decorated
cells.  An off-diagonal cell appears in 729 mixed colourings; a diagonal cell
appears in 728 mixed colourings and one pure colouring.  Double counting gives

```text
729 O + 728 D <= 6558 * 21.
```

Since `D <= 84`, this implies `729(O+D) <= 6558*21+84`, hence
`O+D <= 189` for arbitrary targets.

Orbit 40 sharpens this to 188.  Exactly six mixed colourings have four
forced target edges which themselves form a perfect matching.  Relative to
a fixed perfect matching, the other 24 edges split into six `K2,2` blocks.
A block with no alternating flip has at most two edges, and a block with at
most one flip has at most three.  A graph with at most one alternative
perfect matching therefore has at most `4 + 5*2 + 3 = 17` edges.  Replacing
21 by 17 for those six colourings gives

```text
729 O + 728 D <= 6552*21 + 6*17,
```

and `D <= 84` now rules out 189 cells by three incidences.

An exact fractional cover improves the orbit-40 ceiling further to 180.
Under the 48 target automorphisms, take the following five orbits of mixed
colourings and attach the displayed weight to every member:

| representative | orbit size | weight | local edge cap |
|---|---:|---:|---:|
| `00001111` | 6 | `3/8` | 17 |
| `00122100` | 12 | `1/8` | 21 |
| `01020201` | 12 | `1/4` | 21 |
| `01022010` | 24 | `1/16` | 21 |
| `01101001` | 6 | `1/8` | 21 |

These 60 weighted colourings cover every decorated cell `(u,v,a,b)` with
total weight exactly one.  Summing their valid graph-edge inequalities
therefore has left side exactly `|S|`, while its right side is

```text
6*(3/8)*17 + 12*(1/8)*21 + 12*(1/4)*21
  + 24*(1/16)*21 + 6*(1/8)*21 = 180.
```

Equality at 180 is impossible, so the certified ceiling is actually 179.
If `|S|=180`, positivity of all 60 dual weights forces every displayed local
inequality to be tight.  The 54 cap-21 graphs must then be `K7` plus one
isolated vertex, while each of the six forced-perfect-matching graphs must
have exactly 17 edges and two matching terms.  The equality audit exhausts
all `C(28,7)` minimum matching blockers (exactly the eight vertex stars),
encodes only these necessary local forms in a 6,030-variable, 26,256-clause
CNF, and checks it UNSAT with CaDiCaL 1.9.5 and Glucose 4.2.  A generated
908-addition deletion-free DRUP trace ends in the empty clause; a separate
streaming checker rebuilds the exact CNF and verifies every RUP addition.

Thus an orbit-40 cap of 179 is a redundant consequence of the structural
formula and may help SAT propagation.  The script also accepts
`--no-cell-cap`.  The arithmetic, matching incidences, six special
colourings, `K2,2` block bounds, independently regenerated automorphism
orbits, and exact rational cell cover are audited by

```text
.venv/bin/python computations/verify_n8_structural_cell_ceiling.py
.venv/bin/python computations/verify_n8_orbit40_cell180_equality.py
.venv/bin/python computations/verify_n8_orbit40_cell180_certificate.py
```

The continuing unrestricted portfolio has the following build sizes:

```text
orbit40, cells 28..34, MiniCard, no lex:
  variables=702477, clauses=3572205, literals=10595721,
  triangle guards=210240, pure-zero schemas=35328, triggers=204,
  build RSS=490 MiB
orbit40, cells 28..40, Gluecard4, lex:
  variables=714093, clauses=3641854, literals=10816190,
  triangle guards=210240, pure-zero schemas=35328, triggers=204,
  build RSS=491 MiB
orbit40, cells 28..179 (certified global), MiniCard, lex, replay phase:
  variables=714093, clauses=3641854, literals=10816190,
  triangle guards=210240, pure-zero schemas=35328, triggers=204,
  build RSS=484 MiB
```

Dense global candidates can contain thousands of active binomial rows.  The
full CEGAR loop therefore hashes the rows in their at-most-eight-entry sparse
form and learns one exact unit-triangle symmetry orbit per round.  Each
returned `+/-1` relation is checked columnwise.  If no triangle is found, the
code still runs the exact FLINT/HNF inconsistency core; absence of a triangle
is never treated as consistency.  `--candidate-output` atomically checkpoints
every direct-verified structural model before coefficient analysis.

## Exact outcome semantics

The formula forces the twelve target cells.  By default it forbids every
other constant matching; `--allow-extra-constants` instead represents all
315 pure matching terms exactly.  A decoded structural model is independently
checked by direct enumeration of all \(3^8\) colourings and all 105 matchings.
What happens next is deliberately separated into three modes.

* `--structural-only` prints and records the first direct-verified 0/2
  support, before imposing any coefficient equations.
* `--toric` forms every exponent-difference row and calls the exact integer
  HNF test in `signed_quotient_lattice`.  Inconsistency means that an integer
  dependence has odd coefficient sum.  A sparse relation from the rational
  kernel is used when available.  Otherwise the transformation matrix from
  exact HNF reduction of the augmented lattice guarantees a relation: the
  transformation row producing `(0,...,0,1)` gives an integer dependence
  whose coefficient sum is odd.  The relation is audited explicitly and its
  participating term union is a guarded support cut.  If the lattice is
  consistent, the program checks the pure product with
  `reduced_constant_product`.  For unique pure fibres this product is one
  nonzero monomial.  It then uses an independent SymPy
  Smith decomposition to reconstruct rational phases, converts them to
  powers of one common root of unity, and applies an endpoint-colour gauge at
  vertex zero to make each of the three pure coefficients exactly one.  A
  final integer modular check enumerates all 6,561 colourings and all 105
  matchings before reporting `SAT TORIC EXACT`; the JSON output records the
  root order and exponent of every selected cell.  When extra pure matchings
  are enabled, a nonzero reduced product is instead the exact existence
  criterion; `verify_n8_full_support_solution.py` independently recomputes
  that lattice and quotient-product certificate from the saved support.

Any saved support or root-of-unity solution is checked without SAT by

```text
.venv/bin/python computations/verify_n8_full_support_solution.py OUTPUT.json
```
* The default signed mode solves the opposite-product equations by Gaussian
  elimination over \(\mathbb F_2\), with target-cell signs gauged positive.
  A consistent solution is passed to the original direct signed verifier.

The GF(2) parity cuts in signed mode are valid only for the \(\{+1,-1\}\)
coefficient chart.  They are not used by toric mode and must not be cited as
an exclusion of arbitrary complex phases.  Symmetry images of either kind of
sound core cut are added when lex symmetry is enabled.
