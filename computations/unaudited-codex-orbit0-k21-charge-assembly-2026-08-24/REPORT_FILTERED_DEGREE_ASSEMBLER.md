# Strict filtered-degree charge assembler

`assemble_filtered_degree_exact.py` is the shared exact-Q completeness gate for
the frozen K20--K24 recurrence DAG.  It accepts either the historical `paths`
manifest schema or the newer `groups` schema.  A grouped scalar is added once,
while every lineage ID in the group is checked separately against the DAG.

The frozen required path counts are K20: 36, K21: 52, K22: 76, K23: 59, and
K24: 35.  Complete output is refused if any ID is missing, duplicated, or
extra, if a group has both/neither `id` and `ids`, or if an evidence digest is
not a lowercase 64-hex SHA-256.

Standard, optimized (`-O`), and isolated/no-site (`-I -S`) self-tests agree.
The hostile tests delete one path, duplicate one path, substitute an extra
path, shorten one evidence digest, and supply both manifest schemas; all fail
closed.  The checks use explicit exceptions rather than `assert`, so optimized
mode does not weaken them.

As an integration replay, the generic assembler accepts the authoritative
complete K20 manifest and reproduces

```
full        = 12488470121433187072 / 521603775
irreducible = 12162234158979734656 / 521603775
```

It also reproduces the strict K21 47/52 partial gate and the five missing IDs,
with partial full=irreducible charge
`-448972336918014464/22678425`.  This is only an assembly/completeness result;
it does not infer membership or nonmembership from the charge.

Pinned source SHA-256:
`cf4a5214a15081b91d89c90fc4b79c39e0d54e9b183f442131eec258bf1bce69`.
