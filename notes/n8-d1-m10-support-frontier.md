# N=8 D1: structural audit at the ten-cell frontier

The checker `computations/audit_n8_d1_m10_support_frontier.py` is an exact
scalability and completeness audit.  It does **not** claim that `m=10` is
empty.

The one-colour census extends through size seven.  There are 95,272 valid
seven-cell monochrome supports, but none is minimal: every one contains one
of the known 72 three-cell or 27 four-cell anchors.  Thus the complete
two-colour partition remains `3+3+4`, `3+4+3`, `4+3+3`, and `4+4+2`, with
132, 64, 64, and 52 anchor-unit orbits (312 total).

Those orbit representatives encode 1,196,640,200 raw choices, dominated by
1,159,407,480 choices in `3+3+4`.  Materializing them would be the wrong
algorithm.  The checker instead compiles every unique-fibre repair condition
as a monotone DNF over a 128-bit support mask and searches it symbolically.
The complete search visits only 3,251 memo states.  It proves 41 anchor
branches impossible at the repair level and leaves 271 symbolic branches;
13 of those have no initial unique-fibre repair certificate at all.

To make the next step reproducible, the checker freezes the lexicographically
first `3+3` base-support orbit with exactly four additional off-Sigma cells.
A fibre-core reduction leaves 16 exact fibres and a CNF with 3,539 variables
and 12,897 clauses.  Its DIMACS SHA-256 is
`f0a751847300019fb4a72c5b492340b476babd2c050ec0261bca5ffc049abdda`.
Local CaDiCaL runs report UNSAT, but that solver verdict is deliberately not
promoted to a theorem here: a checked deletion-free RUP/LRAT artifact remains
to be committed.

Emit the frozen input with:

```text
python3 computations/audit_n8_d1_m10_support_frontier.py \
  --emit-dimacs /tmp/n8-d1-m10-first.cnf
```

The mathematical state after this audit is therefore: `m <= 9` is closed,
while `m=10` is open in 271 symbolic anchor branches with a small exact proof
frontier for the first complete `3+3+4` family.

Frozen audit ledger SHA-256:
`24100862cdf91cc587626d0c7b26e8b7490cf6709bcffd2c87551b8f125aa65e`.
