# Reconstruction audit for an exact three-color source at eight sites

This note records a fresh constructive audit of the existing eight-site
searches.  It did **not** produce an exact counterexample.  Its useful output
is instead (i) an exact obstruction to the color-circulant symmetry ansatz,
(ii) an exact recognition of the apparent sparse near-solutions as border
degenerations, and (iii) a further finite exclusion inside the monomial
cube-root ansatz.

Throughout, an aggregate edge matrix is denoted by

\[
 A_{uv}\in \mathbb C^{3\times3},\qquad
 H_8(A)=\sum_{M\in\operatorname {PM}(8)}\bigotimes_{uv\in M}A_{uv}.
\]

The target is \(\Delta_{8,3}=\sum_{a=0}^2e_a^{\otimes8}\).

## 1. Numerical search audit

### Joint order-three symmetry

`computations/search_c3_equivariant_n8.py` couples the vertex permutation
\((012)(345)\), fixing 6 and 7, to cyclic color shift.  It has 84 scalar
parameters (84 complex parameters in complex mode), and the implementation
does evaluate all \(3^8\) output coefficients.  No saved candidate existed
before this audit.  Representative extended runs were:

\[
\begin{array}{c|c|c|c}
\text{mode/seed}&\text{iterations}&\tfrac12\|H-\Delta\|_2^2
  &\|H-\Delta\|_\infty\\ \hline
\text{real}/1&1000&0.5803313421&0.386886\\
\text{complex}/0&1000&0.5803384183&0.386892.
\end{array}
\]

Least-squares and target-normalized runs did not approach zero either; the
normalized search instead grew to norm about 341 at residual loss about
0.986.  These are only negative numerical observations, not an exact
obstruction to the full 84-parameter chart.

### Vertex-translation symmetry

`computations/search_cyclic_n8_full.py` uses arbitrary matrices for cyclic
distances 1, 2, 3 and a symmetric matrix at distance 4, for 33 scalar
parameters.  Across the additional real and complex starts run here, the
best losses were approximately 0.63 (real) and 0.50 (complex), always with
maximum residual one in the low-loss complex runs.  Those points simply
lose at least one target color; none is a candidate.

The script's 11-parameter `--color-circulant` subchart consistently reached
loss one and maximum residual \(2/3\).  Section 2 gives an exact reason this
subchart cannot contain the target.

### Sparse four-regular supports

Every support in `computations/search_sparse_n8_q3.py` already contains the
known expanded-prism border family.  Thus an optimizer approaching zero on
one of these charts is not by itself evidence of a finite solution.  The
most reproducible trajectory (`--extra 0 --seed 0`, real) was

\[
\begin{array}{c|c|c}
\text{maximum evaluations}&\|A\|_2&\|H-\Delta\|_\infty\\ \hline
100&16.24&6.670\cdot10^{-4}\\
200&22.24&1.877\cdot10^{-4}\\
500&32.24&4.213\cdot10^{-5}\\
800&39.83&1.806\cdot10^{-5}\\
4000&71.24&1.759\cdot10^{-6}.
\end{array}
\]

At all five points,
\(\|H-\Delta\|_\infty\|A\|_2^4\) is about \(45.4\).  Inspection of the
800-step point showed that every retained matrix had numerical rank one and
only one same-color entry; four of the sixteen matrices had norm below
\(2\cdot10^{-16}\).  Exact recognition gives the Laurent family in Section
3.  The analogous `--extra 3 --seed 0` run has the same structure and the
same fourth-power scaling.  Other random starts generally stopped at loss
\(1/2\), and complex starts supplied no finite candidate.

## 2. Exact obstruction to edgewise color-circulant matrices

Let \(S e_a=e_{a+1}\), with subscripts modulo three.  A color-circulant
edge matrix obeys

\[
                 (S\otimes S)A_{uv}=A_{uv}.                 \tag{1}
\]

Choose a Fourier basis \(f_p\), \(p\in\mathbb Z/3\), in which
\(Sf_p=\omega^p f_p\).  Equation (1) says that a Fourier coefficient of
\(A_{uv}\) can be nonzero only at a pair \((p,q)\) satisfying
\(p+q=0\pmod3\).  Consequently a Fourier coefficient of any perfect-
matching term can be nonzero only if every matched pair has momenta
\((0,0)\), \((1,2)\), or \((2,1)\).  In particular the total number of
momentum-1 sites must equal the total number of momentum-2 sites.

On the other hand, the Fourier transform of the target is supported on

\[
 \widehat\Delta_{8,3}(p_0,\ldots,p_7)\ne0
 \quad\Longleftrightarrow\quad \sum_i p_i=0\pmod3.          \tag{2}
\]

At \((p_0,\ldots,p_7)=(1,1,1,1,1,1,0,0)\), (2) is nonzero, while every
matching term vanishes by the unequal momentum counts.  Therefore no
source in which every aggregate edge matrix is color-circulant can realize
\(\Delta_{8,3}\).  This proves an exact obstruction to the 11-parameter
color-circulant cyclic search (indeed, to a much larger chart with no vertex
symmetry at all).

## 3. Exact recognition of the sparse attractors

For the first numerical attractor, take the three same-color perfect
matchings

\[
\begin{aligned}
 U_0&=\{02,14,36,57\},\\
 U_1&=\{03,15,24,67\},\\
 U_2&=\{01,23,47,56\}.
\end{aligned}                                               \tag{3}
\]

Give every edge weight one except \(w_{36}=t\) and
\(w_{14}=t^{-1}\).  The union in (3) has exactly five perfect matchings:
the three \(U_a\), and

\[
 \{01,24,36,57\},\qquad \{02,15,36,47\}.                  \tag{4}
\]

The first three have coefficient one and constant colors.  The two in (4)
have distinct mixed endpoint colorings and coefficient \(t\).  Hence

\[
 H_8=\Delta_{8,3}+t\bigl(
 e_{22101000}+e_{01002102}\bigr).                          \tag{5}
\]

Here \(e_{c_0\cdots c_7}=e_{c_0}\otimes\cdots\otimes e_{c_7}\).
For every finite \(t\ne0\), both mixed coefficients in (5) are nonzero.
The limit \(t\to0\) is therefore a border degeneration, not an exact
counterexample.

The second attractor similarly uses

\[
\begin{aligned}
 U_0&=\{07,14,23,56\},\\
 U_1&=\{03,15,24,67\},\\
 U_2&=\{04,16,25,37\},
\end{aligned}                                               \tag{6}
\]

with \(w_{67}=t\), \(w_{24}=t^{-1}\).  Its two additional perfect
matchings are \(\{03,14,25,67\}\) and \(\{04,15,23,67\}\), again with
distinct mixed colorings and coefficient \(t\).  Thus it has the same
form \(\Delta_{8,3}+t(T_1+T_2)\).

`computations/verify_sparse_n8_border_attractors.py` enumerates the perfect
matchings and verifies both identities using exact integer Laurent
exponents.  It thereby checks every one of the \(3^8\) coefficients (all
unlisted colorings have no supported matching).

## 4. Monomial exact searches

The direct audit
`computations/verify_monomial_n8_counterexample.py` was rerun.  Its labeled
\(K_8\) has 38 mixed fibers, all of size two, but the three binomial ratios
in its certificate satisfy \(-d_1+d_6+d_{10}=0\).  Requiring all three
ratios to be \(-1\) contradicts this odd relation, so the no-singleton
labeling cannot be weighted over \(\mathbb C^*\).

A different restricted possibility is that every nonzero edge weight is a
third root of unity, every constant fiber consists of its chosen matching,
and mixed fibers cancel.  A zero sum of third roots has equal multiplicity
in the three phases, so every mixed fiber cardinality must be divisible by
three.  The CEGAR formula in
`computations/search_monomial_triple_cancellation_sat.py` imposes this
necessary condition.  Rerunning all 13 orbits of triples of edge-disjoint
target matchings at \(n=8\) gave exact UNSAT in one to three refinement
rounds for every orbit.  The script's output was clarified to distinguish
proved UNSAT from reaching its round limit.

This last search is deliberately narrow: it does not cover arbitrary
complex weights, multiple constant-fiber terms, or nonmonomial matrices.
Likewise the existing root-of-unity pairing searches at moduli 2, 4, and 8
are sufficient constructions only, not a complete monomial classification.

## 5. Conclusion

No finite exact eight-site counterexample emerged.  The only small residuals
were recognized exactly as boundary points with two unavoidable mixed
coefficients.  The color-circulant symmetry chart is ruled out exactly, and
the remaining broad symmetry searches have residuals of order one.  The
unresolved eight-site territory is therefore the genuinely full-matrix,
finite part of the C3-equivariant or sparse four-regular charts; numerical
near-zero behavior supplies no evidence for a point there.
