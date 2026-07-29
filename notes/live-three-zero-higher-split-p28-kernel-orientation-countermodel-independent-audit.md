# Independent audit: the opposite sheet does not orient the residual kernel

## Verdict and exact scope

**PASS.**  The model in the
[primary note](live-three-zero-higher-split-p28-kernel-orientation-countermodel.md)
is an exact polynomial counterexample to the proposed local implication

\[
 \text{triple weight at }+i
 +\text{ no ramification at }-i
 +\operatorname{ord}_{i^2}\det\eta=1
 \quad\Longrightarrow\quad [1:i]\in\ker\eta_{i^2}.
\]

It is not a realization of the complete \(4^3 3^6\) profile and therefore
is not a counterexample to Krenn's conjecture.  Its precise force is to rule
out a kernel-orientation inference from those local data alone.

## Sheet jets reconstructed over \(\mathbb Q\)

I rebuilt the displayed vectors \(E(\tau),O(\tau)\) directly and expanded
\(\sqrt{1+\tau}\) through order six.  Taylor coefficients and factorial-scaled
derivatives have the same ranks.  The two rank sequences and pivot orders are

\[
\begin{array}{c|c|c|c}
\text{sheet}&\operatorname{rank}(G^{[0]},\ldots,G^{[r]})
 &\text{pivot orders}&\text{weight}\\ \hline
+&(1,2,3,3,4,5,6)&(0,1,2,4,5,6)&3\\
-&(1,2,3,4,5,6)&(0,1,2,3,4,5)&0.
\end{array}
\]

Since \(\tau=z^2-1\) is a regular parameter at both \(z=1\) and \(z=-1\),
this independently proves the claimed exact triple sequence on the positive
sheet and the unramified sequence on the opposite sheet.

## Quotient derivative and primitive scalar

At \(\tau=0\), the reconstruction gives

\[
 E_0=e_0,\qquad O_0=e_1,\qquad E'_0=e_2,\qquad O'_0=0.
\]

Rather than reading off the stated answer, I formed a basis of covectors
annihilating \(L_0=\langle E_0,O_0\rangle\) and applied it to
\([E'_0\ O'_0]\).  The resulting quotient matrix has rank one and right
kernel

\[
                         \ker\eta_0=\langle(0,1)\rangle.
\]

Thus it is not \(\langle(1,1)\rangle\).  All twelve nonzero \(4\times4\)
minors of

\[
                         [E\ O\ E'\ O']
\]

were then computed independently.  Their monic gcd is exactly \(\tau\), not
\(\tau^2\) or a larger polynomial, so the residual determinant drop is
simple.

Finally, substituting \(\tau=z^2-1\) into

\[
                         F(z)=E(\tau)+zO(\tau)
\]

produces six coordinate polynomials of degree at most nine.  Their
\(10\times6\) coefficient matrix has rank six.  The example therefore lives
inside the correct saturated degree cap; it is not merely a formal analytic
germ.

## Consequence

The proposed degree-five interpolation closure of the \((2,4)\) branch
cannot start by assigning the six kernel directions \([1:i]\) from the two
sheet vanishing sequences.  A valid closure must use additional polynomial
information, such as both annihilator identities, another selected row, or a
global compatibility among several moving squares.

The standalone checker
[verify_live_three_zero_higher_split_p28_kernel_orientation_countermodel_independent_audit.py](../computations/verify_live_three_zero_higher_split_p28_kernel_orientation_countermodel_independent_audit.py)
imports no primary verifier and performs every calculation over \(\mathbb Q\).
