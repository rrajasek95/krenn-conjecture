# The global cut--Wick route is sharp at four sites and closed at six

## Result

Let (V_i=\mathbb C^d), let (A_{ij}\in V_i\otimes V_j) be arbitrary
decorated pair tensors, and put

\[
 H_n(A)=\sum_{M\in\operatorname {PM}([n])}
             \bigotimes_{ij\in M}A_{ij}.                    \tag{1}
\]

There is a sharp global theorem at four sites:

\[
                 H_4(A)=\Delta_{4,k}
                 \quad\Longrightarrow\quad k\leq3,         \tag{2}
\]

and equality is attained.  In contrast, for every even (n\geq6), no
polynomial identity of the output tensor alone -- including identities made
from fixed contractions, flattenings, catalecticants, apolar covariants, or
secant equations -- can force (k\leq2).  The ternary diagonal tensor

\[
                  \Delta_{n,3}=\sum_{a=0}^2e_a^{\otimes n} \tag{3}
\]

lies in the ordinary and Zariski closure of the image of (1).  This remains
true when the finite covariances in the approximating family are required to
be nonsingular.  Thus a direct output-only polynomial/rank invariant cannot
prove the desired six-site-and-higher obstruction.

The exact cut--Wick expansion below explains the transition.  On a balanced
three-by-three cut, its all-cross channel is a (3\times3) permanent, and a
single cross matching already gives a flattening of maximal rank (d^3).
The surviving global route must retain nonclosed source membership, a
denominator singular at (3), lower Wick sectors together with the covariance,
or the physical one-hot incidence structure.  It cannot avoid all three
physical descents while seeing only (1).

For odd (n), (1) is zero and a nonzero GHZ target is impossible trivially;
all statements below concern the nontrivial even orders.

## 1. Exact cut--Wick identity

Partition the sites as (L\sqcup R=[n]).  For equally sized subsets
(I\subseteq L), (J\subseteq R), define the cross permanent tensor

\[
 \operatorname {Per}_{I,J}(A)=
 \sum_{\sigma:I\overset\sim\longrightarrow J}
       \bigotimes_{i\in I} A_{i,\sigma(i)}.                 \tag{4}
\]

Empty hafnians and permanents are one.  Canonically reordering tensor
factors, (1) has the exact expansion

\[
 H_n(A)=
 \sum_{\substack{I\subseteq L,\ J\subseteq R\\
                  |I|=|J|\\
                  |L\setminus I|,|R\setminus J|\ \mathrm{even}}}
 H_{L\setminus I}(A)\otimes H_{R\setminus J}(A)
       \otimes\operatorname {Per}_{I,J}(A).                \tag{5}
\]

Indeed, intersect a perfect matching (M) with the cut.  Its cross edges
have endpoint sets (I,J) and give one bijection (I\to J); its remaining
edges are independent perfect matchings of (L\setminus I) and
(R\setminus J).  Conversely, those three pieces have disjoint endpoints
and reconstruct (M) uniquely.  This proves (5) coefficient by coefficient,
without positivity, genericity, or a rank assumption on any (A_{ij}).

After evaluating a colour word, write the resulting scalar edge entries as
(b_{ij}).  For (|L|=|R|=3), only one or three crossing edges are possible,
so (5) reads

\[
 \operatorname {Haf}(B)=
 \sum_{i\in L,\,j\in R}
 b_{ij}\operatorname {Haf}(B_{L\setminus i})
       \operatorname {Haf}(B_{R\setminus j})
 +\operatorname {Per}(B_{L,R}).                            \tag{6}
\]

The first sector contains nine perfect matchings and the permanent contains
the other six.  Thus (6) is an exact identity, but it does not impose a small
rank condition: the permanent is an independent all-cross channel.

## 2. The sharp four-site theorem

Fix a site (p).  Expanding a matching by the partner of (p) gives

\[
 H_4(A)=\sum_{j\ne p} A_{pj}\otimes
                   H_{[4]\setminus\{p,j\}}(A).             \tag{7}
\]

Each of the three summands has partition rank at most one, across
(\{p,j\}\mid[4]\setminus\{p,j\}).  The diagonal tensor
(\Delta_{4,k}) has partition rank exactly (k).  One quick proof of the
latter fact is induction on tensor order: contract a coordinate against a
covector annihilating all singleton factors in a putative decomposition;
the contracted diagonal retains at least (k-u) diagonal entries after
removing (u) singleton terms, while only (r-u) partition-rank-one terms
remain.  The base case is ordinary matrix rank.  Hence (7) proves (2).

The bound is attained with rank-one, same-colour edges.  Give the two edges
of each (K_4) perfect matching one colour:

\[
 \begin{array}{c|c}
 0&01\mid23\\
 1&02\mid13\\
 2&03\mid12.
 \end{array}                                                \tag{8}
\]

The support has exactly those three perfect matchings and their tensor sum
is exactly (e_0^{\otimes4}+e_1^{\otimes4}+e_2^{\otimes4}).

## 3. Flattening and catalecticant candidates fail maximally

Let (n=2h), (L=\{0,\ldots,h-1\}), and
(R=\{h,\ldots,2h-1\}).  Set

\[
             A_{i,h+i}=\sum_{a=0}^{d-1}e_a\otimes e_a,
 \qquad A_{ij}=0\quad\hbox{otherwise}.                     \tag{9}
\]

There is one supported perfect matching.  Consequently

\[
 H_{2h}(A)_{x_0\ldots x_{h-1},y_0\ldots y_{h-1}}
       =\prod_{i=0}^{h-1}\delta_{x_i,y_i}.                  \tag{10}
\]

The (L\mid R) flattening is the identity matrix of size (d^h), so it has
maximal rank (d^h).  In particular, at (n=6,d=3) the rank is (27), not
two or three.  Any contraction leaving one paired block can similarly retain
rank (d).  Thus no universal low-flattening-rank or low-catalecticant-rank
claim is available for arbitrary decorated pair matrices.

This does not by itself rule out a subtler polynomial identity.  The closure
counterexample does.

## 4. Sharp counterexample to every output-only polynomial separator

The theorem and two independent exact checkers pinned below construct, for
every even (n\geq6), a Laurent family of decorated pair matrices satisfying

\[
             H_n(A(t))=\Delta_{n,3}+\sum_{r\geq1}t^rT_r,    \tag{11}
\]

with a nonsingular (3n\times3n) covariance for every (t\ne0) and

\[
                       \det Z(A(t))=(-1)^{3n/2}.            \tag{12}
\]

The six-site seed is the triangular prism

\[
\begin{array}{c|ccc}
0&03:t&12:t^{-1}&45:1\\
1&14:1&02:1&35:1\\
2&25:1&01:1&34:1,
\end{array}                                                 \tag{13}
\]

whose three colour matchings give the three pure words and whose sole extra
matching gives (t e_{012012}).  A valuation-preserving
vertex-to-triangle operation propagates (13) by two sites at a time.  This is
an explicit ordinary-limit, not merely a dimension count.

Let (P) be any polynomial in the coordinates of the output tensor which
vanishes on every (H_n(A)).  Substituting (11) gives an ordinary polynomial
in (t) which vanishes for every (t\ne0), hence at zero.  Therefore

\[
                            P(\Delta_{n,3})=0.              \tag{14}
\]

Every fixed contraction, flattening, exterior power, catalecticant, apolar
covariant, tensor product, or symmetrization has polynomial coordinates in
the entries of (H_n(A)).  Pulling back any polynomial relation on its output
reduces to (14).  In particular, every universal rank upper bound expressed
by minors is inherited by the ternary GHZ boundary point and cannot exclude
it.  The same argument applies to a rational invariant whose denominator is
nonzero at (Delta_{n,3}).

Hence the requested global output identity exists sharply at four sites but
cannot exist in the proposed form at any even order at least six.  This is a
counterexample to the invariant route, not an exact ternary Krenn source:
the Laurent parameter diverges in the source while its top tensor converges.
That nonclosed finite-source membership is exactly what an output-only
polynomial invariant forgets.

## Reproducibility

The new checker verifies (5) coefficientwise for every cut through eight
sites, (8) on all (3^4) words, and the exact ranks in (10).  It pins the
uniform Laurent theorem's two independent checkers from commit `f88b514`:

* `verify_global_wick_top_invariant_counterguard.py`:
  `192c03668e56262315e685f49c29fafeed071faf2a292dfdc94544fd7a5f4183`;
* `verify_global_wick_top_invariant_counterguard_independent_audit.py`:
  `7904fa7841aebbeeb95196fde2e1d16e0a7c0857e79f62f9ba95611d7dcb7565`.

Run

```text
python3 computations/verify_global_cut_wick_invariant_boundary.py
python3 -O computations/verify_global_cut_wick_invariant_boundary.py
python3 -I computations/verify_global_cut_wick_invariant_boundary.py
python3 -S computations/verify_global_cut_wick_invariant_boundary.py
```

All modes print digest
`f3f391d6e2d742d5d405d5a681354bade5c629dd88f26d662d01aa7b7d52bc61`.
