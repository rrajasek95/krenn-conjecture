# The collapsed cohafnian equations admit an exact axis-pure countermodel

## Result

The polynomial equations

\[
 Q(x)=x_0Q_0+x_1Q_1+x_2Q_2,\qquad
 \operatorname {haf}(Q)=x_0^3,
\]

and

\[
 p_i^TC(Q)s_j=\delta_{ij}x_i^2,\qquad i,j\in\{1,2\},
\]

do **not** by themselves force a cohafnian-rank or Pluecker contradiction.
There is an exact rational `11`-edge countermodel.  Its failure is sharp:
the displayed equations hold only because different fully polarized site
words have been collapsed to the same colour-count monomial.  Restoring the
physical word grading exposes nonzero mixed carriers immediately.

Checker:

```text
computations/verify_h3_axis_pure_commutative_cohafnian_counterguard.py
```

Frozen ledger SHA-256:

```text
0a2bedd4201feba39c763eea8ddcbeefae2ea8ea114c65a32428c85ace8e38bb
```

## The inverse-rectangle identity

Use vertices `0,...,5`, put `q01=q23=q45=x0`, and set

\[
\begin{array}{c|cccc}
 &q_{14}&q_{15}&q_{34}&q_{35}\\ \hline
x_1\text{-coefficient}&a&f&g&b
\end{array},\qquad
\begin{array}{c|cccc}
 &q_{04}&q_{05}&q_{24}&q_{25}\\ \hline
x_2\text{-coefficient}&h&c&d&e.
\end{array}
\]

All other edges vanish.  For `p1=e0,p2=e1,s1=e2,s2=e3`, the selected
cohafnian block is

\[
 \begin{pmatrix}x_1&0\\0&x_2\end{pmatrix}
 \underbrace{\begin{pmatrix}a&f\\h&c\end{pmatrix}}_U
 \underbrace{\begin{pmatrix}b&e\\g&d\end{pmatrix}}_V
 \begin{pmatrix}x_1&0\\0&x_2\end{pmatrix}.            \tag{1}
\]

Thus the four response equations are exactly `UV=I`.  Meanwhile

\[
 \operatorname {haf}(Q)=x_0^3+
 (ac+fh+bd+eg)x_0x_1x_2.                              \tag{2}
\]

If `V=U^{-1}` and `D=det(U)`, the leakage coefficient is

\[
             (ac+fh)(1+D^{-2}).                       \tag{3}
\]

It can vanish with `U` invertible.  Take

\[
 U=\begin{pmatrix}1&1\\-1&1\end{pmatrix},\qquad
 V={1\over2}\begin{pmatrix}1&-1\\1&1\end{pmatrix}. \tag{4}
\]

Then `UV=I`, `det(U)=2`, and (2) is exactly `x0^3`.  Hence neither the
cohafnian sandwich nor its obvious determinant/Pluecker consequences can
exclude the collapsed packet.

## Full polarization reveals the carrier

The cancellation in (2) is not physical.  Its four nonzero mixed unary
coefficients occur on four distinct site words:

```text
002121 :  1/4
002112 : -1/4
210021 : -1
210012 :  1
```

They sum to zero only after all words with colour count `(2,2,2)` are
identified with `x0*x1*x2`.  The two aggregate-zero crossed response
cofactors behave the same way: their two matching terms occupy distinct
response words, rather than cancelling inside one physical coefficient.

Therefore this matrix is not a physical exact source, and it does not
contradict the existing support lower bounds.  It instead freezes the exact
limit of the proposed algebraic shortcut:

> A proof cannot use only `Haf(Q)` and the four commutative cohafnian
> entries.  It must retain the full wordwise cohafnian equations (or prove a
> source-valid polarization lift).  In the inverse-rectangle packet above,
> that refinement immediately produces a nonzero mixed carrier.

This is support-free and independent of the finite axis-pure census.
