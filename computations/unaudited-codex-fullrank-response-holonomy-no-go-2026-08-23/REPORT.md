# Full-rank response transition holonomy is a coordinate tautology

Status: **UNAUDITED exact negative theorem and source-labelled counterguard**.
This falsifies the proposed fixed-cap transition mechanism at the stated
data level.  It does not rule out a theorem that also uses pure
normalization or compares genuinely different cap pairs.

## 1. Literal response-edge charts

Fix cap pair `67`.  For a residual edge `ab`, let

```text
R_ab : Mat_3 -> Mat_3,
R_ab(K)_(alpha,beta)
 = sum_(i,j) K_ij (
     A_6a[i,alpha] A_7b[j,beta]
     + A_6b[i,beta] A_7a[j,alpha]).                    (1)
```

This is the endpoint-ordered response formula from the carrier theorem.
Each `R_ab` is a `9x9` matrix of source degree two.  On the principal open

```text
delta_ab=det(R_ab) != 0                                 (2)
```

write `K_ab` for a copy of `Mat_3` in response coordinates
`y_ab=R_ab k`.  There is only one canonical transition compatible with the
same physical cap covector `k`:

```text
tau_(f<-e) = R_f R_e^(-1)
           = N_fe/delta_e,
N_fe       = R_f adj(R_e).                              (3)
```

Thus these apparent `K`-spaces are six coordinate charts on one fixed
nine-dimensional vector space.  They are not independently supplied
fibres.

For a tetrahedron face with response-edge charts `u,v,w`, the smallest
cleared nonlinear face defect is

```text
D_uvw = N_uw N_wv N_vu
        - delta_u delta_v delta_w I_9.                  (4)
```

It has source degree `54`.  But

```text
adj(R)R=R adj(R)=det(R)I
```

reduces (4) to zero **as a polynomial identity**, before imposing a single
`X5` row.  The checker verifies all `4*81=324` entries for the four faces
`012,013,023,123` of the residual tetrahedron `0123`.

This is not the frozen universal linear cyclic audit: (3)--(4) are the
nonlinear rational transitions and their cleared composition.  The exact
outcome is that their nonlinearity is only Cramer's rule.

## 2. Literal full-X5 cross-word decoration

For a fixed residual word `o` on sites `0,...,5`, assemble the nine literal
amplitude rows into the cap-word matrix

```text
E_o[i,j] = F_(o,i,j).                                   (5)
```

The audit uses the two source-labelled packets

```text
o=001122, 012012,
```

namely 18 full words.  Their profile census is exactly

```text
12 profile 3+3+2 rows,  6 profile 4+2+2 rows.           (6)
```

The first twelve are the genuine offcount-five shell absent from `X4`.
In response coordinates the contracted row is

```text
ell_(o,e)(y_e)=vec(E_o)^T R_e^(-1)y_e.                  (7)
```

Transporting (7) through (3) gives the cleared degree-38 identity

```text
vec(E_o)^T adj(R_f) R_f adj(R_e)
 - delta_f vec(E_o)^T adj(R_e)=0.                       (8)
```

Again (8) holds for **every** matrix `E_o`; the checker tests a nonzero
formal `E` so this is not an artefact of specializing `F_w=0`.  Consequently
the literal full-X5 equations `E_o=0` do not create curvature.  They merely
say that a zero covector remains zero under a coordinate change.

## 3. Exact counterguard

Keep only the twelve cap-star blocks

```text
A_6a, A_7a,  0<=a<=5,                                  (9)
```

at the deterministic integral values frozen by the checker; set every
residual-residual block and `A_67` to zero.  The source digest is

```text
8b239185dede0a19fb44ea4f2912c776ad88a75db1ad987025adaab06a3dceab.
```

All six tetrahedron response maps are invertible.  Their exact determinants
are recorded in the result file; in particular every face carrier has a
displayed rank-nine response-edge minor (`012:R_03`, `013:R_02`,
`023:R_01`, `123:R_01`).

Every eight-site perfect matching uses the two cap stars and then leaves
four residual vertices, while (9) has no residual-residual edge.  Hence all
`6,561` top amplitudes are zero.  In particular every homogeneous mixed
`X5` row, including all 18 rows in (6), holds literally.

Nevertheless the source is not simultaneously channel-diagonalizable even
under the full local `GL_3` gauge.  For an even cycle `(a,b,c,d)`, put

```text
H_abcd=A_ad^(-T) A_cd^T A_bc^(-1) A_ab^T.              (10)
```

It transforms by conjugation at `a`.  Simultaneously diagonal edge blocks
would therefore make all such transports based at `a` commute.  At (9),

```text
rank [H_6071,H_6072] = 3,
([H_6071,H_6072])_00
 = -58646232810472348347 / 28119185468076386398.        (11)
```

Thus full response rank plus the literal mixed cross-word equations used by
the transition construction does not force a simultaneous channel gauge.
The guard is deliberately outside normalized `X5`: its three pure
amplitudes are `(0,0,0)`, not `(1,1,1)`.  It therefore does not refute the
eight-site conjecture; it proves that pure normalization or some other
source coupling is load-bearing.

The reverse half of the suggested dichotomy is also not a formal rank
statement.  Vanishing of one selected `delta_ab` need not lower the full
`108x9` carrier rank, and carrier rank drop does not put all four blockers
outside its row span.  The frozen W40 tetrahedron controls exhibit the latter
phenomenon at `X4`: all four canonical face carriers have rank three and are
still blocked.  Full `X5` may exclude that control, but the implication
requires additional equations.

## 4. Precise surviving target

The fixed-cap full-rank holonomy theorem is retired: all of its face defects
are universal adjugate identities.  A non-tautological transition must have
at least one of the following extra inputs:

1. a source-labelled comparison between **different cap pairs or different
   quotient spaces**, so the maps do not telescope through one common `k`;
2. a normalized pure-row term whose transport is not functorial under (3);
3. a nonlinear matching identity that couples two distinct residual words
   before setting each `E_o` separately to zero.

Merely adding more fixed-cap response edges or more zero mixed rows cannot
produce such a defect.

## 5. Replay

```sh
python3 computations/unaudited-codex-fullrank-response-holonomy-no-go-2026-08-23/audit_fullrank_response_holonomy.py --check-results
python3 -O computations/unaudited-codex-fullrank-response-holonomy-no-go-2026-08-23/audit_fullrank_response_holonomy.py --check-results
python3 -I -S computations/unaudited-codex-fullrank-response-holonomy-no-go-2026-08-23/audit_fullrank_response_holonomy.py --check-results
```

All three modes are byte-identical.  The hostile
`--mutate-crossed-orientation` replay fails.  Logical SHA-256:

```text
697612e1aa1b6643aff255adbad45de083d5651fed4f3236be1ad2d609bac113
```
