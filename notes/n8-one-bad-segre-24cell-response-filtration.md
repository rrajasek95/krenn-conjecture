# The 24-face cocharacter filters the complete response module

## Exact filtration

On the six residual sites use the integral site/colour weights

\[
u=((0,0,0),(0,1,1),(0,1,0),(0,0,1),(0,1,0),(0,0,1)).
\]

They have the exact residual-\(q\) properties needed by the Segre chart:

- every cell of the fixed fourteen-cell \(H\) has weight zero;
- every cell of the 24-cell face has weight zero;
- all other 52 mixed cells have strictly positive weight;
- all 45 diagonal cells have nonnegative weight; and
- every `00` cell has weight zero, so every pure-0 matching is retained.

For a residual output word \(w=(w_0,\ldots,w_5)\), define

\[
g(w)=\sum_{x=0}^{5}u_{x,w_x}.
\]

Give a star coordinate at residual site \(x\) and residual colour \(i\)
weight \(u_{x,i}\).  Every physical monomial in the coefficient of \(w\)
in

\[
p_i s_j q^{[2]}
\]
then has weight exactly \(g(w)\): its two star factors and its two
\(q\)-edges cover each residual site once.  Thus every response coefficient
is homogeneous, and the crossed zero tensors split as a direct sum of their
grades.

The three target grades are

\[
g(0^6)=0,\qquad g(1^6)=g(2^6)=3.
\]

In particular, both diagonal response anchors live in grade three.  The
exact grade distributions are frozen by
[`verify_n8_one_bad_segre_24cell_response_filtration.py`](../computations/verify_n8_one_bad_segre_24cell_response_filtration.py).

## Associated-graded odd triangle

The hereditary certificate in `4a213d8` uses diagonal-response binomials

\[
G_{rs}=Q_{rs}(p_rs_s+p_ss_r).
\]

Here the two terms use the same literal \(q\)-matching \(Q_{rs}\), so they
have the same fine source multidegree as well as the same output-word grade.
For a triangle \(r<s<t\), write

\[
A=p_r,\ B=p_s,\ C=p_t,\qquad a=s_r,\ b=s_s,\ c=s_t.
\]

The exact identity

\[
2ABCabc=(Ca)(Ab)(Bc+Cb)-(Cb)(Ab)(Ac+Ca)
          +(Cb)(Ac)(Ab+Ba)
\]
becomes a source-row identity after multiplication by
\(Q_{st}Q_{rt}Q_{rs}\).  Each of its four displayed terms contains exactly
the same six star coordinates and the same three matching factors.
Therefore it is homogeneous in the **full fine source grading**, not merely
after physical projection.  Passing to the Rees module or associated
graded module preserves it literally.

The checker reconstructs every allowed matching term, audits output-word
homogeneity, and verifies this fine-degree equality for all 13,756 witness
triples in each diagonal response.  Hence the odd-triangle clauses used by
`4a213d8` descend through this residual filtration; there is no new graded
counterguard inside the fixed \(H\) chart.

## What remains unproved

This removes one possible obstruction to the chart-cover argument, but it
does not supply the chart cover itself.  The exact missing global statement
is:

> Every entry-minimal projection-degenerate common-\(q\) packet satisfying
> the unary top and all four responses either produces a clean cap, or can
> be put by source gauge/permutation and a response-compatible initial
> degeneration into the normalized fourteen-cell \(H\) chart.

The existing chain does not prove this:

- `cdb809f` classifies the physical matching-incidence circuits;
- `cd08db9` extracts the source-labelled multiplicity-cube boundary;
- `772290e` constructs one coefficient-feasible top-null \(H\) completion;
- `c9b2571` analyzes initial faces only **after** \(H\) and a pure unary
  matching have been fixed.

These results isolate a counterguard orbit and then close its complete
24-cell face via `4a213d8`; they do not show that an arbitrary source must
enter that orbit.  Extending the residual cocharacter to the two deleted
sites in a target-stabilizing, nonnegative way is also not asserted here.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_one_bad_segre_24cell_response_filtration.py
.venv/bin/python -O computations/verify_n8_one_bad_segre_24cell_response_filtration.py
```
