# Symmetry-broken live-chart separator SAT

Date: 2026-08-23  
Status: `UNRESOLVED_NO_SAT_NO_UNSAT`

The forbidden set of chart types `{11,24,25}` is invariant under `S8 x S3`.
Every admissible support has a live pure perfect matching in each colour, so a
site permutation may first send a live colour-0 matching to
`01|23|45|67`.  The initial fixed-matching phase retained all 39,060 labelled
forbidden triples and added every mixed singleton in each model as an exact
batch.  At its checkpoint it had reached round 420 and 6,834 distinct
singleton gadgets without a terminal model or UNSAT result.

The stronger reduction is also sound and exhaustive.  Choose one live pure
matching in each of the three colours.  Their ordered triple lies in one of
the certified 31 atlas orbits.  Types 11, 24, and 25 are prohibited, leaving
exactly 28 representative 12-cell seeds.  The split solver reused every
learned singleton clause globally because each gadget is a support-valid
implication independent of the seed.

The split phase terminalized at its bounded deadline after 104 solver calls,
6,830 exact singleton gadgets, and 131.23 seconds.  All 28 cases remained
active; 24 had at least one two-second interrupted call and four remained
active without a call interruption.  No case was certified UNSAT, and no
singleton-free support was found.

Therefore this gate proves neither existence of a support avoiding all three
chart types nor that `{11,24,25}` is a hitting set.  In particular it does not
prove hitting number at least three.  SAT here would still be support
feasibility only, not a coefficient-level X5 source.

Replay of the frozen scope and symmetry census:

```bash
python3 computations/unaudited-codex-n8-live-chart-cluster-counterguard-2026-08-23/audit_separator_symmetry_split.py --check-results
python3 -O computations/unaudited-codex-n8-live-chart-cluster-counterguard-2026-08-23/audit_separator_symmetry_split.py --check-results
python3 -I -S computations/unaudited-codex-n8-live-chart-cluster-counterguard-2026-08-23/audit_separator_symmetry_split.py --check-results
```

The hostile `--mutate` mode deletes one allowed orbit and must fail.  Replaying
the SAT search itself is not required by this checker and would constitute a
new bounded search.

