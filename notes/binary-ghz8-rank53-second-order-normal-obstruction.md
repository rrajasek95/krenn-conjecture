# Second-order obstruction to the two non-chart rank-53 tangents

This is an exact formal-local statement at the rational rank-53 binary GHZ8
seed. It does not classify distant components or the unrestricted binary
GHZ8 fibre.

## Tangent decomposition

At the rational seed (A^ast), the full `256 x 112` GHZ Jacobian has rank
84 and hence nullity 28. The rational chart contributes 26 tangent
directions. Exact reduction of the 67 missing-cell columns modulo the chart
image leaves a two-dimensional kernel, with convenient free missing
coordinates

\[
                 (4,7,1,1),\qquad (5,6,0,0).
\]

Call the corresponding exact tangent lifts (T_0,T_1). The first uses 12
missing cells and the second uses 5, so the earlier one-/two-cell tangent
isolation does not see them.

## Quadratic obstruction

For a tangent (T), a second-order lift

\[
 A(s)=A^ast+sT+s^2R+O(s^3)
\]

requires the quadratic matching coefficient (H(T,T)) to lie in the image
of the full Jacobian (J). Three sparse exact functionals in the left
cokernel of (J) are

\[
 \lambda_0=[11001000]-\frac{1175}{258}[01001000],
\]

\[
 \lambda_1=[11101000]-\frac{1175}{258}[01101000],
 \qquad
 \lambda_2=[01100000].
\]

Here brackets denote coefficient rows indexed by binary words. On the three
normal quadratic coefficients they give the diagonal matrix

\[
\begin{pmatrix}
 \dfrac{1566568103750000}{145242430893}&0&0\\
 0&\dfrac{631124000000}{21744264209}&0\\
 0&0&-\dfrac{6048000}{27732773}
\end{pmatrix}
\]

with columns (H(T_0,T_0)), (B(T_0,T_1)), and (H(T_1,T_1)).
Thus the (a^2,ab,b^2) normal coefficients are independent in
\(operatorname{coker}J\).

This obstruction cannot be canceled by changing the chart-tangent part of
the first derivative. Exact calculation shows that all 351 chart-chart
quadratic terms and all 52 chart-normal cross terms vanish under the three
functionals. Consequently, for

\[
             T=C+aT_0+bT_1,qquad C\in T_{A^ast}\mathcal C,
\]

the three necessary second-order equations include nonzero scalar multiples
of (a^2,ab,b^2). A second-order lift therefore forces (a=b=0).

The checker
[verify_binary_ghz8_rank53_second_order_normal_obstruction.py](../computations/verify_binary_ghz8_rank53_second_order_normal_obstruction.py)
reconstructs all tangent vectors, verifies the three cokernel functionals,
and checks the 403 chart-containing quadratic reductions using exact
`Fraction` arithmetic.

## Scope

The theorem excludes a second-order lift whose first derivative has a
nonzero class transverse to the rational chart. It explains the observed
quadratic residual scaling in numerical continuation of (T_0,T_1).

It does not exclude a formal arc tangent to the chart to first order and
leaving it only at a higher order, a component whose closure does not contain
(A^ast), or a distant exact source. In particular it gives no global
rank-53 bound and no conclusion about rank 54 or 55 elsewhere.
