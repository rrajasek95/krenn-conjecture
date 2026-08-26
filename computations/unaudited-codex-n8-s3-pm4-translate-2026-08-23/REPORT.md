# Universal S3 versus translated N4 triples

The universal cubic transfer kernel `S3` is not the earlier 66-row
degree-eight attachment: degree and coefficient profiles already separate
them.  More strongly, none of the 66 cubic monomials is incident to any of
the `2,206 * 240 = 529,440` degree-one translates of the literal N4 leading
triples.  The touched translated-cell component therefore consists of 66
isolated rows, has rank zero, and admits a one-coordinate exact separator.

This is exhaustive without materializing the half-million cells.  The 6,618
quadratic N4 terms partition into 2,206 disjoint triples.  Deleting each of
the three possible factors from a cubic monomial therefore identifies every
possible incident translated cell.  All 198 inverse lookups miss.

The exact checker/result are
[`audit_s3_pm4_translate.py`](audit_s3_pm4_translate.py) and
[`results_s3_pm4_translate.json`](results_s3_pm4_translate.json).  The result
is limited to degree-one translates of the N4 leading triples; it does not
include lower-provider tails, `S4`, or the full degree-ten residual.

