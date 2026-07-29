# Six pure lifts on two physical pairs have no common-power source

## 1. Exact theorem

Let \(U\) be a six-set. At every site \(u\), let \(V_u\) contain three
distinguished independent vectors

\[
                         e_0^{(u)},e_1^{(u)},e_2^{(u)}.
\]

For a pair \(R\subset U\), put

\[
             E_i(R)=\bigotimes_{u\notin R}e_i^{(u)}.
\]

Fix two distinct physical pairs \(P,Q\). For six nonzero complex numbers
\(\lambda_i,\mu_i\), set

\[
             F=\sum_{i=0}^2\bigl(\lambda_iE_i(P)+\mu_iE_i(Q)\bigr).
                                                                    \tag{1}
\]

All products are in the site-square-zero algebra

\[
 \mathcal R_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u),
 \qquad V_uV_u=0.                                                   \tag{2}
\]

**Theorem 1.1 (two-pair six-term obstruction).** There is no quadratic
\(q\in\mathcal R_U\) satisfying

\[
                         q^{[2]}=F,\qquad q^{[3]}=0.                 \tag{3}
\]

This holds both when \(P,Q\) meet and when they are disjoint. The quadratic
is arbitrary: its endpoint blocks may be full \(3\times3\) tensors, may be
asymmetric in the two endpoints, and may use arbitrary complex
cancellation. No support, purity, rank, nonvanishing, or genericity
condition is imposed on \(q\).

The self-contained exact checker
[verify_two_pair_six_term_common_power.py](../computations/verify_two_pair_six_term_common_power.py)
constructs the complete coefficient ideal and proves it is the unit ideal
over \(\mathbb Q\) in both pair orbits.

## 2. Arbitrary local dimensions and all six weights

Choose a linear projection of each \(V_u\) onto the displayed
three-dimensional subspace which fixes its three axes. Extending it by
\(1\mapsto1\) gives an algebra homomorphism of (2) which fixes \(F\) and
commutes with bracket powers. Thus a solution in larger local spaces would
project to a solution with exactly three local coordinates. It is enough
to rule out that coordinate problem.

All six coefficients in (1) can be normalized simultaneously without
extracting roots. For each colour \(i\), independently choose nonzero site
scalars \(t_{i,u}\) such that

\[
 \prod_{u\in U}t_{i,u}=1,\qquad
 \prod_{u\in P}t_{i,u}=\lambda_i,\qquad
 \prod_{u\in Q}t_{i,u}=\mu_i.                                    \tag{4}
\]

If \(P=ab,Q=ac\) meet, take

\[
 t_{i,a}=1,\qquad t_{i,b}=\lambda_i,\qquad t_{i,c}=\mu_i,
\]

put \((\lambda_i\mu_i)^{-1}\) at one of the three unused sites, and put
one at the other sites. If \(P=ab,Q=cd\) are disjoint, put
\(\lambda_i,1\) at \(a,b\), put \(\mu_i,1\) at \(c,d\), and put
\((\lambda_i\mu_i)^{-1},1\) at the two unused sites. This proves (4) in
both cases.

Scale the three displayed axes at every site by

\[
                         e_i^{(u)}\longmapsto t_{i,u}e_i^{(u)},      \tag{5}
\]

and extend this to a linear automorphism of \(V_u\), for example by fixing
a chosen complementary subspace. The induced algebra automorphism takes

\[
 \lambda_iE_i(P)\longmapsto
 \lambda_i\prod_{u\notin P}t_{i,u}E_i(P)=E_i(P),                  \tag{6}
\]

and similarly for \(Q\). It commutes with bracket powers. Hence no
generality is lost by taking all six coefficients equal to one. Notice
that the three colours use disjoint scaling variables, so a shared physical
pair introduces no coupling between their normalizations.

Up to relabelling \(U\), two distinct pairs have exactly two orbits:

\[
 (P,Q)=(01,02)\quad\hbox{or}\quad(P,Q)=(01,23).                    \tag{7}
\]

Among the \({15\choose2}=105\) unordered pair choices, 60 are adjacent and
45 are disjoint. The checker verifies this census before treating the two
representatives.

## 3. The exact simultaneous \(qF=0\) kernel

Bracket powers obey

\[
                              q q^{[2]}=3q^{[3]}.                   \tag{8}
\]

Consequently (3) implies the necessary linear equation

\[
                                  qF=0.                            \tag{9}
\]

Write \(q_R(a,b)\) for the endpoint-ordered coordinate of the quadratic
block on \(R=\{u,v\}\), with \(u<v\). There are

\[
                         {6\choose2}3^2=135                        \tag{10}
\]

such coordinates. When a block of \(q\) multiplies \(E_i(P)\), it is
nonzero only when both its sites lie in the missing pair \(P\), hence only
when that block is the \(P\)-block itself. Therefore, for every six-site
coordinate word \(w\in\{0,1,2\}^U\), the complete coefficient equation in
(9) is

\[
 \sum_{\substack{R\in\{P,Q\},\ 0\le i\le2\\
                   w|_{U\setminus R}\equiv i}}
                  q_R(w|_R)=0.                                    \tag{11}
\]

Equal words in (11) are collected before row reduction; no summand is
silently separated. Exact rational RREF gives

| pair orbit | nonzero coefficient rows | rank | kernel dimension |
|---|---:|---:|---:|
| adjacent | 45 | 18 | 117 |
| disjoint | 51 | 18 | 117 |

The checker constructs one rational basis vector for every free column,
checks every vector against every row of (11), and checks rank plus
nullity equals 135.

## 4. Both unsaturated common-power ideals are unit

For a four-set \(S=\{u_0,u_1,u_2,u_3\}\) and local word
\(c\in\{0,1,2\}^S\), the exact coefficient of \(q^{[2]}\) is

\[
\begin{aligned}
 &q_{u_0u_1}(c_0,c_1)q_{u_2u_3}(c_2,c_3)
 +q_{u_0u_2}(c_0,c_2)q_{u_1u_3}(c_1,c_3)\\
 &\hspace{32mm}
 +q_{u_0u_3}(c_0,c_3)q_{u_1u_2}(c_1,c_2).                         \tag{12}
\end{aligned}
\]

The checker substitutes the full 117-parameter kernel of (11) into all

\[
                         {6\choose4}3^4=1,215                       \tag{13}
\]

coefficients of

\[
 q^{[2]}-\sum_{i=0}^2\bigl(E_i(P)+E_i(Q)\bigr).                   \tag{14}
\]

It sends the resulting quadratic generators to Singular over
\(\mathbb Q\), with no saturation and no auxiliary nonvanishing
conditions. In both cases the exact Gröbner basis is [1]. The ordered
row, RREF, and generator streams are frozen together by SHA-256:

| pair orbit | variables | generators | ledger SHA-256 | ideal |
|---|---:|---:|---|---|
| adjacent | 117 | 1,215 | 038c784c558b61d11d87e8e77753c4c63c460041aef8e1d3e2c7e1a541f2e02d | [1] |
| disjoint | 117 | 1,215 | 1c2fbc31726f15bb2ff1be6c0db53330f6181293279a61f3337beb2ab8e3b8e7 | [1] |

Since these are unsaturated affine ideals, the calculation includes every
zero and cancellation branch of \(q\). A unit ideal over \(\mathbb Q\)
remains a unit ideal after extension to \(\mathbb C\), proving Theorem 1.1.

## 5. Independent audit of the needed \((2,2,1)\) dependency

The existing
[two-two-one obstruction](two-two-one-monomial-common-power-obstruction.md)
does legitimately cover the special case needed here. Despite the word
“monomial” in its filename, only its five **target lifts** are pure
monomials. Its \(q\) has all 135 endpoint-ordered coordinates, its linear
kernel is the complete kernel of \(qF=0\), and its 1,215 quadratic equations
are all coefficients of \(q^{[2]}-F\). It uses neither a unit/monomial
ansatz for \(q\) nor a saturation. Its 195 support orbits include both
two-physical-pair cases: orbit 1 is adjacent and orbit 154 is disjoint;
both replay to [1].

The new checker also reconstructs these two special ideals independently,
without importing either old builder. Here colours zero and one occupy
both \(P,Q\), while colour two occupies \(Q\) only. Its independently
ordered ledgers are

| control | rows / rank / nullity | ledger SHA-256 | ideal |
|---|---:|---|---|
| adjacent \((2,2,1)\) | 39 / 18 / 117 | 65aa8dcdfbbeb883c262981c4b06c77b84764d945444b5c9a268da788bccab81 | [1] |
| disjoint \((2,2,1)\) | 43 / 18 / 117 | 77ce7cebc198aa491f2aa88054909f22b19a391a30da23c0ae4955e6ddd87d56 | [1] |

Thus the older result is safe to use for the five-term branch, including
arbitrary endpoint blocks and complex cancellation.

## 6. The complete aligned three-field branch closes

Use the setup and notation of
[the aligned three-field theorem](aligned-three-field-common-power-obstruction.md).
Its power Hall lemma says that the three nonempty active-pair families
\(H_0,H_1,H_2\) have no system of distinct representatives. For three
families, Hall's theorem says this can happen only if

\[
 H_i=H_j=\{P\}\quad\hbox{for some }i\ne j,
 \qquad\hbox{or}\qquad
 |H_0\cup H_1\cup H_2|\le2.                                      \tag{15}
\]

The first alternative is exactly the same-singleton collision excluded by
Lemma 3.2 of that note. Thus every aligned solution would obey

\[
                         |H_0\cup H_1\cup H_2|\le2.                \tag{16}
\]

The union cannot have size one, because then two of the nonempty families
would be the forbidden same singleton. Hence the union is exactly
\(\{P,Q\}\) for distinct pairs \(P,Q\).

Up to relabelling colours and interchanging \(P,Q\), there are only three
multiplicity profiles:

\[
                             (2,2,2),\qquad(2,2,1),\qquad(2,1,1).  \tag{17}
\]

The first is excluded by Theorem 1.1. The second is excluded by the
independently audited theorem in Section 5. In the last profile, the two
singleton colours must occupy different pairs, since otherwise they would
be a forbidden same-singleton collision. Relabel so that

\[
 H_0=\{P,Q\},\qquad H_1=\{P\},\qquad H_2=\{Q\}.                    \tag{18}
\]

Let

\[
 B_{ij}(R)=p_{i,a}\otimes s_{j,b}
             +s_{j,a}\otimes p_{i,b}\qquad(R=\{a,b\})              \tag{19}
\]

be the literal endpoint response tensor from the aligned note. In the
zero \(H_1=\{P\}\) module, the row pair \((0,0)\) gives

\[
                              B_{00}(P)=0,                          \tag{20}
\]

because its aggregate target coefficient and its four outside line
factors are nonzero. The same zero response in the singleton
\(H_2=\{Q\}\) module gives

\[
                              B_{00}(Q)=0.                          \tag{21}
\]

But the diagonal colour-zero response is supported on exactly these two
pairs. Equations (20)--(21) make it zero, contradicting its nonzero target
\(X_0\). Thus the \((2,1,1)\) profile is impossible without using any
power calculation.

**Corollary 6.1 (full aligned-three-field obstruction).** The aligned
three-field setup has no solution at all. This includes arbitrary genuine
linear mixtures at hard zero-diagonal sites and every pattern of one- or
two-site deviations; the earlier coordinate-permutation restriction is no
longer needed.

For an independent computational control only, the checker also constructs
the unrestricted common-power ideals for the \((2,1,1)\) profile after the
same per-colour weight normalization (using its evident one-pair
specialization for a singleton colour). They too are unit:

| control | rows / rank / nullity | ledger SHA-256 | ideal |
|---|---:|---|---|
| adjacent \((2,1,1)\) | 33 / 18 / 117 | 15f664ff5212765ba9d67b722b795b66fc6fee7be2af073fb5ba0b72b6a38e3d | [1] |
| disjoint \((2,1,1)\) | 35 / 18 / 117 | b69d746581794a828838c0fb514dcd67a7a0100adf188e8add762d6cd2a06a0e | [1] |

These last two ideals are not a logical dependency of Corollary 6.1.

The corollary still does not supply the missing unconditional descent of a
general multiplier to three aligned line fields. That descent remains the
global frontier.

## 7. Reproduction

Run

    uv run python computations/verify_two_pair_six_term_common_power.py

The default replay checks the 105 pair-character ranks, the adjacent versus
disjoint orbit census, both independent \((2,1,1)\) controls, both
\((2,2,1)\) controls, both full \((2,2,2)\) ideals, every frozen ledger,
and every unit-ideal result.
