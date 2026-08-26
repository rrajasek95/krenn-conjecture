# Rootless fine-Macaulay audit

Status: **UNAUDITED bounded exact PASS; the one-anchor Gröbner strategy is
nonterminal.**  This package constructs the literal triangle cross-word
holonomy, the polarized clean-error coefficient, and their source-labelled
Macaulay exchange closure.  It does not prove ideal nonmembership or the
eight-site conjecture.

## Exact finite block

For the canonical cap pair `67`, triangle `012`, and mixed word
`01211222`, the checker expands the three-slice holonomy determinant `H`
and the coefficient `chi` of `K00*K11*K22` in the clean error.  Over the
pinned prime `32003` it obtains

```text
H terms                                      18,630
direct-free H terms                           9,792
chi terms                                     1,800
RRR-only chi terms                              720
compatible mixed X5 words                       108
degree-nine Macaulay rows                    33,156
degree-nine monomial columns              2,083,914
H terms absent from X5 + 8 chi localizers     11,790
direct-free H terms absent from X5 + RRR       6,552
```

In particular, the raw degree-nine block has literal monomial separators.
The support of `H` and the support of `chi` are disjoint at this degree.
This is a precise manifestation of the three-copy/one-copy mismatch: a
holonomy term chooses three independent residual cofactor matchings, while
a clean-error term comes from one residual matching packet.

## Attempts to repair the mismatch

Multiplying by one whole pure hafnian still leaves respectively `7,488`,
`8,424`, and `2,796` unsupported terms in colours `0,1,2`.  Individual pure
matching monomial charts can remove the support obstruction, so support
alone is not a theorem.  A bounded search over 256 cell-weight term orders
has best uncovered count `10,660`; 112 target terms have a unique mixed-row
divisor, and the three required word rows impose incompatible leading
matching choices.  The resulting unavoidable singleton lower bound is 80.

The first exact source-labelled exchange block has

```text
52,368 rows / 4,578,698 columns,
51,866-row / 4,551,084-column residual core.
```

Four forced boundary columns already quotient to literal clean-error rows,
so the cap attachment is genuinely present; it was not omitted from the
complex.  Saturating every forced pivot and adjoining the corresponding X5
and clean rows remains nonterminal through the configured 64-round bound.
At the last completed stage it has

```text
75,784 X5 rows + 24 clean rows,
6,616,428 columns,
75,388 core rows / 6,611,826 core columns,
420 leaf assignments, and new boundary candidates still present.
```

The large core therefore grows instead of triangularizing.  This does not
prove nonmembership: higher exchange rounds, multiple pure anchors, or a
different localization could still close it.  It does rule out the hoped
short proof in which one pure anchor and the first clean coefficient make a
small Gröbner cone.

## Physical-graph quotient

The companion exact checker forgets endpoint colours only after collecting
the decorated terms.  The `18,630` holonomy terms occupy `2,670` labelled
physical multigraphs, while the eight localized clean rows occupy `110`,
with `74` graph supports in common.  Nevertheless the signed holonomy
projects to the **zero polynomial**: every physical-graph coefficient
cancels.  Hence the obstruction is not a graph-topology class.  It is the
alternating colour holonomy carried by the determinant.  Any useful smaller
quotient must retain that sign/local-system representation; a support graph,
cycle type, or uncoloured matching complex necessarily erases the target.

## Exact colour marginal and the relative obstruction

There is nevertheless a small positive identity after making the opposite
projection.  Identify every physical edge carrying the same ordered endpoint
colour pair, so the source ring becomes

```text
Q[y00,y01,...,y22].
```

The `18,630`-term holonomy becomes a twelve-term degree-nine polynomial (and
degree thirteen after the fixed pure cone matching).  Projecting every mixed
`X5` row gives `5,211` distinct quartics.  Over characteristic zero Singular
finds an exact source lift of the target using only nine of them, with nine
nonzero degree-nine multipliers.  One initially returned word had no
edge-aware lift; deleting that generator still leaves a certificate, now on
the compatible Hamming-shell words

```text
10000000  11111110  12111111  12121111  20000000
21111110  21111111  21112111  22111111.
```

The reduced basis has size `299`, the remainder is exactly zero, and the
identity is checked internally as `matrix(I)*L=T`.  No clean-error generator
is used.  This is a genuine cross-word theorem in the colour marginal, not a
modular screen.

The same nine-row proof does **not** lift after retaining both physical-graph
and global ordered-colour-pair degrees.  Allowing every semigroup multiplier
which lets those rows touch the target gives `49,031` rows of rank `46,073` at
the pinned prime, while the complete `13,974`-term target remains as the
remainder.  The larger first-exchange packet behaves the same way: `48,464`
projected X5 rows, all four forced clean rows, and all `113` abstract clean
shifts touching the target have rank `48,581`, but leave the same remainder.

Together with the physical projection above, this identifies the obstruction
precisely.  It is neither graph topology nor colour algebra separately; it is
the **edge--colour correlation class** between the two marginals.  The next
proof object should be a relative/Čech or coefficient-valued exchange map
which lifts the nine-row colour certificate through that correlation kernel.
Another unlabelled determinant or another one-anchor peeling order cannot see
this class.

The twelve-term colour target itself has the exact factorization

```text
-675*y00^6*y11^2*(2*y12^2+y11*y22)*det((y_ab)_{0<=a,b<3}).
```

Thus the relative class is specifically a determinant/Cauchy--Binet lifting
problem, not an arbitrary residual polynomial.  The nine nonzero source
multipliers are stored explicitly in
`results_colour_only_hamming_certificate.json`; the characteristic-zero
identity and this factorization are both checked inside Singular.

## Normal-jet lifting evidence

Expanding away from the physical-edge diagonal gives the first tractable
positive mechanism in the full labelled direction.  Mark one physical edge
at a time by

```text
A_e[ab] = y_ab + epsilon*z_e,ab.
```

For all `28*9=252` first normal directions, the obstruction obtained from the
nine-row colour certificate reduces exactly to zero modulo the same 5,210-row
colour ideal.  Selecting exact first-order lifts, all `28*45=1,260` same-edge
quadratic products also reduce to zero.  Six adjacent/disjoint and
triangle/cap/outside edge-pair representatives contribute another `486`
mixed quadratic directions, again with zero remainder.  These are exact
characteristic-zero calculations, not modular rank screens.

The recursion also terminates as an actual polynomial identity on several
nonlinear slices.  Numeric adjacent, disjoint, triangle--cap, weighted-cross,
three-edge, and four-edge paths terminate through the homogeneity guard
orders `10..13`.  More strongly, two parameter-valued calculations pass over
polynomial coefficient rings without denominators:

* a four-parameter perfect-matching slice over `Q[u1,u2,u3,u4]`; and
* the complete nine-parameter cap-edge block `A_67`, whose target dependence
  has order four and whose corrections stop after order five.

This does not yet prove full decorated ideal membership: simultaneous normal
directions from all 28 edge blocks remain.  It does, however, replace the raw
Macaulay search by a concrete candidate theorem: **formal exactness of the
colour certificate along the physical-edge diagonal**, equivalently
acyclicity of its coefficient-valued matching-exchange obstruction module.
The bounded checks show vanishing through the complete second normal layer
and exact termination on generic polynomial slices.

## The compact perturbation closure

The lifting rows do not proliferate immediately.  Deterministic exact lifts
of all 252 first normal directions use only 19 word rows: the original nine
and ten new rows.  Retesting the exceptional quadratic remainders adds only
three more words.  Call the resulting packet `closure22`.  Its characteristic
zero Gröbner basis has 28 elements, and its minimal-resolution Betti totals
are

```text
1, 22, 121, 337, 528, 487, 267, 82, 11.
```

Most importantly, this is not an orbit-representative screen.  The checker
constructs every one of the 252 literal edge-cell directions and every
unordered quadratic monomial in them.  All

```text
binomial(252+1,2) = 31,878
```

second-order obstructions reduce exactly to zero modulo `closure22` over
`Q`.  Complete polynomial blocks on `A_67` and on `A_01+A_67` also terminate
exactly.  Thus the small packet is a genuine second-order deformation
closure of the colour certificate.

Greedy order-by-order lifting is not a sound higher-order test, because a
syzygy discarded at one order may be needed later.  The one-shot checker
instead substitutes an entire scalar path and tests the total ideal in
`Q[y00,...,y22,t]`.  Six sparse paths pass exactly in characteristic zero.
For the deliberately dense path perturbing all 252 cells, independent primes
1009 and 1013 both give a 404-element basis and verified degree-nine lifts
(63,512 and 57,449 terms respectively).  Exact modular reconstruction over
`Q`, followed by a sequential characteristic-zero standard-basis check, also
gives a 404-element basis and zero remainder.  Thus even this dense path has
an exact total lift; the earlier order-by-order failure was solely a bad
syzygy-gauge choice.

The local branch can be kept symbolic rather than collapsed to one parameter.
With all 36 entries of `A01`, `A02`, `A12`, and `A67` independent, the target
has parameter order five and the exact recursive identity terminates at order
eleven.  This covers the complete cap block and all three blocks of the
residual triangle simultaneously.

The same coefficient-field calculation scales much farther once every
denominator is audited.  There are **no parameter-dependent denominators** in
any of the following exact lifts; all displayed denominators are ordinary
nonzero rational integers and may be cleared globally:

```text
marked blocks                                      parameters   last check
K5 on {0,1,2,6,7}                                      90          13
all 13 edges internal to the 5|3 shores                117          15
all 15 edges crossing the 5|3 shores                   135          15
```

Thus `closure22` gives polynomial identities on each of the two complementary
shore coordinate subspaces, not merely on generic localizations.  They do not
formally glue: mixed monomials involving both shore packets remain.  A direct
dense bivariate test keeps one parameter for every within-shore direction and
one for every cross-shore direction.  After exact collection the target has
10,132 terms.  `msolve`'s compiled F4 normal-form engine computes a
4,957-element basis over `F_1009` and returns the exact normal form `[0]` in
about 61 seconds.  Adding the hostile constant mutation returns `[1]` with
the same basis profile.  This is a guarded finite-field theorem on the dense
two-plane; it is not yet the full 252-parameter comparison map.

An order-by-order bigraded lift chooses the wrong syzygy gauge and first fails
at total degree four.  As with the earlier dense univariate recursion, this is
not nonmembership: the one-shot F4 calculation proves that another compatible
choice exists.  Future work should therefore retain the whole syzygy module
or use one-shot normal forms, rather than interpreting a greedy obstruction as
geometric curvature.

The successful planes do **not** globalize to the full edge--colour
correlation ring.  An exact square-zero parameter quotient first removes a
computational ambiguity: after adjoining the parameter squares, dead repeated
directions can be discarded during expansion.  The resulting compiled F4
normal forms are zero for deterministic mixed normal planes of ranks three
(`2+1`) and four (`2+2`); the rank-five `3+2` calculation reached the fixed
ten-minute cap and has no verdict.  These are genuine simultaneous normal
tests, but they still aggregate many physical directions.

The next exact quotient retains all 28 labelled physical-edge multiplicities
together with the nine ordered colour-pair multiplicities.  For every
degree-nine semigroup multiplier having a term in the **original target
support**, the complete `closure22` packet gives

```text
translated rows                     128,516
projected rank mod 32003             124,368
coned target terms                    13,974
remainder terms                       13,636
```

Back-substitution produces a functional on only 16 semigroup
columns, with integral coefficients of absolute value at most four.  A second
literal replay over `Z` verifies that it annihilates **all 128,516 rows
exactly**, while its pairing with the coned holonomy target is `1`.  This is a
characteristic-zero separator for the first target-touching layer, not merely
a modular rank screen.

It is **not** a full ideal-nonmembership certificate.  The separator itself
detects translated rows of words already in `closure22` whose supports meet
its 16 columns but not the original target columns.  Those rows arise at the
next exchange round and were deliberately absent from the first-layer
matrix.  Thus the exact conclusion is more useful and narrower: the
low-rank identities require higher exchange closure in the joint
edge--colour grading.  The next computation is an incremental CEGAR closure,
adding precisely the translated rows which cross each successive small
integral separator; adding new X5 word types is necessary only if the existing
22-word exchange component stops.

That incremental closure is now complete in the joint semigroup.  Starting
from the 124,368-dimensional first layer, 24 separator-guided rounds add 533
independent translations of the existing words.  Round 25 has no crossing
translation.  Its terminal functional has support 100 and integral
coefficients of absolute value at most four.  Exhaustive convolution over
**every abstract degree-nine translation of all 22 words** gives zero
pairing, while the target pairing is again `1`.  Therefore this terminal
functional is a genuine characteristic-zero separator even in the enlarged
joint edge/colour semigroup.  In particular, `closure22` alone cannot yield
the universal degree-thirteen identity; at least one new mixed-word type is
mathematically necessary.  The next bounded gate is to classify the new word
orbits crossing this 100-column functional, adjoin the smallest
source-faithful family, and repeat.

There remains an essential provenance guard.  `closure22` lives in the
colour marginal; it is not itself the final anchored 108-word top packet.
The missing theorem is therefore not another low-order reduction but a
source-labelled comparison map carrying this compact deformation complex
through the edge--colour correlation class.

## Consequence for the proof strategy

The clean error attaches, but only after traversing a huge coefficient-valued
matching-exchange component.  The next useful object should therefore be the
smaller adjacent full-nine comparison on the triangle rank strata: it keeps
the fixed channel labels that are erased by both the one-anchor Macaulay
block and the physical-graph quotient.  Its natural language is an
exterior/adjugate comparison of the labelled full-nine matrices, targeting
the remaining common-plane/six-line dichotomy directly.

## Replay and scope

The dependency-free Rust implementation is in `rust-fine/`.  From the
repository root:

```sh
cargo test --release --manifest-path computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/rust-fine/Cargo.toml
cargo run --release --manifest-path computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/rust-fine/Cargo.toml
```

The full run is memory- and time-intensive because it materializes more than
six million monomials.  `KRENN_EXCHANGE_CAP` gives a smaller bounded replay.
All conclusions are exact only for the explicitly constructed finite blocks;
no characteristic-zero ideal membership, radical membership, or global
triangle-branch exhaustion is inferred.

The physical-graph checker is byte-identical under standard, optimized, and
isolated Python modes (stdout SHA-256
`a8d604860272f62a7874f4ec8363cde3885b861764db4bd77e01c73ca33c05ef`).
Its script/result hashes are respectively
`78c370d989f598247a8f38b2fd2f333102ee11f141a7adbac9f941f2aa15eb7d`
and
`8b71f50d1e2adc76c98311dd2a6f3a444fe072f8760166a0ac8c004fd645e3b6`.

The characteristic-zero certificate is replayed by
`audit_colour_only_hamming_certificate.py --check-results`; its stored lift
digest is `c094beb3878a5689d6f33b6ef2b39e9c99807bba54331d9fd96cbbecb12db458`.
The quotient ladder and joint-correlation screen are replayed by
`audit_colour_holonomy_quotients.py --check-results`.

The normal-lifting packet is replayed by

```sh
python3 audit_first_edge_deviation_lift.py --check-results
python3 audit_same_edge_second_order_lift.py --check-results
python3 audit_two_edge_second_order_lift.py --check-results
python3 audit_scalar_path_complete_lift.py --check-results
python3 audit_symbolic_matching_path_lift.py --check-results
python3 audit_symbolic_cap_edge_lift.py --check-results
python3 audit_perturbation_closure_resolution.py --check-results
python3 audit_closure22_full_quadratic.py --check-results
python3 audit_scalar_path_direct_total_lift.py --check-results
python3 audit_scalar_path_direct_total_lift.py --path dense_all_cells --modular-q --timeout 600
python3 audit_symbolic_full_triangle_cap_blocks_lift.py --check-results
python3 audit_symbolic_fivesite_cap_triangle_lift.py --check-results
python3 audit_symbolic_two_shore_internal_lift.py --check-results
python3 audit_symbolic_cross_shore_lift.py --check-results
python3 audit_two_shore_bivariate_msolve.py --check-results
python3 audit_two_shore_bivariate_msolve.py --mutate-target
python3 audit_lowrank_normal_plane_msolve.py --internal-rank 2 --cross-rank 1 --squarezero --check-results
python3 audit_lowrank_normal_plane_msolve.py --internal-rank 2 --cross-rank 2 --squarezero --check-results
python3 audit_closure22_joint_semigroup.py --check-results
python3 audit_closure22_joint_cegar.py --check-results
```

The first, scalar-path, and symbolic checks are also verified under isolated
Python.  The all-edge second-order and six-pair ledgers are deterministic
exact Singular computations but are substantially slower.
