# Adversarial audit of the arbitrary-complex six-site assembly

## Outcome

**PASS.**  The rank-graph case split covers every collection of arbitrary
complex $3\times3$ aggregate blocks on six sites.  In particular, the
finite support relaxations do not silently replace an exceptional zero block
by a rank-at-least-two block.  The only implementation weakness found was
that the $f=4$ checker printed, rather than asserted, its final `closed`
flag; `computations/verify_f4_support_obstruction.py` now asserts that flag.
This was fail-open verification plumbing, not a gap in the displayed five
case outcomes.

## 1. Forced-anchor quantifiers

Fix a site $p$ and colour $r$.  Contracting the star identity at $p$
by a covector $\lambda$ in the coordinate torus expresses the nondegenerate
three-colour diagonal tensor on the other five sites as a sum of slices
centred at the possible neighbours $j$.  The one-slice covering lemma says
that, for every such $\lambda$, some retained slice has its singleton factor
on $\mathbb C e_r$.  The finitely many corresponding constructible sets
cover the irreducible torus, so one is dense.  Its two off-axis coordinate
linear forms vanish identically, while its $r$-coordinate form is nonzero.
Thus, for every ordered pair $(p,r)$, there is a neighbour $j$ with

\[
 A_{pj}=a_{pj,r}\otimes e_r^{(j)}\ne0,\qquad
 H_{[6]\setminus\{p,j\}}(A)\ne0.                         \tag{1}
\]

The neighbours obtained for the three values of $r$ are distinct: one
nonzero matrix cannot have image simultaneously in two different coordinate
lines.  Notice the direction in (1): the coordinate factor is at the
opposite endpoint $j$.  This is exactly the `factor(tail,head,color)`
convention in all four support checkers.  No same-colour or endpoint-symmetry
assumption is made.

## 2. Rank graph and edge bound

Partition the fifteen pairs as

\[
 R=\{uv:\operatorname {rank}A_{uv}=1\},\qquad
 F=\{uv:\operatorname {rank}A_{uv}\ne1\}.                \tag{2}
\]

Thus $F$ is the disjoint union of zero blocks and blocks of rank at least
two.  Equation (1) gives three distinct $R$-neighbours at every site, so

\[
                         d_F(v)\le2.                       \tag{3}
\]

Consequently $2|F|=\sum_vd_F(v)\le12$, hence
$f:=|F|\le6$.  This count uses all rank-one neighbours, not merely
nonzero aggregate support, and treats a zero block as an $F$-edge exactly
as required.

Every simple graph of maximum degree two is a disjoint union of paths and
cycles.  On six labelled vertices the complete isomorphism census is:

| $f$ | graph types for $F$ |
|---:|---|
| 0 | $6P_1$ |
| 1 | $P_2\sqcup4P_1$ |
| 2 | $2P_2\sqcup2P_1, P_3\sqcup3P_1$ |
| 3 | $3P_2, P_3\sqcup P_2\sqcup P_1, P_4\sqcup2P_1, C_3\sqcup3P_1$ |
| 4 | $P_5\sqcup P_1, P_4\sqcup P_2, P_3\sqcup P_3, C_3\sqcup P_2\sqcup P_1, C_4\sqcup2P_1$ |
| 5 | $P_6, C_3\sqcup P_3, C_4\sqcup P_2, C_5\sqcup P_1$ |
| 6 | $C_6, C_3\sqcup C_3$ |

The repository census checks enumerate every labelled graph and verify
disjoint orbit sizes for $0\le f\le5$.  For $f=6$, equality in the
degree sum makes $F$ two-regular; the only partitions of six into simple
cycle lengths at least three are $6$ and $3+3$.

## 3. Zero-versus-higher-rank semantics

The common support encoding used for $f\le5$ assigns an activity bit
$t_e$ and nine entry bits to every $e\in F$.  Its implications are

\[
 x_{e,ij}\Longrightarrow t_e,\qquad
 t_e\Longrightarrow
 \bigvee_{i\ne k,\ j\ne l}(x_{e,ij}\wedge x_{e,kl}).     \tag{4}
\]

Thus $t_e=0$ forces the entire matrix support empty, while every actual
rank-at-least-two matrix extends the encoding by choosing two nonzero cells
from a nonzero $2\times2$ minor.  Formula (4) is only a necessary support
condition and therefore safely overapproximates the active case.  The
rank-one factors on $R$ have independent nonempty endpoint supports.

The branch-by-branch audit is as follows.

| strata | treatment of zero exceptional blocks |
|---|---|
| $f=0$ | There are none.  `rankone-anchor-fibre-cegar.md` excludes arbitrary asymmetric rank-one factors directly. |
| $f=1,2,3$, nontriangle | `support_formula` retains every activity assignment.  All minor witnesses and Laurent cuts are conditional on activity, so an actual zero uses $t_e=0$. |
| $f=3, C_3\sqcup3P_1$ | The stabilizer certificate first permits zero triangle edges.  Its partition-rank blocks handle supports with fewer than three active exceptional terms; the triangle-rigidity block is invoked only when all three are active and rank at least two. |
| $f=4$ | Each good-edge contradiction is conditional on $t_e=1$.  In the first three graph rows a particular good edge is forced active; in $C_4\sqcup2P_1$, all four edges are good and the all-zero assignment is UNSAT; the remaining graph is directly UNSAT. |
| $f=5, P_6$ | The support formula initially permits zero path blocks, then proves all five activity bits and all 45 entries forced before applying coefficient rectangles. |
| $f=5, C_3\sqcup P_3, C_5\sqcup P_1$ | The zero-or-rank-at-least-two relaxation itself is UNSAT. |
| $f=5, C_4\sqcup P_2$ | The exact cancellation-transfer loop starts from the same zero-permitting formula and ends UNSAT, so all $2^5$ activity patterns are covered. |
| $f=6, C_6$ | The saturated checker explicitly uses `allow_zero_exceptional_matrices=True`; it first forces all six activity bits and all 54 entries before the minor argument. |
| $f=6, C_3\sqcup C_3$ | Zero edges are eliminated before the rank-at-least-two checker: a zero chord opposite two higher-rank edges violates the higher-rank-two-path lemma; with at most one other nonzero edge, the remaining bilinear form has a coordinate-torus zero.  Hence all six triangle edges are genuinely rank at least two. |

This exhausts zeros rather than moving them into a smaller-$f$ case, which
would have been invalid because a zero matrix is not rank one.

## 4. Complex cancellation and rank conclusions

Every support formula uses only two universal coefficient necessities: a
constant word has a supported matching, and a mixed word cannot have exactly
one.  The latter is valid over $\mathbb C$ because a supported matching
monomial is a product of nonzero entries.  Fibres with two or more terms are
left unconstrained until an explicit algebraic lemma applies.

The Laurent cuts divide only by variables occurring in supported monomials,
so all denominators are nonzero.  Their integer exponent and parity
identities retain arbitrary complex phases.  The rectangle arguments first
force every factor they cancel to be nonzero; their four equations then say
that a specified $2\times2$ minor vanishes.  Finally, membership in $F$
is used only after activity has been proved: an active actual $F$-block has
rank at least two, contradicting the forced rank-at-most-one conclusion.

Parallel decorated sources and endpoint-colour asymmetry cause no additional
case.  Parallel sources on $uv$ have already been summed into the arbitrary
aggregate matrix $A_{uv}$, and every matrix entry or directed rank-one
factor in the support encodings remains independent.

Combining Sections 1--4 with the cited semantic certificates therefore
proves the claimed six-site statement:

\[
 \boxed{H_6(A)\ne\Delta_{6,3}
        \text{ for every family of complex }3\times3\text{ aggregate blocks}.}
\]
