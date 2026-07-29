# Independent audit: the unrestricted polarized eight-site model

## Verdict

The construction in
[polarized-eight-site-unrestricted-counterexample.md](polarized-eight-site-unrestricted-counterexample.md)
is correct.  A clean-room exact expansion confirms

\[
                         z\,{q^3\over 3!}=\Delta_{8,3}
\]

over \(\mathbb Z\), with nine unit cells in \(q\), three unit cells in
\(z\), and exactly three surviving decorated matchings.  The displayed
\(3\times3\) cross block of \(z-aq\) is the identity for every \(a\), so
the same pair cannot obey \(z=a q+4ps\) for linear \(p,s\).

This audit found no flaw.  Its independent checker is
[verify_polarized_eight_site_unrestricted_counterexample_independent.py](../computations/verify_polarized_eight_site_unrestricted_counterexample_independent.py).
It neither imports nor calls the discovery checker.

## 1. Literal data checked

The audit enters the cells directly, without generating them from the three
claimed perfect matchings:

\[
\begin{aligned}
\operatorname{supp}(q)=\{&23_0,45_0,67_0,
                          01_1,36_1,57_1,
                          02_2,14_2,56_2\},\\
\operatorname{supp}(z)=\{&01_0,24_1,37_2\}.
\end{aligned}
\]

All coefficients are one.  These are nine and three distinct
endpoint-colour cells.  In particular, \(01_0\in z\) and \(01_1\in q\)
are kept distinct even though they lie on the same physical pair.

## 2. Two independent coefficient expansions

First, the checker forms all \(\binom{28}{4}=20475\) four-edge subsets of
\(K_8\) and filters for pairwise-disjoint endpoints.  Exactly 105 subsets
remain, as required for the perfect matchings of eight labelled vertices.
For every matching it tests each of its four edges as the distinguished
\(z\)-edge.  Thus all \(105\cdot4=420\) underlying
matching/distinguished-edge positions are inspected, including positions
whose relevant cell is absent.

The resulting normalized divided-power coefficient counter has precisely

\[
 (00000000)\longmapsto1,\qquad
 (11111111)\longmapsto1,\qquad
 (22222222)\longmapsto1,
\]

and no other word.  The three decorated supports reconstructed by this
enumeration are exactly

\[
\begin{aligned}
 &\{01_0,23_0,45_0,67_0\},\\
 &\{24_1,01_1,36_1,57_1\},\\
 &\{37_2,02_2,14_2,56_2\}.
\end{aligned}
\]

Second, independently of the matching normalization, the checker directly
multiplies every one of the \(3\cdot9^3=2187\) ordered choices in
\(zqqq\) in the site-square-zero algebra.  Eighteen ordered choices
survive: the six permutations of the three \(q\)-cells for each of the
three displayed supports.  Hence every pure word has raw coefficient
\(6=3!\); division by \(3!\) gives coefficient one.  This checks both the
factorial and the absence of cancellation assumptions over \(\mathbb Z\).

## 3. Independent rank audit

Use the row modes

\[
                         (0,0),(2,1),(3,2)
\]

and column modes

\[
                         (1,0),(4,1),(7,2).
\]

Direct lookup in the literal cell lists gives

\[
                         q_{R,C}=0,\qquad z_{R,C}=I_3.
\]

Consequently \((z-aq)_{R,C}=I_3\), independently of \(a\), and its
determinant is one.  For arbitrary linear forms \(p,s\), however,

\[
 (ps)_{R,C}=p_Rs_C^{\mathsf T}+s_Rp_C^{\mathsf T}
            =
 \begin{bmatrix}p_R&s_R\end{bmatrix}
 \begin{bmatrix}s_C^{\mathsf T}\\p_C^{\mathsf T}\end{bmatrix},
\]

so its rank is at most two.  As a separate exact mechanical check, the
audit expands the determinant of the generic right-hand matrix as a sparse
polynomial in twelve independent variables; every monomial cancels and the
polynomial is identically zero.  Multiplication by four does not change
this rank bound over \(\mathbb C\).  Therefore no \(a,p,s\) can satisfy
\(z-aq=4ps\) for this \((q,z)\).

## 4. Scope boundary

This is an unrestricted *polarized* countermodel, not a counterexample to
Krenn's conjecture.  The audit additionally computes the ordinary divided
power \(q^4/4!\).  It contains exactly the two mixed words

\[
                         11000000,qquad 22212111,
\]

each with coefficient one, and is not \(\Delta_{8,3}\).  More
fundamentally, the polarized equation contains the extra quadratic \(z\),
whereas Krenn's original equation uses the fourth power of a single
quadratic.

Nor is this a countermodel inside the actual shared pair-cap ansatz: the
rank-three minor proves that this particular \(z\) lies outside even the
one-row form \(a q+4ps\).  What the example refutes is only a proposed
uniform obstruction for arbitrary solutions of \(zq^3/3!=\Delta_{8,3}\).
The literal pair-cap formula, compatibility of two rows sharing \(p,s\),
or overlap of physical-pair identities remains available to attack the
conjecture.

## 5. Reproduction

Run

```text
.venv/bin/python computations/verify_polarized_eight_site_unrestricted_counterexample_independent.py
```

The exact output is

```text
independent polarized eight-site audit: PASS
C(28,4) filtering gives 105 perfect matchings: PASS
all 420 matching/distinguished-edge positions checked: PASS
9 q-cells + 3 z-cells give exactly 3 divided-power terms: PASS
ordered expansion gives coefficient 3!=6 before normalization: PASS
q^4/4! has two mixed words, so this is not a Krenn counterexample: PASS
constant I_3 cross block and symbolic rank<=2 pair-cap test: PASS
```
