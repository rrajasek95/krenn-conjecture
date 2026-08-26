# Recursive C4-boundary descent: exact support no-go

Date: 2026-08-23  
Status: `SUPPORT_RECURSION_FALSE_COEFFICIENT_FEASIBILITY_UNRESOLVED`

## Verdict

The proposed recursive lemma is false at the support/literal-incidence level.
The first chart-1 boundary admits an explicit dense support on which the
normalized base chart is an isolated vertex of the live C4 exchange graph,
none of the archived block-diagonal or matching-hole antecedents holds, and
every one of the 6,558 literal mixed rows has at least twelve live normalized
monomials.  Thus neither singleton propagation nor the exact round-6
42-killer packet forces a different transition.

This does **not** settle the coefficient-coupled X5 implication.  The complete
Laurent feasibility gate on this support timed out at 300 seconds without a
basis.

## Explicit support

Normalize the twelve chart-1 cells on `01|23|45|67`.  Make all 168
cross-colour cells live.  In colour `c`, retain the base matching and the
following twelve additional diagonal edges:

```text
c=0: 03 05 06 07 13 15 24 25 26 27 46 56
c=1: 02 03 14 15 16 17 24 34 36 37 56 57
c=2: 02 04 05 12 16 17 24 26 34 36 56 57
```

This has 216 live cells, of which 204 remain variables after normalization.
It satisfies

```text
A_02[0,0] = 0,
A_02[1,1] != 0,
A_02[2,2] != 0.
```

For every pair of edges in the base matching and each of the two possible
C4 replacements, exactly one entering edge is live in each colour.  Hence
there are zero live C4 exits from the base chart.  Nevertheless the three
pure fibres contain respectively 10, 13, and 12 live perfect matchings; the
other pure matchings differ from the base through longer alternating cycles.

The support is not block diagonal because every cross-colour cell is live.
It has neither a matching-hole nor a zero-cross mask.  It is also far outside
the small sparse support closures.

## Literal row census and the 42-killer control

After substituting the twelve normalized anchors, every mixed polynomial has
12--105 distinct live monomials.  The minimum by colour multiplicity is

```text
7+1       12       6+2       15       6+1+1     15
5+3       18       5+2+1     20       4+4       28
4+3+1     30       4+2+2     32       3+3+2     42
```

Therefore the literal equations provide no support singleton which could
force a new diagonal cell.  The round-6 D12 dual row

```text
A_02[1,1] A_14[1,1] A_36[1,1] A_57[1,1]
```

is live on this support.  The companion matching
`02|16|34|57` is also live in colour 1 and in colour 2.  The archived 42
incident killers therefore remain genuine cancellation columns, not a
support implication selecting an alternate C4 flip.

## Why a well-founded flip statistic does not repair this

C4 chart transitions are reversible on every overlap, so no statistic can
strictly decrease along every live transition.  One could instead orient
edges by a chosen global statistic and ask every nonclosed vertex to have a
lower neighbour.  The support above defeats that support-level formulation:
the normalized vertex has no live neighbour at all and does not meet a known
closure antecedent.

The construction transports under the stabilizer/site-colour symmetries of
the marked chart-1 boundary.  A single counterguard is enough to rule out a
universal recursion derived only from live-cell incidence.  It does not
assert an analogous guard for every one of the 416 boundary orbits.

## Full coefficient gate

The exact restricted system has

```text
nonanchor Laurent variables          204
literal source equations           6,561
source monomial terms             372,669
pure residual term counts          9, 12, 11
F4SAT final saturator              product of all 204 variables
prime                              1,073,741,827
```

Native `msolve -S -g 2 -t 4` reached the 300-second cap and was terminated
with return code `-15`.  Both output streams were empty.  Sampled RSS stayed
below 5,849,240 KiB, within the requested 12 GB cap.  This is neither a
modular unit nor a modular witness, and makes no characteristic-zero claim.

## Remaining exact statement

Any valid recursive atlas theorem must use a coefficient-sensitive identity
coupling different mixed words, not merely the existence of live matching
terms or the 42 incident D12 columns.  Precisely the still-open possibility is
that the full coefficient-coupled X5 equations exclude the isolated support
above or force an archived closure after a non-support specialization.

## Replay

```bash
python3 computations/unaudited-codex-n8-c4-recursive-boundary-no-go-2026-08-23/audit_recursive_boundary_counterguard.py --check-results
python3 -O computations/unaudited-codex-n8-c4-recursive-boundary-no-go-2026-08-23/audit_recursive_boundary_counterguard.py --check-results
python3 -I -S computations/unaudited-codex-n8-c4-recursive-boundary-no-go-2026-08-23/audit_recursive_boundary_counterguard.py --check-results
```

The hostile `--mutate` mode invents one live base C4 exit and must fail.  The
300-second modular discovery gate is frozen and should not be replayed by the
checker.

