# The last one-zero four-centre deviations are impossible

## 1. Outcome

Retain the live normal form

\[
 S_i=P_i\Delta,
 \qquad P_iHP_j^{\mathsf T}=(\beta_i+\beta_j)q_{ij},       \tag{1}
\]

where (H) is invertible, symmetric, and zero diagonal, and assume that
the rank-three graph (G_3(q)) is connected and spanning.  In the sharp
four-centre chart, the singular shore consists of four nonzero centre
sites and one literal zero-star site (y):

\[
 W=U\sqcup A\sqcup\{y\},\qquad |A|=4,qquad
 P_u\text{ invertible }(u\in U),\quad P_a\ne0, \det P_a=0,
 \quad P_y=0.                                             \tag{2}
\]

The two deviations left open in
[`four-centre-common-power-one-hole-obstruction.md`](four-centre-common-power-one-hole-obstruction.md)
do not occur in a full cap identity.

1. Two nonzero singular sites can never have opposite (\beta)-values.
   This conclusion is global: it needs connectedness of (G_3(q)), but
   not the one-zero assumption in (2).
2. Once opposite values are removed, contracting any two nonzero
   singular sites by annihilators of their star images kills the complete
   left side of every diagonal cap equation.  With only the one zero site
   (y), both contracted sites would have to be matched to (y).
   Consequently the two star images must jointly contain all three target
   axes.
3. The four centres forced by either surviving isotropic pattern cannot
   satisfy that pairwise axis-cover condition.  This includes arbitrary
   non-diagonal complementary columns.

Thus both four-centre patterns are excluded throughout the sharp
one-zero/equality-five chart, not merely at the two diagonal rational test
points.  The argument uses the first two-centre contraction of the common
power; it is strictly stronger than the constant-colour matching-hole
coefficient used in the preceding note.

The scope is important.  If the singular shore has two or more literal
zero-star sites, two annihilated centres can be paired to two different
zero sites, so the proof below does not close that larger stratum.

## 2. Opposite beta values cannot occur on the nonzero singular shore

Let

\[
 U=\{i:\det P_i\ne0\}.
\]

The live propagation theorem says that (U) is a complete live
component and that every rank-three edge leaving (U) first meets a
literal zero-star site.  We use the following additional consequence of
(1).

**Lemma 2.1 (beta parity on the singular shore).**  For every singular
site (z) with (P_z\ne0), there is (u\in U) such that

\[
                         \beta_z=\beta_u\ne0.             \tag{3}
\]

In particular, two nonzero singular sites never obey
(\beta_z+\beta_w=0).

**Proof.**  Choose a shortest path

\[
                        u=v_0,v_1,\ldots,v_m=z            \tag{4}
\]

in (G_3(q)) from (U) to (z).  Every (v_k), (k>0), lies outside
(U), and (P_{v_1}=0).  On the first edge, (1) and the invertibility of
(q_{v_0v_1}) give
(\beta_{v_0}+\beta_{v_1}=0).  On every later edge both endpoint matrices
are singular, so

\[
 \operatorname {rank}(P_{v_{k-1}}HP_{v_k}^{\mathsf T})\le2,
 \qquad \operatorname {rank}q_{v_{k-1}v_k}=3.
\]

Equation (1) again forces
(\beta_{v_{k-1}}+\beta_{v_k}=0).  Hence

\[
                         \beta_z=(-1)^m\beta_u.           \tag{5}
\]

But (1) also holds on the pair (u,z), whether or not that pair is an
edge of (G_3(q)).  Since (P_uH) is invertible and (P_z\ne0),

\[
                         P_uHP_z^{\mathsf T}\ne0.         \tag{6}
\]

Therefore (\beta_u+\beta_z\ne0).  Equations (5)--(6) force (m) even,
(\beta_z=\beta_u), and (\beta_u\ne0), proving (3).

Now suppose (P_z,P_w\ne0) are singular and
(\beta_w=-\beta_z).  Apply (3) to (z), obtaining a live (u) with
(\beta_u=\beta_z).  The pair (u,w) has zero right side in (1), while
its left side has rank (operatorname {rank}P_w>0).  This contradiction
proves the last assertion.  (square)

Notice that the lemma does not prohibit the expected opposite pair
(\beta_y=-\beta_u) when (P_y=0).  It prohibits precisely the proposed
repair edge between two sites of the **nonzero** singular shore.

## 3. The two-centre one-hole contraction

Write the polarized cap identity on the even internal set (|W|=2r) as

\[
 {p(x)p(z)q^{r-1}\over(r-1)!}
       +(x^{\mathsf T}Bz){q^r\over r!}
   =\sum_{c=0}^2{x_cz_c\over d_c}X_c,                   \tag{7}
\]

where the local value of (p(x)) at site (i) is (P_ix), every
(d_c\ne0), and (X_c=\bigotimes_{i\in W}e_c^{(i)}).

For a nonzero singular site (a), put

\[
                         L_a=\operatorname {Ann}(\operatorname {im}P_a)
                              \ne0.                       \tag{8}
\]

**Lemma 3.1 (pairwise target-axis cover).**  Under the one-zero
assumption (2), every two distinct sites (a,b\in A) satisfy

\[
 \boxed{\quad
   \{c:e_c\in\operatorname {im}P_a\}
       \ \cup\ 
   \{c:e_c\in\operatorname {im}P_b\}
       =\{0,1,2\}.\quad}                                \tag{9}
\]

**Proof.**  Choose arbitrary (eta_a\in L_a) and
(eta_b\in L_b).  Lemma 2.1 and (6) show that
(\beta_a+\beta_k\ne0) for every nonzero-star site (k\ne a).
Consequently (1) gives

\[
              \eta_a^{\mathsf T}q_{ak}
       ={1\over\beta_a+\beta_k}
          \eta_a^{\mathsf T}P_aHP_k^{\mathsf T}=0       \tag{10}
\]

for every (k\ne a,y); the analogous identity holds at (b).  The
marked factor (P_ax) is also killed by (eta_a), and similarly at
(b).

Contract (7) at (a,b) by (eta_a,\eta_b).  In a surviving matching,
each of (a,b) would therefore have to use its sole possible un-killed
edge, the edge to (y).  One site (y) cannot be paired twice.  Both the
marked response and the direct common-power term on the left of (7)
vanish.  Taking (x=z=e_c) leaves

\[
                 0={\eta_a(e_c)\eta_b(e_c)\over d_c}
                         \bigotimes_{i\notin\{a,b\}}e_c^{(i)}.       \tag{11}
\]

Thus (eta_a(e_c)\eta_b(e_c)=0) for every pair of annihilators.  The
functional (eta\mapsto\eta(e_c)) vanishes identically on
(operatorname {Ann}(\operatorname {im}P)) exactly when
(e_c\in\operatorname {im}P).  For each (c), (11) therefore puts
(e_c) in at least one of the two images.  This is (9).  (square)

This argument keeps the actual common power.  In particular it does not
assume that any constant-colour scalar edge vanishes.

## 4. The coordinate rank-one direct quadratic

After permuting colours, let

\[
                         B=\lambda E_{00},\qquad\lambda\ne0.        \tag{12}
\]

Its isotropic plane is (K=\langle e_1,e_2\rangle).  The minimum pattern
contains two (1)-centres and two (2)-centres.  A (d)-centre obeys

\[
                   0\ne P_aK\subseteq\mathbb C e_d,     \tag{13}
\]

so (e_d\in\operatorname {im}P_a) and
(operatorname {rank}P_a\le2).  Define its coordinate-axis coverage by

\[
                         C_a=\{c:e_c\in\operatorname {im}P_a\}.     \tag{14}
\]

For the two (1)-centres, (9), (13), and (|C_a|\le2) force their two
coverage sets to be

\[
                              \{0,1\},\quad\{1,2\}.      \tag{15}
\]

The same argument forces the two (2)-centre sets to be

\[
                              \{0,2\},\quad\{1,2\}.      \tag{16}
\]

But the (1)-centre and (2)-centre carrying the two copies of
({1,2}) violate (9).  This is the desired contradiction.  No
restriction was placed on the complementary columns (P_ae_0); a
generic non-diagonal column merely makes (C_a) smaller and reaches the
contradiction sooner.

## 5. The two-coordinate-factor rank-two quadratic

After permuting colours, write the isotropic components as

\[
                  K_0=\{v_0=0\},\qquad K_1=\{v_1=0\}.   \tag{17}
\]

The four-site minimum pairs the component incidences in two copies of
each of the following types:

\[
 \begin{array}{c|cc}
       &K_0&K_1\\ \hline
 10& e_1&e_0\\
 22& e_2&e_2.
 \end{array}                                             \tag{18}
\]

For a type (10) centre, linearity and
(K_0+K_1=\mathbb C^3) give

\[
                         \operatorname {im}P_a
                            =\langle e_0,e_1\rangle.      \tag{19}
\]

For a type (22) centre, the same sum gives

\[
                         \operatorname {im}P_a=\mathbb C e_2.       \tag{20}
\]

The two type (22) centres therefore have joint axis coverage only
({2}), contradicting (9).  Hence the second four-centre pattern is
also impossible.

## 6. Why the old constant-word test alone does not suffice

There are exact non-diagonal data satisfying (1), all centre incidences,
the connected spanning nonbipartite rank-three graph condition, and all
eighteen constant-word projections of (7).  The checker gives a small
rational example with (B=E_{00}), (Delta=I), three live sites, four
centres, and one zero site.  Its three constant-word response matrices
are exactly

\[
                         E_{00},\qquad E_{11},\qquad E_{22}.         \tag{21}
\]

It is not a full cap solution: the coefficient of the one-defect word
(00000001) in the (00) equation is (18), rather than zero.  Thus a
proof based only on repaired constant-colour scalar matchings would fail.
The two-centre contraction detects the mixed output information which
that scalar projection discards.

## 7. Exact audit

[`verify_live_four_centre_final_deviations.py`](../computations/verify_live_four_centre_final_deviations.py)
enumerates all coordinate-axis coverage sets allowed by the two minimum
patterns and verifies that none satisfies (9).  It also checks the exact
non-diagonal boundary example from Section 6: every block relation, all
centre incidences, rank-three connectivity and oddness, all eighteen
constant-word cap projections, and the displayed mixed-word residual.
