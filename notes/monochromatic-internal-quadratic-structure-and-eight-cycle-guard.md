# Monochromatic internal quadratics at eight vertices: structure, and an eight-row guard

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.

## 1. Outcome

The question asked was whether an eight-vertex three-colour GHZ realization
can have a **monochromatic** internal quadratic on a residual chart — a
strict generalization of the trade note's slice-specific infeasibility, and a
partial case of the conjecture at \(n=8\) if it could be proved.

**It is not proved, and no counterexample was found.**  What came out is an
exact reduction of the whole \(9\times729\) system, five structure theorems
valid over any field with no positivity and no genericity, one new guard, one
residual branch pinned by the closed form of T1, and one pinned by an explicit
surviving support configuration.

The sharpest new object is a guard that fails **one** equation.

## 2. The eight-cycle guard

Take the alternating eight-cycle \(u\!-\!0\!-\!1\!-\!2\!-\!3\!-\!4\!-\!5\!-\!v\!-\!u\)
with edge colours \(0,1,0,1,0,1,0,1\); as chart data,

\[
 p_0(0,0)=s_0(5,0)=d_{11}=1,\qquad
 q_1(01)=q_0(12)=q_1(23)=q_0(34)=q_1(45)=1,
\]

everything else zero.  Its internal quadratic is monochromatic, and it
satisfies **\(6560\) of the \(6561\) equations**.  Its only failure is

\[
 \operatorname{Row}(2,2,2^6)=0\qquad\text{against target }1 .
\]

This is the canonical binary realization seen inside the three-colour setting.
It satisfies one equation more than the seven-row guard, which fails two — but
the two are complementary rather than nested, since their failure sets are
disjoint: the seven-row guard fails the colour-0 and colour-1 anchors and
*satisfies* the colour-2 one, and this guard is the mirror image.  Neither
blocks strictly more proofs than the other; together they show that a proof
must use \(\operatorname{Row}(2,2,2^6)\) **and** at least one of
\(\operatorname{Row}(0,0,0^6)\), \(\operatorname{Row}(1,1,1^6)\).  Its
content:

> Every hypothesis in the \(h=3\) system except the third colour's anchor is
> simultaneously satisfiable.  Any proof that does not use that anchor is
> therefore wrong.

**It admits no monochromatic completion, over any field.**  Freeze the eight-cycle's entire
colour-0/colour-1 sector; free the entire colour-2 sector — \(q_2\),
\(p_i(x,2)\), \(s_j(y,2)\) — and all nine direct scalars, sixty unknowns; and
impose all \(9\times729\) rows.  Exhaustive monomial branching closes all
\(695\) nodes with no open leaf.  Every coefficient in the frozen system is
\(\pm1\) and every branch closes on the constant \(-1\), so the reductions and
closures are characteristic-independent: **within the monochromatic chart**,
the canonical two-colour realization cannot be upgraded to three colours by
any colour-2 material.

Cross-colour internal edges carrying colour \(2\) at one end lie outside that
chart and are **not** covered.  Freeing the sixty of them leaves \(3381\)
equations in \(120\) unknowns which the same branching does not decide; that
figure comes from an exploratory run and is not reproduced by the checker.

This is slice-specific in the same sense as the trade note's result — it fixes
one colour-0/1 sector, and there is no classification of such sectors here.

## 3. Structure theorems

All are identities over every monomial, or short hand proofs from such
identities, and hold over any field.

**T1 (class factorization).**  With \(q\) monochromatic, every word has zero or
two odd colour classes — three is impossible.  There are \(183\) all-even
words (three pure, \(180\) not, matching the leak note's count) and \(546\)
two-odd words.  On all-even words the row factorizes over the classes; on
two-odd words with odd classes \(a,b\) and even class \(e\),

\[
 \operatorname{Row}(i,j,w)=h_e(S_e)\bigl[\mathfrak p_a(S_a)_i\,\mathfrak s_b(S_b)_j
  +\mathfrak p_b(S_b)_i\,\mathfrak s_a(S_a)_j\bigr],
 \qquad
 \mathfrak p_c(T)_i=\sum_{x\in T}p_i(x,c)\,h_c(T\setminus x).
\]

So the \(4914\) two-odd rows carry **no direct-block monomial at all**: that
part of the system is purely star-bilinear.

**T2 (sharp anchor lemma).**  If all fifteen four-hole cofactors
\(H_c(e)=\operatorname{haf}(q_c|_{W\setminus e})\) vanish, the colour-\(c\)
anchor row is identically zero, whatever the stars and direct block contain.
Every colour therefore needs a nonzero cofactor.  This strictly sharpens
**L0** of [`three-anchor-internal-quadratic-leak.md`](three-anchor-internal-quadratic-leak.md):
L0 asks for two disjoint edges in the support, which is a support condition and
does not imply a nonzero cofactor.  T2 is the cancellation-proof form.

**T3 (label-kernel rank).**  The \(18\times3\) star matrix \([p_i(x,c)]\) has
rank at least two, and likewise for the second star.  In the rank-two case
with kernel \(e_{j_0}\): \(p_{j_0}\equiv0\); \(d_{j_0j}=0\) for \(j\neq j_0\);
\(d_{j_0j_0}h_{j_0}(W)=1\); and \(\operatorname{haf}_w(q)=0\) for every word
other than \(j_0^6\), so no rainbow perfect matching exists across the three
supports and every row away from \(j_0^6\) becomes star-only.

**T4 (handle rigidity).**  For every site \(x\), colour \(a\), odd subset
\(T\subseteq W\setminus\{x\}\) and ordering \((b,e)\) of the other two
colours, put \(R=W\setminus(\{x\}\cup T)\),
\(\mathfrak u=h_e(R)\,\mathfrak p_b(T)\) and
\(\mathfrak v=h_e(R)\,\mathfrak s_b(T)\).  Then there is an exact
\(3\times3\) matrix equation
\(P_a(x)^{\mathsf T}\mathfrak v+\mathfrak u^{\mathsf T}S_a(x)=0\) — \(576\)
of them, all verified as identities.  The factor \(h_e(R)\) must be carried:
the row identity is \(h_e(R)\bigl[\cdots\bigr]=0\), not \([\cdots]=0\).  The rank-one alternative gives: if
\(P_a(x)\) and \(S_a(x)\) are both nonzero then either
\(\mathfrak u=\mathfrak v=0\) or \((\mathfrak u,\mathfrak v)\) is proportional
to \((P_a(x),-S_a(x))\); "exactly one of the two zero" is impossible.

The site corollary is weaker than it first looks, and the weaker form is the
correct one: at every site, at least one of (i) the first star matrix has rank
\(\leq1\) there, (ii) the second does, (iii) some colour \(b\) has
\(U_b(x)=V_b(x)=0\), where \(U_b(x)=\mathfrak p_b(W\setminus x)\) and
\(V_b(x)=\mathfrak s_b(W\setminus x)\).  A configuration with two colours full and the third star
row zero genuinely escapes (i) and (ii), so (iii) cannot be strengthened.

**T5 (colour blindness).**  If a star is blind to a colour \(a\) then
\(\operatorname{Row}(i,j,a^6)=d_{ij}h_a(W)\), forcing \(d\) to be a multiple of
\(E_{aa}\).  Hence at most one colour is blind, across both stars.

## 4. What is open, pinned

1. **The rank-three branch of T3** is untouched.  Its exact residual is the
   \(1647\) all-even equations together with the \(4914\) direct-block-free
   bilinear equations of T1, with T4 constraining the latter site by site but
   leaving the "(iii) null colour" branch open at every site.
2. **The rank-two branch is not closable at support level.**  Its support
   conditions reduce to a finite question — a minimal edge cover inside
   \(\operatorname{supp}q_{j_0}\) each of whose edges extends to a matching,
   disjoint from the other two supports, each other colour with a live
   four-hole outside those supports, and no rainbow matching — and that
   question is **satisfiable**.  The branch is pinned by an explicit survivor
   rather than by a count, since the count depends on how the finite question
   is normalized and no checker here fixes that:
   \(\operatorname{supp}q_{j_0}=\{01,23,45\}\),
   \(\operatorname{supp}q_a=\operatorname{supp}q_b=\{14,35\}\).  Killing this
   branch requires more than the supports.

   *Correction (later the same day).*  It also requires more than the
   **two-colour** star equations.  The branch reduces to a self-contained residual in labels and
   colours \(\{1,2\}\) — \(288\) equations in \(78\) unknowns, with no direct
   block and no colour-\(0\) or label-\(0\) datum — and that residual is **satisfiable over
   \(\mathbb Z\)** by an explicit witness.  So the branch cannot be closed
   through its two-colour star sector at all; everything it still contains sits
   in the colour-\(0\) and label-\(0\) equations.  See
   [the colour-pencil note](monochromatic-colour-pencil-and-rank-two-reduction.md),
   which also gives T6, a constraint on the rank-three branch of item 1.

Two side facts worth keeping.  No cubic graph on eight vertices has exactly
three perfect matchings.  Over all \(19355\) labelled cubic graphs on eight
vertices the perfect-matching count is \(5\) (\(12600\) graphs), \(6\)
(\(3360\)), \(7\) (\(2520\)) or \(9\) (\(875\)); every one of them is a
union of three disjoint perfect matchings, so the \(32970\) unordered Kotzig
triples of \(K_8\) already exhaust the family.  So a monochromatic solution
would have to use genuine cancellation rather than a leak-free
configuration.  And the whole system is invariant under
\(q\mapsto q/\tau\), \(p\mapsto\tau p\), \(s\mapsto\tau s\),
\(d\mapsto\tau^3d\), which is the grading of
[the weight note](terminal-class-weight-invisibility-and-fourhole-grade-ladder.md),
found here independently.

## 5. Audit

The dependency-free checker
[`verify_monochromatic_internal_quadratic_structure.py`](../computations/verify_monochromatic_internal_quadratic_structure.py)
pins its model to the audited one by reproducing the seven-row guard ledger
\((00,0^6,-1)\), \((11,1^6,-1)\) symbolically before anything else, then
verifies T1 as an identity on all \(6561\) rows, the two word-type counts, the
absence of direct-block monomials on the two-odd rows, T2 in full, the
label-kernel identity and the label-blind rows on which T3 rests, the \(576\)
handle identities of T4 with its rank alternative, the first-star half of the
T5 identity, the eight-cycle guard's \(6560/6561\) ledger, the \(695\)-node
closure of its completion problem, and the rank-two support survivor.  The
remaining steps of T3 and T5, and the site corollary of T4, are short hand
proofs from those identities and are **not** machine-checked.  Standard library only, exact
`Fraction`, about seven seconds, passing normal, `-O` and `-I -S`, identical
across hash seeds.

The eight-cycle guard was independently reconstructed during audit, from the
eight-vertex matching tensor rather than from the chart formula: monochromatic
internal edges, exactly one failing coefficient, namely \((2,2)\) at \(2^6\)
with residual \(-1\).  No checker in the repository performs that
reconstruction.
