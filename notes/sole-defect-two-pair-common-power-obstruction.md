# Two physical pairs remain impossible with one deficient local frame

## 1. Exact theorem

Let \(U\) be a six-set with distinguished site \(o\).  At every good site
\(v\ne o\), choose independent vectors
\(a_0^{(v)},a_1^{(v)},a_2^{(v)}\).  At \(o\), choose three arbitrary
nonzero vectors whose span has dimension at most two.  For a field \(r\)
and pair \(R\), put

\[
                         A_r(R)=\bigotimes_{u\notin R}a_r^{(u)}.   \tag{1}
\]

Fix distinct physical pairs \(P,Q\).  Let each \(H_r\) be one of
\(\{P\},\{Q\},\{P,Q\}\), and assume no two \(H_r\)'s are the same
singleton.  Give every active lift an arbitrary nonzero complex
coefficient and set

\[
                         F=\sum_{r=0}^2\sum_{R\in H_r}
                                  \lambda_{rR}A_r(R).             \tag{2}
\]

**Theorem 1.1 (sole-defect two-pair obstruction).**  There is no quadratic
\(q\) in the site-square-zero algebra such that

\[
                              q^{[2]}=F,\qquad q^{[3]}=0.          \tag{3}
\]

The endpoint blocks of \(q\) are arbitrary.  The theorem permits arbitrary
local dimensions, both endpoint orders, zero blocks, and complex
cancellation.  It is power-only and does not use response rows.

The family hypothesis is exactly the response-compatible ordinary Hall
failure on two physical pairs.  Up to field relabelling its three
cardinality profiles are

\[
                         (2,2,2),\qquad(2,2,1),\qquad(2,1,1),     \tag{4}
\]

where the two singleton fields in the last profile use different pairs.

## 2. Projection and simultaneous coefficient normalization

Project the five good spaces onto their three field axes and the bad space
onto the span of its three field vectors.  The induced unital algebra
endomorphism fixes \(F\) and commutes with bracket powers.  As in the
distinct-lift theorem, the only bad-site matroids are

\[
\begin{array}{c|c}
\text{type}&(a_0^{(o)},a_1^{(o)},a_2^{(o)})\\ \hline
\text{three-line circuit}&((1,0),(0,1),(1,1)),\\
\text{coincident pair}&((1,0),(0,1),(1,0)),\\
\text{rank one}&((1),(1),(1)).
\end{array}                                                       \tag{5}
\]

All active coefficients in (2) may be normalized to one using only good
sites, so the dependent bad frame causes no scaling compatibility.

For a singleton family \(H_r=\{R\}\), choose a good site
\(y\notin R\) and scale the \(r\)-axis there by
\(\lambda_{rR}^{-1}\).

Now suppose \(H_r=\{P,Q\}\).  Since \(P\ne Q\) and only \(o\) is bad, the
symmetric difference \(P\mathbin\triangle Q\) contains a good site \(x\).
Orient the names as \(A,B\) so that \(x\in A\setminus B\).  The complement
of \(P\cup Q\) contains a good site \(y\).  Thus \(x\) is absent from
\(A_r(A)\) and present in \(A_r(B)\), while \(y\) is present in both
lifts.  Scale the \(r\)-axis at these two good sites by

\[
                         t_y=\lambda_{rA}^{-1},\qquad
                         t_x=\lambda_{rA}\lambda_{rB}^{-1}.       \tag{6}
\]

The new coefficients are

\[
                  \lambda_{rA}t_y=1,\qquad
                  \lambda_{rB}t_xt_y=1.                          \tag{7}
\]

This includes the case in which one direction of
\(P\mathbin\triangle Q\) is only \(o\): the other direction supplies
\(x\), and \(y\) lies outside the union.  At a good site the three field
axes are independent, so these scalings can be performed independently for
all fields.  No root extraction is used.

## 3. Complete orbit and ideal census

For a fixed unordered pair \(\{P,Q\}\), there are thirteen labelled family
systems satisfying the theorem's hypothesis:

* one of profile \((2,2,2)\);
* six of profile \((2,2,1)\);
* six of profile \((2,1,1)\).

There are \(\binom{15}{2}=105\) choices of the physical-pair set, hence
1,365 labelled systems.  The group \(S_5\) permuting the good sites acts on
them.  The circuit and rank-one matroids also permit every field
permutation; the coincident matroid permits only the swap of its equal
fields.  Direct canonicalization gives

\[
\begin{array}{c|c|c|c|c}
\text{bad type}&\text{orbits}&q\text{-cells}&
   \operatorname{rank}(qF=0)&\text{kernel dimensions}\\ \hline
\text{circuit}&17&120&12,15,18&108,105,102\\
\text{coincident pair}&31&120&12,15,18&108,105,102\\
\text{rank one}&17&105&6,12,18&99,93,87.
\end{array}                                                       \tag{8}
\]

The necessary equation \(qF=0\) follows from
\(q q^{[2]}=3q^{[3]}\).  For each orbit, the checker collects equal
six-site words before exact rational RREF, substitutes a complete kernel
basis into every coefficient of \(q^{[2]}-F\), and asks Singular for the
unsaturated Gröbner basis over \(\mathbb Q\).  There are 945 four-site
coordinate words in each two-dimensional bad case and 675 in rank one.
Every one of the \(17+31+17=65\) affine ideals is the unit ideal.  Hence
there is no solution over \(\mathbb C\), proving Theorem 1.1.

The complete family, cell, linear-row, RREF, and quadratic-generator
streams have the frozen combined SHA-256 values

| bad type | combined ledger SHA-256 |
|---|---|
| circuit | 160c496ed05d7ae56180c07fd59eb8b2e3fd94b07d4426c32d8e4417827039a6 |
| coincident pair | 0a8cd248765959003754da8ed277b71e571396eb6fcbf8aa3e23d85b7e4e805b |
| rank one | c25cbabf59c739dd062e4dcc98246a83a98a1d3d17457433e4a42e62007ed068 |

## 4. Response consequence and reproduction

In a sole-defect three-field response solution, every active field family is
nonempty, and the response singleton lemma excludes
\(H_r=H_s=\{P\}\).  If the three families had no ordinary system of
distinct representatives, Hall's theorem would force their union to be
exactly two physical pairs and their profile to be one of (4).  Theorem 1.1
therefore gives:

**Corollary 4.1.**  Every sole-defect three-field common-power response
solution has an ordinary system of distinct active-pair representatives.
Every such representative system is locally nonseparable at the deficient
site.

The second sentence uses the distinct-lift field-selection corollary:
ordinary representatives exist by this note, but a locally separable choice
would reduce to three distinct lifts and is impossible.

The standalone checker
[verify_sole_defect_two_pair_common_power.py](../computations/verify_sole_defect_two_pair_common_power.py)
reconstructs the 105 normalization incidences, all 1,365 labelled systems,
all 65 orbits, exact kernels, ideals, unit results, and frozen ledgers:

    uv run python computations/verify_sole_defect_two_pair_common_power.py

The fast ledger replay omits only the Singular calls:

    uv run python computations/verify_sole_defect_two_pair_common_power.py --ledger-only

This closes the entire no-ordinary-SDR branch at one deficient site.  The
remaining active-family systems possess an SDR, and the
[sole-defect packet theorem](sole-defect-nonseparable-packet-common-power-obstruction.md)
closes every locally nonseparable SDR pattern.  Hence the two theorems,
together with the response singleton lemma, close the entire sole-defect
response branch.
