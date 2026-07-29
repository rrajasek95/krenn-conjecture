# A four-site dressed multiplier retains at most two colours

## 1. Result

Let \(D=\{0,1,2,3\}\), let \(V_i\cong\mathbb C^3\), and work in the
site-square-zero algebra

\[
 {\cal R}_D=\bigotimes_{i\in D}(\mathbb C\oplus V_i).
                                                               \tag{1}
\]

Write

\[
 T=\sum_iT_i,\qquad V=\sum_iV_i',\qquad T_i,V_i'\in V_i,       \tag{2}
\]

with completely arbitrary local vectors.  Zero components, local
dependence, arbitrary complex coefficients, and arbitrary superpositions
of the three target axes are all allowed.  For a fixed target basis put

\[
                 X_c=\bigotimes_{i\in D}e_c^{(i)},\qquad 0\le c\le2,
                                                               \tag{3}
\]

and consider

\[
 \mu_{T,V}:({\cal R}_D)_2\longrightarrow({\cal R}_D)_4,\qquad
                         Q\longmapsto TVQ.             \tag{4}
\]

**Theorem 1.1 (arbitrary-superposition obstruction).**  For every \(T,V\)
in (2),

\[
        \#\{c:X_c\in\operatorname {im}\mu_{T,V}\}\le2. \tag{5}
\]

Thus the coordinate-monomial hypothesis in the earlier
[four-site theorem](four-site-coordinate-monomial-dressed-packet-obstruction.md)
is unnecessary.  The bound remains sharp by its binary four-cycle model.

At the smallest isotropic dressed-cap order \(m=4\), the common multiplier
is \(F=TV\).  If all three diagonal target coefficients are nonzero, the
three diagonal rows give quadratics \(Q_c\) with

\[
                             TVQ_c=X_c.                \tag{6}
\]

Theorem 1.1 excludes this for arbitrary local superpositions.  Neither the
six off-diagonal rows nor the special form of the three \(Q_c\)'s is needed.

## 2. The local two-planes and pair blocks

Put

\[
             S_i=\operatorname {span}(T_i,V_i'),\qquad
             r_i=\dim S_i\in\{0,1,2\}.                 \tag{7}
\]

For distinct sites define the endpoint-ordered two-site tensor

\[
             W_{ij}=T_i\otimes V_j'+V_i'\otimes T_j
                         \in S_i\otimes S_j.            \tag{8}
\]

If \(Q_P\) is the component of a quadratic \(Q\) supported on the two-set
\(P\), only the block on the complementary pair can multiply it without a
repeated physical site.  Consequently

\[
 \operatorname {im}\mu_{T,V}
   =\sum_{\{i,j\}\subset D}
       \mathbb C W_{ij}\otimes
       \bigotimes_{k\notin\{i,j\}}V_k,                 \tag{9}
\]

with tensor factors restored to the fixed site order.

There is one rank fact which will be used repeatedly.  If \(r_i=r_j=2\),
then \(W_{ij}\) has tensor rank two.  Indeed, let \(L_i,L_j\) be the
three-by-two matrices with columns \((T_i,V_i')\) and
\((T_j,V_j')\).  Both have rank two, and the matrix of (8) is

\[
                    L_i
                    \begin{pmatrix}0&1\\1&0\end{pmatrix}
                    L_j^{\mathsf T}.                   \tag{10}
\]

The middle matrix is invertible and the two outside maps are respectively
injective and surjective on their two-dimensional images, so (10) has
rank two.  This statement uses no noncancellation or genericity assumption.

## 3. A quotient obstruction for one product target

Let \(X=\bigotimes_i x_i\ne0\) be any product tensor and define

\[
                         O(X)=\{i:x_i\notin S_i\}.      \tag{11}
\]

**Lemma 3.1 (two outside sites).**  If
\(X\in\operatorname {im}\mu_{T,V}\), then

1. \(|O(X)|\le2\);
2. if \(O(X)=\{k,l\}\), the complementary two sites cannot both have
   local rank two.

**Proof.**  For \(i\in O(X)\), apply the quotient
\(\pi_i:V_i\to V_i/S_i\).  The image \(\pi_i(x_i)\) is nonzero.  Every
summand in (9) has two distinguished sites on which it lies in the local
spaces \(S_i\).  Any three-set of quotient sites meets those two sites, so
applying quotients at three members of \(O(X)\) kills the entire image (9)
but not \(X\).  This proves the first assertion.

Now suppose \(O(X)=\{k,l\}\), with complementary pair \(\{i,j\}\).  After
applying \(\pi_k\otimes\pi_l\), every summand of (9) vanishes except the
one whose distinguished pair is \(\{i,j\}\).  Hence the nonzero tensor

\[
       \pi_k(x_k)\otimes\pi_l(x_l)\otimes x_i\otimes x_j
\]

can lie in the quotient of (9) only if

\[
                         x_i\otimes x_j\in\mathbb C W_{ij}. \tag{12}
\]

The left side of (12) has tensor rank one.  If \(r_i=r_j=2\), equation
(10) says the nonzero right-hand generator has rank two, a contradiction.
This proves the second assertion. \(\square\)

The lemma is a statement about the whole column space.  In particular, it
does not select an individual nonzero summand of \(TVQ\), and arbitrary
complex cancellation is retained.

## 4. Three aligned targets are impossible

For each target colour put

\[
                         O_c=O(X_c).                   \tag{13}
\]

At site \(i\), the \(r_i\)-dimensional space \(S_i\) contains at most
\(r_i\) of the three independent coordinate lines.  Therefore

\[
       \#\{c:i\in O_c\}\ge3-r_i.                       \tag{14}
\]

If all three \(X_c\)'s belonged to the image, Lemma 3.1 would give

\[
       12-\sum_i r_i
          \le\sum_c|O_c|\le6,\qquad\text{so}\qquad
                         \sum_i r_i\ge6.                \tag{15}
\]

Up to permuting the four sites, the only remaining rank profiles are

\[
             2222,\qquad2221,\qquad2220,\qquad2211.    \tag{16}
\]

Each is impossible.

* **Profile \(2222\).**  A set \(O_c\) of size two would have a rank-two
  complementary pair, contrary to Lemma 3.1.  Hence every
  \(|O_c|\le1\), so there are at most three outside incidences.  But each
  of the four proper planes \(S_i\) misses at least one coordinate line,
  giving at least four incidences by (14).

* **Profile \(2221\).**  Let \(r\) be the rank-one site.  If \(S_r\)
  contains no coordinate line, then \(r\in O_c\) for every colour.  Any
  rank-two site misses some colour \(c\); that gives two outside sites
  whose complement has rank profile \(22\), or at least three outside
  sites, contradicting one of the two parts of Lemma 3.1.  Otherwise
  \(S_r=\mathbb Ce_k\) for one colour \(k\).  For either other colour
  \(a\), every rank-two plane must contain \(e_a\), by the same argument.
  Hence all three rank-two planes equal the coordinate plane spanned by
  the two colours other than \(k\).  They all miss \(e_k\), so
  \(|O_k|=3\), again impossible.

* **Profile \(2220\).**  Every colour is outside at the rank-zero site.
  A rank-two site misses some colour \(c\).  Those two outside sites have
  a rank-\(22\) complement unless \(c\) is outside still more sites; the
  former contradicts part 2 and the latter part 1 of Lemma 3.1.

* **Profile \(2211\).**  The union of the two rank-one lines contains at
  most two coordinate lines.  Choose a colour \(c\) contained in neither.
  Then its two outside sites have rank-\(22\) complement, unless it has a
  third outside site.  Both alternatives contradict Lemma 3.1.

This exhausts (16) and proves Theorem 1.1.

## 5. Scope and audit

The theorem closes the arbitrary-local-superposition frontier only on a
four-site common complement.  For \(m>4\), the dressed multiplier is
\(TVz^{[m-4]}\), and the additional common power is not covered by (9).
The theorem also cannot eliminate the scalar-matrix-unit binary packet,
because the two-colour four-cycle construction attains equality in (5).

The dependency-free checker
[verify_four_site_arbitrary_superposition_dressed_packet_obstruction.py](../computations/verify_four_site_arbitrary_superposition_dressed_packet_obstruction.py)
audits the pair-complement channel count, the canonical rank-two block,
all local-rank profiles, and every abstract outside-incidence ledger
allowed by (14) and Lemma 3.1.  The quotient and rank arguments above are
the uniform proof, not a finite substitute for arbitrary complex vectors.
