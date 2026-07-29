# Claude/Codex comparison and integration record

## Repository provenance

The Codex workspace had no Git metadata when this audit began.  It was
initialized as `main` at commit `eeff1f8`, preserving 1,606 tracked research
artifacts and the Codex-only post-snapshot routes.  Claude's repository had
started from an earlier inherited Codex snapshot (`f26e564`) and then added
17 commits.  Those 17 commits were replayed in order; the only conflict was
the pair of append-only living documents
`current-proof-audit-and-next-steps.md` and `route-registry.md`, resolved by
retaining both branches' entries.  Eight adjacent-direction files present in
Claude's inherited snapshot but absent locally were restored separately in
`dadb6ac`.

## Complementary mathematical advances

Claude's strongest new result is the independently audited fan six-port
exclusion: a good pair cannot occupy a regular nonbipartite Hessian chart.
The subsequent escape-chart analysis eliminates defect zero, connected
bipartite, isolated-vertex, and single-edge defect-one charts.  Claude also
added the repaired fixed-interior rank-one branch cover, exact transverse-cap
exclusions plus a one-silent-site countermodel, a self-contained foundation
draft through orders 2, 4, and 6, and a negative census of the four-cell
varied-`q` region at order eight.

The Codex-only delta supplies different guards and provenance constraints:
the induced-zero shore/24-port reduction, an audited abstract 81-row capped
countermodel, an all-even complete-bipartite common-quadratic family showing
that density and pure normalization do not replace mixed GHZ vanishing, and
the cubic common-cofactor-zero boundary blocking a raw
nullity-to-common-kernel inference.  These are complementary to Claude's
exclusions and were retained.

The first new integrated advance closes Claude's sole order-ten defect-one
residual.  All 24 `K_{1,3} + K_4` patterns have a two-vertex deletion with
zero complementary matching power, producing a nine-dimensional block
kernel disjoint from gauge.  The primary and clean-room checkers are
`fan_escape_chart_bipartite_sparse_check.py` and
`audit_fan_escape_k13_k4_n10_independent.py`.

## Claims not promoted

The full upper bound for every even order at least eight remains open.  The
uncommitted `2^4 1^5` sole-plane package in Claude's worktree is not a
certificate: both closure scripts contain unset squeeze constants, the note
contains placeholders, and the chart-1 lift was not reproduced.  Those files
were therefore not imported as a theorem.  The repaired `4336` structural
checker was imported only as a necessary-identity audit; after replacing its
generic determinant expansion it runs in seconds, and its transverse example
has degree 12 rather than the draft's asserted degree 13.

The order-eight varied-`q` result is a scoped negative census, not a uniform
upper bound.  Its combinatorial census has two implementations; the residual
ideal clean-room regeneration is a deterministic 1,709-of-17,078 sample, and
the omitted 75 MB compatible ledger prevents a repository-only replay of one
witness script.  The foundation draft deliberately stops at order six.

## Audit runtime policy

Fast structural replays are the default.  Expensive Gröbner/Hilbert
regeneration must be explicitly requested and must state its expected
runtime.  In particular, the rank-one verifier now checks geometry and frozen
ledger hashes by default (about four seconds); `--full-singular` opts into all
16 characteristic-zero jobs.  Exact identities should be checked through
factored/frame forms instead of expanding enormous generic determinants when
the two arguments are mathematically equivalent.
