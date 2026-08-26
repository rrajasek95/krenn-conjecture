# GLD19--GLD22 import-boundary audit

Audit date: 2026-08-20.

## Outcome

The external GLD19--GLD22 sequence is real, internally consistent progress on
one **literal all-seven fixed-`Q` response-map-zero branch**, but it does not
close any currently open arrow in the local proof programme.

The finite parts and all eight upstream focused replays pass at external
commit

```text
2244a513888bf39294cf749001ff3be60bd280a8
```

The strongest new result, GLD22, excludes one same-graph dense companion
subcell only after imposing a common private root-to-port bijection.  It uses
four roots, a residual pair, and four ports--a ten-site chart.  It therefore
does not apply directly to the local `N=8` `X4 -> active clean cap` problem.
It also does not construct the source-labelled comparison, terminal, or
clean cap required by local `PAComp`.

This packet is deliberately **unaudited** and is not imported into
`PROOF-SKETCH.md` or the certified dependency spine.

## Reproducibility snapshot

```text
local repository:  /Users/rishi/workplace/krenn-conjecture
local HEAD:        25bf92a5333c649dc80bfc62ada33b2f5f6dd4c0
external repository: https://github.com/YesterdaysLemon/krenn-gu-research
external HEAD:     2244a513888bf39294cf749001ff3be60bd280a8
prior local external-import pin: f17afa1
new first-parent commits since that pin: 31
```

The checker freezes SHA-256 hashes for eighteen files: GLD15 and GLD18, the
four GLD19--GLD22 theorem statements, eight primary/independent replay
programs, and four hostile scope reviews.  Run:

```bash
python3 computations/unaudited-external-gld19-22-import-audit-2026-08-20/verify_import_boundary.py
python3 computations/unaudited-external-gld19-22-import-audit-2026-08-20/verify_import_boundary.py \
  --external /path/to/krenn-gu-research-at-2244a513
```

The source-pinned run completed with:

```text
18/18 source hashes: PASS
8/8 upstream focused replays: PASS
GLD19: 201/3136 twelve-row support cells: PASS
GLD19: 663 five-row-zero support controls: PASS
GLD20: 517 corrected channel types: PASS
GLD20: 467715 raw support cells, 254995 F=empty: PASS
GLD21: 63 dominant/dense channels, 1347 raw cells: PASS
GLD22: 24 diagonal gates and 24 ten-site -2hP detectors: PASS
```

The local checker independently reconstructs the finite support ledgers and
uses an exact `Fraction` ten-vertex perfect-matching expansion for GLD22.  As
in the external papers, these computations do not replace the arbitrary-field
written proofs.

## Exact progress in GLD19--GLD22

| result | extra input | proved output | still not proved |
|---|---|---|---|
| GLD19 | one fixed graph/contraction/basis/window and literal zero of all six pair response maps plus the four-port response map | diagonal direct/channel blocks; a complete 201-cell complementary support classification; a five-row detector; opposite raw-pair annihilation on a three-full side | response-map zero, a legal selector, exclusion of the stratum, cross-window integration, activity, or a permanent consequence |
| GLD20 | GLD19 zero-map branch plus common physical two-dimensional shores | exactly 517 corrected channel types and 467,715 compatible raw support cells; the full-capable edge family is intersecting (empty, single, adjacent pair, star, or triangle); conditional pure-target quotient absorption | exclusion of the 254,995-cell `F=empty` residue, a nonzero legal operator row, same-graph integration, or a permanent consequence |
| GLD21 | a two-active-colour GLD20 subcell with at least one corrected `K4` | the missing colour is dead; direct support lies in the dominant colour; `h=0` is excluded; for `h!=0` the all-dead and Hamming-one companion slices are fixed; twelve dense nuisance absorptions | exclusion of `h!=0`, an augmented minor/operator row, source integrability, or a permanent consequence |
| GLD22 | dense `K4/K4`, `h!=0`, same graph, and one common colour-diagonal private root-port matching with twelve nonzero scalars | all twelve active root-root diagonal entries vanish; each of 24 oriented matching packages has coefficient `-2hP!=0`; hence this private subcell is empty in characteristic zero | colour-dependent private permutations, nonprivate root-port arrays, proper-secondary cliques, other `F=empty` cells, the whole response-zero branch, or the conjecture |

The external hostile reviews agree with these boundaries.  In particular,
GLD21 supplies an explicit formal companion assignment showing why its
fixed-`Q` linear equation alone cannot prove same-graph integrability; GLD22
adds exactly one sufficient integrability chart rather than a general one.

## The local and external interfaces are not the same objects

There are four easy-to-miss collisions of notation or scope.

### 1. The two meanings of `h`

In local `PAComp(h)`, `N=2h+2`; thus local `h=3` means an eight-site source.
In GLD19--GLD22, `h=H_Q(z_Q)` is a field scalar carried by the residual pair.
External statements such as `h!=0` say nothing by themselves about local
`PAComp(h)` at any order.

### 2. The two response maps

The local root-integration packet uses

```text
R_ab(K) = K contract (A_pa A_qb + A_pb A_qa)
```

for a selected pair `p,q`, a cap covector `K`, and six residual sites.  The
external map is

```text
R_S(a,b) = [a M_S + b Z_S] modulo the pure GHZ subspace
```

for an operator-coefficient pair `(a,b)` in a fixed-`Q` deck target.  One is
a block-valued cap error; the other is a quotient-valued mixed response of
two labelled deck layers.  No source-labelled map between them is present in
either repository.

### 3. Response-star is much weaker than all-seven response zero

The local response-star criterion only says that the nonzero residual
`R_ab(K)` edges have matching number at most one.  GLD19 assumes the literal
vanishing of every mixed coordinate of all six pair maps and the four-port
map.  Response-star does not imply that hypothesis, even after forgetting
the type mismatch above.

### 4. The site budget changes where the result can land

The raw GLD19--GLD20 tensor identities are computed on `Q_2 union U_4`, so
their finite algebra can inform a six-site residual-window analysis.  Their
fixed-module witness interpretation uses a four-root output.  GLD21--GLD22
retain all of

```text
R_4 disjoint-union Q_2 disjoint-union U_4,
```

and GLD22 verifies a direct ten-vertex matching expansion.  The local `N=8`
cap problem has only the selected pair plus six residual sites, not four
additional roots plus that fixed-`Q` window.

## What can be imported safely

The following conditional packet is safe to cite in future unaudited work:

> Given a source-labelled same-graph fixed-`Q` chart whose deck projections
> and companion equation are identified with GLD15/GLD18, and given literal
> zero of all seven external response maps, GLD19--GLD21 reduce the branch to
> their recorded support/companion residues.  If the residue is dense and its
> root-to-port blocks have one common nonzero private colour-diagonal
> bijection, GLD22 excludes it in characteristic zero.

This is a useful conditional exclusion for a possible ten-site or larger
fixed-`Q` branch.  It is not one of the accepted local terminals:

- it does not give a literal source-ideal unit or Fredholm separator;
- it does not produce an active clean cap;
- it does not give a source-valid strict reduction;
- it does not construct the response-to-`AugP2` comparison;
- it does not promote a fixed-window cokernel to the source Macaulay
  terminal.

The local obstruction remains exactly the one described in
[`h3-response-ks-to-cap-r0-multiplicative-comparison-gate.md`](../../notes/h3-response-ks-to-cap-r0-multiplicative-comparison-gate.md): after forgetting
source grades, the normalized chain-map shape exists, but the physical
source contains no typed degree-zero response-to-cap arrow.  External
response-map vanishing classifies the target-side residue; it does not
manufacture that missing arrow.

## Progress relative to the local repository

The two projects are ahead on different axes.

- The external project is materially ahead on a systematic fixed-`Q`,
  arbitrary-order local atlas: GLD19--GLD22 turn one response-invisible branch
  into exact finite support strata and reach a genuine same-graph exclusion
  on the common-private dense chart.
- The local project is materially ahead on the global proof architecture and
  accepted terminals: six-site impossibility, clean-pair descent, the
  arbitrary-field block-diagonal `N=8` theorem, the intrinsic cap equations,
  and an explicit source-labelled `PAComp`/terminal-promotion boundary.
- Neither project proves the general Krenn--Gu conjecture.  The external
  result does not change the local open table because the source bridge and
  the remaining response-zero charts are both open.

The honest progress delta is therefore: **a verified conditional branch
classification and one ten-site integrability subcell exclusion, but zero
new unconditional local theorem and zero closed `PAComp` arrow.**

## Recommended next use

Do not redirect the current `N=8` attack through GLD22.  Continue the local
`X4 -> active clean cap` / thirteen-exit work there.

For external transfer, the highest-value next lemma is a separate
source-labelled `FixedQBridge` at the first ten-site chart.  It must:

1. derive the external `M_S`, `Z_S`, `Gamma_Q`, and legal operator spaces
   from one local exact source without changing its fibre;
2. identify, rather than merely analogize, the external mixed quotient maps
   with explicit local occurrence-labelled rows;
3. preserve the same graph through the companion/root data;
4. turn every failure into one of the accepted local terminals; and
5. route all non-private and colour-dependent-private residues, not only the
   GLD22 chart.

Until such a bridge exists, GLD19--GLD22 should remain a strong external
lemma packet and a source of finite test cases, not a dependency of
`PAComp` or the proof spine.
