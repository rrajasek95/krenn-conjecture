# An external full Cartan column gives a separator, not automatically a unit

## Result

Let

\[
 J=\binom Mh:X\longrightarrow Y\oplus k,
 \qquad b=\binom g\alpha,
 \qquad A=(J\;b).                                     \tag{1}
\]

There is an unconditional full-column alternative.

1. If `b in im J`, choose `Jy=b`.  Then `(-y,1)` is a unit-coordinate
   kernel vector of `A`.
2. If `b` is external to `im J`, rank rises by one over `J` and there is a
   normalized left separator

   \[
                       \lambda^TJ=0,
                       \qquad\lambda^Tb=1.             \tag{2}
   \]

The second branch is not automatically the bright source-unit branch.  It
is only a Fredholm separator for the new full column until its physical
readout is identified.

Checker:
[`verify_augmented_cartan_full_column_separator_guard.py`](../computations/verify_augmented_cartan_full_column_separator_guard.py).

## Why one-rank externality is insufficient

Take `M=0`, `h=0`, and `b=(1,0)`.  The full column is external and (2)
exists, but it merely detects a new independent auxiliary column.  It does
not isolate an old nonzero optical monomial or the normalized target
constant.

The physical pure-row triangular guard is the same phenomenon in the
relevant block shape.  Let

\[
 M=\begin{pmatrix}1&-1\\2&-2\end{pmatrix},\qquad
 h=(1,-1),\qquad g=0,\qquad\alpha=1.                  \tag{3}
\]

Here `h` already lies in `row M`.  The bottom target-scalar column is
external to `J`, so (2) exists and rank rises by one.  Nevertheless the
three-by-three determinant is zero.  This is the abstract form of the
pinned result that a literal pure target row cannot repair a zero-Fitting
mixed component by itself.

## When the bright two-rank coupling occurs

A two-rank gain relative to `M` requires both independent directions:

\[
 h|_{\ker M}\ne0,
 \qquad [g]\ne0\text{ in }\operatorname{coker}M.       \tag{4}
\]

The first condition makes `J` gain one row rank over `M`; the second makes
`b` gain one column rank over `J`.  Then

\[
                  \operatorname{rank}A
                    =\operatorname{rank}M+2.           \tag{5}
\]

This is the rectangular anchor--Cartan coupling.  In a square corank-one
specialization it is the nonzero Schur product.  The checker contrasts (3)
with an exact rank-one block where `h=(1,0)` and `g=(0,1)` give the full
two-rank gain.

## Physical interpretation of the separator

The covector `lambda` in (2) is an arbitrary dual functional on the complete
coefficient/readout rows.  It closes the source proof only after one of the
following additional statements is proved:

* `lambda` is a physically typed terminal or Fitting readout;
* its row combination isolates a nonzero **old optical occurrence** after
  localization; or
* it isolates the normalized target constant.

If it isolates only the newly adjoined Cartan chain coordinate, it can be a
presentation pivot or contractible auxiliary direction rather than a
contradiction.  Therefore replacing the two-rank alternative by “the full
column is either in the image or gives a source unit” is invalid.

This also explains why anchor visibility remains load-bearing on the
determinant-bright branch of the filtered marked-lift program.

## Verification

```text
python3 computations/verify_augmented_cartan_full_column_separator_guard.py
python3 -O computations/verify_augmented_cartan_full_column_separator_guard.py
python3 -I -S computations/verify_augmented_cartan_full_column_separator_guard.py
```

Frozen ledger SHA-256:

```text
7f708b931af316b3a68b464ae1fcd0abc98530ff6194a608b9b9763fa964ad63
```
