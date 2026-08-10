# The multisite cap defect is not itself a physical curved chart

## Outcome

Let a selected pair `P,Q` have the arbitrary multisite one-bad packet on
`2h` residual sites, `h>=3`,

\[
 q^{[h]}=X_0,\qquad
 p_i s_j q^{[h-1]}=\delta_{ij}X_i
 \quad(i,j\in\{1,2\}).                                  \tag{1}
\]

For the permanent-null correction

\[
 R=p_1s_1+p_1s_2-p_2s_1+p_2s_2,                         \tag{2}
\]

a nonzero `q^[h-2] R^[2]` or `q^[h-3] R^[3]` is a genuine
obstruction to the fixed clean cap.  It is **not**, however, a physical
matching of the original source and therefore does not by itself select a
second physical pair, a curved two-chart overlap, or another active clean
cap.

The obstruction is source provenance, not tensor rank.  A further theorem
must transgress the repeated endpoint-use grade through a new physical
full-nine coefficient.  Termwise identification of the cap defect with a
curved witness is invalid at every order.

## Endpoint-use grading

Give `p_1,p_2` degree `(1,0)`, `s_1,s_2` degree `(0,1)`, and `q`
degree `(0,0)`.  The two coordinates count uses of the deleted endpoints
`P,Q`.  A physical perfect matching in the `P,Q` deletion chart has only
two possibilities:

* it uses the direct edge `PQ`, leaving a residual term of grade `(0,0)`;
* it uses one `P` star and one `Q` star, leaving a residual term of grade
  `(1,1)`.

These are exactly the direct and two-star summands of every one of the nine
physical pair rows.  In contrast,

\[
 q^{[h-k]}R^{[k]}\quad\hbox{has endpoint-use grade }(k,k). \tag{3}
\]

For `k>=2`, a monomial in (3) would use each deleted endpoint at least
twice.  It lives in the Rees/Schur correction algebra after the endpoint
labels have been forgotten; it cannot be lifted termwise to an original
perfect matching.  The checker verifies explicitly that all eight
quadratic sectors have grade `(2,2)` and all sixteen cubic sectors have
grade `(3,3)`.

This proves the following sharp negative statement, uniformly in `h`:

> **Provenance obstruction.**  Nonvanishing of a repeated-label cap tail
> cannot itself be the source-provenant witness of a physical curved
> full-nine overlap.  Any valid routing must introduce an additional
> physical pair and use a full-nine row which changes the endpoint-use
> presentation, or construct an independent cap whose complete higher tail
> vanishes.

The statement does not rule out a global matching-exchange theorem using
all of (1).  It rules out the tempting direct inference “nonzero second
fundamental tensor = curved physical two-chart witness.”

## Smallest exact guard and the missing coefficient

The six-residual-site packet in
[`n8-one-bad-multisite-permanent-null-defect.md`](n8-one-bad-multisite-permanent-null-defect.md)
is the smallest literal guard.  After adjoining the normalized direct block
`A_PQ=E00`, it satisfies **eight of the nine** physical pair rows exactly:

```text
01 02 10 11 12 20 21 22 : exact, coefficient by coefficient
00                         : fails only at word 000000
```

Its sole discrepancy is

\[
 [000000]\bigl(q^{[3]}-X_0\bigr)=-1.                    \tag{4}
\]

All four binary rows are exact, including the two cross-zero tensors, yet

\[
 qR^{[2]}=2[111211]\ne0.                                \tag{5}
\]

Both literal cap-tail monomials behind (5) use an inactive arm, no displayed arm is
doubly good, and the repeated-row fan is the flat pair `E11/E11`.  Thus the
missing datum is literal and unique: the `00` diagonal full-nine coefficient
at the pure word.  The guard is not a Krenn counterexample because (4) is
precisely the unary top equation in (1).

## Exact remaining theorem

The full one-bad assumption restores (4), so the all-order proof gate is
not closed by this guard.  What remains is a source-level transgression:

> Use the pure `00` matching together with a nonzero grade `(2,2)` or
> `(3,3)` cap tail to produce either (i) a second **physical** active good
> pair with the complete diagonal and off-diagonal full-nine rows and
> nonzero overlap curvature, or (ii) a different active cap with every
> higher insertion grade zero.

No current identity performs that grade change.  The already certified
curved minimal packet shows what the landing row must look like: a mixed
off-diagonal zero coefficient sharing a localized factor with a diagonal
pure anchor.  Establishing such a private/shared factor from arbitrary
multisite cancellation is the missing matching-exchange lemma.

## Verification

Run

```sh
uv run python computations/verify_n8_one_bad_multisite_permanent_null_defect.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_multisite_permanent_null_defect.py
```

The checker audits the formal endpoint-use grades, reconstructs the literal
defect matchings, verifies all `3^6` coefficients in all nine pair rows, and
freezes (4) as the sole failure.
