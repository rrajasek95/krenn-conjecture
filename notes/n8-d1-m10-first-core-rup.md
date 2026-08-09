# N=8 D1: checked RUP closure of the first ten-cell core

The deletion-free proof in
`computations/certificates/n8_d1_m10_first_core.glucose42.drup.gz`
rigorously closes the exact lexicographically first `3+3+4` support-base
family frozen by `computations/audit_n8_d1_m10_support_frontier.py`.
Consequently this entire complete ten-cell family is empty; this is one
closed family inside the still-open `m=10` frontier, not a closure of all
`m=10` branches.

The input is the previously frozen 3,539-variable, 12,897-clause CNF with
DIMACS SHA-256
`f0a751847300019fb4a72c5b492340b476babd2c050ec0261bca5ffc049abdda`.
Glucose 4.2 was used only to generate a candidate DRUP trace.  Deletion lines
were removed, leaving 4,090 clause additions and a final empty clause.  The
standard-library checker `computations/verify_n8_d1_m10_first_core_rup.py`
does not invoke or trust a SAT solver: it reconstructs the exact input,
checks every added clause by reverse unit propagation using a persistent
two-watch database, and checks that the last addition is empty.

Run the independent check in normal and optimized Python modes with:

```text
python3 computations/verify_n8_d1_m10_first_core_rup.py
python3 -O computations/verify_n8_d1_m10_first_core_rup.py
```

The optional generator requires `python-sat` and reproduces the frozen
artifact:

```text
.venv/bin/python computations/generate_n8_d1_m10_first_core_drup.py
```

The deletion-free payload SHA-256 is
`12be9116c777e020d0362117aec555393a6be6119ee41ce955d13d8c1ac6647b`;
the deterministic gzip SHA-256 is
`edacb7215a32476d2b7c22def364be589c5d9ef7f507ec88b4442468c07c5bd1`.
The checked ledger SHA-256 is
`9c18787620e328c8ff104891b31087074bf90788bb28f41973efeb3fc5ccf772`.

Four further base-support orbits identified by the same core architecture
now have independently checked proof traces; see
`notes/n8-d1-m10-additional-core-rups.md`.  Together the five certificates
close three branches that survived the repair-DNF audit, so the remaining
symbolic frontier is at most 268 of the original 271 branches.
