# Higher splits: consecutive constant-core role transfers

## 1. Uniform theorem

Put

\[
 h=t-r-1,\qquad p=h+k,\qquad k\ge1.                       \tag{1}
\]

Assume all isolated-star pivots vanish.  Fix three exceptional value
classes \(A,B,C\).  Suppose that, for \(n=0,\ldots,k\), the selection

\[
                    A^{a+n}B^{b-n}C^j,\qquad
                    a+b+j=h,                              \tag{2}
\]

uses positive available multiplicities and leaves a singleton class in its
complement.

**Theorem 1.1 (consecutive role transfer).**  The \(k+1\) selections
(2) cannot all be legal on the no-extra-singular stratum.

Every selection represents three value classes, so its Hermite residual is
a nonzero constant.  Transferring one selected label from \(B\) to \(A\)
multiplies the normalized regular common-pole cofactor by one fixed unit
\(R(w)\).  The order-\(k\) residue is therefore a degree-\(k\) polynomial
in the transfer count \(n\), with a structurally nonzero leading
coefficient.  It cannot vanish at \(0,1,\ldots,k\).

This theorem is different from the moving-value root bound: the value
classes \(A,B,C\) stay fixed while their two selected multiplicities move.

## 2. The transfer unit

Write \(w=z+\mu\).  A selected role \(r\) at value \(x\) contributes the
normalized unit

\[
 \widehat\rho_{r,x}(w)=
 \left(1-{w\over x+\mu}\right)^{-r}
 \left(1+{w\over x-\mu}\right)^{-(r+1)}.                 \tag{3}
\]

Changing \(r\) to \(r+1\) multiplies (3) by

\[
 I_x(w)=
 \left(1-{w\over x+\mu}\right)^{-1}
 \left(1+{w\over x-\mu}\right)^{-1}.                     \tag{4}
\]

Thus one transfer \(B\to A\) multiplies the common cofactor by

\[
                         R(w)={I_A(w)\over I_B(w)},
 \qquad R(0)=1.                                          \tag{5}
\]

Its first logarithmic jet is

\[
\begin{split}
 \gamma
   &:=(\log R)'(0)\\
   &=-{2\mu\over A^2-\mu^2}
      +{2\mu\over B^2-\mu^2}\\
   &={2\mu(A-B)(A+B)\over
      (A^2-\mu^2)(B^2-\mu^2)}\ne0.                       \tag{6}
\end{split}
\]

The last inequality uses the standing cyclic-stratum facts
\(\mu\ne0\), \(A,B\ne\pm\mu\), and that distinct exceptional values are
nonopposite.

All factors independent of \(n\), including the fixed role at \(C\), form
one unit \(U(w)\) with \(U(0)\ne0\).  The scalar constant Hermite residual
may vary with \(n\), but it is nonzero and cancels from the zero-residue
condition.  Hence every selection (2) gives

\[
                         [w^k]\,U(w)R(w)^n=0.             \tag{7}
\]

## 3. Exact finite difference

Put

\[
                         f(n)=[w^k]\,U(w)R(w)^n.          \tag{8}
\]

Since

\[
 R(w)^n=\exp\!\bigl(n\log R(w)\bigr),\qquad
 \log R(w)=\gamma w+O(w^2),                              \tag{9}
\]

\(f(n)\) is a polynomial in \(n\) of degree at most \(k\).  Its leading
coefficient is

\[
                         {U(0)\gamma^k\over k!}\ne0.      \tag{10}
\]

Equivalently, its \(k\)-th forward difference is the nonzero constant

\[
                         \Delta^k f(n)=U(0)\gamma^k.      \tag{11}
\]

Equation (7) says that \(f\) vanishes at the \(k+1\) consecutive integers
\(0,\ldots,k\), contradicting (10) or (11).  This proves Theorem 1.1.

## 4. First \(k=3\) application

At

\[
                 (h,k;\lambda)=(8,3;(4,4,4,3,3,3)),      \tag{12}
\]

choose the three quartic classes \(A,B,C\), select three labels at \(C\),
and use the four cores

\[
                    A^1B^4C^3,\quad A^2B^3C^3,\quad
                    A^3B^2C^3,\quad A^4B^1C^3.           \tag{13}
\]

All are available and legal: the single unselected mate at the fixed
quartic \(C\) is a singleton in every complement.  Their three-class
residuals are nonzero constants.  Theorem 1.1 with \(k=3\) therefore
eliminates (12), the first profile in the updated \(h=8,k=3\) collision
frontier.

For \(k=2\), the same theorem applied to three consecutive transfers is
the independent quartic-role check used in the closure of
\((4,4,3,3,3,3)\).

## 5. Audit

[verify_live_three_zero_higher_split_consecutive_role_transfer.py](../computations/verify_live_three_zero_higher_split_consecutive_role_transfer.py)
checks the exact normalized transfer factor, the nonzero first jet,
the degree and leading coefficient in \(n\) through order eight, the
finite-difference identity, every complement in (13), and the location of
(12) in the exact old \(h=8,k=3\) residual census.
