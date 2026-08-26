# UNAUDITED RISK PROBE — Gate I intertwiner (tau_-) feasibility (2026-08-12)

**Status: UNAUDITED external probe; not spine material. Pinned HEAD
`b63c76c8624996044423a0dde60a2b60c9e8fa3d`; all work from a git-archive
snapshot; exact Fraction arithmetic. Baseline
`verify_h3_cut_swap_odd_prism_kdu_typing_gate.py` PASSES with matching
ledger (86c90e80…). Scripts: probe_source/target/compare/dimensions/
isotypic_mutations.py.**

## VERDICT: INCONCLUSIVE — no obstruction found, but the match carries
limited evidential weight. Leaning: risk not yet reduced.

## Strongest positive result

The Cartan boundary B = (1−ρ)(w−1)u_W (the computable part; see limits)
decomposes EXACTLY over the Klein orbit of the unshared-label packet:
B = −(E+T0) + (E−T0) + (E+T1) − (E−T1), remainder zero — i.e. the corner
coefficient vector is ALPHA=(−1,+1,+1,−1) on the nose, in the literal
checkers' corner order. Of 6 role-assignments of (s,w) to the Klein
involutions, exactly 2 reproduce ALPHA (forced up to s↔w). B lies purely
in the (ρ−,w−) isotypic (other three projectors exactly 0), confirming
the ρ-even adjacent-power companion exclusion. Endpoint/tail marginals,
aggregate sums, corner disjointness all match. One convention note: the
match to the signed Weyl needs a diagonal sign twist on the W' grade
(legitimate isomorphism); the basis-free invariant (product of corner
signs) is +1 on both sides.

## Why the match is weak — four measured facts

1. **K d(u_012) is not data.** H_w exists in committed code only on
   2-variable polynomial de Rham forms; no d or J_col on the collision
   labels. Only dK+Kd = B is computable; K d(u) is known modulo an
   uncomputed term.
2. **The target is 75 distinct vectors** (5 components × 15 four-subsets,
   digests required distinct; components not isomorphic — feature counts
   19116 vs 18576 for comp 3; two colour characters (8,3,3)/(8,4,2)).
   The corner labels are never matched to specific literal columns.
3. **Klein-group realizability gap (C10).** Searching all degree-preserving
   site×colour symmetries: components 1,2,3 induce a Klein group on the 6
   pure columns (24 regular 4-corner systems each), but components 0 and 4
   induce S3 — NO Klein four subgroup, hence 0 systems. Component 0 is the
   typing-gate checker's own representative. Repairable in principle (s,w
   need not be site permutations) but nothing committed realizes them on
   the literal module.
4. **Zero overdetermination.** dim Hom_Klein(source 30-dim, comp-1 288-col)
   = 2144; on the residual isotypic alone 7×70 = 490 minus 70 required
   conditions = **420 free dimensions** (348/420 for comps 2/3). J(M_v)
   sits in (s−,w−) — consistent, but consistency is cheap.

## Two typing facts any tau_- must absorb (design constraints)

- **C9 fine-grade collapse:** the source word grade separates the corners
  into diagonal pairs across grades W (18-multidegree) and W' — ρ and w
  are grade-CHANGING; on the target all four corners share one PURE_WORD
  24-multidegree and component symmetries are grade-PRESERVING. So tau_-
  cannot be injective on the word grading: the source word/tail datum must
  be absorbed into the target MULTIPLIER, not the target word.
- **The three shared labels impose nothing on the residual:** l vanishes
  exactly there, so ρ-equivariance's free coherences constrain Phi only
  off the residual.

## Untestable with committed constructors

Protected/terminal functionals (D, W, target, ainc, Eq, residue, eta/
sigma) do not exist on U_15; s and w as operators on the literal module;
corner↔literal-column dictionary; the scalar A in J3·Phi = A·J_col.

## Mutation controls

Sign flip, wrong ρ, wrong root sites, target coefficient mutations all
detected. One control reported honestly as NOT firing: rebuilding the
corner basis from an unsigned-Weyl mutation reproduces ALPHA — the
corner-coefficient invariant is basis-relative; "all signs are fixed" is a
statement about a chosen basis.

## What would settle Gate-I feasibility

1. Construct J_col (or any differential) on the 15 collision labels so
   K d(u_012) becomes data. 2. Realize s,w on the literal module and pin
   the corner→pure-column dictionary in one component (also decides the
   S3-vs-Klein gap). 3. Decide whether tau_- may be non-injective on word
   grading and what replaces word/tail typing if so. 4. Re-run an
   invariant comparison designed to be overdetermined.
