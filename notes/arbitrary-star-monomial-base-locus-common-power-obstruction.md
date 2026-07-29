# Arbitrary star rows do not lift the monomial base locus

## 1. Outcome

The coordinate support assumption on the six star rows in
[`invertible-monomial-base-locus-common-power-obstruction.md`](invertible-monomial-base-locus-common-power-obstruction.md)
can be removed completely while the common degree-four multiplier remains
the sum of three pure monomial lifts.  The missing pairs need not initially
be assumed distinct: the nine responses force distinctness.

Let \(U\) be a six-set.  At every \(u\in U\), let \(V_u\) contain three
distinguished independent vectors
\(e_0^{(u)},e_1^{(u)},e_2^{(u)}\).  Choose three two-sets
\(P_0,P_1,P_2\subset U\), repetitions allowed, and nonzero complex numbers
\(\lambda_i\), and put

\[
 F_i=\bigotimes_{u\notin P_i}e_i^{(u)},\qquad
 F=\sum_{i=0}^2\lambda_iF_i,\qquad
 X_i=\bigotimes_{u\in U}e_i^{(u)}.                       \tag{1}
\]

The six forms

\[
 p_0,p_1,p_2,s_0,s_1,s_2\in\bigoplus_{u\in U}V_u       \tag{2}
\]

are now arbitrary.  They may reach any number of sites, have arbitrary
components outside the three displayed colour axes, vanish, be dependent,
and use every possible complex cancellation.  Impose all nine exact
responses

\[
                 p_i s_jF=\delta_{ij}\lambda_iX_i
                 \qquad(0\le i,j\le2).                 \tag{3}
\]

The responses first rule out every repeated-pair triple, and there are only
two possible support graphs among the remaining distinct pairs:

1. three disjoint edges;
2. a two-edge path and a disjoint edge.

Both shapes really do admit (3); coordinate rows give witnesses.  However,
neither can also satisfy

\[
                         F=q^{[2]},\qquad q^{[3]}=0       \tag{4}
\]

for a six-site quadratic \(q\).  Thus (1)--(4) have no complex solution.
This closes the arbitrary-star version of the three-monomial base locus.

The exact checker
[`verify_arbitrary_star_monomial_base_locus_obstruction.py`](../computations/verify_arbitrary_star_monomial_base_locus_obstruction.py)
enumerates all \(15^3=3375\) colour-indexed pair triples, rejects all 645
repeated-pair triples directly, recovers the 455 distinct labelled-edge
sets, verifies the two positive response tables, and computes unsaturated
characteristic-zero unit ideals for the three excluded graph types.

## 2. The literal pairwise response equations

Work in the site-square-zero algebra

\[
 \mathcal R_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u),
 \qquad V_uV_u=0.                                      \tag{5}
\]

Write \(p_{i,u}\) and \(s_{j,u}\) for the components of the forms at site
\(u\).  If \(P_k=\{a,b\}\), multiplication by \(F_k\) kills every component
of a linear form except those at \(a,b\).  Consequently its literal
two-site response is

\[
 B_{ij}^{(k)}=
 p_{i,a}\otimes s_{j,b}+s_{j,a}\otimes p_{i,b}
 \in V_a\otimes V_b.                                  \tag{6}
\]

There is no cancellation between different \(k\)'s.  Indeed, for
\(k\ne\ell\), choose a site outside \(P_k\cup P_\ell\), which is possible
because that union has at most four of the six sites.  The corresponding
local factor is \(e_k\) in every tensor from the \(F_k\) response space and
\(e_\ell\) in every tensor from the \(F_\ell\) response space.  The two
spaces are therefore linearly disjoint.  It follows that (3) is exactly

\[
 \boxed{
 B_{ij}^{(k)}=
 \delta_{ij}\delta_{ik}\,
 e_i^{(a)}\otimes e_i^{(b)}}
 \qquad(0\le i,j,k\le2).                               \tag{7}
\]

Notice that the nonzero weights have cancelled from the sole nonzero
equation.  Formula (7) retains both endpoint orders in (6); replacing it by
one ordered product would be an invalid coordinate-row assumption.

If the \(V_u\)'s contain additional colour directions, choose a linear
projection \(V_u\to\langle e_0^{(u)},e_1^{(u)},e_2^{(u)}\rangle\) fixing
the three displayed axes.  Together with the identity on scalars, these
maps induce an algebra homomorphism of the site-square-zero algebras.
Applying it to (7) shows that any solution in larger local spaces gives a
solution of the same equations in three dimensions.  It is enough to
classify the latter, without restricting the original forms.

### 2.1 Repeated pairs are impossible

Suppose \(P_i=P_k=\{a,b\}\) for distinct \(i,k\).  In (7), take the
diagonal row \((i,i)\).  The equation indexed by the lift \(k=i\) says

\[
 B_{ii}^{(i)}=e_i^{(a)}\otimes e_i^{(b)},
\]

whereas the equation indexed by the lift \(k\ne i\) says

\[
 B_{ii}^{(k)}=0.
\]

Because the underlying endpoint pair is the same, the two left sides are
the identical tensor
\(p_{i,a}\otimes s_{i,b}+s_{i,a}\otimes p_{i,b}\).  Their right sides
are respectively nonzero and zero, a contradiction.  Thus (3) itself
forces \(P_0,P_1,P_2\) to be distinct; this uses neither a coordinate-row
assumption nor the common-power equations.

## 3. Exact support-graph classification

Three distinct edges in a simple graph have exactly five unlabelled shapes.
Their labelled counts on six vertices are

| shape | degree multiset on used sites | labelled triples |
|---|---:|---:|
| three-edge star | \((3,1,1,1)\) | \(60\) |
| triangle | \((2,2,2)\) | \(20\) |
| three-edge path | \((2,2,1,1)\) | \(180\) |
| two-edge path plus a disjoint edge | \((2,1,1,1,1)\) | \(180\) |
| three-edge matching | \((1,1,1,1,1,1)\) | \(15\) |

The counts sum to \(455=\binom{15}{3}\), so no intersection or endpoint
case is omitted.  Before quotienting by the six assignments of the three
distinct edges to the three target colours, the checker sees 2730 ordered
distinct triples.  Together with the 645 repeated triples already rejected,
these exhaust all \(15^3=3375\) colour-indexed triples.

For a representative \(P_k=\{u_k,v_k\}\), expand (7) in the three local
coordinate bases.  With independent affine variables

\[
 p_{i,u,\alpha},s_{j,u,\alpha}\qquad
 (i,j,\alpha\in\{0,1,2\}),                             \tag{8}
\]

the 243 equations are

\[
 p_{i,u_k,\alpha}s_{j,v_k,\beta}
 +s_{j,u_k,\alpha}p_{i,v_k,\beta}
 -\delta_{ij}\delta_{ik}\delta_{\alpha k}\delta_{\beta k}=0.
                                                                    \tag{9}
\]

These are the full affine equations: there is no saturation, no declared
nonzero variable, and no rank or support split.  Singular over
\(\mathbb Q\) returns the reduced conclusion \([1]\) for representatives of
the three-edge star, triangle, and three-edge path.  Hence those systems
have no solution over \(\mathbb C\), including every degenerate and
cancellation stratum.  Relabelling sites and simultaneously relabelling
the edge index, row index, and distinguished colour takes any labelled
member of a graph type to its representative, so one exact ideal per type
suffices.

For reproducibility, the generator ledgers and exact audit sizes are

| type | variables | equations | SHA-256 of ordered generators |
|---|---:|---:|---|
| three-edge star | 72 | 243 | `6bbc861333ee4695fd0566ad1d781cfcb660c1ec5e3c32057dc225e847e60a46` |
| triangle | 54 | 243 | `6c02a565de695e6cd49f8f2d0d1660aefc2b85ba7291678f3b45235cb9efb760` |
| three-edge path | 72 | 243 | `ee68af14f146776443fc1479188c9e9cb4439850097a457e4f2cc895e426a905` |

The two remaining shapes have literal solutions.  For three disjoint pairs
\(P_i=\{u_i,v_i\}\), take

\[
 p_i=e_i^{(u_i)},\qquad s_i=e_i^{(v_i)}.                \tag{10}
\]

For the second shape, label

\[
 P_0=\{a,b\},\qquad P_1=\{b,c\},\qquad P_2=\{d,e\}
                                                                    \tag{11}
\]

and take

\[
 (p_0,s_0)=(e_0^{(a)},e_0^{(b)}),\quad
 (p_1,s_1)=(e_1^{(b)},e_1^{(c)}),\quad
 (p_2,s_2)=(e_2^{(d)},e_2^{(e)}).                       \tag{12}
\]

A direct substitution in (7), also performed by the checker, verifies all
nine products.  This proves the claimed if-and-only-if classification.

## 4. Common powers exclude both surviving shapes

Let \(q=\sum_{\{u,v\}}q_{uv}\) be an arbitrary quadratic, with
\(q_{uv}\in V_u\otimes V_v\).  The unordered matching powers obey

\[
                         q q^{[2]}=3q^{[3]}.             \tag{13}
\]

Thus (4) gives \(qF=0\).  Only \(q_{P_i}\) can multiply \(F_i\) without
repeating a site.  As above, the three resulting full-support response
spaces are linearly disjoint because the missing pairs are distinct.
Since every \(\lambda_i\ne0\),

\[
                         q_{P_0}=q_{P_1}=q_{P_2}=0.      \tag{14}
\]

### 4.1 Three disjoint pairs

Write the pairs as \(A=\{a_0,a_1\}\), \(B=\{b_0,b_1\}\), and
\(C=\{c_0,c_1\}\).  Equation (14) leaves only the \(AB,AC,BC\) blocks.
The \(A\cup B\) and \(A\cup C\) coefficients of \(q^{[2]}=F\) are

\[
 q_{AB}^{[2]}=\lambda_2F_2,\qquad
 q_{AC}^{[2]}=\lambda_1F_1.                             \tag{15}
\]

Every coefficient on two \(A\)-sites, one \(B\)-site, and one \(C\)-site
is zero, so

\[
                         q_{AB}q_{AC}=0.                 \tag{16}
\]

Put \(X_{ij}=q_{a_i b_j}\) and \(Y_{ik}=q_{a_i c_k}\).  A nonzero matching
term can be selected in each equation of (15); after independently swapping
the two \(B\)- and two \(C\)-sites, assume
\(X_{00},X_{11},Y_{00},Y_{11}\ne0\).  The four-site coefficients of (16)
are

\[
                         X_{0j}Y_{1k}+X_{1j}Y_{0k}=0.    \tag{17}
\]

The cases \((j,k)=(0,1),(1,0)\) first show that all eight displayed blocks
are nonzero.  Flattening either equality in (17) across its two crossed
bipartitions shows that all four blocks have tensor rank one and identify
the same factor line at each \(A\)-site.  Varying \(j,k\) therefore gives

\[
 X_{ij}=x_{ij}a_i b_j,\qquad Y_{ik}=y_{ik}a_i c_k       \tag{18}
\]

with fixed nonzero local vectors and nonzero scalars.  The first equation
of (15) now says the line of \(a_i\) is the colour-2 line, while the
second says the same line is the distinct colour-1 line.  This is
impossible.

### 4.2 A two-edge path plus a disjoint edge

Use (11), and let \(f\) be the sixth site.  From (14),

\[
                         q_{ab}=q_{bc}=q_{de}=0.         \tag{19}
\]

The target coefficient on \(U\setminus P_2=\{a,b,c,f\}\) reduces to

\[
                         q_{ac}q_{bf}=\lambda_2F_2\ne0. \tag{20}
\]

Hence both factors are nonzero.  Successively reading the zero coefficients
on the supports

\[
 abcd, abce, abdf, abef, bcdf, bcef                 \tag{21}
\]

and using only (19), (20), and injectivity of tensoring by a nonzero
disjoint-support tensor gives

\[
 q_{bd}=q_{be}=q_{ad}=q_{ae}=q_{cd}=q_{ce}=0.           \tag{22}
\]

But the coefficient on \(U\setminus P_0=\{c,d,e,f\}\) is then

\[
 q_{cd}q_{ef}+q_{ce}q_{df}+q_{cf}q_{de}=0,              \tag{23}
\]

contrary to its required nonzero value \(\lambda_0F_0\).

The two cases complete the obstruction.

## 5. Exact scope

This theorem allows completely arbitrary six star rows and arbitrary local
vector-space dimensions.  Its restrictive hypothesis is instead the exact
three-term monomial form (1); distinctness of its missing pairs is a
consequence of the response equations.  It does not cover a common
degree-four multiplier whose \(i\)-th target lift is a sum of several
four-site tensors.  It therefore does not by itself close the full cyclic
or diagonal direct-block orbit and
is not a global proof of route U1.  The next bounded enlargement is to keep
the arbitrary rows and all nine products while replacing one \(F_i\) by a
genuine multi-monomial four-site lift; dropping the products would re-open
the known repeated-pair \(K_4\) common-power countermodel.
