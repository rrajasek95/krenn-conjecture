# The formal occupancy split does not yet flatten the cap Bockstein

## 1. Outcome

Keep the off-diagonal notation of
[`five-exposed-site-yoneda-cup-obstruction.md`](five-exposed-site-yoneda-cup-obstruction.md):

\[
 a\ne b,\qquad \alpha=A_{pq}(a,b)\ne0,\qquad
 \kappa=AU-BF\ne0,
\]

and expose the five physical sites \(p,q,r,s,x\).  The proposed
restriction--insertion route first takes the \((x,c)\)-coefficient of the
four-cut comparison and then restores the sites \(r,s\).  Its hoped-for
output is

\[
             (\operatorname {tgt},\operatorname {ores}_c)
                   =(0,-\kappa\overline Y_c).             \tag{1}
\]

When nonvanishing is at issue, assume \(\overline Y_c\ne0\), as in the
cited five-site ledger.

This note separates two constructions which must not be identified.  On
one cap chart, the off-diagonal block of the **evaluated cap-multiplication
complex** is genuinely nonzero and is exactly the familiar odd-residue map

\[
                  \Theta\longmapsto[\Theta t_cq_0^{[h-2]}]. \tag{1a}
\]

It sends the scalar-zero cap to \(-\overline Y_c\).  By contrast, the
formal partial-matching state module has a tautological occupancy splitting.
Tensoring it with the elementary chart-symbol complex preserves that
splitting.  This proves a zero connecting map only for the resulting formal
state complex, whose differential is \(1\otimes d\) and does not contain cap
multiplication.

For every exposed set \(S\) and distinguished \(x\in S\), the formal
partial-matching module has a canonical decomposition into states in which
\(x\) is starred and states in which \(x\) is joined by a direct edge:

\[
 \mathsf P(S)=
 \mathsf P_{x\text{-star}}(S)\ \oplus\!
 \bigoplus_{y\in S\setminus\{x\}}
       \mathsf P_{xy\text{-direct}}(S).                  \tag{2}
\]

It gives a split short exact sequence of formal state modules.  There are
two useful sections.  The bare section declares \(x\) starred and is graded
by the number of exposed direct edges.  The full exposure section adds,
with coefficient one, every alternative in which \(x\) is joined directly
to an unmatched old site.  It is filtered and has only degree-zero and
degree-one pieces.  Both pieces commute with the formal two-chart
comparison differential.  Hence the formal connecting homomorphism is zero,
and each direct-edge piece preserves formal comparison boundaries.

For five sites the three direct-edge layers have sizes

\[
                         1,\ 10,\ 15.                    \tag{3}
\]

The two canonical cap charts both evaluate, state by state and with the
same factor \(h\), to the same formal \(1/10/15\) state family.  At
\(h=3\), the all-star state has negative divided-power exponent and both
evaluations send it to zero.  Splitting with respect to \(x\) refines the
formal counts (3) as

\[
 (1,10,15)=(1,6,3)+(0,4,12),                             \tag{4}
\]

where the first vector counts \(x\)-starred states and the second counts
states containing a direct edge \(xy\).  Thus the fully expanded all-label
five-site row is statewise equal in the two charts, in every occupancy and
direct-edge layer.

This does **not** prove that the occupancy sequence for an evaluated
pair-comparison/cap-multiplication total complex is chain-split.  Indeed,
on one chart the canonical unmatched-state section fails to commute with
cap multiplication by exactly the off-diagonal block (1a).  To obtain a
zero pair-comparison Bockstein one would have to define that total complex,
including cap multiplication and target augmentation, and exhibit a
section or homotopy cancelling the two chart defects.  Statewise equality
of the single universal row does not supply such a construction.

The augmented target--residue lock still rules out two elementary moves.
Keeping only the response \(-\kappa\overline Y_c\) drops the target
coordinate of the one-chart relation cycle, while cancelling its target by
an admitted same-complement, same-power companion gives \((0,0)\).  These
facts do not classify a cross-quotient restriction--insertion operation.

No trace division, nonzero star, or second direct block is used in the
formal splitting or target--residue ledger.  Those statements specialize
unchanged at \(\tau=0\) and on the direct-free boundary \(B=0\), where
\(\kappa=AU\ne0\).  But the desired target-zero class (1) remains open in
those specializations: no evaluated pair-comparison Bockstein or
source-Rees extension is constructed here.

## 2. The formal partial-matching state module

Let \(S\) be a finite set of exposed sites and fix a colour word
\(\gamma:S\to\{0,1,2\}\).  Write \(\operatorname {Match}(S)\) for the
partial matchings on \(S\), including the empty matching, and let

\[
 \mathsf P(S,\gamma)
   =\bigoplus_{M\in\operatorname {Match}(S)}\mathbb C[M]. \tag{5}
\]

This is the formal state module, before distinct source monomials are
allowed to cancel after evaluation.  It is graded by \(|M|\), the number
of direct exposed edges.  For evaluation, suppose \(S\) is exposed from a
divided matching power on \(2m\) physical sites.  If the common complement
is equipped with an internal quadratic \(z\), endpoint stars
\(\ell_{u,\gamma_u}\), and direct entries
\(a_{uv}^{\gamma_u\gamma_v}\), its state evaluation is

\[
 \operatorname {wt}_S(M)=
 \left(\prod_{uv\in M}a_{uv}^{\gamma_u\gamma_v}\right)
 \left(\prod_{u\in S\setminus V(M)}\ell_{u,\gamma_u}\right)
 z^{[m-|S|+|M|]}.                                       \tag{6}
\]

As usual, a negative divided power is zero.  Formula (6) is the uniform
exposed-set formula; summing it over \(M\) is the corresponding coefficient
of the matching tensor.  In the five-site cap row below the ambient power
has \(m=h+1\), so its exponent is \(h-4+|M|\).

Fix \(x\in S\).  Let \(\mathsf K_x(S,\gamma)\) be the span of matchings
which cover \(x\), and define

\[
 \begin{aligned}
 \pi_x[M]&=
   \begin{cases}
    [M],&x\notin V(M),\\
    0,&x\in V(M),
   \end{cases}\\
 j_x[N]&=[N],
 \end{aligned}                                           \tag{7}
\]

where on the right \(N\) is regarded as a matching on
\(S\setminus\{x\}\), with \(x\) declared unmatched in \(j_xN\).  Then

\[
 0\longrightarrow \mathsf K_x(S,\gamma)
 \longrightarrow \mathsf P(S,\gamma)
 \mathop{\longrightarrow}^{\pi_x}
 \mathsf P(S\setminus\{x\},\gamma|_{S\setminus\{x\}})
 \longrightarrow0                                       \tag{8}
\]

is exact and \(\pi_xj_x=1\).  Moreover

\[
 \mathsf K_x(S,\gamma)
 \cong\bigoplus_{y\in S\setminus\{x\}}
   \mathsf P(S\setminus\{x,y\},
             \gamma|_{S\setminus\{x,y\}})[1],          \tag{9}
\]

by deleting the unique direct edge \(xy\) incident to \(x\).  The shift
\([1]\) records that adjoining \(xy\) raises \(|M|\) by one.

The bare section \(j_x\) records only the \(x\)-star branch.  The formal
coefficient-exposure section is instead

\[
 s_x[N]=j_x[N]+\sum_{y\in S\setminus(\{x\}\cup V(N))}
                         [N\cup\{xy\}].                  \tag{9a}
\]

It also satisfies \(\pi_xs_x=1\).  To see why (9a) is the physical map,
regard \(x\) as part of the old complement.  Then

\[
 q_{\rm old}=z+e_c^{(x)}\ell_{x,c},\qquad
 \ell_{y,\gamma_y}^{\rm old}
   =\ell_{y,\gamma_y}
       +e_c^{(x)}a_{xy}^{c\gamma_y}.                    \tag{9b}
\]

Taking the \((x,c)\)-coefficient of the weight of \(N\) gives the first
term of (9a) by differentiating the divided matching power, and one term
for each unmatched \(y\) by differentiating its star.  The normalized
divided power makes every coefficient one.  This reconstructs every formal
state on \(S\) exactly once after summing over \(N\).  It implements
coefficient exposure on the universal state sum; it is not an inverse
defined on arbitrary evaluated polynomials, where distinct state weights
may coincide or cancel.

Equations (8)--(9) are the canonical site-occupancy sequence.  They are
not a dimension count: every state occurs in exactly one summand, and the
formal coordinate assembly is explicit.  Under (6) and (9a), the first summand supplies
the \(x\)-star and the other summands supply each possible direct edge
\(xy\).  Hence the formal exposure lift retains all direct/star
alternatives without postulating an inverse on the evaluated image.

## 3. The one-chart occupancy block is the odd residue

The split state module must not be confused with the off-diagonal block of
one cap multiplication map.  Let \(W=D\sqcup\{x\}\), where
\(|D|=2h-1\), and write

\[
 q=q_0+\sum_j e_j^{(x)}t_j,\qquad
 \Theta=\overline\Theta+\sum_j e_j^{(x)}L_j.             \tag{O1}
\]

Put \(A=q_0^{[h-1]}\) and \(B=q_0^{[h-2]}\).  In the decomposition by
whether \(x\) is occupied, the colour-\(c\) block of multiplication by
\(q^{[h-1]}\) is

\[
 (L_c,\overline\Theta)\longmapsto
                 L_cA+\overline\Theta t_cB.             \tag{O2}
\]

The first summand is the normal image.  Passing to

\[
 C_{q_0}={\mathcal R_{2h-1}(D)\over
                    \mathcal R_1(D)A}                    \tag{O3}
\]

leaves the occupancy off-diagonal

\[
 \delta_{x,c}(\overline\Theta)
       =[\overline\Theta t_cB]=\rho_c(\overline\Theta). \tag{O4}
\]

Thus the one-chart occupancy filtration is triangular, not block
diagonal, and (O4) need not vanish.  If the row is target-augmented,

\[
       \Theta q^{[h-1]}=\sum_j\lambda_jX_j,              \tag{O5}
\]

then its \((x,c)\)-coefficient and (O2)--(O3) force

\[
                 \delta_{x,c}(\overline\Theta)
                       =\lambda_c\overline Y_c.          \tag{O6}
\]

For the normalized off-diagonal scalar-zero cap,
\(\lambda_c=-1\), so (O6) is exactly
\(-\overline Y_c\).  This is the valid cap Bockstein.  The question is
whether applying it to a target-zero **pair comparison**, followed by a
source-faithful reassembly of \(r,s\), can retain that one-chart value.
The next sections prove only that the fully expanded formal comparison row
has zero statewise difference.  They do not prove that the evaluated
pair-comparison Bockstein vanishes.

## 4. The formal chart-symbol comparison complex is chain-split

Let \(\mathsf D\) be the elementary two-chart comparison complex

\[
 \mathsf D_1=\mathbb C\mathbf g,
 \qquad
 \mathsf D_0=\mathbb C\mathbf b_{pq}\oplus
              \mathbb C\mathbf b_{pr},
 \qquad
 d\mathbf g=\mathbf b_{pq}-\mathbf b_{pr}.               \tag{10}
\]

The formal partial-matching chart-symbol complex on \(S\) is

\[
             \mathsf C(S,\gamma)=
                   \mathsf P(S,\gamma)\otimes\mathsf D, \tag{11}
\]

with differential \(1\otimes d\).  Tensoring (8) by \(\mathsf D\) gives

\[
 0\longrightarrow \mathsf K_x\otimes\mathsf D
 \longrightarrow \mathsf C(S,\gamma)
 \mathop{\longrightarrow}^{\pi_x\otimes1}
 \mathsf C(S\setminus\{x\},\gamma|)\longrightarrow0.    \tag{12}
\]

Both \(j_x\otimes1\) and the full exposure section
\(s_x\otimes1\) commute with \(d\), so (12) is split as a short exact
sequence of complexes.  Write

\[
                    s_x=j_x+\eta_x,                     \tag{12a}
\]

where \(\eta_x\) is the direct-edge sum in (9a).  The map \(j_x\)
preserves \(|M|\), while \(\eta_x\) raises it by one.  Each separately
commutes with \(d\).  Therefore

\[
 \boxed{\delta_x^{\rm form}=0\quad\text{on formal comparison homology,
 and both filtered pieces preserve formal comparison boundaries}.}
                                                               \tag{13}
\]

This supplies a literal chain lift of every formal quotient state for the
differential \(1\otimes d\).  It is not a chain lift for cap multiplication.
Formula (O2) shows the failure explicitly: applying cap multiplication
after the unmatched-state section produces the occupied term
\(\overline\Theta t_cB\), whereas sectioning after the quotient map does not.
Modulo the normal image, that section defect is (O4).

Repeated formal exposure gives repeated split sequences.  Iterating (9a),
first for one site and then for another, is the all-label coefficient
**extraction** map from fewer exposed sites to more.  It commutes with (10)
because it acts on the \(\mathsf P\)-factor.  Reassembly in the reverse
direction is its inverse only on the actual universal all-label image; no
inverse on arbitrary evaluated classes is proved.

## 5. The five-site row is the visible splitting

For \(S=\{p,q,r,s,x\}\), a partial matching has zero, one, or two direct
edges.  Their numbers are respectively

\[
 1,\qquad \binom52=10,\qquad
 5\cdot3=15.                                             \tag{14}
\]

The universal all-label state sum is

\[
 \begin{aligned}
 \mathcal S_5={}&
   \sum_{|M|=2}a_M\ell_{S\setminus V(M)}z^{[h-2]}
  +\sum_{|M|=1}a_M\ell_{S\setminus V(M)}z^{[h-3]}\\
  &+\ell_p\ell_q\ell_r\ell_s\ell_xz^{[h-4]}.           \tag{15}
 \end{aligned}
\]

For the endpoint-ordered variables in the five-site note, direct
expansion of both canonical cap charts gives

\[
             \mathcal A_{pq}^{ij;k\ell c}
              =h\mathcal S_5
              =\mathcal A_{pr}^{ik;j\ell c}.             \tag{16}
\]

The equality is statewise: every nonzero monomial indexed by a partial
matching has coefficient \(h\) in both charts.  At \(h=3\), the all-star
state evaluates to zero on both sides because \(z^{[-1]}=0\).  The row also
retains the target

\[
 h\,\mathbf1_{i=j=k=\ell=c}\,Y_i^{D_5}                 \tag{17}
\]

in both charts.  Hence their oriented difference is zero before or after
target augmentation.

Splitting (14) according to the occupancy of \(x\), the \(x\)-starred
states are the partial matchings of four sites and have layer counts
\((1,6,3)\).  If \(x\) is direct-matched, choose its partner in four ways;
the remaining three sites contribute either zero or one further edge.
This gives \((0,4,12)\).  Their sum is (4).  Thus the formal difference of
the universal row vanishes in every direct-edge grade.  This statement
does not identify the connecting class of an evaluated cap complex.

## 6. Why the apparent residue is not an augmented class

For fixed labels \(k,\ell\), ordinary target insertion is

\[
 I_{rs}^{k\ell}(f)=e_k^{(r)}e_\ell^{(s)}f.               \tag{18}
\]

On the fixed \((r,k),(s,\ell)\)-occupancy summand this is a section of
coefficient extraction.  At formal source-state level, full coefficient
exposure is (9a), and (15) shows exactly its direct/star terms.  Both maps
commute with the chart-symbol differential, so applying them to (16) still
gives zero in the formal comparison complex.

The scalar-zero cap cycle has, in units of \(\overline Y_c\), the locked
target--residue pair \((-1,-1)\).  Multiplication by \(\kappa\) gives
\((-\kappa,-\kappa)\).  Within the already defined one-chart augmented
relation complex and its admitted same-power companions, two elementary
moves are therefore fixed:

* discard the target coordinate and see the number
  \(-\kappa\overline Y_c\); the result is not a cycle of the augmented
  complex;
* retain the target coordinate and cancel it by an admitted same-power
  companion; the target--residue lock supplies
  \((+\kappa,+\kappa)\), and the result is \((0,0)\).

Thus neither target deletion nor same-power target cancellation produces
(1).  The formal complex (10)--(12) also produces zero.  But no evaluated
pair-comparison occupancy connecting morphism has been defined here, so it
would be circular to claim that (1) is not its value.  Choosing different
contractions on the two chart copies is chart-dependent in the formal
complex unless an additional compatibility or homotopy is supplied; a
separately constructed cross-quotient operation could provide precisely
such data.

## 7. Degenerate specializations

The formal splitting and exposure maps in (7)--(9a) have coefficients zero
or one and are defined before evaluating any direct entry, star, trace, or matching
power.  Consequently every specialization of the physical coefficients
retains the formal chart-symbol chain splitting.

At \(\tau=0\), the scalar-zero relation remains an augmented relation
cycle but is not a lift of the radial generator.  The formal comparison
map remains zero, while the evaluated pair-comparison Bockstein remains
undefined and cannot be inferred from that fact.

On the direct-free boundary \(B=0\), one has \(\kappa=AU\ne0\).  Some
evaluated state weights may vanish, but the formal state splitting and
chart-symbol section remain.  If the odd class survives, the desired
output is the nonzero class \(-AU\overline Y_c\); this note neither
constructs nor excludes it in an evaluated cross-quotient complex.

## 8. Exact scope

The proved statements are:

* the statewise split exact sequence (8)--(9), including its direct-edge
  grading;
* the induced **formal chart-symbol** chain splitting (12) and its
  vanishing connecting map (13);
* the exact five-site occupancy refinement (4) of the \(1/10/15\) row;
* statewise equality of the two cap charts and their augmented targets;
* coefficient-one formal exposure, including its degree-zero/one pieces;
  and
* coefficient-independence of those formal facts, including at \(\tau=0\)
  and the direct-free boundary.

The argument does **not** prove that the evaluated cap-multiplication
occupancy sequence, an augmented pair-comparison total complex, or every
source filtration splits.  In particular, it does not exclude the
separately requested relative Rees extension, a nontrivial filtration
homotopy between distinct odd quotients, or a higher operation with
independently proved well-definedness.  The complete partial-matching row
is formally flat, but that fact alone does not close the missing datum.

The dependency-free checker
[`verify_site_occupancy_bockstein_partial_matching_flatness.py`](../computations/verify_site_occupancy_bockstein_partial_matching_flatness.py)
enumerates every partial-matching state through nine exposed sites, checks
the formal split/exposure and its grading for every distinguished site,
verifies the nonzero one-chart cap-multiplication section defect, checks the
five-site \(x\)-occupancy counts, reconstructs the two cap-chart
\(15/10/1\) expansions, and audits the augmented target/residue ledger.
It runs unchanged under `python -O`.
