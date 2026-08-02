# The first chart-26 cross-word compatibility cell

## Exact bounded result

Start with the 6,558 degree-four homogenized normalized generators and the
two nonzero reduced degree-five cells in the support-stabilizer orbit of the
first star-minor transport.  There are 22 non-product critical pairs between
those two cells and the earlier basis whose LCM has degree six.

Order them first by LCM monomial and then by source label, and reduce each
remainder against the full basis already accepted in that order.  The first
three nonzero remainders have leading monomials

```text
0951abcfebf5
0951abd0eaf9
0948cfcfebef
```

and respectively 504, 504, and 546 terms.  The first two leading monomials
are squarefree.  The third contains coordinate `cf` twice and is therefore
the first non-squarefree leading cell in this orbit-extended schedule.  It
has no (t) factor.

The third critical pair is between the original word code 11,

```text
00000102,
```

and the transform-zero degree-five transport cell based on codes 1 and 2.
It changes the colour at vertex 5 after performing the transport at vertex
7.  The repeated coordinate decodes as

```text
cf = (4,6; 0,0).
```

Thus its leading multigraph uses the off-support edge (46{:}00) twice.
This is the first exact algebraic trace of a cross-word/backtracking
compatibility: two elimination orders return through the same source edge.

## Scope

This calculation does **not** prove that `0948cfcfebef` is a minimal
generator of the final initial ideal.  The support-stabilizer orbit contains
only two of the degree-five cells; the other original-original degree-five
S-pairs have not all been adjoined.  A Bianchi/commutator combination with a
second cross-word cell may cancel the square, and another degree-five lead
could divide this provisional degree-six lead.  The checker therefore
freezes a bounded source-labelled compatibility cell, not a radicality
obstruction.

The structural next test is to generate the opposite-order transport with
the same repeated edge, subtract the two monic degree-six cells, and reduce
that Bianchi difference.  If the square cancels, its next leading term is
the genuine cross-vertex curvature datum.

## Verification

Run

```text
python3 computations/verify_n8_chart26_first_degree6_compatibility.py
```

The checker reconstructs the original generators, the full four-source
degree-five stabilizer orbit, the 22-pair degree-six schedule, and the first
three incremental exact reductions.  It freezes every accepted polynomial
by SHA-256 and audits the repeated source coordinate directly.
