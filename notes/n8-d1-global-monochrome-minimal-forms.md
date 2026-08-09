# N=8 D1: global monochrome minimal forms

The 72 three-cell traces and 27 special four-cell supports for each colour
are the complete minimal monochrome forms at every support cardinality.  The
checker `computations/verify_n8_d1_global_monochrome_minimal_forms.py` turns
the earlier size-bounded census into an all-size theorem.

For one colour there are 22 off-Sigma cells.  Exhaustive enumeration through
size eight gives the following valid/minimal counts:

| size | valid | minimal |
|---:|---:|---:|
| 2 | 0 | 0 |
| 3 | 72 | 72 |
| 4 | 1,179 | 27 |
| 5 | 8,382 | 0 |
| 6 | 34,657 | 0 |
| 7 | 95,272 | 0 |
| 8 | 189,990 | 0 |

The global promotion is elementary.  Any valid support contains a full
matching trace `T`, of size at most four.  If the support contains no residue
perfect matching, neither does `T`, so `T` is already a valid subset.  If it
contains at least two residue perfect matchings, choose two of them; their
union with `T` is valid and has size at most eight.  (Exactly one residue
matching is the excluded case in the definition of validity.)  The exhaustive
size-eight census therefore forces either a known triple or special four in
every valid support, irrespective of its size.

The checker verifies this reduction for all 99 distinct full traces and all
three pairs of residue perfect matchings, separately for both colours.  Its
ledger SHA-256 is
`c3b4f739b0ceb180dd3b4869dc1df72f86ee4af8a4c153b87e1060cb9e454102`.

Consequently the entire D1 all-support locus is covered by the same 312
two-colour anchor-unit charts used in the finite m frontiers.  Higher m can
create new completions inside these charts, but cannot create a new
monochrome anchor type.
