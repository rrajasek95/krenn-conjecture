# Triangle cross-word holonomy and the first literal cap attachment

Status: **UNAUDITED exact structural PASS**.  This report identifies a
source-labelled cross-word syzygy and a finite open/boundary attack on the
three diagonal triangle-blocker branches.  It does not prove the full
eight-site theorem, and it does not yet close the direct-pair blocker branch.

## Outcome

Fix the cap pair `67` and residual triangle `T={0,1,2}`.  For each fixed
colour word on `T`, the 243 full `X5` equations are affine-linear in exactly
three source cells, one on each edge `01,02,12`.  Comparing outside words is
therefore a literal comparison of different target coordinates through the
same three physical variables.

The comparison has the exact generic rank ladder

```text
one outside word       rank 19
two outside words      rank 26
three outside words    rank 27.
```

The last rank jump is a `3x3` determinant of the three six-site cofactor
vectors.  Four rows satisfy the signed Cramer/Hilbert--Burch identity

```text
sum_(s=0)^3 lambda_s F_s
  = sum_(s=0)^3 lambda_s (b_s-t_s),
lambda_s=(-1)^s det(C_0,...,C_hat_s,...,C_3),             (1)
```

because `sum lambda_s C_s=0`.  Here `C_s` is the coefficient row of the
three internal triangle cells, `b_s` is the 60-matching packet avoiding all
three triangle edges, and `t_s` is the GHZ target coordinate.  Taking three
mixed rows and one pure row makes the target term

```text
                 det(C_0,C_1,C_2).                       (2)
```

This is a literal target-augmented comparison map: it uses actual full `X5`
rows and changes the output word without declaring a word-reset operation.
The four-row specialization by itself remains inside one pure residual-word
block.  The stronger rootless-to-pure comparison requires the global
27-column construction in Section 3.1 below.

## 1. Literal triangle decomposition

Every perfect matching of eight sites uses either zero or one edge of the
three-site triangle.  The exact matching partition is

```text
avoids 01,02,12                 60
uses 01                         15
uses 02                         15
uses 12                         15.
```

For a fixed triangle word `(a,b,c)`, write

```text
x=A_01[a,b],  y=A_02[a,c],  z=A_12[b,c].
```

Each of the 243 outside words gives

```text
             C_o,01 x + C_o,02 y + C_o,12 z + b_o=t_o.   (3)
```

The checker reconstructs all `6,561*105=688,905` matching occurrences.
The 27 triangle-word systems share the same 27 physical triangle cells, so
globally (3) is one source map `D_T:k^27 -> k^6561`, not 27 independent
formal systems.  The unweighted incidence shadow has rank 19 and its
eight-dimensional kernel is the familiar vertex-potential gauge.  Physical
cofactor weights can and do lift the rank to 27.

## 2. Three-word holonomy

Write the three cofactor vectors for outside word `s` as

```text
                 (u_s(c),v_s(b),w_s(a)).
```

Two generic outside words leave one common dark vector.  Relative to the
first word, put

```text
alpha_c=u_1(c)/u_0(c),
beta_b =v_1(b)/v_0(b),
gamma_a=w_1(a)/w_0(a).
```

Its three edge components are exactly

```text
X_ab=v_0(b)w_0(a)(gamma_a-beta_b),
Y_ac=u_0(c)w_0(a)(alpha_c-gamma_a),
Z_bc=u_0(c)v_0(b)(beta_b-alpha_c).                       (4)
```

A third word evaluates (4) by

```text
det [[u_0(c),v_0(b),w_0(a)],
     [u_1(c),v_1(b),w_1(a)],
     [u_2(c),v_2(b),w_2(a)]].                            (5)
```

Thus (5) is a literal curvature/holonomy: it vanishes when the third
cofactor packet is in the affine span of the first two, and otherwise kills
the last dark direction.  The exact abstract rational model has ranks
`19,26,27`.  The archived controls also reach full global rank:

```text
W40/X4: outside words 10222,10111,00000; ranks 15,24,27
W25/X3: outside words 00000,11111,10000; ranks 15,26,27.
```

Both controls have the expected one-column augmented rank jump because they
are not full `X5` points.

## 3. Cap-word specialization

The load-bearing specialization fixes sites `0,...,5` to one pure colour
`c` and varies only the ordered colours `(i,j)` on cap endpoints `6,7`.
Choose three mixed cap pairs and the pure pair `(c,c)`.  In (1), place the
four signed cofactors in the corresponding entries of a `3x3` matrix `K`.
Then

```text
sum_(i,j) K_ij C_ij=0,
K_cc=-det(C_mixed,0,C_mixed,1,C_mixed,2).                (6)
```

Consequently the multiplier of the pure target is literally the diagonal
triangle blocker `K_cc`, not an anonymous determinant.  An exact dense
rational source in the checker has a nonzero chart for all three colours,
so these minors are not identically zero polynomials.  W40 and W25 lie on
this restricted determinant boundary; that is a scope control, not a claim
about a hypothetical full `X5` point.

Equation (6) is a pure-block provenance bridge.  On a diagonal-blocked
triangle branch,

```text
                  K_cc in rowspan L_T,                   (7)
```

so evaluating (7) on the same Cramer matrix replaces the target term in
(1) by literal outside-response data `L_T(K)`.  At this stage the three
internal triangle source cells have disappeared.  No scalar localization,
word reset, or invented chain cell is used.

### 3.1 The literal rootless-to-three-pure comparison

All 6,561 rows share the same 27 internal triangle cells.  This permits a
genuine comparison across triangle words, not just across cap-endpoint words.
Take the mandatory full words

```text
01211222, 00000000, 11111111, 22222222
```

with respective weights `1,2,4,8`.  The checker constructs a 27-row basis
from only four outside-word slices

```text
11222, 00000, 11111, 22222.
```

Writing `B` for its `27x27` internal-cell coefficient matrix and
`D=det(B)`, Cramer's rule gives a polynomial row dependence, after clearing
`D`, which contains the mixed rootless row and all three separately labelled
pure rows.  Every other row in the dependence is mixed.  On an exact
normalized source, its target side is therefore

```text
                         (2+4+8) D = 14 D.               (6a)
```

The basis has the exact rank ladder `19+7+1`.  The companion Singular replay
factors its determinant into monomial open factors, five two-slice `2x2`
minor factors (one repeated), and

```text
H = det [[u00,v00,w00],
         [u10,v10,w10],
         [u20,v20,w20]],                              (6b)
```

up to the frozen sign convention.  The third-word holonomy occurs to the
first power.  After localizing the elementary one- and two-slice factors,
the whole global attachment is controlled by the single scalar `H`.  The
factorization has 144 expanded terms and is replayed by
[`factor_rootless_three_pure_basis.sing`](factor_rootless_three_pure_basis.sing).

This is the theorem-shaped cross-word object requested by the older residual
Macaulay route, but it is not yet its conclusion.  Equation (6a) says that
the triangle-avoiding packets combine to `14D`; it does not show that their
image in the residual cubic quotient vanishes.  The remaining question is
now precise: after the full-nine/common-power reductions, does this
combination represent the line-dependent coefficient `chi`, and does `X5`
force its `H`-component to vanish?  A positive answer gives the common clean
root; an independence witness retires this attachment.

## 4. Exact remainder and the next finite gate

The 60 triangle-avoiding matchings in `b_s`, relative to cap `67`, split as

```text
6   direct A_67 terms,
18  responses on the three internal triangle edges,
36  responses on the twelve edges represented in L_T.    (8)
```

This is exactly the sector split found independently by the universal
five-set theorem.  After (7), all target and 36 outside-response terms live
in the same `L_T(K)` module.  The only source sectors not already in that
module are the `6+18` direct/opposite-edge packet.

The next bounded calculation is therefore precise:

1. for each pure colour and each nonzero cap-word minor, substitute one
   diagonal membership witness into (1);
2. adjoin the three cyclic five-set augmented identities;
3. test whether the remaining `6+18` packet reduces to zero, or leaves one
   primitive separator;
4. on the complementary chart, impose rank at most two on the `8x3` mixed
   cap-word coefficient matrix and use its determinantal syzygies directly.

There are only `3*binom(8,3)=168` raw open charts before the evident colour
and cap symmetries.  The boundary is generated by the same 56 minors per
colour.  This is a finite incidence calculation with a standard
determinantal complex, not a full 6,571-equation Groebner basis.

The subsequent dependency-free Rust audit
[`five-set response surjectivity`](../unaudited-codex-five-set-response-surjectivity-2026-08-22/REPORT.md)
now closes the `18`-term part on an explicit open: if the three cyclic
five-set quotient maps have rank nine, the nine functionals on each omitted
response edge lie in `rowspan L_T`.  A dense exact control has this rank for
all 1,680 triangle-colour groups.  The old all-pair missing-row
countermodel has it for 332/1,680 groups; its remaining groups screen below
rank nine at both audit primes (a boundary candidate, not yet a
characteristic-zero upper-rank certificate).  What remains is therefore
the six direct terms on the open, together with a source-faithful
classification of the rank-drop boundary.

## 5. What is and is not proved

Proved exactly here:

1. the triangle-local affine source decomposition;
2. the `19 -> 26 -> 27` holonomy formula;
3. the universal four-row source-labelled Cramer identity;
4. the cap-word specialization making its target multiplier a literal
   diagonal blocker;
5. the exact remainder split `60=6+18+36`;
6. a bounded global dependency containing `01211222` and all three pure
   words, and its exact `19+7+1` determinant factorization with one linear
   holonomy factor.

Not proved:

- that one of the restricted cap-word minors is nonzero at every exact
  source;
- that the `6+18` packet vanishes after the cyclic substitutions;
- closure of the rank-at-most-two boundary;
- the fourth blocker `<K,A_67> in rowspan L_T`;
- identification or annihilation of the global holonomy class in the
  residual Macaulay quotient.

Thus this is a solid attack on the three diagonal branches, not a theorem
claim.  Its value is that both failure modes have mathematical shape:
holonomy-open gives a literal cap attachment, while holonomy-zero is a
determinantal degeneration.

## Replay

```sh
python3 computations/unaudited-codex-triangle-crossword-observation-2026-08-22/audit_triangle_crossword_observation.py --write-results
python3 -O computations/unaudited-codex-triangle-crossword-observation-2026-08-22/audit_triangle_crossword_observation.py
python3 -I -S computations/unaudited-codex-triangle-crossword-observation-2026-08-22/audit_triangle_crossword_observation.py
```

The hostile command

```sh
python3 computations/unaudited-codex-triangle-crossword-observation-2026-08-22/audit_triangle_crossword_observation.py --mutate-cramer-sign
```

must fail.  The standard result logical digest is recorded in
`results_triangle_crossword_observation.json`.
