# Independent audit of the good-pair fan and six-port triple-cofactor reduction

## Verdict

**PASS, with the scope restrictions in Sections 8--9 below indispensable.**
I reconstructed the argument in
[good-pair-fan-six-port-triple-cofactor-reduction.md](good-pair-fan-six-port-triple-cofactor-reduction.md)
without using its checker as evidence.  The following claims are valid:

1. an exact ternary aggregate source has at least
   \(N(N-7)/2\) unordered pairs whose two deleted-endpoint star maps are
   injective, and some vertex lies in a fan of at least \(N-7\) such pairs;
2. at \(N\geq16\), that fan has either at least \(N-15\) nonregular charts,
   or three neighbours joined to its centre by literal zero **aggregate**
   ternary blocks, with the asserted two-site row supports;
3. at \(N\geq24\), the corresponding alternatives are \(N-23\) nonregular
   charts or three zero-block neighbours which are pairwise good;
4. two zero-block neighbours give exactly the 27 endpoint-ordered equations

   \[
     p_c\bigl(b_{de}q^{[m-2]}+s_dt_eq^{[m-3]}\bigr)
        =\delta_{c=d=e}X_c^W;
   \]

5. the two-hole anchor lemma and the projection onto at most six physical
   hole ports are exact and cancellation-safe; and
6. the displayed three-port response table satisfies all 27 projected
   equations but does not supply the common physical cofactors needed to
   realize them.

No genericity, positivity, same-colour endpoint condition, or termwise
vanishing is used.  The argument is a conditional reduction, not a proof of
Krenn's conjecture: it leaves the extra-Hessian-kernel, disconnected, and
connected-bipartite fan charts, and it leaves simultaneous physical
common-cofactor compatibility open in the regular branch.

The independent executable audit is
[audit_good_pair_fan_six_port_triple_cofactor_reduction_independent.py](../computations/audit_good_pair_fan_six_port_triple_cofactor_reduction_independent.py).
It imports neither primary artifact.

## Frozen primary inputs

The primary files audited here had SHA-256 digests

    3f16b2ab5d1f053f38f76c2dd7bc4e03efebff785baae78cb97420486d065a65  notes/good-pair-fan-six-port-triple-cofactor-reduction.md
    56c65b063ee972394c6e8b7824e10a5624cbfab260b7e2a14862a9095405af99  computations/verify_good_pair_fan_six_port_triple_cofactor_reduction.py

The independent checker has SHA-256 digest

    dc2c909163576510f286161a9ff1bb8727d3713fdf1fa845a75724805c48633c

## 1. The pair count and fan

Fix a vertex \(u\).  For each neighbour \(x\), let

\[
 L_{u\leftarrow x}=\operatorname{im}_u A_{ux}\subseteq V_u,
 \qquad T_u=\sum_{x\ne u}L_{u\leftarrow x}.
\]

The mode-\(u\) image of every matching term lies in \(T_u\).  The
mode-\(u\) flattening of the exact target is

\[
 \sum_{c=0}^2 e_c^{(u)}\otimes X_c^{B\setminus\{u\}},
\]

whose left image is all of \(V_u\).  Thus \(T_u=V_u\).  This is a statement
about the complete aggregate tensor; it does not select any matching term.

For a family of subspaces spanning a \(d\)-space, at most \(d\) members can
be deletion-essential.  Indeed, for every essential member \(L_i\), choose
a covector \(\phi_i\) annihilating all the other members but not \(L_i\),
and choose \(x_i\in L_i\) with \(\phi_i(x_i)\ne0\).  The matrix
\((\phi_i(x_j))\) is diagonal with nonzero diagonal, so the \(x_i\)'s are
independent.  Here \(d=3\), hence at most three deleted neighbours make the
star at \(u\) noninjective.

There are at most \(3N\) deficient directed pairs.  Every bad unordered pair
has at least one deficient orientation, and distinct bad pairs give distinct
directed pairs.  Therefore

\[
 |E(G_{\rm good})|\geq {N\choose2}-3N={N(N-7)\over2}.
\]

Its average degree is at least \(N-7\), proving the fan bound.  The phrase
"factor of two" in the primary outcome refers to reducing the previous
directed-deficiency budget from \(6N\) to \(3N\); the two displayed good-edge
lower bounds are not in a constant ratio.

## 2. The hereditary good clique

The bad-pair graph is \(4\)-degenerate.  The equality case of the
essential-subspace lemma is important here.  If \(u\) has three essential
neighbours, their mode-\(u\) supports are three independent lines and every
other block incident with \(u\) is the zero tensor.  Deleting one of those
zero blocks is harmless at both endpoints, so the total bad degree of \(u\)
is at most three.

Suppose an induced bad graph had minimum degree five.  It could contain no
vertex of the preceding equality type.  Orient each bad edge toward an
endpoint at which deletion is deficient.  Every remaining vertex has at
most two essential neighbours, so the orientation has indegree at most two
and hence at most \(2|D|\) edges.  Minimum degree five requires at least
\(5|D|/2\) edges, a contradiction.  Thus the bad graph is \(5\)-colourable,
and every set \(D\) contains a good clique of size at least
\(\lceil|D|/5\rceil\).

This argument also checks a subtle point: if the mode-\(u\) support of
\(A_{uv}\) is zero, then \(A_{uv}\) itself is zero, so its mode-\(v\)
support is zero as well.  A zero block cannot make the opposite orientation
deficient.

## 3. What the Hessian theorem really implies

Delete a good pair \(r,u\), let \(q\) be the internal quadratic, and let
\(p_c,s_d\) be the two endpoint rows.  Write \(|B\setminus\{r,u\}|=2t\).
The off-diagonal pair equations, in divided-power normalization, are

\[
       a_{cd}q^{[t]}+p_cs_dq^{[t-1]}=0\qquad(c\ne d).       \tag{A1}
\]

If the source Hessian \(Z\mapsto Zq^{[t-1]}\) has only its vertex-gauge
kernel, (A1) says

\[
 p_cs_d+{a_{cd}\over t}q=Z^\alpha,
 \qquad (Z^\alpha)_{ij}=(\alpha_i+\alpha_j)q_{ij},
 \qquad \sum_i\alpha_i=0.                                \tag{A2}
\]

On a rank-three internal block, the block of \(p_cs_d\) has matrix rank at
most two.  Hence the scalar multiplying \(q_{ij}\) in (A2) must vanish.
Along every rank-three edge,

\[
 \alpha_i+\alpha_j={a_{cd}\over t}.
\]

If that graph is connected and nonbipartite, subtracting
\(a_{cd}/(2t)\) makes the \(\alpha\)'s alternate across every edge; an odd
cycle makes them all zero.  The zero-sum condition then gives \(a_{cd}=0\)
and \(\alpha=0\).  Equation (A2), now on every physical pair and not merely
the rank-three edges, gives

\[
                              p_cs_d=0.                  \tag{A3}
\]

Multiplication \(s\mapsto ps\) in the site-square-zero algebra is injective
exactly when \(p\) meets at least three physical sites.  Three nonzero
components force every component of an annihilator to vanish; for one or
two support sites the familiar same-site or antipodal vector is a nonzero
annihilator.  If one \(p_c\) met three sites, (A3) would force both rows
\(s_d\), \(d\ne c\), to vanish.  The two corresponding diagonal equations
would make \(q^{[t]}\) proportional to two distinct pure target tensors,
which is impossible.  Therefore each \(p_c\) meets at most two sites, and
the symmetric argument gives the same result for every \(s_d\).

This reconstructs the cited source-Hessian theorem and shows exactly where
all of its hypotheses enter.  In particular, no "generic Hessian" is
assumed: charts with an extra kernel are placed explicitly in the escape
alternative.  Connected bipartite rank-three graphs are likewise retained
as escape charts in the fan dichotomy.

## 4. From a regular fan to literal zero blocks

For a fixed fan centre \(r\), let \(S_c(r)\) be the global physical-site
support of its colour-\(c\) row.  A regular nonbipartite fan pair \(\{r,u\}\)
gives

\[
                         |S_c(r)\setminus\{u\}|\leq2.    \tag{A4}
\]

If four different deletions satisfy (A4), then \(|S_c(r)|\leq2\).  A
support of size at least four fails after every deletion; a support of size
three could work only if all four deleted vertices belonged to that
three-set.  Hence the union

\[
                         C=\bigcup_{c=0}^2S_c(r)
\]

has at most six sites.  Every regular neighbour outside \(C\) has all three
rows zero, so its complete endpoint-ordered aggregate block with \(r\) is
literally zero.  Applying the same Hessian theorem at that neighbour, and
using the zero block toward \(r\), shows that each of its three global rows
is individually supported on at most two sites.  Their union may have six
sites; the theorem does not put all three rows on one common two-set.

The fan has at least \(N-7\) members.  If at most eight are regular, at
least \(N-15\) are escape charts.  Otherwise at least nine are regular and,
after removing \(C\), at least three zero-block neighbours remain.  This is
the first dichotomy, valid in its nonvacuous stated range \(N\geq16\).

For \(N\geq24\), if at most sixteen fan pairs are regular, at least
\(N-23\) are escape charts.  Otherwise at least seventeen are regular and
at least eleven lie outside \(C\).  Section 2 supplies a three-vertex good
clique among them.  Call it \(u,v,w\).  In a triple \((r,u,v)\), goodness of
\(\{r,u\}\), together with \(A_{rv}=0\), makes the remaining \(r\)-star
injective.  Goodness of \(\{u,v\}\), together with \(A_{ur}=0\), makes the
remaining \(u\)-star injective, and similarly for \(v\).  Thus all three
sparse row frames in the hereditary triple slice are genuinely aggregate
injective.

## 5. The two-hole coordinate anchor

Let \(F\) have degree \(|U|-1\) and decompose it into sectors
\(F_{\widehat x}\), indexed by the unique missing physical site.  If a
linear form \(p\), supported at \(a,b\), satisfies \(pF=X_c^U\), then only

\[
               p_aF_{\widehat a}+p_bF_{\widehat b}=X_c^U \tag{A5}
\]

can survive.  Quotient the \(a\)-factor by \(\mathbb Cp_a\) and the
\(b\)-factor by \(\mathbb Cp_b\).  The left side vanishes, while the right
side becomes

\[
 (e_c^{(a)}\bmod p_a)\otimes(e_c^{(b)}\bmod p_b)
     \otimes X_c^{U\setminus\{a,b\}}.
\]

It can vanish only if \(p_a\parallel e_c^{(a)}\) or
\(p_b\parallel e_c^{(b)}\).  Quotienting only the anchored factor proves
the stated divisibility of the opposite hole sector when exactly one
alternative occurs.  The one-support case is equality of nonzero simple
tensors and gives both the coordinate line and the normalized residual
pure tensor.

Applied to every sparse first-contraction equation, this supplies a target
coordinate anchor in each row.  At the fan centre its anchors remain in
\(W\), because both extracted blocks are zero.  At \(u\), the only possible
anchor outside \(W\) is on the direct \(uv\) block.  If row \(d\) anchors
there, then \(b_{de}=0\) for \(e\ne d\) and \(b_{dd}\ne0\).  The reverse
endpoint gives the corresponding column statement.  No assertion that all
anchors survive in \(W\) is needed or made.

## 6. The exact 27-row triple contraction

Take two zero-block neighbours \(u,v\) and put
\(W=B\setminus\{r,u,v\}\), where \(N=2m\).  With named endpoint order,

\[
 h=q+\sum_c e_c^{(r)}p_c+\sum_d e_d^{(u)}s_d
       +\sum_e e_e^{(v)}t_e
       +\sum_{d,e}b_{de}e_d^{(u)}e_e^{(v)}.              \tag{A6}
\]

There is no \(ru\) or \(rv\) term because those complete aggregate blocks
are zero.  A perfect matching meeting all three named vertices has exactly
two possible forms:

* it uses \(uv\), sends \(r\) into \(W\), and internally matches the
  remaining \(|W|-1\) sites; or
* it sends \(r,u,v\) to three distinct sites of \(W\), then internally
  matches the rest.

In \(h^{[m]}=h^m/m!\), every physical perfect matching occurs once.  The
two classes therefore contribute, with no missing factorial,

\[
       b_{de}p_cq^{[m-2]},\qquad p_cs_dt_eq^{[m-3]}.
\]

Contracting the exact target at the three named slots gives zero unless
\(c=d=e\), and gives \(X_c^W\) otherwise.  This proves all 27 equations.
The derivation uses equality of complete matching sums, so arbitrary complex
cancellation remains inside each displayed aggregate.  If a stored block
uses the reverse numerical order, transposing it into named \(u\mid v\)
order makes \(b_{de}\) carry \(d\) at \(u\) and \(e\) at \(v\), exactly as
claimed.

## 7. Why only six hole ports remain

Each response

\[
 R_{de}=b_{de}q^{[m-2]}+s_dt_eq^{[m-3]}
\]

has degree \(|W|-1\), so it decomposes uniquely as
\(\sum_xR_{de,\widehat x}\).  The three centre rows are supported on
\(C\), \(|C|\leq6\).  In the product \(p_cR_{de,\widehat x}\), a component
of \(p_c\) at site \(y\) vanishes unless \(y=x\), because every other site
is already occupied.  Thus every sector with its hole outside \(C\) is in
the common kernel of all three \(p_c\)'s.  Discarding precisely those
sectors loses no equation.

The retained sectors occupy every site of \(D=W\setminus C\), so any
functional on \(\bigotimes_{y\in D}V_y\) can cap them.  Choose at every
site a covector taking value one on each of the three target axes, and take
their product \(K\).  Then

\[
 p_c\overline R_{de}
    =\delta_{c=d=e}K(X_c^D)X_c^C
    =\delta_{c=d=e}X_c^C.                               \tag{A7}
\]

This projection is cancellation-safe and uses actual physical hole
sectors.  It does not claim that the capped tensor factors again as a power
of a quadratic on \(C\); it remains the literal cap of the two common-edge
terms in the displayed physical response.

## 8. The abstract response is a countermodel only to an abstract finish

On three sites labelled \(0,1,2\), take

\[
 p_c=e_c^{(c)},\qquad
 \overline R_{de}=0\ (d\ne e),\qquad
 \overline R_{dd}=\bigotimes_{x\ne d}e_d^{(x)}.
\]

For \(c=d\), multiplication fills the unique hole and gives \(X_c\).  For
\(c\ne d\), \(p_c\) attempts to use a site already occupied by
\(\overline R_{dd}\), so the product is zero.  All 27 equations (A7) hold,
and the \(p_c\)'s are independent.

This model supplies no rows \(s,t\), direct block \(b\), internal quadratic
\(q\), or three simultaneous redecompositions for \(uv,uw,vw\).  It is
therefore not a source and not a Krenn counterexample.  It proves only that
aggregate rank plus the abstract response table cannot finish the route.
The primary note correctly leaves as its next gate the compatibility of
three capped response tables coming from the same physical blocks and the
same common matching cofactors.

## 9. Quantifier and palette audit

All statements above concern one exact ternary aggregate source.  For a
larger palette, projecting every physical colour space onto any fixed three
target colours gives such a source, so the reduction may be applied to that
chosen triple.  However:

* its good graph, Hessian, supports, zero blocks, and set \(C\) may depend on
  the chosen colour triple;
* a zero block means zero after aggregation and that ternary projection; it
  does not mean that every parallel decorated source on the physical pair
  vanishes individually, nor that cells using other palette colours vanish;
* no simultaneous choice across all palette triples has been proved.

These are scope boundaries, not gaps in the stated ternary theorem.
Aggregation itself is valid with arbitrarily many parallel sources because
a physical perfect matching uses at most one source with a given neighbour
pair; summing their endpoint-colour weights into one block preserves every
matching coefficient.  Zero weights, asymmetric endpoint colours, and
complex cancellation are therefore all retained.

Regular nonbipartite means exactly: the pair-deleted Hessian kernel is the
vertex-gauge space and the rank-three internal graph is connected and
nonbipartite.  The theorem does not assert that a regular pair exists.  Its
dichotomies count the complementary charts explicitly.  Nor does it turn
the capped responses into a physical source on six sites.  Those two facts
are the honest remaining conjecture-level work.

## 10. Independent executable checks

The standalone checker uses methods different from the primary one.  It:

* exhausts all 28 subspaces of \(\mathbb F_3^3\), four proposed essential
  members, and an arbitrary combined background subspace (871,555 spanning
  cases), finding no four deletion-essential members and confirming the
  sharp coordinate-line triple;
* exhausts actual support/fan subsets and all even threshold ledgers through
  order 120;
* checks the linear-annihilator support threshold and the odd-cycle
  alternation rank over \(\mathbb F_5\);
* exhausts 17,298 two-hole tangent-space membership tests over
  \(\mathbb F_5\);
* expands 39,366 signed-integer tensor coefficients at \(N=8\), using all
  six numerical orders of three nonconsecutive named endpoints, and checks
  the direct-edge/three-star partition with endpoint transposition and
  divided-power normalization;
* constructs arbitrary near-top tensors and verifies the physical-hole
  projection and capping identity for both product and entangled caps; and
* checks all 27 entries of the three-port abstract response table.

Both the primary checker and this independent checker return `PASS`.  The
finite calculations audit the exact ledgers and algebraic identities; the
uniform proofs above establish the characteristic-zero theorem.
