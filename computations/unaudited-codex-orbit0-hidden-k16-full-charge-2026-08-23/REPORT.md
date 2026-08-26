# Full hidden-parent immediate K3/K4 cycle charges

## Terminal result

`PASS_FULL_HIDDEN_K3_K4_IMMEDIATE_CHARGE` under the 300-second / 8-GB gate.
The exact pass took 46.97 seconds and streamed all 6,229,700 nonzero merged
hidden-parent profiles.  Their scaled coefficient sum is
`146230609431055564800` at `U=400591699200`.

The previously omitted immediate components are:

- K19 path `[2,3]`: full charge
  `-860516707072888995840`, irreducible charge
  `-737533302215736950784` (both scaled by U).
- K20 path `[2,4]`: full charge
  `76746165907211550720`, irreducible charge
  `72477746180476305408` (both scaled by U).

The corresponding unscaled rational values are
`-74697630822299392/34773585`, `-45729991456828928/24838275`,
`2220664522778112/11591195`, and `1850432653709056/10227525`.

## Exact guards

The input profile weight already includes the two pivot signs and denominators:
`w2=-mass*U/(m1*m2)`.  The evaluator applies no additional sign.  For every
K3/K4 tail it reconstructs the 24-port cycle partition and tests the child
anchor signature for another available pivot before adding to the irreducible
charge.

Before the full abstract pass, all 62,678 witness-bearing prefix keys were
replayed literally.  All 5,766,376 K3/K4 tail comparisons between abstract and
literal cycle partitions pass, and the four frozen prefix charges are recovered
exactly.  The merged input header, strict key order, wildcard tag, nonzero
weights, EOF, record count, and total scaled weight are also asserted.

The full stream has 199,350,400 K3 profile-tail terms, of which 147,397,352
pass the irreducibility test, and 373,782,000 K4 profile-tail terms, of which
332,684,520 pass.  These are profile-term counts, not literal occurrence counts:
the merged profile stores aggregate coefficients but not source multiplicity.

## Scope

This repairs only the immediate 77-cycle charges for missing paths `[2,3]` and
`[2,4]`.  It does not run the K2 `[2,2]` collection, emit later child tails,
combine these values with the previously visible component subtotal, or prove
membership/nonmembership.

Source SHA-256: `005a5cac783333ab6cd74567e93e7415e6165aae8a16f9e4fde5066544b69fb0`.
Result SHA-256: `aa25a2deee2aff213b9f49b9f61826d161293651ccafa1cd7332ef978ae89934`.
Logical digest: `d2aecd117945f9c6cec786aaca605def751335b33e2788cf7d7a32a3681eac41`.
