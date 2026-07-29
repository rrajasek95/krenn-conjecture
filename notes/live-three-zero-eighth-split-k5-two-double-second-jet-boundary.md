# The eighth split at \(k=5\): the two-double full-residue boundary

## 1. Scope

For the still-open profile

\[
                              3^3 2^2 1^{10},             \tag{1}
\]

the all-order mixed-role theorem selects all ten singleton classes.  The
complement has signature \(3^3 2^2\), so its two relation polynomials fill
\(\mathbb C[z]_{\leq1}\).  At either complementary double \(u\), the
residue equations consequently force both

\[
                              B_u'(u)=B_u''(u)=0.          \tag{2}
\]

At a complementary triple \(a\), the same linear target gives the two direct
conditions

\[
                              B_a''(a)=B_a'''(a)=0.        \tag{3}
\]

There is no selected double to exchange with an outside double.  This note
shows that all ten direct complementary-residue equations (2)--(3), two at
each of the five complementary roots, are structurally consistent.  Thus
even the entire direct complementary-residue package does **not** by itself
close (1).  This is a boundary model for that local route, not a realization
of the full collision profile and not a counterexample to the conjecture.

## 2. Exact boundary model

Take the common-pole parameter \(\mu=0\), complementary double values

\[
                              u=2,\qquad v=3,
\]

and complementary triple values \(1,4,5\).  Put

\[
\begin{aligned}
H(z)={}&8286z^{10}+8286z^9+8286z^8-25786851z^7
          +362953470z^6\\
     &-2285123704z^5+8099136386z^4-17184131115z^3\\
     &+21620151100z^2-14846006000z+4280724000.           \tag{4}
\end{aligned}
\]

The ten roots of \(H(z)=\prod_{r\in\mathcal R}(z+r)\), counted after an
irrelevant scalar normalization, define the ten selected singleton values.
For each complementary value \(a\in\{1,2,3,4,5\}\), set

\[
 m_1=m_4=m_5=3,\qquad m_2=m_3=2,
\]

and define its local unit by

\[
 B_a(z)={z^5H(z)\over
       \displaystyle\prod_{b\ne a}(z-b)^{m_b+1}}.       \tag{5}
\]

At a root of multiplicity \(m_a\), the residue of
\(B_a(z)S(z)/(z-a)^{m_a+1}\) vanishes for every linear \(S\) exactly when

\[
                         B_a^{(m_a-1)}(a)
                         =B_a^{(m_a)}(a)=0.              \tag{6}
\]

Exact differentiation verifies (6) at all five roots.  Equivalently, the
ten homogeneous equations on the eleven coefficients of a general
degree-at-most-ten polynomial \(H\) have rank eight, and (4) is a
degree-ten member of their kernel.

The data are structurally admissible for this local test.  Namely,

\[
 \gcd(H,H')=1,\qquad \gcd(H(z),H(-z))=1,                \tag{7}
\]

and \(H\) is nonzero at \(0,\pm1,\ldots,\pm5\).  Hence its ten roots are
nonzero and simple, no two are opposites, and none of the corresponding
singleton values equals or is opposite to a displayed double or triple
value.  The displayed repeated values are themselves nonzero, distinct,
and pairwise nonopposite.

The first equality in (7) is the exact distinctness check.  The second is
the exact nonoppositeness check and avoids any numerical root
approximation.

## 3. Consequence

The three-double profile \(3^3 2^3 1^8\) is closed because a selected/outside
double swap compares both logarithmic jets.  Profile (1) has no selected
double, and (4)--(7) show that imposing every residue visible in the full
linear target still cannot replace that swap.  Any continuation for (1)
must use selected-lift coupling beyond the dual image residues, or another
compatibility condition not contained in this direct package.

## 4. Exact audit

[verify_live_three_zero_eighth_split_k5_two_double_second_jet_boundary.py](../computations/verify_live_three_zero_eighth_split_k5_two_double_second_jet_boundary.py)
checks the profile and degree data, the rank-eight ten-row coefficient
system, all ten rational derivative equations, squarefreeness,
nonoppositeness, and separation from every displayed structural value.
