# Mixing literal cycles can repair the aggregate Hessian pullback

## 1. Outcome

The four individual cycle normals in the
[all-cycle seven-row guard](two-anchor-hessian-all-cycle-seven-row-guard.md)
all miss the row space of the scalar \(K_6\) hafnian Hessian.  Their span
does not.  In that exact corank-one packet,

\[
 \lambda=2\,d\kappa_{25}^{(0)}{}_q
              -d\kappa_{25}^{(1)}{}_q                    \tag{1}
\]

still detects the cap edge \(\beta=\mathbf e_{01}\), but annihilates the
whole Hessian kernel.  Hence it has an explicit four-set pullback.

This is a positive aggregate repair.  It shows that failure of every
*individual* dark-cycle choice is not yet a failure of their linear span.
It does not show that the two orientations can be combined before the
common matching power while preserving the physical direct/star/internal
grading.  That is precisely the filtered source-provenance problem.

## 2. The cycle-span criterion

Let \(H:E\to E^*\) be any symmetric linear map, let
\(Z=\ker H\), fix a cap direction \(\beta\in E\), and let
\(\lambda_1,\ldots,\lambda_k\in E^*\) be candidate curvature normals.
Define

\[
 \begin{aligned}
 R:\mathbb C^k&\longrightarrow Z^*,
 &R(a)(z)&=\sum_i a_i\lambda_i(z),\\
 b&=(\lambda_1(\beta),\ldots,\lambda_k(\beta))
       \in(\mathbb C^k)^* .                              \tag{2}
 \end{aligned}
\]

Then there is a combination

\[
 \lambda(a)=\sum_i a_i\lambda_i\in\operatorname {row}H,
 \qquad \lambda(a)(\beta)\ne0                            \tag{3}
\]

if and only if

\[
                         b\notin\operatorname {im}R^*.    \tag{4}
\]

Indeed, symmetry gives
\(\operatorname {row}H=Z^\perp\), so compatibility is exactly
\(a\in\ker R\).  Such an \(a\) can be detected by \(b\) exactly when
\(b\) does not annihilate \(\ker R\).  The annihilator of \(\ker R\) is
\(\operatorname {im}R^*\), proving (4).

If \(H\) has corank one and \(z\) spans its kernel, put

\[
                         h=(\lambda_i(z))_{i=1}^k.        \tag{5}
\]

Criterion (4) becomes the elementary test

\[
        \boxed{\text{a detecting compatible mixture exists}
                    \iff b\notin\mathbb C h.}             \tag{6}
\]

Thus checking each coordinate \(h_i\ne0\) is insufficient: those values
must be compared with the cap-detection vector \(b\).

## 3. Exact repair of the corank-one guard

Use the support, cap, and kernel from the cited guard:

\[
\begin{aligned}
 Q={}&\{01,02,03,04,05,13,14,23,25,34\},\\
 \beta={}&\mathbf e_{01},\\
 z={}&\mathbf e_{01}-\mathbf e_{04}-\mathbf e_{12}
                         +\mathbf e_{24},
 \qquad \ker H_q=\mathbb Cz .                           \tag{7}
\end{aligned}
\]

Order the four literal normals by

\[
 (25,0),(25,1),(34,0),(34,1).
\]

Their two evaluation vectors are

\[
                         b=(1,1,1,1),
 \qquad                   h=(1,2,1,2).                   \tag{8}
\]

They are not proportional.  Taking
\(a=(2,-1,0,0)\) gives \(a\cdot h=0\) and \(a\cdot b=1\).
After inserting the \(0/1\) edge values, (1) is

\[
 \boxed{\lambda=
     \mathbf e_{01}^*+\mathbf e_{12}^*
       -2\mathbf e_{15}^*+\mathbf e_{25}^*.}             \tag{9}
\]

It satisfies

\[
                         \lambda(z)=0,
 \qquad                   \lambda(\beta)=1.              \tag{10}
\]

An explicit pullback, written in the complementary-edge indexing of the
four-set space, is

\[
\begin{aligned}
 \theta={}&-\tfrac34\mathbf e_{02}+\tfrac34\mathbf e_{03}
 -\tfrac34\mathbf e_{04}+\tfrac34\mathbf e_{12}
 +\tfrac34\mathbf e_{13}-\tfrac34\mathbf e_{15}\\
 &-\tfrac34\mathbf e_{23}+\tfrac14\mathbf e_{34}
 +\tfrac34\mathbf e_{45}.                                \tag{11}
\end{aligned}
\]

Direct multiplication gives

\[
                              H_q\theta=\lambda.          \tag{12}
\]

Thus the guard has no aggregate Hessian obstruction once these two
orientation normals may be mixed.

## 4. Exact scope

The result replaces a four-way literal choice by one small linear system.
For a general scalar base of larger Hessian corank, (4), not the
coordinatewise tests, is the exact condition.  No universal assertion that
(4) always holds is made here.

More importantly, (12) lives only in the scalar matching algebra.  The
[filtered provenance criterion](hessian-pullback-filtered-source-provenance.md)
still requires the mixture to lie in the image of the literal cap-family
top rows, enlarged only by genuinely admitted overlap grades.  The
[sum-channel guard](two-chart-selector-provenance-sum-channel-guard.md)
shows why simply adding the two Bianchi orientations does not establish
that source validity.  The two missing diagonal anchors may still be the
mechanism which makes (1) grade-preserving, but they are not needed merely
to solve the aggregate row-space equation in this guard.

The dependency-free
[checker](../computations/verify_k6_cycle_span_hessian_mixing.py) reuses the
audited guard data and verifies (8)--(12), including the explicit rational
pullback and the unchanged nonzero cap detection.
