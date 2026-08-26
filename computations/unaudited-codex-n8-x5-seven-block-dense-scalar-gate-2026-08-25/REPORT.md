# Canonical seven-block dense scalar gate

Status: **the scalar obstruction is reduced to two exact finite ideals, but neither ideal produced a characteristic-zero basis or unit certificate within the hard 60-second gate.** The general dense locus remains open; no countermodel is claimed.

The formal guard gives `L67(I3)=0`. Hence `rank(L67)<=8`, and `I3` makes all three diagonal activities live. If `tr(A67)` is nonzero, cap `67` is immediately active. Actual cap-pairing failure is stronger than trace zero: it is exactly the adjoint-image equation

```text
A67 = A06^T X A57 + Y A57 + A56^T Y^T A17
    + A26^T Z A57 + A56^T Z^T.
```

Together with the guard, this equation makes trace zero automatic. The three canonical guard matrices also imply `A56^T=-A26 A57^T`, `(I-A17 A26)A57^T=0`, and `rank(A57)<=2` on the exact nonzero-block stratum.

For cap `45`, star center `2`, the response map is `A04 K [A35^T|A56|A57]`. With `P=Row(A04)` and `Q=Col(A35^T)+Col(A57)`, failure of this star has only two color-symmetric forms:

1. `P=Q=Q^3` (response rank nine); or
2. `e_i in P intersect Q` for some coordinate `i` (a diagonal activity dies).

The exact ideal builder expanded all 6,561 X5 amplitude equations from the thirteen supported perfect matchings, all 27 nontrivial guard scalars, nine adjoint-image equations, and trace zero. The coordinate branch has 6,604 generators in 138 variables; the full-rank branch has 6,616 generators in 162 variables. Exact Singular `slimgb` runs over `Q` were externally capped at 60 seconds. Both produced no stdout, basis, or unit-ideal certificate before termination; the full-rank branch returned timeout code 124.

This is a bounded obstruction, not evidence that a solution exists. The exact next step is to split by the sealed thirteen two-sandwich incidence patterns before elimination. Monolithic Gröbner computation is not a safe proof route at this scale.
