# Orbit-85 branch-relative tail audit

## Verdict

The branch-relative gap is real and occurs already in the trimmed orbit-85
proof.  Of its 93 inside-free (FR) antecedents, 19 are attached to the one
audited live witness star of their colour and have an exact source lift.  The
other 74 are attached to residual free-set stars that are not localized.  No
uniform division-free lift of those 74 equations follows from their literal
mixed amplitude rows.  Consequently the previously frozen order-two circuit
is a valid constructible-branch linearization, but it is not the true
coefficient of a certificate over the literal X5 plus pure-normalization
ideal.

This is a provenance counterguard, not a new solve and not a claim that the
full normalized X5 fibre has a point.

## Exact deformation convention

Use

    A_ij^(ab) = delta_(a,b) d_ij^a + epsilon T_ij^(ab),   a != b for T.

For an even-profile mixed word `w`, write its literal source row as

    F_w(A(epsilon)) = F_w(D) + epsilon^2 Tail2_w(D,T) + O(epsilon^3).

There is no linear term.  `Tail2_w` is the exact sum of matching monomials
having exactly two cross-colour edges, as in the preceding package.

## FR equations: exact lift and exact gap

An FR branch equation has the form `P=0`, where `P` is a product of two
residual monochromatic hafnians.  Its corresponding literal mixed amplitude
row is

    F = x P + epsilon^2 Q + O(epsilon^3),   Q=Tail2_w,

where `x` is the same-colour star entry at that free site.

At the selected witness site, `x` is already live and has an inverse `u`.
The checker expands the integral identity

    u F - P = P(ux-1) + epsilon^2 uQ.

Thus the source-faithful lift of this FR antecedent is `uF`; its true
order-two coefficient is `u Tail2_w`, not zero.  Across all 448 orbit-85 FR
rows, 96 have this form.  The trimmed 502-clause proof uses 19 of them, all of
profile `4+2+2`, contributing 19*30=570 Tail2 monomial occurrences.

At a residual free-set site, `x` is not one of the chart's live factors.
Only `xP` is visible at diagonal order in the literal source row.  The quotient
specialization

    x=0, P=1

kills `xP` but not `P`.  Unrelated pure/open factors may remain nonzero, so
pure normalization does not repair this missing division.  This proves that
there is no uniform local identity recovering `P` from this source row
without adding an inverse for `x`.  It does not purport to satisfy every other
X5 row; proving that those other rows recover `P` would itself be a new global
ideal-membership theorem.

There are 352 residual FR rows in the full orbit branch.  The trimmed proof
uses 74: 70 of profile `4+2+2` and four of profile `6+2+0`.  If one elects to
retain them as extra branch equations, their potential order-two source tails
contain 70*30+4*90=2,460 monomial occurrences.  From the literal source
packet alone their coefficient is undefined, rather than zero.

## Complement and localizer antecedents

For an outside-free star, let `P_j` be its 32 residual products and retain the
constructible complement localizer

    L = sum_j r_j P_j - 1.

With literal full rows `F_j=xP_j+epsilon^2 Q_j+...`, the exact identity is

    sum_j r_j F_j - xL
      = x + epsilon^2 sum_j r_j Q_j + O(epsilon^3).

Therefore the true C0 derived-star coefficient is
`sum_j r_j Tail2_wj`.  The previous proof circuit already sees these terms
through its explicit amplitude references.  It uses five distinct complement
localizers, 17 times in total.

The equation `L=0` itself is not a literal X5 or pure-normalization equation;
it is the algebraization of the chosen constructible complement.  Under the
stated off-diagonal-only substitution its `P_j(D)` and fixed witnesses have
zero epsilon derivative, so it may be held constant only as an additional
branch hypothesis.  The 384 guarded selector inverses and nine unguarded
opens involve monochromatic hafnians and likewise have zero off-diagonal
coefficient.  They introduce no further omitted tail term.

## Corrected order-two interface

The antecedent replacement rule is therefore:

| antecedent | order-two replacement |
|---|---|
| literal mixed amplitude | `Tail2_w` |
| FR at selected live witness | `u_x Tail2_w` |
| FR at residual free-set site | undefined from literal packet |
| C0 derived star | `sum_j r_j Tail2_wj` |
| fixed complement/open/localizer | zero, conditional on retaining the branch |

Because 74 compiled FR leaves are in the third row, there is no
source-faithful whole-core `C2` yet.  The smallest repair is either to split
and localize each corresponding residual star, or to retain `P=0` to order two
as a genuinely new branch-persistence hypothesis.  Algebraically gluing the
constructible branch cover is the alternative global repair.

## Frozen census

The replay checks the original 4.62 MB certificate DAG directly.  Its relevant
core references are:

| kind | occurrences | distinct |
|---|---:|---:|
| mixed amplitude | 569 | 185 |
| inside-free FR | 93 | 93 |
| complement localizer | 17 | 5 |
| guarded inverse | 312 | 137 |
| unguarded open | 12 | 7 |

The checker also enumerates all 105 perfect matchings of K8, independently
recomputes every FR profile/Tail2 term count, and expands the live-star and
complement identities over the integers.

## Replay

    python3 computations/unaudited-codex-n8-diagonal-orbit85-branch-tail-audit-2026-08-23/check_branch_tail.py
    python3 -O computations/unaudited-codex-n8-diagonal-orbit85-branch-tail-audit-2026-08-23/check_branch_tail.py
    python3 -I -S computations/unaudited-codex-n8-diagonal-orbit85-branch-tail-audit-2026-08-23/check_branch_tail.py
