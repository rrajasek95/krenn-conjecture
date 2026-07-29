# Independent audit of the arbitrary-star monomial obstruction

## 1. Verdict

The theorem in
[the primary note](arbitrary-star-monomial-base-locus-common-power-obstruction.md)
is sound over \(\mathbb C\), and the literal response equations give one
useful strengthening: the three missing pairs do **not** need to be assumed
distinct.  All nine products first force them to be distinct.  Among the
remaining triples, arbitrary site-supported star rows solve the response
table exactly for two graph shapes:

1. three disjoint pairs;
2. a two-edge path plus a disjoint pair.

The already proved common-power arguments exclude both shapes.  Those
arguments involve only \(F\) and \(q\), after the response classification,
so they contain no residual one-site-star assumption.

The standalone
[independent checker](../computations/audit_arbitrary_star_monomial_base_locus_obstruction_independent.py)
does not import the primary program.  It reconstructs the response tensors,
checks all \(15^3=3375\) colour-indexed pair triples, verifies both positive
response tables, and regenerates the three bad-type unsaturated unit ideals
with different representatives and different variable and generator orders.

## 2. Literal reconstruction of all nine products

Let \(U\) have six sites and work in

\[
 \mathcal R_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u),
 \qquad V_uV_u=0.
\]

For \(P_k=\{a,b\}\), let \(F_k\) be pure colour \(k\) on
\(U\setminus P_k\), and write

\[
 p_i=\sum_u p_{i,u},\qquad s_j=\sum_u s_{j,u}.
\]

Every component of \(p_i\) or \(s_j\) on a site already occupied by
\(F_k\) dies.  Two components on the same missing site also multiply to
zero.  Thus the complete coefficient left on the two missing endpoints is

\[
 B_{ij}^{(k)}=
 p_{i,a}\otimes s_{j,b}+s_{j,a}\otimes p_{i,b}.          \tag{A1}
\]

Both endpoint orders in (A1) are essential and are present in every
checker generator.

Responses belonging to different lift colours cannot cancel.  For
\(k\ne\ell\), the union \(P_k\cup P_\ell\) uses at most four sites, so at
some other site the first response space has fixed factor \(e_k\) and the
second has the independent fixed factor \(e_\ell\).  This remains true when
the two missing pairs coincide.  Splitting

\[
 p_i s_j\sum_k\lambda_kF_k=\delta_{ij}\lambda_iX_i
\]

into those linearly disjoint response spaces and using
\(\lambda_k\ne0\) gives exactly

\[
 B_{ij}^{(k)}=
 \delta_{ij}\delta_{ik}
 e_i^{(a)}\otimes e_i^{(b)}.                            \tag{A2}
\]

There is no genericity or termwise inference inside one tensor space here;
the separation occurs between visibly independent fixed-colour subspaces.

If a local space has directions beyond the three displayed axes, choose a
linear projection onto their span which fixes those axes.  Extending it by
the identity on scalars gives a homomorphism
\(\mathbb C\oplus V_u\to
\mathbb C\oplus\langle e_0,e_1,e_2\rangle\), because both positive-degree
parts square to zero.  Tensoring these homomorphisms over the sites sends
any putative large-dimensional solution of (A2) to a three-dimensional
one while fixing its right side.  Consequently the three-coordinate ideal
calculation loses no possible solution.

## 3. Repeated pairs are already contradictory

Suppose \(P_i=P_k=\{a,b\}\) with \(i\ne k\).  Apply (A2) to the diagonal
row \((i,i)\).  For lift index \(i\), it requires

\[
 p_{i,a}\otimes s_{i,b}+s_{i,a}\otimes p_{i,b}
 =e_i^{(a)}\otimes e_i^{(b)}.
\]

For lift index \(k\), the identical left side is required to be zero.
This is impossible.  The checker verifies this literal pair of equations
for each of the 645 repeated triples among the \(15^3=3375\) ordered
colour-indexed triples.  The remaining 2730 triples have three distinct
edges; dividing by their six assignments to target colours leaves
\(\binom{15}{3}=455\) labelled-vertex edge sets.

This also explains why repeated pairs cannot be advertised as an open case
once all nine products are retained.  They remain a countermodel only for
the common-power equations with the products discarded; see Section 7.

## 4. Complete distinct-edge census and exact ideals

Three distinct edges on six labelled vertices have the following five
unlabelled shapes and labelled-edge-set counts:

| graph | degree multiset | count |
|---|---:|---:|
| \(K_{1,3}\) | \((3,1,1,1)\) | 60 |
| \(K_3\) | \((2,2,2)\) | 20 |
| \(P_4\) | \((2,2,1,1)\) | 180 |
| \(P_3+K_2\) | \((2,1,1,1,1)\) | 180 |
| \(3K_2\) | \((1,1,1,1,1,1)\) | 15 |

The counts sum to 455.  The independent program obtains them directly
from all triples rather than taking the table as input.

After projection to three local coordinates, (A2) contributes, for every
\(i,j,k,\alpha,\beta\in\{0,1,2\}\), the scalar equation

\[
 p_{i,a,\alpha}s_{j,b,\beta}
 +s_{j,a,\alpha}p_{i,b,\beta}
 -\delta_{ij}\delta_{ik}\delta_{\alpha k}\delta_{\beta k}=0. \tag{A3}
\]

There are \(3^5=243\) equations.  Variables on sites outside the union of
the missing pairs do not occur in any response, so omitting those irrelevant
free variables does not set them to zero.  There are 18 variables per used
site: two row families, three rows, and three local coordinates.

The independent generator streams reverse the endpoint terms, change the
factor order within each commutative monomial, permute all five equation
indices, change the variable order, and use different labelled
representatives.  Singular over \(\mathbb Q\) returns \([1]\) without any
saturation for the three impossible types:

| graph | variables | generators | independent SHA-256 |
|---|---:|---:|---|
| \(K_{1,3}\) | 72 | 243 | `5db7d6a3e8a71ac92c07ecf8d1ad0d268c54806826c7ba20685aa9d7889bd783` |
| \(K_3\) | 54 | 243 | `3c6580eed805be19a40c83a302d60b382323ac07fdd6057bea21c22ae69aee32` |
| \(P_4\) | 72 | 243 | `e58f7e989eb125e5b5d9bf4217e77f8982dfa4d45eb6efad1eb056105627545c` |

Because these are full affine ideals, the result includes zero components,
dependent rows, rank drops, and every cancellation stratum.  A unit ideal
over \(\mathbb Q\) rules out complex solutions.  Relabelling vertices and
simultaneously relabelling edge indices, response rows, and coordinate
colours transports every member of a graph type to its representative.

## 5. The two response tables really exist

For a matching \(P_i=\{u_i,v_i\}\), choose

\[
 p_i=e_i^{(u_i)},\qquad s_i=e_i^{(v_i)}.
\]

For the other surviving shape, orient the path and write

\[
 P_0=\{a,b\},\qquad P_1=\{b,c\},\qquad P_2=\{d,e\}.
\]

Then take

\[
 (p_0,s_0)=(e_0^{(a)},e_0^{(b)}),\quad
 (p_1,s_1)=(e_1^{(b)},e_1^{(c)}),\quad
 (p_2,s_2)=(e_2^{(d)},e_2^{(e)}).
\]

The checker substitutes both witnesses into every one of the 243 scalar
instances of (A2), not only the three diagonal equations.  In particular,
the shared path vertex causes no hidden off-diagonal response: one path edge
points into it and the other points out of it.  Thus \(3K_2\) and
\(P_3+K_2\) are genuinely realizable at product-table level.

## 6. Why arbitrary rows do not affect the common-power obstruction

Assume one of the two surviving pair shapes and additionally

\[
 F=q^{[2]},\qquad q^{[3]}=0,
\]

where bracket powers are unordered matching sums.  The integral identity

\[
 q q^{[2]}=3q^{[3]}
\]

gives \(qF=0\).  Only \(q_{P_i}\) can fill the two holes of \(F_i\).
The three full-support spaces are linearly disjoint by the same outside-site
colour argument used above, so

\[
 q_{P_0}=q_{P_1}=q_{P_2}=0.                            \tag{A4}
\]

No \(p_i\) or \(s_j\) occurs from this point onward.

For three disjoint pairs \(A,B,C\), (A4) leaves only the \(AB,AC,BC\)
blocks.  The \(A\cup B\) and \(A\cup C\) coefficients require

\[
 q_{AB}^{[2]}=\lambda_2F_2,\qquad
 q_{AC}^{[2]}=\lambda_1F_1,
\]

while the two-\(A\), one-\(B\), one-\(C\) coefficients require
\(q_{AB}q_{AC}=0\).  Select one nonzero matching term from each displayed
power.  The four crossed zero equations propagate nonvanishing to all eight
participating edge blocks.  Flattening a crossed equality

\[
 X_{0j}Y_{1k}=-X_{1j}Y_{0k}
\]

across its two bipartitions forces all four tensors to have rank one and
identifies their local factor lines.  Varying \(j,k\) makes the same line at
each \(A\)-site occur in both block families.  The first pure power forces
that line to be colour 2 and the second forces it to be the independent
colour 1 line, a contradiction.  This uses arbitrary edge tensors in
arbitrary local spaces, not coordinate star rows.

For \(P_0=ab\), \(P_1=bc\), \(P_2=de\), let \(f\) be the unused site.
Equation (A4) says \(q_{ab}=q_{bc}=q_{de}=0\).  The target coefficient on
\(abcf\) gives

\[
 q_{ac}q_{bf}=\lambda_2F_2\ne0.
\]

The zero coefficients on
\(abcd,abce,abdf,abef,bcdf,bcef\), read in that order, then give

\[
 q_{bd}=q_{be}=q_{ad}=q_{ae}=q_{cd}=q_{ce}=0.
\]

Each inference only uses injectivity of tensoring by one of the already
nonzero disjoint-support tensors, so no cancellation or illegal division is
hidden.  The required coefficient on \(cdef\) is consequently

\[
 q_{cd}q_{ef}+q_{ce}q_{df}+q_{cf}q_{de}=0,
\]

contradicting \(\lambda_0F_0\ne0\).  This completes the common-power audit
for the second response type.

## 7. Weights, repeated-pair countermodel, and scope

Nonzero weights are essential to the stated active three-target model.
They are used only to divide the separated response equations and to know
that the three pure target coefficients are nonzero.  If some
\(\lambda_i=0\), both the corresponding lift in \(F\) and its target
response disappear; the theorem deliberately makes no claim about that
degeneration.

If the nine products are dropped, repeated pairs do give a common-power
countermodel.  Put all three missing pairs equal to \(P\).  On the four-site
complement, colour the three perfect matchings of \(K_4\) by 0, 1, and 2,
and let \(q\) be the sum of their six correspondingly coloured edge
tensors.  Edges of different colours always meet, while the two edges of
each matching are disjoint.  Hence

\[
 q^{[2]}=F_0+F_1+F_2,qquad q^{[3]}=0.
\]

It cannot satisfy the products: Section 3 already gives a direct
zero-versus-nonzero contradiction.  Thus the response table, not merely the
power equations, is indispensable.

The final theorem allows arbitrary support and arbitrary local dimensions
for all six star rows, arbitrary nonzero complex weights, all endpoint
orders, all cancellations, and initially arbitrary missing pairs.  Its
remaining restrictive hypothesis is that the common degree-four multiplier
has exactly one pure four-site monomial lift per target colour.  It does not
cover multi-monomial target lifts and therefore does not close the full
cyclic or diagonal direct-block orbit, the global U1 route, or Krenn's
conjecture.

## 8. Reproduction

From the repository root:

```text
python3 computations/audit_arbitrary_star_monomial_base_locus_obstruction_independent.py --workers 3
```

The audited run returned:

```text
colour-indexed pair triples checked: 3375
repeated-pair contradictions: 645
ordered distinct triples: 2730
unlabelled-edge-set census: {'K1_3': 60, 'K3': 20, 'P3_plus_K2': 180, 'P4': 180, 'three_K2': 15}
literal witnesses: three_K2, P3_plus_K2
K1_3 unsaturated QQ ideal [1]
K3 unsaturated QQ ideal [1]
P4 unsaturated QQ ideal [1]
independent arbitrary-star monomial obstruction audit: PASS
```
