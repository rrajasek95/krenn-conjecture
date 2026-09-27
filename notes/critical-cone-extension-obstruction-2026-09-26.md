# A quadratic-cone direction with an unavoidable cubic error

September 26, 2026. **Exact characteristic-zero example and rejection
certificate; analytic interpretation awaiting independent audit.**

[Replay and explicit fixture](../computations/critical-cone-2026-09-26/README.md) ·
[Earlier fourth-order identity](critical-core-higher-jets-2026-09-26.md)

At the completely singular source \(Q\), write
\(A(t)=Q+tB+t^2C+\cdots\). The previous result gives

\[
 H_2=QB^{[2]},\qquad H_3=QBC+H(B).
\]

A near-GHZ arc at this base must cancel both of these orders before a
nonzero target can appear. Testing only \(H_2=0\) is insufficient.

## 1. The quartic shortcut fails over the complex numbers

There is a sixteen-cell first direction \(B\), given in
[fixture.json](../computations/critical-cone-2026-09-26/fixture.json), for which

\[
 QB^{[2]}=0,
 \qquad
 \sum_{e\subset\{0,\ldots,4\}}
       \frac{B_e(b,b)}{2q_e}H_{w(e,b)}(B)=-\omega\ne0.   \tag{1}
\]

Here \(q_e=Q_e(a,a)\), and \(w(e,b)\) puts \(a\) on the endpoints
of \(e\) and \(b\) elsewhere. Thus the quartic expression from the earlier
note does not vanish on the whole quadratic cancellation cone. A proof
claiming that it does would be false even over \(\mathbb Q(\omega)\).

For a compact specification of \(B\), its root cells are
\(B_{05}(b,b)=B_{45}(b,b)=B_{35}(a,b)=1\). Its core \(bb\) cells are
\(B_{01}=B_{02}=-1\), \(B_{14}=B_{24}=1\). Its remaining core cells are:

| Edge | Endpoint colors | Weight |
|---|---|---|
| 01 | ab | \(-1-\omega\) |
| 02, 03 | ab | \(\omega\) |
| 12 | ab | \(-\omega\) |
| 12, 13 | ba, ab respectively | \(1+\omega\) |
| 13 | ba | \(-\omega\) |
| 23 | ba | \(1+\omega\) |
| 34 | ba | \(1\) |

Every unlisted cell is zero. Equation (1) is checked against all 729 ternary
quadratic output coefficients, not only a selected palette of constraints.

## 2. This direction cannot be extended to cancel cubic error

The same direction has the stronger obstruction

\[
 \boxed{(H_3)_{aabbbb}+(1+\omega)(H_3)_{ababbb}
        -(H_3)_{babbab}+(H_3)_{bbabab}=2\omega.}           \tag{2}
\]

All four words are off target. The linear combination of \(QBC\) in (2)
is zero for **every one of the 135 complex entries of \(C\)**. The remaining
combination of \(H(B)\) is exactly \(2\omega\). The next source jet also
cannot help at this order, because \(DH(Q)=0\).

Consequently this first direction cannot start a near-GHZ arc, even though
it cancels all quadratic output and makes the formal quartic expression
nonzero. Equation (2) is a four-coordinate left-null certificate for failure
of the cubic extension equation.

In fact the vector of these four cubic errors has norm at least one:
the coefficient vector in (2) has norm two, while \(|2\omega|=2\).

## 3. Consequence for the search

The useful sequence of tests is now explicit:

1. Solve the quadratic cancellation equations for a first direction.
2. Test the linear cubic extension equation in the free second jet.
3. Analyze the quartic target only for directions that pass both tests.

The package includes exploratory finite-field and exact search scripts, but
its acceptance checker uses a saved exact fixture and verifies (1)--(2)
directly. It rejects a corrupted first direction and a corrupted witness.
No finite-field sample is being treated as a characteristic-zero proof.

This rejects one exact direction and one proposed universal shortcut. It
does not classify every extendable direction, prove a fifth-order onset,
or disprove the unrestricted square-root rate law.
