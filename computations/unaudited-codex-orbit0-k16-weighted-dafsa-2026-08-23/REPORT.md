# Orbit-zero `K16` weighted decision diagram

## Result

The complete frozen orbit-zero `K16` residual has a compact, exact,
provenance-preserving representation.  Its 1,848,174 sorted literal
factor-stabilizer representatives form an ordinary 17,606,956-node trie.
Exact suffix-language minimization reduces this to a weighted acyclic diagram
with **768,820 nodes and 1,192,523 arcs**.  Terminals retain the rational
coefficient mass; transitions retain all 252 literal cell identifiers and
their multiplicities.

This is a positive symbolic interface, not a membership proof.  It replaces
the 160 MB JSON / 701,717,184 labelled-row expansion as a residual and
coefficient oracle.

## Encoding and exactness

Every monomial is a nondecreasing length-24 byte string.  A state is merged
only when all three data agree:

1. its depth in the 24-label word;
2. its exact rational terminal value, if any;
3. its complete labelled map to already-minimized suffix states.

The binary is bottom-up: every edge points to a lower state ID.  A dynamic
language count at the root replays exactly 1,848,174 accepted keys.  The input
file SHA-256, a separate streamed record SHA-256, and five fixed
row/coefficient samples are checked before and after construction.  Sample
orbit sizes under the exact order-384 factor stabilizer recover literal
coefficients from the stored orbit masses.

The node distribution is strongly concentrated in the middle levels; there
are only 80 weighted terminal states.  The binary file is roughly 21 MB and
is pinned by digest in the result JSON.

## Applying literal source incidence

The diagram supports both directions locally:

- for a source column `(word,U)`, generate its 105 perfect-matching outputs
  and query each sorted 24-label key in 24 transitions;
- for inverse incidence, constrain traversal to keys containing a specified
  four-cell perfect-matching term as a submultiset, then subtract it to recover
  the multiplier `U`.

There is one load-bearing guard.  Terminal coefficients are masses of complete
`H`-orbits, not coefficients of one labelled monomial.  Literal arithmetic
must divide by the exact orbit size, or stay consistently in the orbit-mass
basis.

The diagram contains only the collected nonzero `K16` residual.  It does not
contain zero-residual `K16` rows or the `K12`--`K15` rows required for a sound
lower-kernel closure.  Those must still come from the literal source provider.
Thus the correct next architecture is a lazy source-incidence DFS with this
diagram as the target/coefficient oracle; materializing a Macaulay matrix or
the 701-million-row support remains unnecessary.

## Complete target-incidence pass

The exact Rust inverse-incidence provider streamed all 1,848,174 terminal
representatives and canonicalized every literal mixed degree-24 source column
under the same order-384 factor stabilizer.  It found **98,609,090 distinct
target-touching source-column orbits** in 107.619 seconds.  The count first
exceeded two million at terminal 37,910.  Therefore the mandated two-million
size guard fires before any output expansion or rank calculation.

The provider was checked at two smaller interfaces.  For the lexicographic
`q` row it agrees exactly with the older combinations-of-positions provider:
both return the same 106 literal columns.  On the first 10,000 terminals it
sees 731,859 raw incidences and 647,409 column orbits, agreeing with an
independent Python implementation.  The already-validated lex-`q` provider's
first lower frontier has 7,485 `K<=16` row orbits.  This is a local frontier
control only: expanding a putative full frontier from 98.6 million columns was
deliberately not attempted.

This census is the load-bearing size conclusion.  It is not a statement that
the lower-kernel frontier has 7,485 rows, and it is not a rank or membership
result.

## Source-column language automaton

The complete inverse-incidence union was also compressed without a global
98.6-million-key hash set.  The provider emitted 137,311,379 raw canonical
keys into 69 independently sorted/deduplicated runs (112,332,174 run-local
unique keys), merged them exactly, and minimized suffix languages on the fly.
The resulting column DAFSA has **39,763,164 states and 71,283,240 arcs**.  Its
root language count independently replays all 98,609,090 source-column
orbits.  Generation, external sorting, union, and minimization took 166.085
seconds, inside the 300-second gate.

Each 22-byte key is the two-byte canonical word code followed by the sorted
20-cell multiplier.  The 515,468,936-byte binary is replayed node by node:
all edge labels are strictly increasing, all targets point to earlier state
IDs, the arc count and file length agree, and dynamic language counting at the
root agrees with the merged-key count.  Fixed first/last keys, an accepted
query, and a hostile root-count mutation guard the interface.

Provenance is preserved by the *pair* of automata rather than duplicated in
the column terminal.  Given `(word,U)`, the literal provider emits its 105
matching outputs and queries the original weighted target DAFSA; that returns
the exact target row and orbit mass.  Thus source incidence is local.  The
column DAFSA alone is only a language-membership oracle and must not be treated
as a coefficient matrix.

## Fine grading: exact negative decomposition result

The full target and column languages occupy **one** orbit of the
24-coordinate site-by-colour endpoint grading.  Its representative is

```text
(2,2,2 | 2,2,2 | 2,2,2 | 2,2,2 | 2,2,2 | 2,2,2 | 2,2,2 | 2,2,2).
```

The exhaustive stream covers all 1,848,174 target-row `H`-orbits and all
98,609,090 source-column `H`-orbits.  The latter traversal unfolds
843,704,501 ordinary prefix states from the minimized column DAFSA.  Both
grade supports agree and the sole block has counts `(1,848,174,
98,609,090)`, so every requested quantile equals the corresponding total.
Thus this fine grading does **not** split the incidence problem into smaller
blocks.

For three deterministic column keys (first, middle, and last), all 105
literal perfect-matching outputs were reconstructed; all 315 output grades
equal their column grade exactly.  The exhaustive census took 10.120 seconds.
It stores only grade counts and never expands equation rows or launches rank.

## Cycle-partition quotient: exact separator

The balanced fine grade has a useful second quotient.  Regard its 24
site-colour ports as vertices.  Every degree-24 row is a 2-regular multigraph,
so it maps to its cycle-length partition of 24.  A balanced source multiplier
has degree one at the eight word ports and degree two elsewhere; hence it is
four path components plus closed cycles.  Closing the eight endpoints by the
105 physical perfect matchings gives a cycle-partition vector determined only
by the four path lengths and closed-cycle lengths.

The exhaustive column-language stream realizes 811 multiplier profiles.
Three first/middle/last literal columns were expanded as controls: for all
315 completions, the literal cycle-partition counter equals the abstract
profile vector.  The weighted target DAFSA has 118 nonzero cycle partitions;
its coefficients were summed as exact rational `H`-orbit masses, not as one
representative's labelled coefficient.

The projected target is **outside** the exact rational source span.  At both
primes 32003 and 32009, the 811 realized profiles have rank 252, while the
complete 1,162-profile abstract family has rank 271 and adjoining the target
raises it to 272.  The load-bearing characteristic-zero result is an explicit
77-partition integer dual (maximum coefficient 2,956,800): it annihilates all
1,162 abstract four-path/cycle completion vectors exactly over the integers,
but pairs with the orbit-mass target as `-311258112`.

The 1,162-profile replay is the soundness guard for the standalone `K16`
polynomial.  The target-touching language
misses 351 combinatorially possible profiles, but the exported dual kills them
too.  Consequently it kills every literal balanced degree-24 mixed source
column, whether or not that column touched the frozen residual support.  A
column in another fine grade pairs trivially with this balanced-grade
functional.

There is a decisive conservation guard.  The original structured polynomial
`a*T` is the product of the three anchor base matchings with three independent
105-term pure perfect-matching sums.  Its cycle vector is computed without
expanding the `105^3 = 1,157,625` terms: the one-colour base-plus-matching
vector is convolved three times.  It has support 30 and pairs with the 77-term
dual as **zero**.  Therefore the dual proves only that the frozen collected
`K16` residual, viewed as an exact polynomial, is outside the degree-24 mixed
source span.  It does **not** prove `a*T` or the full localized target is
outside.  In the prior filtered congruence, omitted `K17`--`K24` tails must
carry charge `+311258112`, cancelling the residual's `-311258112`.  This is
not by itself a statement about the full localization or the other 30 charts.

## Spectral-sequence charge migration: frozen-interface blocker

The natural next audit was to carry this charge, and preferably the full
49-dimensional cycle-quotient normal form (`320 - 271 = 49`), separately
through `K16,...,K24`.  The frozen K14-to-K16 provider does not expose that
stream.  Its source code explicitly retains only the twelve K2 tails of each
mixed singleton pivot,

```python
tails = tuple(term for term in terms if F.row_k_degree(term) == 2)
```

and serializes only the collected irreducible K16 residual.  In contrast, the
audited full mixed-word K profile is `K0:1, K2:12, K3:32, K4:60` for each of
the three colour factors.  The cutoff-8 certificate (236 nonzero source terms)
and telescoping identity certify the full congruence abstractly, but no frozen
artifact iterates the complete `R=T-S` layers K8--K12, all K2/K3/K4 terms of
`E0 E1 E2`, and the chosen pivot tails into a collected K16--K24 residual.

Thus conservation gives one exact terminal fact: the omitted K17--K24 layers
have aggregate cycle charge `+311258112`.  Their distribution by K-degree and
their 49-dimensional normal-form vectors are **not determined** by the frozen
interface.  Computing them would require a new broad factorized reconstruction,
which was outside this bounded audit.  The replayable interface audit records
the four exact iterator/provenance fields required for that future stream.

## Refined `(K-degree, cycle partition)` abstract quotient

The bounded fallback retains the multiplier anchor count, the eligible subset
of the four base-pair completion edges, and records output coordinates by
`(K-degree, cycle partition)`.  This refinement does **not** separate the
structured target even at the abstract-profile level.  There is an exact
14-profile positive certificate.

For each fixed ordered pair of pure matchings `(M1,M2)`, regard
`a*H_{M1}*H_{M2}` as a degree-20 abstract multiplier and the remaining pure
matching as the 105 completions.  Its four paths are the four base-pair edges,
each of length one; all four base completion edges are eligible anchors;
the multiplier anchor count is `12 + |M1 intersect Mbase| + |M2 intersect
Mbase|`; and the closed cycles are the two partitions of `Mbase union Mi`.
Grouping the `105^2=11025` ordered pairs produces only 14 refined profiles.
Their 105-completion vectors sum **exactly** to the 30-coordinate structured
`a*T` vector, including every K-degree coefficient (total `105^3=1157625`).

Therefore no functional that annihilates the entire sound abstract profile
superset can separate `a*T` in this refined quotient.  This is not literal
mixed-ideal membership: the audit does not prove that the 14 abstract profiles
are jointly realized by actual mixed-word columns.  A source-faithful refined
column census would be the next interface, but the requested abstract gate has
already failed and no 98.6-million-column rescan was launched.

## Coloured-necklace refinement: exact diamond no-go

A still finer target-rooted experiment retains the cyclic port-colour word of
each 2-regular component, canonicalized up to rotation and reversal.  A valid
abstract relation cuts four cycles at collectively mixed-colour endpoints and
sums the 105 perfect-matching completions; the unique four-cycle term is
oriented toward terms with fewer cycles.  The structured target has 125
initial coloured states and mass `105^3`.

The signed exact replay is terminally **negative as a separator construction**.
A deterministic choice of cuts reaches 14,848 states and a 10,354-coordinate
normal form, but the second distinct alternative-cut relation already gives a
nonzero terminal diamond.  The first counterguard is the state

```
00 . 00 . 11112222 . 000011112222
```

using all four cycles, with alternative cuts `(0,0,0,1)` versus the canonical
cut.  The two exact reduced right sides have supports 19 and 20 and are unequal;
both are exported literally in the result JSON.  Thus the oriented reduction
is not confluent, its nonzero deterministic normal form is not a functional on
the full abstract relation quotient, and inverse parents would be load-bearing
even if the forward diamonds had passed.  No coloured-necklace nonmembership
claim follows.

An earlier intermediate `110592 * (0^8 . 1^8 . 2^8)` value is retracted: it
was caused by Python `Counter += Counter()` retaining only positive
coefficients.  The frozen script uses an explicit signed nonzero filter, and
standard, optimized, and isolated replays all reproduce the 10,354-coordinate
normal form and the same second-relation diamond.

### Bounded critical-pair quotient

The corrected target normal vector was next reduced against the terminal
differences of alternative-cut relations in its reached downward closure.  A
single sparse `p=32003` gate stopped at the 235-second cap after 678 processed
states and 106,948 cut choices.  It found 4,310 distinct nonzero critical
relations, of modular rank 4,046 with 1,587,294 basis nonzeros; the normal-form
provider had expanded to 44,185 memoized states.  The target remainder was
still nonzero, with support 10,353 versus the original 10,354.

This is strictly **unresolved**.  The nonzero modular remainder is only evidence
inside the reached downward closure and is not a separator; inverse parents and
unreached critical components remain outside it.  Conversely, no modular zero
landed, so there was no characteristic-zero certificate to replay and no valid
retirement of the entire coloured-necklace quotient.  The 4,046 selected
independent relation rows are exported by exact source state/cuts/support/pivot
labels for a resumable implementation.  The lightweight verifier checks their
digest and the bounded-result logical hash; it does not rerun discovery.

## Scope

This represents one frozen canonical `H`-equivariant reduction on the
orbit-zero anchors-one chart.  It is not pivot-independent, does not establish
filtered membership or localization, and says nothing about the other 30
charts.

## Replay

```sh
python3 build_k16_weighted_dafsa.py
python3 -O build_k16_weighted_dafsa.py
python3 -I -S build_k16_weighted_dafsa.py
python3 build_k16_weighted_dafsa.py --mutate  # must fail
python3 verify_k16_source_incidence_result.py
python3 -O verify_k16_source_incidence_result.py
python3 -I -S verify_k16_source_incidence_result.py
python3 verify_k16_source_incidence_result.py --mutate  # must fail
rustc -O verify_k16_column_dafsa.rs -o /tmp/verify_k16_column_dafsa
/tmp/verify_k16_column_dafsa
/tmp/verify_k16_column_dafsa --mutate  # must fail
rustc -O census_k16_fine_grades.rs -o /tmp/census_k16_fine_grades
/tmp/census_k16_fine_grades
/tmp/census_k16_fine_grades --mutate  # must fail
python3 verify_k16_fine_grade_census.py
python3 -O verify_k16_fine_grade_census.py
python3 -I -S verify_k16_fine_grade_census.py
python3 verify_k16_fine_grade_census.py --mutate  # must fail
rustc -O census_k16_cycle_profiles.rs -o /tmp/census_k16_cycle_profiles
/tmp/census_k16_cycle_profiles
python3 solve_k16_cycle_partition_quotient.py
python3 -O solve_k16_cycle_partition_quotient.py
python3 -I -S solve_k16_cycle_partition_quotient.py
python3 solve_k16_cycle_partition_quotient.py --mutate  # must fail
python3 audit_k16_cycle_charge_migration_interface.py
python3 -O audit_k16_cycle_charge_migration_interface.py --verify
python3 -I -S audit_k16_cycle_charge_migration_interface.py --verify
python3 audit_kcycle_abstract_refinement.py
python3 -O audit_kcycle_abstract_refinement.py --verify
python3 -I -S audit_kcycle_abstract_refinement.py --verify
python3 audit_kcycle_abstract_refinement.py --mutate  # must fail
python3 audit_coloured_necklace_target_reduction.py
python3 -O audit_coloured_necklace_target_reduction.py --verify
python3 -I -S audit_coloured_necklace_target_reduction.py --verify
python3 audit_coloured_necklace_critical_span.py  # bounded 235-second gate
python3 verify_coloured_necklace_critical_span_result.py
python3 -O verify_coloured_necklace_critical_span_result.py
python3 -I -S verify_coloured_necklace_critical_span_result.py
python3 verify_coloured_necklace_critical_span_result.py --mutate  # must fail
```
