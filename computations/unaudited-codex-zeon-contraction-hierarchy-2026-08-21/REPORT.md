# Source-relative zeon contraction hierarchy

Status: **UNAUDITED exact structural closure**.  Literal contraction through
one, two, and three sites has been derived and checked by matching enumeration.
The hierarchy is source-faithful, but it is not a smaller module: with the
exposed physical colours retained, every fixed contraction set is just a
re-indexing of the original 6,561 tensor coefficients (6,558 mixed rows).

## Literal operator and identities

Put

\[
 B_S=\bigotimes_{i\in S}(\mathbb C\oplus V_i),\qquad V_i^2=0,
 \qquad q=\sum_{i<j}A_{ij},
\]

and write `q^[m]` for the divided matching power.  For a site `i` and
physical colour `c`, `D_(i,c)` means contraction of the actual `V_i` factor
by the coordinate covector `e_(i,c)^*`; it is zero on components not
occupying `i`.  Operators on distinct sites commute.  This is a literal
linear contraction on the site-graded vector space, **not** a derivation of
the square-zero quotient.

Let `W` be the complement of the displayed contracted sites.  Write
`l_(p,a)` for the `a`-row of the star from `p` into `W`, and
`a_pr[a,b]` for the physical cell of the internal edge `pr`.  Direct
partition of perfect matchings gives

\[
 D_{p,a}q^{[4]}=l_{p,a}q_W^{[3]},                       \tag{1}
\]

\[
 D_{p,a}D_{r,b}q^{[4]}
 =a_{pr}[a,b]q_W^{[3]}+l_{p,a}l_{r,b}q_W^{[2]},        \tag{2}
\]

and, for three distinct sites,

\[
\begin{aligned}
 D_{p,a}D_{r,b}D_{s,c}q^{[4]}
 ={}&\bigl(a_{pr}[a,b]l_{s,c}+a_{ps}[a,c]l_{r,b}
              +a_{rs}[b,c]l_{p,a}\bigr)q_W^{[2]}\\
    &+l_{p,a}l_{r,b}l_{s,c}q_W.                        \tag{3}
\end{aligned}
\]

For the GHZ target, the right side is `X_(W,c)` precisely when every
contracted colour is the same `c`, and is zero otherwise.

The exact matching partitions are

```text
contracted sites   matching type                         count
1                  1 crossing + 3 residual                105
2                  internal pair + 3 residual              15
                   2 crossing + 2 residual                 90
3                  1 internal + 1 crossing + 2 residual    45
                   3 crossing + 1 residual                 60
```

These sum to the 105 perfect matchings of `K8` at every layer.  The checker
enumerates the matchings, rather than assuming the displayed expansions.

## Exact module-rank theorem

Fix any site set `U`.  Record both the contracted colour word in
`tensor_(u in U) V_u` and every residual colour word.  Concatenating them is
a bijection

\[
 \{0,1,2\}^{U}\times\{0,1,2\}^{[8]\setminus U}
       \longrightarrow \{0,1,2\}^{8}.
\]

Therefore the full coordinate matrix of `D_U(q^[4]-GHZ)` is a permutation
matrix of rank `3^8=6561`.  Removing the three pure target coordinates leaves
rank `6558`.  This was frozen for `|U|=1,2,3`, including hashes of the three
ordered label ledgers.  The same proof applies for every larger `U`.

Thus the third contraction layer is not a new or smaller source-faithful
module.  Keeping all coordinates gives exactly the original normalized
source ideal; dropping coordinates can only weaken it.

The first nontrivial pair layer (2) is the frozen full-nine/carrier identity.
Contracting it against a carrier matrix `K` gives

\[
 s_Kq^{[3]}+r_Kq^{[2]}=T_K,
 \quad s_K=\langle K,A_{pr}\rangle,
 \quad r_K=\sum_{a,b}K_{ab}l_{p,a}l_{r,b}.
\]

Its literal response edge is

\[
 (r_K)_{uv}[\alpha,\beta]=\sum_{a,b}K_{ab}
 \left(A_{pu}[a,\alpha]A_{rv}[b,\beta]
       +A_{pv}[a,\beta]A_{ru}[b,\alpha]\right),
\]

which is exactly the frozen response-star carrier formula.  All nine exposed
colours and all `3^6` residual words are the 6,561 original word rows.  The
frozen tail-response theorem retains the source-labelled subset

```text
7+1        8
6+1+1     12
3+3+2    360
total     380
```

and `X5` supplies it because at `n=8,d=3`, `X5` is all 6,558 mixed rows.

## Crosswalk to the archived polar routes

- `full-nine-pure-slice-channel-routing.md`: the equation
  `M_d=E_dd-F_d a` is the constant residual-word scalarization of (2).
  Its channel-routing lemma is a projection of the same pair layer.

- `target-blocked-site-polar-descent.md`: the cap equation
  `beta q^[2]=sum lambda_c X_c` is a selected pair/carrier projection.
  The one-site polar and two-site dark quotient are further literal
  contractions/quotients of that projection.  Their strength comes from
  incidence and blocking hypotheses, not new source rows.

- `determinant-split-route.md`: its six-site `3+3` formula is the same
  three-site matching partition as (3): six all-cross bijections, plus nine
  internal-left/internal-right/cross placements.  It is applied there to a
  standalone six-site top equation (or requires a branch on which that
  equation has first been isolated); it is not an extra consequence of the
  eight-site equations.

- `h3-hamming-one-normal-incidence-compound-transgression.md`: this is the
  genuinely different operation.  The ordinary Hamming-one polar is
  `Gamma_x=rho_x o iota_x^q`, while the four-hole term needs the appended
  value `nu_x=rho_x(beta_x)`.  Re-inserting the response incidence `beta_x`
  is second order in the response and is not another `D_U` coordinate.  The
  unresolved scalar is the archived cancellation

  \[
  \alpha\sum_x\nu_x=-24\,(u^{\{3\}})^T J_3v^{\{3\}}. \tag{4}
  \]

Accordingly, there is no missing *linear site-down* layer.  The smallest
genuinely missing higher datum is nonlinear response-dependent normal
reinsertion (or an equivalent overlap identity proving (4)).

## Sharp loss-of-information controls

Two exact controls prevent promotion of the hierarchy into an unwarranted
lower-power or smaller-row theorem.

1. On one physical colour, take the perfect matching
   `01|23|45|67` and add the chord `02`.  The fourth divided powers are
   identical—the chord belongs to no perfect matching—but the third divided
   power gains the literal term `02|45|67`.  Hence the top tensor does not
   determine the actual lower powers `q,q^[2],q^[3]` outside the contracted
   combinations (1)--(3).

2. The frozen partial remote point satisfies pure normalization, all twelve
   selected `6+1+1` rows, and all eight selected `7+1` rows, but it fails 138
   of the 360 `3+3+2` rows.  Thus a selected linear-tail contraction packet
   is strictly weaker than the full mixed layer.  This is a control against
   the smaller packet, not a counterexample to `X5`.

The archived tagged-incidence mutation supplies the complementary sharp
control: its selected all-word/Hamming-one polar data stay fixed while the
four-hole coefficient changes from `0` to `2`, and the incidence rank jumps
`3 -> 4`.  Hence literal/Hamming-one first-response data do not manufacture
`nu_x`.

## Replay

```sh
python3 computations/unaudited-codex-zeon-contraction-hierarchy-2026-08-21/audit_zeon_contraction_hierarchy.py --write-results
python3 -O computations/unaudited-codex-zeon-contraction-hierarchy-2026-08-21/audit_zeon_contraction_hierarchy.py
python3 -I -S computations/unaudited-codex-zeon-contraction-hierarchy-2026-08-21/audit_zeon_contraction_hierarchy.py
```

All three modes pass with byte-identical stdout SHA-256
`0a72e9a22d9a293c74780364517d6f8bc3a5fe68b701dfe09a47e86e56e9c433`.
The logical result digest is
`2864c5a426f9aac920013d1d9ac44b01e0e233e5888d25f3109db80aac88d7b5`.
The script and result SHA-256 values are respectively
`a7587f3e6d38c8d7c4fb6e9ba9b684226ff6d628959716852bdfbe73e9299da9`
and `0861f75b1cb729d1550673a8ff9252c0fb756ef455e8a1f4c218bb7dc9aa3cc7`.

The two relevant archived checkers were also replayed.  The blocked-site
checker passes 160 coefficient cuts, 729 companion proportionalities, 101
blocking geometries, and the exact seven-held/two-missing diagonal-row guard.
The `h3` checker passes the marked `C2/C3` identities, the `0 -> 2` mutation,
and the exact incidence-cokernel rank jump `3 -> 4`.
