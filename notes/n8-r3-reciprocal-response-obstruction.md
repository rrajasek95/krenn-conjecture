# The sharp (r=3) reciprocal response packet is empty

## Outcome

The sole sharp three-reciprocal incidence frontier from
[`n8-r3-reciprocal-sharp-normal-form.md`](n8-r3-reciprocal-sharp-normal-form.md)
cannot satisfy the exact ternary matching equations.  The contradiction is
termwise over arbitrary complex aggregate blocks; no support positivity,
generic coefficient, finite-field, or Gröbner assumption is used.

Let (p,s) be the two forced nonadjacent coordinate-cubic sites and let

\[
 p_i=\alpha_i e_i^{(u_i)},\qquad
 s_i=\beta_i e_i^{(v_i)},\qquad \alpha_i\beta_i\ne0,     \tag{1}
\]

be their literal port stars on the six outer sites (W).  Their direct
block is zero.  If (q) is the internal quadratic on (W), the complete
nine-row system is therefore

\[
                 p_i s_j q^{[2]}=\delta_{ij}X_i.          \tag{2}
\]

All neighbor-triple overlap sizes (m=0,1,2,3) now close:

1. sharp essential-incidence equality makes every cubic arm essential at
   its cubic endpoint and nonessential at its outer endpoint;
2. all nonessential endpoint supports at an outer site lie on one common
   line (L_w), while a cubic arm is a same-colour coordinate cell;
3. hence a shared neighbor (u_i=v_j) forces (i=j); but then the diagonal
   product (p_i s_i) is zero in the site-square-zero algebra, contradicting
   (2); and
4. with disjoint triples, (L_{u_i}=L_{v_i}=\mathbb Ce_i).  In the pure
   colour-(i) response, the four remaining sites have common lines
   (e_j,e_j,e_k,e_k).  Every (q)-edge contributing (e_i) at both ends
   would have to be essential at both endpoints, impossible in the sharp
   equality case.  Thus all three pure-cofactor matching monomials vanish.

This closes the entire `r=3` sharp normal form.  Combined with the earlier
incidence reduction, three reciprocal witness pairs no longer leave a
coefficient frontier at (N=8).  The result is specific to the equality
packet with two isolated cubic sites; it does not by itself close the curved
rank-one overlap branch occurring for at most two reciprocal pairs.

## Exact response reduction

The cubic-vertex theorem gives three different physical neighbors at each
cubic site and one arm of each target colour.  Since (A_{ps}=0), sorting
eight-site perfect matchings by the two arms used at (p,s) gives exactly

\[
 [H_8(A)]_{ij}=p_i s_jq^{[2]}.                            \tag{3}
\]

There is no direct (q^{[3]}) term.  Equation (2) means, whenever
(u_i\ne v_j),

\[
 H_{W\setminus\{u_i,v_j\}}(q)=
 \begin{cases}
  (\alpha_i\beta_i)^{-1}e_i^{\otimes4},&i=j,\\
  0,&i\ne j.
 \end{cases}                                             \tag{4}
\]

If (u_i=v_j), the left side of (2) is already zero because both degree-one
forms occupy the same physical site.  In particular the pure rows require

\[
                              u_i\ne v_i.                 \tag{5}
\]

The proof below shows that (5) and sharp endpoint equality are incompatible
with every overlap pattern, before the mixed equations in (4) are needed.

## All overlap strata

Normalize the first neighbor triple to

\[
                         (u_0,u_1,u_2)=(0,1,2).           \tag{6}

The second triple is an arbitrary injection of its three labelled colours
into the six outer sites.  The exact labelled census is

\[
\begin{array}{c|r|r|r|r}
m&\text{assignments}&\text{common-line conflict}&
  \text{diagonal collision}&\text{survive}\\ \hline
0&6&0&0&6\\
1&54&36&18&0\\
2&54&45&9&0\\
3&6&5&1&0
\end{array}                                               \tag{7}
\]

Here is why the two failure columns are exact.  The sharp packet has
eighteen bad selected edges and eighteen essential endpoint charges.  No bad
edge is essential at both ends.  Every cubic arm is bad and essential at the
cubic endpoint, so it is nonessential at the outer endpoint.  The endpoint
flag theorem puts all such nonessential supports at (w) on one line
(L_w).  From (1),

\[
                         L_{u_i}=\mathbb Ce_i,qquad
                         L_{v_j}=\mathbb Ce_j.             \tag{8}

If (u_i=v_j) with (i\ne j), (8) gives two different common lines at one
site, impossible.  If (i=j), (5) fails.  Therefore no overlap survives;
the only remaining case is (m=0).

## The disjoint case has no pure coefficient

When (m=0), the two neighbor triples partition (W).  Fix a target colour
(i), and write ({i,j,k}={0,1,2}).  Deleting the two port sites
(u_i,v_i) leaves

\[
             u_j,v_j,u_k,v_k,qquad
             (L_{u_j},L_{v_j},L_{u_k},L_{v_k})
              =(e_j,e_j,e_k,e_k).                        \tag{9}

Consider any one of the three perfect matchings of these four sites.  For
one of its (q)-blocks to carry the pure colour (i) at an endpoint (w),
the endpoint support cannot lie in (L_w), because (L_w) is (e_j) or
(e_k).  That block must therefore be essential at (w).  To contribute
the pure (e_i\otimes e_i) cell, it must be essential at both endpoints.
But sharp equality permits no outer edge essential at both ends.  Hence each
of the two blocks in every matching has zero relevant cell, and

\[
             [e_i^{\otimes4}]
             H_{W\setminus\{u_i,v_i\}}(q)=0.             \tag{10}

Equation (10) contradicts the nonzero diagonal row in (4).  Notice that the
three matching terms vanish separately; arbitrary complex cancellation and
parallel source summands cannot change the conclusion.

The checker audits all six labelled orders of the disjoint second triple,
all three target colours, and all three four-site matchings: exactly (54)
pure matching terms are forced to zero.

## Relation to existing obstructions

The coordinate-plane mixed-packet theorem is not needed.  Its hypotheses
put every internal endpoint space in a prescribed two-plane.  Here the sharp
essential equality supplies a stronger statement tailored to the cubic
ports: a pure response edge would have to be double-essential, and such an
edge does not exist.  This avoids weakening the packet or silently importing
a plane hypothesis not proved by the reciprocal incidence theorem.

The argument also differs from adjacent-cubic descent.  The cubic sites here
are nonadjacent, so no direct coordinate edge can be removed.  Instead their
two literal star packets expose the impossible four-site pure cofactor.

## Reproduction

```text
python3 computations/verify_n8_r3_reciprocal_response_obstruction.py
python3 -O computations/verify_n8_r3_reciprocal_response_obstruction.py
```

The checker pins the exact sharp-normal-form artifacts, exhausts all (120)
labelled second-neighbor injections by overlap size, and audits the (54)
vanishing pure matching terms in the disjoint stratum.
