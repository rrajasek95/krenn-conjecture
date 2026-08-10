# Every optional subset of the Segre 24-cell face is response-empty

## Result

Fix the fourteen-cell Segre--\(K_4\) quadratic \(H\).  Allow arbitrary
support and coefficients on

- all forty-five diagonal `00`, `11`, `22` cells;
- all twenty-four endpoint-star coordinates of \(p_1,p_2,s_1,s_2\); and
- an **arbitrary subset** of the twenty-four mixed cells

```text
02:02 02:10 02:12 02:20  03:01 03:10 03:20 03:21
04:02 04:10 04:12 04:20  05:01 05:10 05:20 05:21
12:02 13:01 14:02 15:01  23:21 25:21 34:12 45:21.
```

There is no complex point satisfying the unary top and four one-bad
responses

\[
q^{[3]}=X_0,\qquad
p_i s_jq^{[2]}=\delta_{ij}X_i\quad(i,j\in\{1,2\}).
\]

No assumption that the support meets the exceptional incidence classes
\(A\) and \(B\) is needed.  Consequently this closes every intermediate
support between the diagonal Segre chart and the maximal 24-cell face.

The checker is
[`verify_n8_one_bad_segre_anchor_24cell_response_face.py`](../computations/verify_n8_one_bad_segre_anchor_24cell_response_face.py).

## Why the odd triangle is hereditary

The maximal allowed source universe contains literal diagonal-response rows
with exactly two matching terms

\[
 g_{rs}=Q_{rs}(p_r s_s+p_s s_r).
\]

The checker accepts such a row only when the two terms use the **same two
physical \(q\)-cells**, not merely the same Boolean support variables.  Thus
the fixed \(H\) coefficient and every optional face/diagonal coefficient are
identical in both terms.  Passing to a smaller support has only two effects:

1. if a cell in \(Q_{rs}\) is deleted, both terms disappear together;
2. otherwise the same two-term row survives unchanged.

For a triangle \(r<s<t\), write

\[
A=p_r,\ B=p_s,\ C=p_t,\qquad a=s_r,\ b=s_s,\ c=s_t.
\]

The integral identity already used on the mandatory face is

\[
2ABCabc=(Ca)(Ab)(Bc+Cb)-(Cb)(Ab)(Ac+Ca)
          +(Cb)(Ac)(Ab+Ba).
\]

After multiplication by the three matching monomials \(Q_{st}Q_{rt}Q_{rs}\),
this gives an ordinary source-row certificate.  Hence the six star
coordinates and all optional cells used by the three \(Q\)'s cannot be
simultaneously nonzero.  The resulting conditional clause is valid on
every subset; this is the missing hereditary form of the maximal-face
argument.

## Exact support certificate

The Boolean formula reconstructs every physical matching term in
\(q^{[3]}\) and the four response tensors.  It imposes only necessary
conditions for a coefficient point:

- each target coefficient has at least one live monomial;
- each zero coefficient has either zero or at least two live monomials;
- every activated diagonal-response odd triangle obeys the integral
  identity above.

Before the odd-triangle clauses, the unrestricted optional support shadow is
satisfiable.  After the conditional clauses it is UNSAT.  The final formula
has

```text
10,915 variables
90,542 clauses.
```

Glucose produces a deletion-free proof with 13,158 additions ending in the
empty clause.  A fresh CaDiCaL instance checks every addition by reverse unit
propagation.  The pinned digests are

```text
formula 49f9879f7e5cc117c63ce886b3cefa5586e38601dd7599eae15f2ca7e777d24c
proof   3563bda3b92b4183f1402b7e12580cd5f466a59e43ce8bfe1ea9072c1059a794
ledger  539937103167ea8a95f72454e88602abc30a317b4aa11a21fe3dd4fd8fb746be
```

## Consequence and scope

This positively supersedes the mandatory-24-cell theorem `710e2f5` and the
separate minimal two-cell checks **inside this fixed Segre--\(K_4\) chart**:
support non-heredity is no longer a gap on this face.  It also makes the
\(A/B\) cocharacter split unnecessary after the chart has been reached.

It does not prove that an arbitrary one-bad source has an initial form in
this fixed \(H\) chart.  Accessibility/normalization into the Segre chart
remains the external global step, and no Krenn counterexample is produced.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_one_bad_segre_anchor_24cell_response_face.py
.venv/bin/python -O computations/verify_n8_one_bad_segre_anchor_24cell_response_face.py
```
