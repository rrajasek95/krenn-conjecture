# Independent audit of the coordinate-monomial common-power obstruction

## 1. Verdict

This is a clean-room audit of
[the primary note](invertible-monomial-base-locus-common-power-obstruction.md).
The two stated obstructions are correct over an arbitrary field, provided
the bracket powers retain their stated meaning as unordered matching sums.
In particular:

1. no quadratic has the three disjoint coordinate-monomial four-site
   tensors, with arbitrary nonzero weights, as its second matching power
   while its third matching power vanishes; and
2. after imposing all nine coordinate-monomial star products, allowing the
   three ordered missing pairs to intersect creates only a directed
   two-edge path plus a disjoint edge, and that case is also impossible.

No positivity, genericity, division, unique-factorization assumption, or
termwise inference from an unstructured cancellation is used. I found no
substantive gap. The result remains only a closure of the explicitly
defined six-site coordinate-monomial base-locus submodel; it is not a
global six-site descent theorem and does not resolve route U1.

The standalone
[classification checker](../computations/audit_oriented_missing_pair_classification_independent.py)
tests every one of the \(30^3=27{,}000\) labelled triples of directed
nonloop pairs on six sites, before assuming distinctness or full vertex
use.

## 2. Matching-power identity and characteristic audit

Write a quadratic as

\[
 q=\sum_{\{u,v\}\subset U}q_{uv},
 \qquad q_{uv}\in V_u\otimes V_v.
\]

The bracket power \(q^{[r]}\) is the sum of the products indexed by
unordered \(r\)-edge matchings. Fixing an unordered three-edge matching
\(\{e_1,e_2,e_3\}\), its product occurs in \(q q^{[2]}\) once for each
choice of the distinguished edge contributed by \(q\). Hence its
coefficient is exactly three, and

\[
 q q^{[2]}=3q^{[3]}.
\]

This is an integral coefficient identity. In characteristic zero it
agrees with \(q^{[r]}=q^r/r!\), but the quotient notation is not needed.
In characteristics two and three the bracket sums still make sense. In
particular, \(q^{[3]}=0\) always implies \(q q^{[2]}=0\); in
characteristic three the right side is zero even before using that
hypothesis. Thus the proof's first inference is valid in every
characteristic.

Products of tensors supported at pairwise distinct sites are ordinary
tensor products. Consequently, tensoring by a fixed nonzero pure tensor
is injective, and a product of two disjoint-support tensors is nonzero if
and only if both factors are nonzero. These are the only cancellation or
zero-divisor facts used below.

## 3. Reconstruction of the disjoint-pair proof

Let \(U=A\mathbin{\dot\cup}B\mathbin{\dot\cup}C\), with each part a
two-set, and let \(F_i\) be pure color \(i\) on \(U\setminus P_i\), where
\((P_0,P_1,P_2)=(A,B,C)\). Suppose

\[
 q^{[2]}=\lambda_0F_0+\lambda_1F_1+\lambda_2F_2,
 \qquad q^{[3]}=0,
 \qquad \lambda_i\ne0.                                  \tag{A1}
\]

Multiplication by \(q\) and the identity above give
\(q\sum_i\lambda_iF_i=0\). A block \(q_{uv}\) can multiply \(F_i\)
without a repeated site only when \(\{u,v\}=P_i\). For \(i\ne j\), the
two resulting full-support subspaces are linearly disjoint: on the third
pair \(U\setminus(P_i\cup P_j)\), their fixed coordinate colors are \(i\)
and \(j\). Therefore each term vanishes separately. Injectivity of
tensoring with \(F_i\ne0\), together with \(\lambda_i\ne0\), gives

\[
 q_A=q_B=q_C=0.                                         \tag{A2}
\]

Thus \(q=q_{AB}+q_{AC}+q_{BC}\). Extracting the components supported on
\(A\cup B\) and \(A\cup C\) gives

\[
 q_{AB}^{[2]}=\lambda_2F_2,
 \qquad q_{AC}^{[2]}=\lambda_1F_1.                      \tag{A3}
\]

On a support containing both \(A\)-sites, one \(B\)-site, and one
\(C\)-site, the target is zero. After (A2), its only surviving matching
terms consist of one \(AB\) edge and one \(AC\) edge. Hence

\[
 q_{AB}q_{AC}=0.                                        \tag{A4}
\]

For clarity, the primary note's sentence that no product involving
\(q_{BC}\) has such support is read after (A2): the formal alternative is
an \(AA\) edge times a \(BC\) edge, and its \(AA\) factor is already zero.
This is only an expository shorthand, not a missing term in the argument.

Write

\[
 X_{ij}=q_{a_i b_j},\qquad Y_{ik}=q_{a_i c_k}.
\]

Equation (A3) becomes

\[
 X_{00}X_{11}+X_{01}X_{10}=\lambda_2F_2,
 \qquad
 Y_{00}Y_{11}+Y_{01}Y_{10}=\lambda_1F_1.                \tag{A5}
\]

Each right side is nonzero, so at least one of the two matching products
on each left side is nonzero. Independently swapping the two \(B\)-sites
and the two \(C\)-sites permits the normalization

\[
 X_{00},X_{11},Y_{00},Y_{11}\ne0.                       \tag{A6}
\]

The \(a_0a_1b_jc_k\) coefficient of (A4) is

\[
 X_{0j}Y_{1k}+X_{1j}Y_{0k}=0.                           \tag{A7}
\]

For \((j,k)=(0,1)\), the first product is nonzero, so the second is
nonzero; this forces \(X_{10},Y_{01}\ne0\). For \((j,k)=(1,0)\), the
second product is nonzero, so the first is nonzero; this forces
\(X_{01},Y_{10}\ne0\). Hence all eight blocks are nonzero. This
propagation remains valid in characteristic two because equality of a
nonzero tensor with the negative of another tensor still makes the other
tensor nonzero.

It remains to audit the crossing lemma rather than assume it. For nonzero

\[
 X\in A\otimes B,\quad Y\in C\otimes D,\quad
 Z\in A\otimes D,\quad W\in C\otimes B,
 \qquad XY=ZW,                                           \tag{A8}
\]

flatten across \((A\otimes B)|(C\otimes D)\). The left side has rank one,
whereas the reshaped right side has rank
\(\operatorname{rank}(Z)\operatorname{rank}(W)\). Both ranks are positive,
so \(Z,W\) have rank one. Flattening across
\((A\otimes D)|(C\otimes B)\) similarly makes \(X,Y\) rank one. Equality
of the resulting nonzero fourfold decomposable tensors identifies their
factor lines at every named space. Applying this to every (A7), with the
minus sign absorbed in a scalar, and varying \(j,k\), produces fixed local
lines

\[
 X_{ij}=x_{ij}a_i b_j,\qquad
 Y_{ik}=y_{ik}a_i c_k,
 \qquad x_{ij},y_{ik}\ne0.                              \tag{A9}
\]

The complete bipartite set of equations (A7) is important here: it makes
the line \(\mathbb F a_i\) common to every \(X_{ij}\) and \(Y_{ik}\).
Substitution in (A5) shows that its first equation has local \(A\)-factor
lines \(\mathbb F e_2\), while its second has local \(A\)-factor lines
\(\mathbb F e_1\). Their scalar prefactors cannot vanish because the
right sides do not. Thus the same \(a_i\) line would have to be two
distinct coordinate axes, the required contradiction.

## 4. Reconstruction of all nine products and the pair classification

Now allow ordered missing pairs \(P_k=(u_k,v_k)\) and set

\[
 F=\sum_k\lambda_kF_k,\qquad
 p_i=e_i^{(u_i)},\qquad s_j=e_j^{(v_j)},
\]

where \(F_k\) is pure color \(k\) on \(U\setminus P_k\). A literal
one-term computation gives

\[
 p_i s_jF_k\ne0
 \quad\Longleftrightarrow\quad
 u_i\ne v_j\ \hbox{ and }\ \{u_i,v_j\}=\{u_k,v_k\}.      \tag{A10}
\]

If \(u_i=v_j\), the two linear factors meet at one site and their product
is zero in the local square-zero algebra. Otherwise both sites must be
exactly the two omitted by \(F_k\). Terms with different \(k\) cannot
cancel even for specially chosen nonzero \(\lambda_k\): their four
complement sites carry different fixed coordinate colors.

For \(i=j\), term \(k=i\) is the required \(\lambda_iX_i\). Formula (A10)
shows that any repeated underlying pair would contribute an additional,
linearly independent mixed word. Therefore all three underlying pairs are
distinct. For \(i\ne j\), the required zero product is then equivalent to

\[
 u_i\ne v_j\quad\Longrightarrow\quad
 \{u_i,v_j\}\notin\{P_0,P_1,P_2\}.                      \tag{A11}
\]

This derivation uses all nine products and covers repeated pairs and all
orientations.

Here is an independent classification from (A11). If two underlying
pairs meet, they cannot both point out of their common vertex: taking the
tail of one and the head of the other reproduces the latter pair in
(A11). The same argument excludes two edges pointing into the common
vertex. Hence they form a directed path \(a\to b\to c\), after relabeling.
A third edge:

* cannot meet \(b\), because either orientation agrees there with one of
  the two existing orientations;
* cannot join \(a\) and \(c\), because
  \(\{u_0,v_1\}=\{a,c\}\) is then the third pair;
* cannot join \(a\) to a new site: its only locally possible orientation
  is \(d\to a\), after which \(\{u_1,v_2\}=\{a,b\}=P_0\);
* cannot join \(c\) to a new site, by the symmetric argument.

The third pair is therefore disjoint from the path. Conversely, if no two
pairs meet, all three are disjoint. Thus the only types are three disjoint
pairs, using all six sites, and a directed two-edge path plus a disjoint
directed edge, using five sites and leaving exactly one unused site. The
disjoint edge can have either orientation.

The standalone exhaustive audit directly tests (A10), rather than
assuming (A11). Its output is:

    oriented missing-pair classification independent audit: PASS
    labelled directed triples checked: 27000
    triples satisfying all nine products: 5040
    three disjoint pairs: 720
    directed two-edge path plus disjoint pair: 4320

It also verifies, for every labelled triple, that the literal nine-product
condition is equivalent to distinct underlying pairs plus (A11).

## 5. Literal elimination of the intersecting type

Take the surviving intersecting configuration

\[
 P_0=(a,b),\qquad P_1=(b,c),\qquad P_2=(d,e),
\]

and call the unused sixth site \(f\). Suppose \(F=q^{[2]}\) and
\(q^{[3]}=0\). From \(qF=0\), only
\(q_{ab}F_0,q_{bc}F_1,q_{de}F_2\) can reach full support. These three
subspaces are independent already at site \(f\), which is colored \(0,1,2\)
respectively. Nonzero \(\lambda_i\) and tensor-product injectivity give

\[
 q_{ab}=q_{bc}=q_{de}=0.                                \tag{A12}
\]

The following table independently expands every four-site coefficient
used in the elimination. Each row lists all three perfect-matching terms,
then applies only zeros established in earlier rows.

| support | matching coefficient | consequence |
|---|---|---|
| \(abcf=U\setminus P_2\) | \(q_{ab}q_{cf}+q_{ac}q_{bf}+q_{af}q_{bc}\) | \(q_{ac}q_{bf}=\lambda_2F_2\ne0\) |
| \(abcd\) | \(q_{ab}q_{cd}+q_{ac}q_{bd}+q_{ad}q_{bc}\) | \(q_{bd}=0\) |
| \(abce\) | \(q_{ab}q_{ce}+q_{ac}q_{be}+q_{ae}q_{bc}\) | \(q_{be}=0\) |
| \(abdf\) | \(q_{ab}q_{df}+q_{ad}q_{bf}+q_{af}q_{bd}\) | \(q_{ad}=0\) |
| \(abef\) | \(q_{ab}q_{ef}+q_{ae}q_{bf}+q_{af}q_{be}\) | \(q_{ae}=0\) |
| \(bcdf\) | \(q_{bc}q_{df}+q_{bd}q_{cf}+q_{bf}q_{cd}\) | \(q_{cd}=0\) |
| \(bcef\) | \(q_{bc}q_{ef}+q_{be}q_{cf}+q_{bf}q_{ce}\) | \(q_{ce}=0\) |

The first row makes both \(q_{ac}\) and \(q_{bf}\) nonzero. Every later
inference divides by neither tensor nor scalar; it uses only that the
displayed product has disjoint site support and tensoring by a nonzero
tensor is injective. All six nontarget supports in the table have zero
coefficient in \(F\).

Finally, the required \(F_0\) component on \(cdef\) is

\[
 q_{cd}q_{ef}+q_{ce}q_{df}+q_{cf}q_{de}=0
\]

by (A12) and the last two table rows. This contradicts
\(\lambda_0F_0\ne0\). The chain-plus-disjoint-edge case is therefore
excluded by literal coefficient equations, with no hidden cancellation
assumption.

## 6. Weights, implication, and exact scope

Every use of a weight is only the implication \(\lambda_iF_i\ne0\), so
all three \(\lambda_i\) may be arbitrary nonzero field elements and need
not be normalized or algebraically independent. Zero weights are
deliberately outside this submodel: the nine-cap table being closed has
three active diagonal target values. The theorem makes no assertion about
a degeneration in which one of those values is absent.

At the six-site base locus of the invertible-monomial nine-cap analysis,
the physical source conditions are exactly that the common multiplier be
one second matching power \(F=q^{[2]}\) and that its next power vanish,
\(q^{[3]}=0\). The disjoint formal model from the earlier note has
precisely the first support type, so the disjoint theorem already proves
that it cannot be such a physical lift. Allowing arbitrary ordered missing
pairs while retaining every product
\(p_i s_jF=\delta_{ij}\lambda_iX_i\) gives the hypotheses audited in
Sections 4--5 and is closed as well.

The nine products are essential. If all missing pairs coincide, a
one-factorization of the \(K_4\) on their four-site complement gives a
quadratic with one same-color perfect matching in each of three colors.
Edges from different factors always meet, so its second matching power is
exactly \(F_0+F_1+F_2\); its third matching power is zero because only four
sites are active. It fails the diagonal products through the two extra
mixed words. This independently confirms both the repeated-pair escape
for the power equations alone and why the full product table cannot be
discarded.

The proved implication stops here. General nine-cap solutions can have
star rows supported on several sites and common degree-four target lifts
which are sums of multiple four-site tensors. Neither is covered by the
coordinate-monomial hypotheses. In particular, this theorem does not
close the cyclic or diagonal direct-block orbit in general and does not
establish the all-even descent to six sites.
