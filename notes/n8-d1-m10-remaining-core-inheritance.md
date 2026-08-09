# N=8 D1: exact common-core inheritance census at m=10

The checker
`computations/verify_n8_d1_m10_remaining_core_inheritance.py` classifies the
common 16-fibre support core on all 268 symbolic branches left after the
first five checked support-base certificates.  It includes each branch's
anchor units, so it is stronger than the earlier support-only inputs while
remaining a necessary relaxation of the complete support shadow.

Exactly three branches, `433:46`, `433:47`, and `433:48`, are UNSAT.  More
than just sharing a solver verdict, they admit the identical 30-addition
deletion-free DRUP byte stream.  The checker independently validates that
same RUP template against all three distinct CNFs (3,449 variables and
12,563 clauses, with separately pinned DIMACS hashes) and requires its final
empty clause.  Thus the common support-core template closes all three
branches rigorously and the remaining symbolic frontier falls to at most
265.  The subsequent complete-shadow transfer in
`notes/n8-d1-m10-442-full-shadow.md` eliminates all 22 remaining `4+4+2`
branches and leaves at most 243.

The other 265 branches are not merely native SAT reports: the compressed
artifact `computations/certificates/n8_d1_m10_remaining_core_models.json.gz`
contains a complete assignment for every one, and the standard-library
checker directly evaluates every input clause under every assignment.  This
proves that none of those branches can be closed by the present 16-fibre
palette alone.  It does **not** assert that they extend to the complete
8,100-fibre shadow or to coefficient solutions.

The smallest genuinely new palette survivor is frozen as `442:4`: 2,915
variables, 10,594 clauses, and DIMACS SHA-256
`f596310a36dcc284c8e9713db24dbccc74d877b706ab38663add380a9ca12583`.
Its support base is

```text
(0,4,0,0) (0,4,1,1) (1,5,0,0) (1,6,1,1)
(2,6,0,0) (2,7,1,1) (3,5,1,1) (3,7,0,0)
```

with no additional anchor units and exactly two further off-Sigma cells.
Emit its exact CNF with:

```text
python3 computations/verify_n8_d1_m10_remaining_core_inheritance.py \
  --emit-smallest-dimacs /tmp/n8-d1-m10-442-4.cnf
```

Normal and optimized checks are:

```text
python3 computations/verify_n8_d1_m10_remaining_core_inheritance.py
python3 -O computations/verify_n8_d1_m10_remaining_core_inheritance.py
```

The deterministic generator requires `python-sat`.  The SAT-model payload
SHA-256 is
`428995b49686b142468f5143d92855ea3aa74fba7f0243e4c963a9cb7266e06d`;
the common raw RUP SHA-256 is
`ed24cdb01d6761dd27bb7076b492348b8ade8d60fed38e55cea6c6e0ef90ca02`.
Frozen checked-ledger SHA-256:
`7efb8044156fc1dcd6560baa9566563fd9d38532d2e0ac801a50ff39d9344a93`.
