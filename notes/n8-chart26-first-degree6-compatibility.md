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
are squarefree.  The third contains coordinate `cf` twice and has no
\(t\) factor.

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

Thus its leading multigraph uses the off-support edge \(46{:}00\) twice.
This is the first exact algebraic trace of a cross-word/backtracking
compatibility: two elimination orders return through the same source edge.

## Completion through degree five makes the square minimal

The complete degree-five certificate in
`n8-chart26-complete-degree5-buchberger.md` changes the status of this cell.
The five distinct degree-five divisors of its leading monomial are

```text
0948cfcfeb
0948cfcfef
0948cfebef
09cfcfebef
48cfcfebef
```

and none is among the 84,005 completed degree-five leading monomials.  The
exact degree-six polynomial belongs to the homogeneous ideal, its leading
monomial is not divisible by a degree-four or degree-five initial generator,
and no later generator of degree greater than six can divide it.  Therefore
`0948cfcfebef` is a genuine minimal non-squarefree generator of the initial
ideal for this \(t\)-last order.

A Bianchi/commutator combination with a second cross-word cell can cancel
the square and expose another curvature term, but it cannot remove this
monomial from the initial ideal.  Thus the squarefree-initial-ideal route to
radicality fails for this term order.

This is not evidence that the homogeneous ideal itself is nonradical.  An
ideal may be radical while a particular initial ideal is nonradical; a
different degeneration or a direct radicality argument remains possible.

## Verification

Run

```text
python3 computations/verify_n8_chart26_first_degree6_compatibility.py
```

The checker reconstructs the original generators, the full four-source
degree-five stabilizer orbit, the 22-pair degree-six schedule, and the first
three incremental exact reductions.  It then replays all 84,005 leading
monomials from the complete degree-five certificate and checks every divisor
of the repeated monomial.  It freezes every accepted polynomial by SHA-256
and audits the repeated source coordinate directly.
