# Four pinned one-cell lifts leave exactly four two-cell top packets

## Result

Work over the full 45-variable diagonal-carrier Segre--(K_4) chart from
`a7f8f24`.  The four one-cell directions left by the alternative identities
of `3c12db1` are

\[
  02{:}20,\qquad 03{:}10,\qquad 04{:}20,\qquad 05{:}10.
\]

For each direction, `40d4ca7` supplies a pinned exact `liftstd` source
combination of the literal top rows equal to (2).  Adjoin each of the other
75 missing decorated cells and apply the *same* source combination.  The
exact directed census is

\[
  4\cdot75=300=214\text{ preserved}+86\text{ transgressing}.
\]

The 86 directed transgressions give 80 distinct unordered pairs.  We formed
the full literal ideal of every coefficient of (q^{[3]}-X_0) only for
these 80 pairs.  Exact reduced standard bases over \(\mathbb Q\) give

\[
  80=76\text{ unit ideals}+4\text{ proper ideals}.
\]

The four proper pairs are

\[
\begin{split}
  &02{:}10+02{:}20,\qquad 03{:}10+03{:}20,\\
  &04{:}10+04{:}20,\qquad 05{:}10+05{:}20.
\end{split}
\]

Thus the first genuine two-cell top packet has a simple uniform form: on
one edge (0k), turn on both decorated cells (10) and (20).  Each ideal
has Krull dimension (9), its reduced standard basis begins with
(x_{45}-x_{46}), and its basis sizes are respectively (70,70,80,75).
Because the ideals are proper over \(\mathbb Q\), they have points over
\(\mathbb C\).  No symmetry quotient is used in this conclusion: all 80
critical ideals were computed separately.

## Exact certificate and scope

[`verify_n8_one_bad_segre_cube_pinned_lift_critical_pairs.py`](../computations/verify_n8_one_bad_segre_cube_pinned_lift_critical_pairs.py)
rebuilds the four pinned lifts, verifies their source provenance, audits all
300 second-cell substitutions, and pins the four proper reduced bases by
SHA-256.

This closes the critical-pair audit for the **four `liftstd` certificates**.
It does not repeat the separate cross-variation audit of the twelve
alternative identities.  More importantly, properness here proves a
complex solution of the unary top equation only.  It is not yet a solution
of the four diagonal/cross one-bad response equations.  The next bounded
question is therefore response feasibility on the single uniform packet
(0k{:}10+0k{:}20), not a wider two-cell support search.
