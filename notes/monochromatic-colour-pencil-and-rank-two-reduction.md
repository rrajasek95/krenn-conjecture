# The colour pencil, and where the rank-two branch actually lives

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.  Nothing here is a partial
case of the conjecture.

## 1. Outcome

Neither branch left open by
[the monochromatic structure note](monochromatic-internal-quadratic-structure-and-eight-cycle-guard.md)
is closed.  What is new: one identity, one structure theorem that applies to
**both** branches — the first constraint on the rank-three branch since T4, and
the first that speaks about the whole pencil rather than a single colour — a real
reduction of the rank-two branch, a proof that the reduction goes exactly that
far and no further, and a generalization of the eight-cycle guard from one
chart to fifty-six.

## 2. The colour-pencil identity

Put \(Q_\lambda=\sum_c\lambda_c^2q_c\), and let \(X^\lambda,Y^\lambda\) be the
\(3\times6\) arrays \(\sum_c\lambda_c\,p_i(x,c)\) and
\(\sum_c\lambda_c\,s_j(y,c)\), with
\(H(A)_{xy}=\operatorname{haf}(A|_{W\setminus\{x,y\}})\).  Every monochromatic
GHZ realization satisfies, identically in \(\lambda\),

\[
 \boxed{\operatorname{haf}(Q_\lambda)\,d
  +X^\lambda H(Q_\lambda)\,(Y^\lambda)^{\mathsf T}
  =\operatorname{diag}\bigl(\lambda_0^6,\lambda_1^6,\lambda_2^6\bigr).}
\]

Verified as a formal identity in \(\lambda\) and in all \(162\) unknowns, over
all monomials and all nine label pairs.

**It is a consequence, not an equivalent form.**  The parameter \(\lambda\)
sees only the colour census, so the identity packages the \(6561\) rows into
their \(28\) census aggregates, \(252\) equations.  Do not use it word-wise.

## 3. T6, and the first rank-three constraint

Laplace expansion gives
\(\operatorname{haf}(Q_\lambda)=\sum_yQ_\lambda(x,y)H(Q_\lambda)(x,y)\), so
\(H(Q_\lambda)=0\) forces \(\operatorname{haf}(Q_\lambda)=0\), and the identity
then reads \(\operatorname{diag}(\lambda^6)=0\), i.e. \(\lambda=0\).  Hence

> **T6.**  In any monochromatic GHZ realization, for every nonzero \(\mu\) over
> the algebraic closure, \(\sum_c\mu_cq_c\) has a nonzero four-hole cofactor.

T2 of the companion note is the case \(\mu=e_c\).  A second corollary:
\(q_0,q_1,q_2\) are **linearly independent over any field**, since a dependence
gives \(Q_\lambda=0\).  T3 also drops out of the identity in one line, together
with the fact that the star kernel must be a coordinate vector; that step and
its corollary are short hand proofs and are **not** machine-checked.

Both committed guards violate T6 exactly at the colours whose anchors they
fail, which is the consistency check one wants.

## 4. The rank-two branch: reduced, and the reduction is sharp

Rank two forces some label blind; the diagonal \(S_3\) puts it at \(0\).  So
\(\operatorname{Row}(0,0,w)=d_{00}\operatorname{haf}_w(q)\) word by word, giving
\(d_{00}h_0(W)=1\) and \(\operatorname{haf}_w(q)=0\) for **every** word
\(w\neq0^6\).  On words in colours \(\{1,2\}\) the direct block therefore
vanishes, and labels \(\{1,2\}\) leave a self-contained residual **RP2**:
\(288\) equations — the \(4\times64\) rows together with the \(32\) conditions
\(\operatorname{haf}_w(q)=0\) — in \(78\) unknowns, namely \(q_1,q_2\) and the
star entries for \(i,j,c\in\{1,2\}\), with no direct block and no colour-\(0\)
or label-\(0\) datum at all.  Down from \(6561\) equations in \(162\) unknowns.

**RP2 is satisfiable over \(\mathbb Z\).**  An explicit witness:
\(q_1=\{12,34\}\), \(q_2=\{01,23\}\),
\(p_1(0,1)=p_2(5,2)=s_2(4,2)=s_1(5,1)=1\), all weights one, \(d=0\).

So the rank-two branch **cannot** be closed through its two-colour star sector.
That corrects the natural reading of the companion note's section 4 item 2,
whose corrected text now says killing the branch "requires more than the
supports":
the star equations of the residual are satisfiable, and everything the branch
still contains sits in the colour-\(0\) and label-\(0\) equations.  That is the
pinned residual.

The witness is a **guard, not a solution** — it fails
\(\operatorname{Row}(0,0,0^6)\), verified independently from the matching-tensor
definition.

## 5. The eight-cycle guard is a fifty-six chart family

The RP2 witness is the alternating eight-cycle with its endpoints at cycle
distance two.  Enumerating all endpoint placements up to the transpose symmetry
\(p\leftrightarrow s\): all \(56\) charts, at distances \(1,2,3,4\), fail
exactly one equation — the third colour's anchor —
and only the distance-one chart, the committed guard, uses the direct edge.
Independently reconstructed during audit from the eight-vertex matching tensor:
the alternating eight-cycle deviates from GHZ at exactly one coefficient, and
does so placement-independently.  The committed
[`verify_chart_model_is_official_eqsystem.py`](../computations/verify_chart_model_is_official_eqsystem.py)
already reconstructs the eight-cycle's single deviation from the official
eight-vertex recursion; what is new here is the **placement-independent**
family, which no checker had covered.

The *completion* problem is chart-dependent, since which edges count as
\(q,p,s,d\) changes with the placement.  **All \(56\) monochromatic completions
close, over any field** — \(60\) unknowns each, every coefficient \(\pm1\), at
most \(27\) branch nodes, no open leaf.  This generalizes the committed
one-chart \(695\)-node closure to every chart, and inherits its scope:
cross-colour internal edges carrying the free colour at one end lie outside the
chart and are **not** covered.

## 6. Rank three

Besides T6, one dichotomy on the ternary cubic
\(\Gamma(\mu)=\operatorname{haf}(\sum_c\mu_cq_c)\).  Over the algebraic closure, either \(\Gamma\) has a
zero with all coordinates nonzero — and there
\(X^\lambda H(Q_\lambda)(Y^\lambda)^{\mathsf T}\) is invertible, so both star
matrices have rank three and \(\operatorname{rank}H(Q_\lambda)\geq3\) — or
\(\Gamma\) is a coordinate monomial \(\kappa\mu_0^{a_0}\mu_1^{a_1}\mu_2^{a_2}\),
or identically zero.  The rank-two branch is the sub-case
\(\Gamma=\kappa\mu_0^3\).  Neither side is closed.

## 7. Field coverage, and what failed

Every positive claim above holds **over any field**: T6's \(\mu\) ranges over
the algebraic closure, the linear-independence corollary descends to any field,
and all branch closures use only "a product is zero implies a factor is zero"
plus closure on \(\pm1\).

DPLL over \(\mathbb F_2\) on the full \(6561\)-equation system did **not**
decide within a three-million-node cap.  That figure comes from an exploratory
run and is not reproduced by the checker.  Support-level branching on
the unfrozen rank-two branch stalls, exactly as
[the calibration guard](branch-search-requires-frozen-data-calibration.md)
predicts; no open-leaf result is recorded as evidence.

## 8. Audit

The dependency-free checker
[`verify_monochromatic_colour_pencil_and_rank_two_reduction.py`](../computations/verify_monochromatic_colour_pencil_and_rank_two_reduction.py)
pins its model by reproducing both committed guard ledgers, then verifies the
pencil identity, its Laplace expansion, T6's machine-checkable inputs, the
word-level blind-label identity, the RP2 census and its witness, the
\(56\)-chart ledger, and the \(56\) completion closures.

Standard library only, exact `Fraction` arithmetic, about nine seconds,
passing normal, `-O` and `-I -S`, deterministic across hash seeds.
