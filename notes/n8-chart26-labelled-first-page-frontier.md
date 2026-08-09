# Chart 26 labelled first-page frontier

This audit repairs the scope defect in the global orbit transfer by retaining
literal source rows and columns in the single expanded-prism chart 26.  The
three pure anchor monomials are

```text
P0 = 01|25|34|67  in colour 0
P1 = 03|16|24|57  in colour 1
P2 = 07|14|23|56  in colour 2.
```

Their product is the twelve-cell root.  Localizing at `P0,P1,P2` inverts all
twelve support cells.  At the root itself, no denominator is required:
exhaustive enumeration of all `3^8 * 105` labelled hafnian terms finds five
terms wholly inside the chart support, three pure and exactly two mixed.
Thus every anchor-Laurent translate incident to the root is a unit translate
of one of two literal columns.

## Exact root star

Each mixed column has a `(5,3)` odd complement and 105 labelled outputs.  Its
diagonal-level histogram is

```text
level 12:  3
level 10: 30
level  9: 48
level  8: 24.
```

The two level-12 initials intersect only in the root.  Their exact star matrix
therefore has five rows, two columns, rank two, source kernel zero, and target
cokernel dimension three.  An explicit left functional pairs to one with the
root and annihilates both columns.  Hence the root survives this **two-column
star**.

This is not the full first-page verdict.  The other four level-12 rows have
further incident columns which can alter the cokernel witness.

## Exact expansion frontier

Breadth-first labelled closure in the original balanced multidegree reaches
the 50,000-row cap after processing only 2,939 rows:

```text
discovered rows:       50,000
discovered columns:    14,113
queued rows:           47,061
top-support sizes:     3, 9, or 15
truncated:             yes.
```

This prefix uses no orbit compression and no forbidden denominator.  It does
not yet include all anchor-Laurent translations; those can only enlarge the
first-page component.  Accordingly the closed first-page root cokernel is
**unresolved**.  No deeper diagonal layer is attempted.

The smallest exact next artifact is a streamed sparse labelled matrix for
this entire diagonal-12 component, with anchor-exponent translations stored
symbolically rather than enumerated as separate rows.  A rational left-kernel
witness pairing nontrivially with the root would prove survival; a sparse
column solution would prove killing.

The exact root-star checker is
`computations/verify_n8_chart26_labelled_first_page.py` with frozen ledger
`479d214a27f27710ae0a6ff93a1a2c39d99e3afa2376d26d588b26ea9e6c83dc`.
The bounded closure checker is
`computations/analyze_n8_chart26_labelled_first_page_closure.py`, with frozen
ledger `5727ce606e12e72ab151b33858a941e96cbd002e78559e65d121db72da8f6d03`.
