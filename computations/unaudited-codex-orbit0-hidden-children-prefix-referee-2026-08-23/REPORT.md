# Hidden K16 child referee

## Verdict

**PASS, with the stated filtration scope.**  The measured K2 `[2,2]` prefix,
the shared K2/K3/K4 child provider, and the complete merged-profile K3/K4
charges are internally and source-provenance consistent.  This audit did not
duplicate the full parent/child generation.

## Independent checks

- Scanned all `694,172` canonical K2 prefix records: strict row order,
  nonzero exact weights, and exact pivotability give `408,972` pivotable and
  `285,200` irreducible rows.  Their signed weight sum is
  `-28885058653048012800` at `U=400591699200`.
- Replayed `257` evenly spaced K2 records to the literal parent occurrence,
  second pivot, K2 tail, raw child, H-canonical child, and source sign.
- Independently replayed all `62,678` prefix profile keys and all `5,766,376`
  K3/K4 tails.  Abstract cycle keys equal literal child cycle keys throughout.
- The common cancellation rule is `w2=-w1/m2`; exact tail cardinalities are
  K2/K3/K4 = `12/32/60`.  Pivotability after a response depends exactly on the
  stored anchor signature and chosen tail, so the merged profile interface is
  sufficient for the immediate K3/K4 irreducible-charge projection.
- The complete merged stream has `6,229,700` strictly ordered nonzero profiles,
  common scale `U`, and signed weight sum `146230609431055564800`.  The full
  program pins and replays the literal prefix before using its abstract map.

## Repaired charges and scope

- Missing K19 path `[2,3]` irreducible charge:
  `-737533302215736950784/U = -45729991456828928/24838275`.
- Adding it to the formerly visible K19 subtotal gives the corrected complete
  K19 aggregate `-2117855228554753792/173867925`.
- Missing K20 path `[2,4]` irreducible charge:
  `72477746180476305408/U = 1850432653709056/10227525`.
  This repairs only `[2,4]`; the full K20 aggregate remains incomplete.
- K2 is still a one-H-slice measured prefix.  No full K2 collection or
  downstream K18 reduction is claimed here.

Replay with `audit_hidden_children_prefix.py`.  The machine-readable result is
`results_hidden_children_prefix_referee.json`; it pins every consumed artifact.
