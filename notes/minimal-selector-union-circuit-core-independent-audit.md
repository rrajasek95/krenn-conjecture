# Independent audit: minimal selector-union circuit core

## Verdict

**PASS AFTER CORRECTION.**  The initial draft's matroid-union reduction,
deletion equalities, rank-pair table, endpoint-dark consequence, and
five-site common-rank-two branch were correct.  The audit found a sharper
consequence: equation (3) forces **every** minimizing Rado witness to be
all of \(A\).  The source note now includes that lemma and has removed the
impossible five-site \(d=3,t=1\) flag core.  Only the four-site aggregate
rank pair \((1,2)\) or \((2,1)\) remains as a flag core.

The citation of the full-nine rank-two-shore theorem is valid only when
the six sites are the complete \(h=3\) packet and all nine literal
fixed-label equations hold.  For six sites selected from a larger
\(2h\)-site packet, the matroid conclusion alone does not provide that
theorem's off-site rank or common-power hypotheses.  The source note's
outcome and final paragraph now both state this qualification explicitly.

## 1. Minimal union circuit and rank pairs: PASS

For an inclusion-minimal set \(A\) with

\[
 \rho_P(A)+\rho_S(A)<|A|,
\]

minimality gives the lower bound \(|A|-1\) after deleting any \(x\in A\),
whereas monotonicity bounds the same sum above by
\(\rho_P(A)+\rho_S(A)\le |A|-1\).  Hence

\[
 \rho_P(A)+\rho_S(A)=|A|-1,
 \qquad
 \rho_T(A\setminus\{x\})=\rho_T(A)
 \quad(T=P,S).
\]

Thus every proper subset is independent in \(M_P\vee M_S\), while \(A\)
is dependent, so \(A\) is indeed a union-matroid circuit.  Since each
full matroid has rank three on the six-element set, \(A\ne W\), and adding
the \(6-|A|\) omitted sites proves

\[
 \rho_T(A)\ge |A|-3.
\]

Together with the sum \(|A|-1\), this yields exactly the rank pairs in
source display (11).  There is no confusion between matroid rank and
aggregate linear rank in this part.

## 2. The missing witness lemma

Let \(J_T\subseteq A\) minimize the Rado formula and retain the source
notation

\[
 \rho_T(A)=|A\setminus J_T|
       +\dim\sum_{y\in J_T}L_y^T.
\]

If \(x\in A\setminus J_T\), then the same witness used for
\(A\setminus\{x\}\) gives

\[
\begin{aligned}
 \rho_T(A\setminus\{x\})
 &\le |(A\setminus\{x\})\setminus J_T|
       +\dim\sum_{y\in J_T}L_y^T\\
 &=\rho_T(A)-1.
\end{aligned}
\]

This contradicts the already-proved deletion equality
\(\rho_T(A\setminus\{x\})=\rho_T(A)\).  Therefore

\[
 \boxed{J_P=J_S=A.}
\]

In particular every minimizing witness has this form, and the witness
parameters simplify to

\[
 t_P=t_S=t=0,
 \qquad C_0=A,
 \qquad d_T=\dim\sum_{x\in A}L_x^T=\rho_T(A),
 \qquad d=|A|-1.
\]

The original draft's inequality \(|C_0|\ge d+1\) was correct, but the
stronger witness lemma makes it equality.  Likewise the bound

\[
 \operatorname{rank}(P_x^*\oplus S_x^*)
 \le d_P+d_S=d
\]

is correct for every \(x\in A\).  For \(|A|\le3\), it gives a common
nonzero endpoint-dark physical covector at every site of \(A\), not only
at an unspecified subcollection.

## 3. Corrected classification

The exact possibilities are consequently:

1. \(k=1,2,3\): \(d=k-1\le2\), so all \(k=d+1\) circuit sites are
   endpoint-dark in the stated sense.
2. \(k=4\): \(d=3\), \(J_P=J_S=A\), and the aggregate linear row-span
   dimensions are \((1,2)\) or \((2,1)\).  This is the sole flag core.
3. \(k=5\): \(d=4\), \(J_P=J_S=A\), and both aggregate linear row-span
   dimensions are two.  The unique site \(x_0\in W\setminus A\) raises
   each full rank from two to three and is therefore a coloop of both
   matroids.

The proposed \(k=5,d=3,t=1\) branch can also be contradicted directly.
In its notation, if \(J_P=A\setminus\{z\}\) spans one line, then

\[
 \rho_P(A\setminus\{z\})=\rho_P(J_P)
 \le \dim\sum_{x\in J_P}L_x^P=1,
\]

whereas the rank pair gives \(\rho_P(A)=2\) and equation (3) requires the
deleted rank still to be two.

## 4. Scope of the rank-two-shore routing

In the genuine six-site full-nine packet, the \(k=5\) branch does match
the hypotheses of
[the rank-two-shore theorem](full-nine-rank-two-shore-coordinate-support.md):

* \(d_T=2\) is the dimension of
  \(\sum_{x\in A}L_x^T\), hence the rank of the combined primal endpoint
  map restricted away from the same site \(x_0\), not merely an abstract
  matroid rank;
* \(\rho_T(W)=3\) forces the global combined dual map to be surjective and
  hence the primal endpoint map to be injective; and
* with all nine literal equations and \(|W|=6=2h\), one has \(h=3\).

The cited theorem then genuinely reduces this branch to
\(q^{[3]}\) supported on at most two monochromatic targets (including
zero), or to kernel vectors with disjoint fixed-coordinate supports.
It does **not** close those alternatives.  Similarly, endpoint-darkness
does not supply the missing internal-star and target-incidence hypotheses,
and the four-site flag core is not excluded by the present argument.  The
source note is appropriately explicit that both of those coefficient
implications remain open.

For a larger uniform packet, a common coloop only in a selected six-site
restriction does not imply rank two away from that site among all \(2h\)
sites, and restriction does not automatically preserve a literal
\(q^{[3]}\) system.  No uniform full-nine conclusion follows until that
common-power extraction step is proved.

## 5. Corrections applied

The source note now:

1. proves the missing-witness lemma \(J_P=J_S=A\);
2. deletes the impossible five-site one-plus-two flag alternative; and
3. describes the rank-two branch as a reduction, qualified by the complete
   six-site \(h=3\) full-nine hypotheses.
