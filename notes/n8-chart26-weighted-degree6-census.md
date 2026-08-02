# The weighted chart-26 degree-six frontier

## Exact count without expansion

Under the integral weight of `n8-chart26-feasible-squarefree-weight.md`, the
certified lower basis has 6,558 squarefree degree-four leads and 84,005
squarefree degree-five leads.  Shared-core incidence counts every
non-product LCM-degree-six pair without constructing its S-polynomial:

\[
\begin{array}{c|r|c}
\text{pair type}&\text{LCM-degree-six pairs}&\text{required intersection}\\\hline
4\text{--}4&967{,}750&2\\
4\text{--}5&792{,}653&3\\
5\text{--}5&1{,}165{,}402&4
\end{array}
\]

The total frontier has 2,925,805 pairs.  Coarse invariants consisting of
source-word distances and the site-multigraph signatures of the shared core
and union collapse it to only 7, 15, and 21 structural classes.  The
four-element chart stabilizer gives respectively 933,326, 790,051, and
1,160,461 canonical source-monomial types; most selected pairs occur only
once because the certified weight is not stabilizer-invariant.

Every lower lead has a uniform uncoloured skeleton: all degree-four leads
are `P2+P2+P2+P2`, and all degree-five leads are `P4+P2+P2`.  The LCMs at
the degree-six frontier have only the following two shapes:

\[
\begin{array}{c|r|r}
\text{pair type}&C_4+P_2+P_2&\text{parallel underlying edge}\\
\hline
4\text{--}4&138{,}650&829{,}100\;(2,2,1,1)\\
4\text{--}5&671{,}758&120{,}895\;(2,1,1,1,1)\\
5\text{--}5&76{,}198&1{,}089{,}204\;(2,1,1,1,1)
\end{array}
\]

Thus `P6+P2` and `P4+P4` do not describe the critical LCM.  They appear
after that LCM cancels: they are the simple component-joining terms which a
forest straightening law should retain.

## Structural families

Two source-incidence subfamilies are immediate candidates for the universal
determinantal identities already proved in
`hafnian-star-minor-buchberger-identity.md`:

* 81,456 degree4--degree5 pairs use one of the two source generators of the
  transport cell.  These are the natural Koszul/Laplace incidence pairs.
* 329,268 degree5--degree5 pairs share one source generator.  They contain
  the Plücker and three-colour Koszul configurations, together with
  cross-vertex compatibility cases.

The count alone does not assert that every pair in either family reduces by
one universal formula.  It isolates the exact finite blocks to which those
formulas must be applied.

## Exact representative reductions

One representative of each of the 43 coarse classes was expanded and
reduced exactly against the complete degree-four/degree-five basis in the
certified weighted order.

\[
\begin{array}{c|r|r|r|r}
\text{type}&\text{classes}&\text{zero}&\text{squarefree nonzero lead}
 &\text{nonsquarefree nonzero lead}\\\hline
4\text{--}4&7&3&4&0\\
4\text{--}5&15&0&12&3\\
5\text{--}5&21&9&11&1
\end{array}
\]

The zero representatives include the expected matching-exchange, Plücker,
and Koszul patterns.  The four nonsquarefree representatives are exactly:

\[
\begin{array}{c|r|l|l|l|c|r|r}
\text{type}&\text{class size}&\text{first source}&\text{second source}
 &\text{remainder lead}&\text{repeat}&P_6+P_2&P_4+P_4\\\hline
4\text{--}5&42{,}754&1&(1,10)&0951acc6f4f4&f4&156&82\\
4\text{--}5&38{,}702&1&(1,37)&0952acc6f4f4&f4&164&100\\
4\text{--}5&8{,}412&1&(730,2188)&0309094bc6f4&09&0&0\\
5\text{--}5&45{,}776&(730,1459)&(730,3646)&0409094ec6f4&09&0&0
\end{array}
\]

Here a singleton source is an original degree-four word code and a pair is
the two original codes defining a degree-five transport cell.  In every
case the displayed repeated coordinate has multiplicity two and its
uncoloured skeleton is a `P4+P2+P2` with one parallel edge.

For every simple even path forest there is a unique alternating perfect
matching, obtained by taking alternate edges in each path component.  This
base-matching invariant sharply separates the four representatives.  The
first two contain respectively 238 and 264 simple path terms, spread over
72 and 82 distinct alternating base matchings.  No one of those terms has
the perfect matching of any input source.  They are therefore genuine
base-matching-exchange curvature, not fixed-matching Boolean-cube Bianchi
cells.  The latter two representatives contain no `P6+P2` or `P4+P4` term
at all; their degree-six support is parallel-edge or branched and calls for
a branch-elimination identity before path straightening applies.

The weight has therefore done something useful but incomplete: it repairs
the first known degree-six cell and exposes four coherent
Bianchi-curvature families.  The next theorem should straighten those
families, rather than ask one weight vector to hide them.

## Proposed proof compression

The completed layers suggest viewing the calculation as a small
combinatorial complex.  Perfect matchings are base objects, degree-five
`P4+P2+P2` cells are elementary transports obtained by joining two matching
edges, and degree-six cells measure the failure of two transports to
commute.  Ordinary Laplace/Koszul and Plücker relations give the flat
cells.  The four records above isolate the remaining curvature:

1. Refine and prove a branch-elimination relation for the two coarse classes
   whose selected representatives have no simple path term.
2. Prove a matching-flip Bianchi relation that transports across the
   alternating base matchings in the other two families.
3. Use the source-word and stabilizer actions to propagate those identities
   over each refined orbit, then invoke Buchberger's criterion.

This would replace expansion of 2,925,805 S-polynomials by a finite set of
source-labelled identities.  The census does not yet prove that the four
coarse classes are uniform, so their source labels must be retained when
the identities are formulated.

The first item is now exact for every labelled pair in the two signatures;
see [the full branch-class refinement](n8-chart26-branch-class-uniformity.md).
The coarse classes are not uniform normal-form classes.  Their exact splits
are

\[
 (8{,}412)=(2{,}986\text{ squarefree})+(5{,}426\text{ collision}),
\]

\[
 (45{,}776)=(29{,}212\text{ squarefree})+(16{,}564\text{ collision}).
\]

Every collision form has one decorated coordinate \(x\) of multiplicity two.
On \(x=0\), its restricted source expression is exactly lower-contractible;
on \(x\ne0\), division by \(x^2\) leaves a squarefree Laurent pivot of
skeleton `P3+P2+P2+P1`.  All 21,990 finite \(xG\) colon tests remain lower
normal.  The representative formulas at \(x_{02}^{00}\) were therefore the
first members of a uniform source-square routing rule, not evidence that all
54,188 cells require the same fixed-coordinate split.

The 32,198 squarefree cells do not immediately enter the simple path-forest
complex.  Their leads are branched in 25,908 cases, while 6,290 type-5--5
cells are decorated-squarefree but retain a physical parallel edge.  The
full audit therefore closes the collision route and isolates a distinct
branched/parallel squarefree frontier; it does not finish straightening these
two signatures.

The 43 reductions in this census remain representative data for the other
coarse signatures.  Only the two classes just cited have received a complete
labelled-pair audit.  The next safe step for the path-bearing classes is still
to derive source-labelled formulas and refine them before any large
completion.

## Verification

Run

```text
python3 computations/verify_n8_chart26_weighted_degree6_census.py
```

The checker reconstructs every lower lead, performs the exact incidence
count and stabilizer census, and replays all 43 representative reductions.
