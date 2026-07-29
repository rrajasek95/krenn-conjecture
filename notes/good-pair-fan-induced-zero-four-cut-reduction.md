# A large regular fan forces a growing induced-zero shore

## 1. Outcome

Let \(B\) have even size \(N\), and suppose that arbitrary
endpoint-ordered aggregate blocks satisfy

\[
                         H_B(A)=\Delta_{B,3}.             \tag{1}
\]

Combine the target-flattening good-pair fan with the regular
nonbipartite source-Hessian branch.  Fix an integer \(k\ge1\) with
\(N\ge7k+7\).  One of the following two alternatives holds.

1. At least \(N-7k-6\) pairs in one common-endpoint good fan have an extra
   internal Hessian kernel, a disconnected internal rank-three graph, or a
   connected bipartite internal rank-three graph.
2. There is a shore \(S=\{r,u_1,\ldots,u_k\}\) of \(k+1\) vertices such
   that every aggregate block internal to \(S\) is literally zero.  Every
   colour row from any vertex of \(S\) to its complement is supported on
   at most two physical sites, and each of the \(k+1\) triples of aggregate
   rows is injective.

Thus, after the three named Hessian escape charts are excluded, the size of
the forced zero shore grows linearly with \(N\).  The first four-vertex
case is especially concrete: at \(k=3\) and \(N\ge28\), either at least
\(N-27\) fan pairs escape or there is a literal aggregate zero \(K_4\).

The second alternative has an exact common-power equation.  Write
\(N=2m\), put \(h=k+1\), enumerate \(S=\{x_0,\ldots,x_{h-1}\}\), and put

\[
 D=B\setminus S.
\]

Let \(q\) be the quadratic formed by the blocks internal to \(D\), and
write \(p^{(j)}_c\) for the endpoint-oriented colour-\(c\) row from
\(x_j\) into \(D\).  Then all \(3^h\) shore equations are

\[
 \boxed{
 \left(\prod_{j=0}^{h-1}p^{(j)}_{c_j}\right)q^{[m-h]}
    =\delta_{c_0=c_1=\cdots=c_{h-1}}X_{c_0}^D.}          \tag{2}
\]

For the first new \(h=4\) case, write the four row triples as
\(p_c,s_d,t_e,\ell_f\).  Equation (2) becomes the 81 identities

\[
 p_c s_d t_e\ell_f\,q^{[m-4]}
    =\delta_{c=d=e=f}X_c^D,
 \qquad 0\le c,d,e,f\le2.                               \tag{2a}
\]

Here \(q^{[j]}=q^j/j!\) in the site-square-zero algebra.  Equation (2)
retains the actual common internal quadratic, all endpoint asymmetry,
parallel aggregates, zero entries, and arbitrary complex cancellation.
All zero-block and support statements are for one fixed functorial ternary
projection of the palette.  They do not assert termwise vanishing of
parallel sources or simultaneous zero blocks for every palette triple.
It is not an all-even descent: the remaining task is to exclude this
sparse, four-frame common-power identity or to close the escape charts in
alternative 1.

## 2. Input from a regular good-pair fan

The target-flattening essential-star theorem supplies a vertex \(r\) with
at least \(N-7\) good neighbours.  Call a fan pair regular
nonbipartite when its internal source Hessian has only the vertex-gauge
kernel and its rank-three block graph is connected and nonbipartite.
Let \(F\) be the regular neighbours in the fan.

For every \(x\in F\), the sparse-row consequence of the source-Hessian
equations gives

\[
 |S_c(r)\setminus\{x\}|\le2\qquad(c=0,1,2),             \tag{3}
\]

where \(S_c(r)\) is the global physical support of row \(c\) at \(r\).
If \(|F|\ge4\), the elementary four-deletion argument gives

\[
 |S_c(r)|\le2,
 \qquad
 C:=S_0(r)\cup S_1(r)\cup S_2(r),\qquad |C|\le6.       \tag{4}
\]

Thus every \(x\in Z:=F\setminus C\) satisfies \(A_{rx}=0\).  Applying
the same sparse-row theorem at the other endpoint of the regular pair,
and observing that deleting \(r\) removes a zero block, gives

\[
 \left|S_d(x)\right|\le2\qquad(d=0,1,2).               \tag{5}
\]

In particular, the aggregate nonzero-block degree of each \(x\in Z\) is
at most six.

## 3. Selecting a growing mutually zero set

Form the simple graph \(G_Z\) on \(Z\) in which \(xy\) is an edge
exactly when the aggregate block \(A_{xy}\) is nonzero.  Equation (5)
implies

\[
                              \Delta(G_Z)\le6.           \tag{6}
\]

Greedy colouring therefore uses at most seven colours, and \(G_Z\) has
an independent set of size at least \(\lceil |Z|/7\rceil\).

If \(|F|\le7k-1\), at least

\[
                   (N-7)-(7k-1)=N-7k-6                 \tag{7}
\]

fan pairs are nonregular, which is alternative 1.  If \(|F|\ge7k\),
then

\[
 |Z|\ge |F|-6\ge7k-6,
 \qquad
 \left\lceil {|Z|\over7}\right\rceil\ge k.            \tag{7a}
\]

Hence (6) supplies independent vertices \(u_1,\ldots,u_k\).  Adjoining
the fan centre gives \(S=\{r,u_1,\ldots,u_k\}\), and by construction
every aggregate block internal to \(S\) is zero.  At \(k=3\), this says

\[
 A_{ru}=A_{rv}=A_{rw}=A_{uv}=A_{uw}=A_{vw}=0.           \tag{8}
\]

Notice that no separate good-clique argument is needed.  Deleting a zero
block from an endpoint removes no mode support.  Since the full incident
mode supports span the three-dimensional target mode, every mutual pair in
\(S\) is automatically doubly aggregate-injective.

Moreover, every block internal to \(S\) is zero.  Consequently the star
of any named vertex into \(D\) is its complete global star.  All \(h\)
triples

\[
                    (p^{(j)}_0,p^{(j)}_1,p^{(j)}_2),
             \qquad 0\le j<h,                           \tag{9}
\]

are linearly independent in \(\bigoplus_{x\in D}V_x\), and every row in
(9) has physical support at most two.  The two-hole coordinate-anchor
lemma additionally gives each row a nonzero local component on its
corresponding target axis.  Because every named-to-named block is zero,
every such anchor lies in \(D\).

## 4. Exact zero-shore expansion

Decompose the source quadratic by the \(h\) named vertices:

\[
 a=q+\sum_{j=0}^{h-1}\sum_c e_c^{(x_j)}p_c^{(j)}.       \tag{10}
\]

There is no named-to-named term.  Hence every perfect matching of \(B\)
sends all \(h\) named vertices to distinct sites of \(D\), and matches the
remaining \(N-2h\) sites internally.  Extracting colours
\((c_0,\ldots,c_{h-1})\) at the named slots in \(a^{[m]}\) gives exactly

\[
              \left(\prod_{j=0}^{h-1}p_{c_j}^{(j)}\right)
                         q^{[m-h]}.                      \tag{11}
\]

Divided powers count each residual internal perfect matching once.  The
same \(h\)-slot contraction of the target is zero unless all \(h\) colours
agree, and then equals \(X_c^D\).  This proves (2), with no selection of
individual source terms from a cancelling aggregate coefficient.

The number of matching supports contributing to (11), before colour
decoration, is

\[
       (N-h)_{h}\,(N-2h-1)!!,                           \tag{12}
\]

with \((-1)!!=1\) and \((z)_h=z(z-1)\cdots(z-h+1)\).
The first factor assigns distinct complement sites to the ordered named
vertices, and the second matches the rest.  At \(h=4\), (12) is
\((N-4)(N-5)(N-6)(N-7)(N-9)!!\).

## 5. Cancellation-safe finite-port cap

Let

\[
 P=\bigcup_{j=0}^{h-1}\bigcup_{c=0}^2
       \operatorname{supp}_{\rm phys}(p_c^{(j)}).
                                                               \tag{13}
\]

The sparse-row conclusion gives \(|P|\le6h\), so the four-cut case has at
most 24 physical ports.  A nonzero diagonal equation in (2) selects \(h\)
distinct row-support sites, so necessarily \(|P|\ge h\).  The
degree-\((|D|-h)\) tensor
\(Q=q^{[m-h]}\) decomposes as a direct sum of sectors indexed by its set
of \(h\) missing physical sites.  A product of the \(h\) named rows can
fill such a sector only when every missing site lies in \(P\).  All other
hole sectors are annihilated identically, without separating any cancelling
source terms.

Cap every factor in \(D\setminus P\) by a product covector which takes
value one on each of the three target axes.  The retained hole sectors give
one degree-\((|P|-h)\) tensor \(\overline Q\) on \(P\) satisfying

\[
 \left(\prod_{j=0}^{h-1}p^{(j)}_{c_j}\right)\overline Q
    =\delta_{c_0=\cdots=c_{h-1}}X_{c_0}^P.              \tag{14}
\]

This is a finite interface for fixed \(h\).  In particular, the induced
zero \(K_4\) branch reduces cancellation-safely to 81 equations on at most
24 physical ports.  The tensor \(\overline Q\) is the literal capped
projection of the common matching power in (2); it is not asserted to be a
matching power of a quadratic internal to \(P\).

## 6. Exact frontier

Equation (2) is stronger than an abstract diagonal response table: its
\(3^h\) entries are products of sparse injective star frames against one
and the same matching power \(q^{[m-h]}\).  On the other hand, aggregate
injectivity and support size alone do not identify a nonzero matching term
inside those products.  Complex cancellations in \(q^{[m-h]}\) must be
retained.

There are therefore two concrete continuation targets.

1. Prove that the growing zero-shore identities (2), or already their
   four-frame case (2a), cannot hold for sparse injective row frames with
   coordinate anchors and one common matching power.
2. Show that one of the forced nonregular pairs in alternative 1 yields a
   clean cap, a support-reducing kernel direction, or a smaller exact
   source.

Either result must be uniform in \(|D|\); another bounded support census
would not close the conjecture.

## 7. Exact audit

The standalone checker
[verify_good_pair_fan_induced_zero_four_cut_reduction.py](../computations/verify_good_pair_fan_induced_zero_four_cut_reduction.py)

* checks the full \(k\)-parameter fan, regular/escape, zero-set, and
  seven-colour thresholds for every even order through a large range;
* constructs the sharp disjoint-\(K_7\) support graphs for the independence
  estimate;
* enumerates perfect matchings at orders \(8,10,12\), for every available
  shore size through four, verifies that an induced-zero shore leaves
  exactly the all-star class, and checks (12);
* checks the general \(h\)-hole visibility rule behind the finite
  \(6h\)-port cap;
  and
* audits named-endpoint orientation in representative numerical orderings
  on both sides of the complement labels.

The finite checks audit the displayed ledgers and matching partition.  The
uniform proof is the support-degree selection in Sections 2--3 and the
complete matching expansion in Section 4.
