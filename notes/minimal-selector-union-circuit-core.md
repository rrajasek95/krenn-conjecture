# A minimal selector-union failure has one small flag core

## 1. Outcome

Let \(W\) have six sites, and let \(M_P,M_S\) be the rank-three Rado
matroids of the endpoint-star local row spaces

\[
 L_x^P=\operatorname{im}(P_x^*:V_x^*\to C^*),\qquad
 L_x^S=\operatorname{im}(S_x^*:V_x^*\to D^*).
\tag{1}
\]

Disjoint endpoint selector bases exist exactly when

\[
 \rho_P(B)+\rho_S(B)\ge |B|
 \qquad(B\subseteq W).
\tag{2}
\]

The following reduction was checked in
[the independent audit](minimal-selector-union-circuit-core-independent-audit.md).

**Theorem 1.1 (minimal deficient-core reduction).**  If (2) fails, there
is a nonempty \(A\subsetneq W\), with \(k=|A|\le5\), such that

\[
 \rho_P(A)+\rho_S(A)=k-1,\qquad
 \rho_T(A\setminus\{x\})=\rho_T(A)
 \quad(x\in A,\ T\in\{P,S\}).
\tag{3}
\]

Thus \(A\) is a circuit of \(M_P\vee M_S\), and neither restricted
matroid has a coloop.  More strongly, every minimizing Rado witness for
\(\rho_T(A)\) is all of \(A\).  Consequently

\[
 \rho_T(A)=\dim\sum_{x\in A}L_x^T
\tag{4}
\]

and, at every \(x\in A\),

\[
 \operatorname{rank}(P_x^*\oplus S_x^*)\le k-1.
\tag{5}
\]

There are exactly three size ranges.

1. **Endpoint-dark circuit:** \(k\le3\).  Every site of \(A\) has a
   nonzero physical covector annihilating both endpoint stars.
2. **Four-site flag circuit:** \(k=4\).  The two aggregate endpoint
   row-span dimensions on \(A\) are \((1,2)\) or \((2,1)\).
3. **Common aggregate-rank-two coloop:** \(k=5\).  Both aggregate
   endpoint maps on \(A\) have rank two, and the unique site in
   \(W\setminus A\) is a coloop of both selector matroids.

In a complete literal six-site full-nine packet, case 3 is the
same-site rank-two input of
[the full-nine shore theorem](full-nine-rank-two-shore-coordinate-support.md).
That theorem reduces the branch to a zero, unary, or binary \(q^{[3]}\),
or to coordinate-disjoint fixed-label kernel supports.  It does not close
those alternatives; their stronger uniform treatment is in
[the common-coloop residual coupling](common-coloop-full-nine-residual-coupling.md).

The routing in the preceding paragraph is specific to the complete
\(6=2h\), \(h=3\) packet.  A deficient circuit selected from a larger
\(2h\)-site residual does not by itself preserve the off-site rank or
common-power hypotheses.

The theorem therefore replaces arbitrary deficient-flat classification by
three exact coefficient ledgers.  It does not prove the missing
coefficient implication in the endpoint-dark or four-site flag branches.

## 2. Minimal failure is a union circuit

Choose \(A\subseteq W\) inclusion-minimal with

\[
 \rho_P(A)+\rho_S(A)<|A|.
\tag{6}
\]

For \(x\in A\), minimality and monotonicity give

\[
\begin{aligned}
 \rho_P(A\setminus\{x\})+\rho_S(A\setminus\{x\})
   &\ge |A|-1,\\
 \rho_P(A\setminus\{x\})+\rho_S(A\setminus\{x\})
   &\le \rho_P(A)+\rho_S(A)\le |A|-1.
\end{aligned}
\tag{7}
\]

All inequalities are equalities.  The two individual ranks cannot
increase after deletion, so

\[
 \rho_T(A\setminus\{x\})=\rho_T(A)
 \quad(T=P,S).
\tag{8}
\]

Every proper subset of \(A\) satisfies the matroid-union inequalities,
whereas \(A\) does not.  Therefore \(A\) is a circuit of
\(M_P\vee M_S\).  Also \(A\ne W\), since

\[
 \rho_P(W)+\rho_S(W)=3+3=6=|W|.
\tag{9}
\]

This proves (3) and \(k\le5\).  Adding the \(6-k\) omitted sites can raise
either rank by at most \(6-k\), hence

\[
 \rho_T(A)\ge3-(6-k)=k-3.
\tag{10}
\]

Together with nonnegativity and
\(\rho_P(A)+\rho_S(A)=k-1\), this gives

\[
\begin{array}{c|c}
k&(\rho_P(A),\rho_S(A))\\ \hline
1&(0,0)\\
2&(0,1),(1,0)\\
3&(0,2),(1,1),(2,0)\\
4&(1,2),(2,1)\\
5&(2,2).
\end{array}
\tag{11}
\]

## 3. Deletion stability rigidifies the Rado witness

The Rado rank formula is

\[
 \rho_T(A)=\min_{J\subseteq A}
 \left(|A\setminus J|+
       \dim\sum_{y\in J}L_y^T\right).
\tag{12}
\]

Let \(J_T\) be any minimizing witness.  If
\(x\in A\setminus J_T\), then the same witness in
\(A\setminus\{x\}\) gives

\[
\begin{aligned}
 \rho_T(A\setminus\{x\})
 &\le |(A\setminus\{x\})\setminus J_T|
      +\dim\sum_{y\in J_T}L_y^T\\
 &=\rho_T(A)-1,
\end{aligned}
\tag{13}
\]

contradicting (8).  Hence

\[
 \boxed{J_P=J_S=A.}
\tag{14}
\]

Formula (4) follows.  Since
\(L_x^T\subseteq\sum_{y\in A}L_y^T\), the two endpoint targets being
direct summands gives

\[
\begin{aligned}
 \operatorname{rank}(P_x^*\oplus S_x^*)
 &\le \dim\sum_{y\in A}L_y^P+
       \dim\sum_{y\in A}L_y^S\\
 &=\rho_P(A)+\rho_S(A)=k-1.
\end{aligned}
\tag{15}
\]

This proves (5).

## 4. The three exact circuit sizes

If \(k\le3\), (15) bounds a map from the three-dimensional space
\(V_x^*\) by rank at most two.  Its kernel is a nonzero physical covector
annihilating both endpoint stars.  This holds at every \(x\in A\).

If \(k=4\), (11) and (4) give aggregate linear row-span dimensions
\((1,2)\) or \((2,1)\).  This is the unique flag core; the five-site
one-plus-two candidate from the preliminary witness count is impossible
by (13).

If \(k=5\), both aggregate spans have dimension two.  Writing
\(W\setminus A=\{x_0\}\), each full matroid has rank three, so \(x_0\)
raises both ranks and is a coloop of each.  This proves Theorem 1.1.
\(\square\)

## 5. Exact remaining coefficient target

The independently audited selector guards show why the abstract theorem
cannot close the source problem by itself.

* Endpoint-dark covectors need not kill the incident internal quadratic
  stars or meet the required fixed-target coordinates.
* Even separated fixed-label selectors need not possess an own-edge
  Jacobian lift when the diagonal targets are omitted.
* A common-rank-two coloop in a selected restriction is not automatically
  a common coloop of the complete uniform packet.

The source-level target is now:

> **Deficient-circuit coefficient target.**  Under all nine literal
> response rows on the complete rootless packet, a minimal selector-union
> circuit either supplies the complete coefficient-dark hypotheses of the
> audited three-row contradiction, enters the uniform common-coloop
> curvature quotient, or has the four-site \((1,2)\) flag geometry and
> produces a source-faithful overlap coefficient that annihilates the
> residual Macaulay image.

No unbounded matroid census remains.  The only coloop-free, non-dark
selector obstruction is the four-site line-plus-plane circuit.  A uniform
proof must compare its coefficient chart with the actual remaining common
power rather than treating a six-site restriction as an independent
\(h=3\) source.
