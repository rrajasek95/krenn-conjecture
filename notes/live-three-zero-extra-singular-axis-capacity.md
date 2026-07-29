# Three zero sites leave room for at most three additional singular centres

## 1. Outcome

Retain the cyclic three-zero branch of the two-coordinate-factor,
rank-two direct-quadratic pattern.  Its forced nonzero singular shore contains
two type-`10` centres and two type-`22` centres, with coordinate-axis
coverages

\[
 C(10)=\{0,1\},\qquad C(22)=\{2\}.                     \tag{1}
\]

Let `A_extra` be the set of every other nonzero singular site.  For a
singular site `a`, put

\[
 C_a=\{c:e_c\in\operatorname {im}P_a\},\qquad
 M_a=\{0,1,2\}\setminus C_a .                          \tag{2}
\]

Every `M_a` is nonempty.  The three-zero Hall--Schmidt inequalities imply:

**Lemma 1.1 (extra-centre capacity).**

1. each target colour belongs to \(M_a\) for at most one
   \(a\in A_{\rm extra}\);
2. no \(M_a\) contains both \(0\) and \(1\);
3. the sets \((M_a)_{a\in A_{\rm extra}}\) are pairwise disjoint, and
   consequently

   \[
                         |A_{\rm extra}|\le3.            \tag{3}
   \]
4. every \(a\in A_{\rm extra}\) has the common centre beta value
   \(\beta_a=\mu\).

Thus “additional nonzero singular sites” is a finite incidence boundary,
not an arbitrarily large shore.  Up to permuting the two axes `0,1`, the
possible nonempty missed-axis families are subfamilies of

\[
 \{\{0\},\{1\},\{2\}\},\qquad
 \{\{0,2\},\{1\}\},\qquad
 \{\{1,2\},\{0\}\}.                                  \tag{4}
\]

The statement retains noncoordinate images: `C_a` records only coordinate
axes actually contained in the image.  A noncoordinate line or plane merely
makes `M_a` larger and is therefore covered by the same inequalities.

## 2. Proof

For the full nonzero singular shore `A`, define as in
[live-multiple-zero-hall-factorization.md](live-multiple-zero-hall-factorization.md)

\[
 D_c=\{a\in A:e_c\notin\operatorname {im}P_a\}.
\]

With exactly \(s=3\) literal zero sites, the Hall--Schmidt theorem gives

\[
 |D_c|\le3,qquad |D_c\cap D_d|\le2\quad(c\ne d).       \tag{5}
\]

The two forced type-`22` centres lie in \(D_0\cap D_1\), while the two
forced type-`10` centres lie in \(D_2\).  In fact the base contribution is

\[
 |D_0|=|D_1|=|D_2|=2,qquad |D_0\cap D_1|=2             \tag{6}
\]

before the extra sites are inserted.  Therefore (5) leaves only one unused
slot in each `D_c`.  No two extra sites can miss the same colour, proving
part 1 and pairwise disjointness.  The intersection bound in (5) is already
saturated for `(c,d)=(0,1)`, so an extra site cannot miss both axes, proving
part 2.

Finally, `P_a` is singular, so its image is a proper subspace of the ternary
local space and cannot contain all three coordinate basis vectors.  Hence
`M_a` is nonempty.  Pairwise disjoint nonempty subsets of a three-element set
number at most three, which proves (3).  Listing the possibilities subject to
\(\{0,1\}\not\subseteq M_a\) gives (4).

It remains to synchronize the beta values.  Let \(a\in A_{\rm extra}\).
If \(P_k\ne0\), then the beta-parity lemma excludes
\(\beta_a+\beta_k=0\): this is its direct conclusion when \(P_k\) is
singular, while for invertible \(P_k\) the equality would make the right
side of

\[
       P_aHP_k^{\mathsf T}=(\beta_a+\beta_k)q_{ak}       \tag{7}
\]

zero although its left side has positive rank.  Hence every such block
\(q_{ak}\) has rank at most \(\operatorname {rank}P_a<3\).
Since \(G_3(q)\) is spanning and connected, \(a\) therefore has a
rank-three neighbour \(y\) with \(P_y=0\).  Each of the three zero sites
has beta value \(-\mu\).  Applying (7) to the invertible block \(q_{ay}\)
gives

\[
             0=(\beta_a-\mu)q_{ay},
             \qquad\text{hence}\qquad \beta_a=\mu.       \tag{8}
\]

This proves part 4.  Thus extra singular centres enlarge only the finite
missed-axis family (4); they introduce no new beta class.

## 3. Exact audit

[verify_live_three_zero_extra_singular_axis_capacity.py](../computations/verify_live_three_zero_extra_singular_axis_capacity.py)
enumerates every multiset of nonempty missed-axis subsets, checks (5) after
adjoining the four forced centres, and verifies (3)--(4).  The computation is
only a census audit; the proof above is the complete argument.
