# Research checkpoint: terminal sync and the level-two differential

Checkpoint date: 2026-08-01.

## Status

Krenn's conjecture is **open**. The certified proof spine is unchanged:
`SP-CLEAN-BRIDGE` remains the missing conjecture-level implication. This note
is a synchronization and research checkpoint, not a supersession.

The substantial Claude chain from the terminal clone has been preserved
linearly through `c871c2c`. Its Git topology, provenance, and proof-status
labels were audited before integration; the load-bearing claims identified
below received separate mathematical audits. The synchronized research chain
then adds:

| Commit | Purpose |
|---|---|
| `9b38660` | Remove the only whitespace defect in the imported chain. |
| `04148e6` | Replace the sampled level-two slope check by an exhaustive formal proof over all 84 blocks and 64 words. Independently audited PASS. |
| `9ad3484` | Repair the provenance and scope defects in Claude's two certification records, without changing either mathematical statement. Independently audited PASS. |
| `01764c3` | Prove the R2 pair-pencil rank drop for the four-live/two-dead level-two family. Independently audited PASS. |

The user's two pre-existing, superseded double-polar drafts were not
overwritten. They remain recoverable in stash object
`2c348bed84e266e116460f0048b4fa48e5fd8a19`.

Four untracked Claude checkers were preserved, with exact hashes and trust
labels, on the pushed branch
`archive/claude-orphaned-checkers-2026-08-01` at `4fc726b`. They were not
mixed into the synchronized proof chain.

## Certification boundary

The baseline tag `certified-spine-2026-07-30` remains authoritative. Claude's
records `SUPERSESSION-2026-08-01-01` and `-02` used abbreviated hashes, had no
permanent independent reports, and omitted required scope/frontier updates.
Append-only records `-03` and `-04` procedurally replace them and pin the exact
replacement commits, artifact hashes, auditors, and unchanged statements.

No later research result in this checkpoint supersedes a named certified
dependency. In particular, neither the support theorems nor the level-two
differential currently proves `SP-CLEAN-BRIDGE`.

## What the synchronized work and recovered traces add

The strongest imported results are now:

1. Every vertex and every complementary colour pair is non-rigid. The old
   rigid/private-edge branch is vacuous.
2. At `(8,3)`, the live support graph has no independent four-set.
3. The 2,940 level-two words generate 84 overlapping blocks of 64, totaling
   5,376 incidences; words of colour-count type `(4,2,2)` occur in two blocks.
   In each block, the rare diagonal cell is affine with slope equal to the
   complementary six-vertex binary matching tensor.

The interrupted trace adds the following audited interpretation of those
blocks:

4. Writing the complementary tensor as `Psi(M)`, with endpoint columns
   `P_x,Q_x` and
   `N_xy = P_x Q_y^T + Q_x P_y^T`, the exact block equation is

       dPsi_M(N + (z/3) M) = 0.

5. Exact rank-55 witnesses show that a dense open locus has only the five
   trace-zero vertex-scaling kernel directions. On that locus the block takes
   the Cauchy-gauge form

       N_xy = (nu_x + nu_y) M_xy,    z = -sum_x nu_x.

This is structural progress, but a single block has positive-dimensional
solutions and therefore cannot yield the contradiction by itself.

## Result recovered and completed from the traces

The interrupted L2 trace is
`agent-a1dfcff36e4b0f443`. Its Steps 1--4 contain the sound differential
identity and generic-kernel calculation. Step 5 is invalid on nonempty
zero-sum graphs; Step 6 is a sample rather than a classification; and the
phrase "three-fold determination" is too strong when a slope vanishes.

The universal-rule trace `agent-aac438e5301d9721e` contains a complete hand
proof of R2 at eight vertices. Applying R2 to the rank-55 Cauchy-gauge branch
eliminates the five-invertible/one-dead family immediately. It forces the
four-invertible/two-dead family into 16 pure-column assignments.

The new theorem in
[`level-two-pair-pencil-rank-drop.md`](level-two-pair-pencil-rank-drop.md)
closes all 16 assignments without enumerating algebraic subcases:

- every assignment has an extra live-live tangent-kernel direction, so
  `rank dPsi <= 54`;
- a balanced 2+2 assignment has two extra directions, so
  `rank dPsi <= 53`.

The checker is stdlib-only, runs in about two seconds, and verifies 1,408
formal polynomial identities under normal, optimized, and isolated Python.
An independent agent re-derived R2, every kernel identity, orientation,
generic-to-all specialization, and the arbitrary-live-live scope before PASS.

## Trace results not promoted into the chain

- The independently audited scratch result `Q_C(Per_4)=2` would give a
  cleaner support-independent proof of the already-landed bipartite `4+4`
  exclusion. It does not advance beyond the no-independent-four-set theorem,
  so its interrupted author artifacts were not promoted.
- The heavy cross-colour terminal-class checker claims a useful local
  vanishing result, but its separate audit hit a session limit. It is archived,
  not accepted.
- The three-mode contraction proves the general bound `D <= N-1`; it also
  proves why slice rank is saturated and uninformative at `(8,3)`. It is a
  negative-route result and remains in the archive.
- The support-only 31-branch abstraction already fails at solved `(6,3)`.
  Its reported empirical counts have no committed replay artifact and remain
  soft-quarantined.

## The shortest live continuation

The new rank drop removes two named nontrivial families, but the interrupted
trace did not classify all rank patterns in the generic-kernel equation.
Three precise rocks remain:

1. **Classify without a census.** Derive a rank-pattern-independent
   consequence of `X_x J X_y^T = (nu_x+nu_y)M_xy`, using R2 before choosing
   normal forms. The desired lemma must cover rank-one and mixed-rank `X_x`,
   not just the sampled invertible/dead types.
2. **Use overlapping blocks.** For an edge entry, the valid cross-block
   statement is `F_c^{st}=A_e[s,t]H_c`: a live slope determines the entry,
   while `H_c=0` forces only `F_c^{st}=0`. Either prove enough slopes live or
   exploit the zero-slope branches directly. Do not assume all three slopes.
3. **Kill the trivial generic packet globally.** There is an exact rank-55
   selected-block packet with `P=Q=z=0` satisfying all current support rules,
   no-independent-four-set, and slice-cover activity, while failing 389 of the
   full 6,561 equations. This guard proves that another support theorem is not
   enough; the next argument must couple this block to other L2 blocks or to
   L0/L1 values.

The natural throughline is therefore value-sensitive global compatibility:
local differential normal form, R2-induced tangent rank drop, then overlapping
block consistency. Another support SAT census, a single-block contradiction,
or a return to the inactive terminal cap does not address the remaining guard.

Follow-up: [level-two-one-sided-rank55-guard.md](level-two-one-sided-rank55-guard.md)
strengthens item 3 in the selected block itself.  The equations vanish on the
entire linear family \(Q=z=0\), with arbitrary \(M,P\); an exact member has
every \(P_x\ne0\), all six \(X_x\) of rank one, an everywhere-live slope, and
\(\operatorname{rank}d\Psi_M=55\).  Its support completion also realizes the
literal residual R2 witnesses and a complete live graph.  It is not a full
solution or a replacement for the stronger all-support-rules packet above,
but it shows that cross-block coupling is needed even before both stars vanish.

Second follow-up:
[level-two-one-sided-overlap-collapse.md](level-two-one-sided-overlap-collapse.md)
performs that first coupling.  On the rank-$55$ locus where every residual
deletion graph is connected nonbipartite and every four-site binary cofactor
is live, L1 and the three-/four-rare-colour value rows force the remaining
one-sided star to vanish.  The exact witness in the first follow-up satisfies
these hypotheses: all six five-site cofactor maps have rank $10$, and all
$240$ four-site cofactor coordinates are nonzero.  Consequently that
nonzero-star witness is no longer a global guard.  The live obstruction is
now the zero-star packet $P=Q=z=0$, together with the zero-slope,
rank-deficient, bipartite-deletion, and vanishing-cofactor boundary strata.

Third follow-up:
[level-two-zero-star-four-c-obstruction.md](level-two-zero-star-four-c-obstruction.md)
closes the cofactor-open zero-star packet.  Its mixed four-rare-colour rows
force every symmetric endpoint-pair coefficient to vanish, while the
pure-colour row is exactly a linear combination of those same coefficients
and must equal one.  In addition, rank $55$ plus connected nonbipartite
deletion graphs automatically makes the slope and all four-site cofactors
live by a five-dimensional kernel-budget argument.  The entire generic
one-sided branch is therefore impossible in a full solution.  What remains
is the genuinely two-sided generic-kernel locus and the rank-deficient,
graph-degenerate, or cofactor-vanishing boundary.

Fourth follow-up:
[level-two-fully-invertible-residual-obstruction.md](level-two-fully-invertible-residual-obstruction.md)
closes the dense open residual locus without assuming a one-sided endpoint
pattern.  If all fifteen internal binary blocks are invertible, R2 forces
both endpoint stars to vanish at every residual root.  Rank \(55\) then makes
the slope and four-site cofactors live, so the zero-star theorem contradicts
the pure-colour row.  An exact integral witness verifies that this forbidden
locus is nonempty: every block determinant is nonzero, the differential rank
is \(55\), all \(64\) slope coordinates are live, and all \(240\) cofactor
coordinates are live.  Consequently every rank-\(55\) level-two block in a
hypothetical solution must contain a singular internal \(2\times2\) block.

## Restart checks

1. Read this note, `notes/consolidated-proof-frontier.md`, and
   `certification/BASELINE.md`.
2. Confirm the Git head and preserve the stash; do not pop it over the
   corrected double-polar files.
3. Run `computations/verify_level_two_block_structure_at_eight.py` and
   `computations/verify_level_two_pair_pencil_rank_drop.py` under normal,
   `-O`, and `-I -S`.
4. Modify the certified spine only through an independently audited,
   append-only supersession of a named dependency.
