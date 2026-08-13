# Scalar Fermat equality is too coarse: an exact signed-interference countermodel

Checker:
[`computations/verify_n8_scalar_fermat_signed_interference_countermodel.py`](../computations/verify_n8_scalar_fermat_signed_interference_countermodel.py).

## 1. The tempting scalar reduction

For an eight-site source with endpoint blocks (A_{uv}), identify the output
variables at every site and write

\[
 B_{uv}(x)=\sum_{a,b=0}^2 A_{uv}(a,b)x_ax_b.
\]

Exact tensor equality would imply the necessary scalar identity

\[
 \operatorname{haf}(B(x))=x_0^8+x_1^8+x_2^8. \tag{1}
\]

This is an attractive interference invariant: the left side retains all
matching amplitudes and their signs.  It nevertheless forgets *where* each
colour was detected.  The loss is fatal.

## 2. An integral five-matching construction

Use only the following colour-diagonal edge quadratics:

\[
\begin{array}{c|c@\qquad c|c@\qquad c|c}
01&-x_0^2&02&x_1^2&03&x_2^2\\
23&-x_0^2&45&x_0^2&67&x_0^2\\
14&x_1^2&36&x_1^2&57&x_1^2\\
15&x_2^2&27&x_2^2&46&x_2^2.
\end{array} \tag{2}
\]

All omitted edges are zero.  Deleting respectively sites (1,2,3) from
the seven-site internal packet gives

\[
 H_1=-x_0^6,
 \qquad H_2=x_1^6,
 \qquad H_3=x_2^6. \tag{3}
\]

The first identity contains the interference.  Besides
(23|45|67), there are exactly two mixed internal matchings,
(23|46|57) and (27|36|45), with the same scalar monomial and opposite
signs.  Expanding the full hafnian at site (0) therefore gives

\[
 (-x_0^2)(-x_0^6)+x_1^2x_1^6+x_2^2x_2^6
 =x_0^8+x_1^8+x_2^8. \tag{4}
\]

The checker reconstructs (3)--(4) by exact integer polynomial arithmetic
and independently enumerates all 105 perfect matchings.

Its frozen exact ledger is
`a1ab0292e17c8000ec081afd2599180dc723dad66b1c0cee4378b1f92a376f3f`.

## 3. Why this is not a tensor source

Exactly five physical matchings survive.  Three are the desired pure
matchings.  The remaining two contribute

\[
 +x_0^4x_1^2x_2^2,
 \qquad -x_0^4x_1^2x_2^2 \tag{5}
\]

after scalarization, so (5) cancels.  Before scalarization their output
words are different:

\[
 00002121,
 \qquad 00210012. \tag{6}
\]

Their tensor coefficients are (+1) and (-1), respectively.  They
therefore cannot cancel in the physical output basis.  This is consistent
with the proved colour-diagonal obstruction: (1) is strictly weaker than
the coefficientwise monochromatic equations.

## 4. Proof-frontier consequence

No proof can finish the conjecture using only the diagonal scalar hafnian
polynomial, its Fermat form, or an invariant that identifies output words
having the same colour multiplicities.  Signed interference is indeed the
right phenomenon, but the proof must retain the **fine detector word** (or
an equivalent source-labelled grading).  In the active-route frontier this
means that cycle holonomy must be evaluated in the typed matching complex,
not in its scalar projection.

This countermodel does not satisfy the full tensor equations and is not a
counterexample to the conjecture.  It is a sharp guard against a coarser
proof strategy.
