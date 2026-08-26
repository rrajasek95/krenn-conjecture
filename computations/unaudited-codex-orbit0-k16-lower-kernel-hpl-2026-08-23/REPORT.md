# Orbit-zero `K16`: factorized lower-kernel/HPL interface

## Verdict

The projected 25-signature packet cannot be lifted by a small literal matrix.
The exact collected residual has 1,848,174 factor-stabilizer orbits and
701,717,184 labelled rows; direct expansion is retired.  The smallest
provenance-preserving replacement is the same-head Schreyer/HPL star at a
literal `K14` monomial.  Its first component is already nontrivial, while its
full literal incidence component escapes the 100,000-row bound almost
immediately.

This is a bounded structural result.  It does not decide `K16` membership or
localization.

## Exact local operator

For a literal `K14` monomial `q`, let `P(q)` be the mixed singleton pivots
whose unique anchor head `m_p` divides `q`.  Write

```text
C_p = (q/m_p) H_p = q + B_p + terms of K-degree at least 18,
```

where `B_p` is the twelve-term labelled `K16` tail.  The common-head map is

```text
L_q : Q^{P(q)} -> Q,       alpha |-> sum_p alpha_p,
```

and its exact first HPL/lower-kernel transfer is

```text
D_q(e_p-e_p0) = B_p-B_p0.
```

This retains the quotient monomial and every nonanchor cell label; it is not
the lossy 12-entry anchor signature.

For the lex source-labelled component,

```text
r8 = 000d1955627597c4c6e0e6f3
p6 = 00040875797dcfd3d7eaeef2
q  = 000004080d1955627575797d97c4c6cfd3d7e0e6eaeef2f3.
```

Its canonical anchor signature is
`(0,0,1,0,0,1,1,1,2,1,1,2)`.  It has eight pivots
`0100,0200,1000,1100,1200,2000,2100,2200`.  Their 96 tail occurrences occupy
42 rows, with row-owner histogram `1:16, 2:8, 3:16, 8:2`.  Each pivot owns two
rows inside this local star.  These eight private entries give an exact
identity minor, hence

```text
rank_Q(B)=8,  dim ker(L_q)=rank_Q(D_q)=7,
B alpha=0 and sum(alpha)=1 has no solution.
```

So the first literal tail is not removable by changing the same-head pivot.
This sharpens the projected affine obstruction with full physical provenance.

## Sound literal component census

All degree-24 mixed source columns incident to the 42 tail rows were enumerated
using exact perfect-matching divisors.  There are 3,625 such columns.  Keeping
every output through `K16` gives 67,315 rows:

| K-degree | 12 | 13 | 14 | 15 | 16 |
|---:|---:|---:|---:|---:|---:|
| rows | 5 | 41 | 1,035 | 9,218 | 57,016 |

Thus all lower-filtration cancellations of the first shell are present; only
`K17+`, which is zero in `gr_K^16`, is discarded.

Continuing the exact bipartite closure whole-row-at-a-time crosses the
100,000-row cap after just 73 fully processed rows:

```text
102,110 rows, 5,839 columns, 102,037 queued rows
K12:23, K13:201, K14:2,508, K15:13,992, K16:85,386.
```

No peeling or rank conclusion is drawn from this prefix.  It proves that the
literal target component, not merely the precomputed 701-million-row residual,
is already the wrong representation for a bounded proof.

## Next exact provider

Use the order-384 factor stabilizer `H`, but retain literal orbit
representatives:

- rows are `H`-orbits of labelled degree-24 monomials through `K16`;
- columns are `H`-orbits of literal `(mixed word, degree-20 multiplier)`
  columns;
- a matrix entry is the total coefficient mass from a complete column orbit
  into a complete row orbit;
- incident columns are recovered from a row representative by all
  perfect-matching divisors, then canonicalized; all 105 literal outputs are
  canonicalized with their stabilizer masses.

This quotient is sound in characteristic zero: the target and ideal are
`H`-invariant, so any solution can be averaged.  It is provenance-safe because
it retains the full nonanchor row label and orbit mass.  A target-rooted DFS
must expose all incident column orbits before singleton peeling; only a finite
closed residual may be sent to exact-Q target augmentation.  The lex `q`
itself has trivial `H`-stabilizer, so no further local symmetry shortcut is
available.

## Replay

```sh
python3 audit_k16_lower_kernel_component.py
python3 -O audit_k16_lower_kernel_component.py
python3 -I -S audit_k16_lower_kernel_component.py
python3 audit_k16_lower_kernel_component.py --mutate  # must fail
```

The result pins the 25-cover, the 160 MB literal no-go, the original `R8'`,
and both literal source providers by SHA-256.
