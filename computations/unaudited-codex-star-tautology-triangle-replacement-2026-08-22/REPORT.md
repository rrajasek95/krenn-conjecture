# Star-carrier tautology and the canonical triangle replacement

Status: **UNAUDITED exact source-factorization PASS**.  On normalized full
`X5`, every one of the 168 star carriers is automatically blocked by at least
one diagonal form.  The star part of the 728-carrier bridge is therefore
retired.  A live full-tail cell selects, after symmetry, one canonical
triangle flag, but it does not make the surviving opposite-edge response
nonzero.  The smallest non-tautological incidence target consists of four
canonical triangle blocker branches.

## 1. The universal five-set functional

Fix

```text
cap pair {6,7}, star centre 0,
C={0,6,7}, W={1,2,3,4,5}.
```

For each `u in W`, let `h_u` be the four-site matching tensor on
`W\{u}`.  The certified six-site obstruction gives the exact dual theorem
recorded in
[`five-set-universal-cofactor-annihilator.md`](../../notes/five-set-universal-cofactor-annihilator.md):
there is a functional `beta in V_W^*` such that

```text
beta(V_u tensor h_u)=0 for every u in W,
b=delta_W(beta)!=0.                                    (1)
```

This is universal over arbitrary complex endpoint-ordered edge blocks; it
is not a generic or support statement.

Across the odd cut `C|W`, an eight-site matching crosses once or three
times.  There are 45 one-crossing and 60 three-crossing perfect matchings.
The one-crossing sector factors cofactor-by-cofactor through the five maps in
(1), so

```text
                              beta(T1)=0.                (2)
```

On normalized exact GHZ, (2) gives

```text
beta(T3)=sum_(c=0)^2 b_c e_c^0 tensor e_c^6 tensor e_c^7.
                                                               (3)
```

## 2. Literal three-crossing/response factorization

Let `K` be the cap-pair covector in the coordinate convention of the response
carrier.  For `a<b` in `W`, its literal response edge is

```text
R_ab(K)[alpha,beta]
 = sum_ij K_ij(
     A_6a[i,alpha] A_7b[j,beta]
    +A_6b[i,beta]  A_7a[j,alpha]).                      (4)
```

Define `Gamma_ab,beta: V_a tensor V_b -> V_0` by attaching a vector on
`ab`, joining site 0 to one of the other three sites of `W`, matching the
last two sites internally, restoring all named slots, and contracting the
result by `beta`.  Direct grouping of the 60 three-crossing matchings by the
two neighbours of sites 6 and 7 gives

```text
(id_V0 tensor beta)<K,T3>_(6,7)
       = sum_({a,b} subset W) Gamma_ab,beta(R_ab(K)).    (5)
```

Each of the ten response pairs receives six matching patterns: two endpoint
orientations for 6 and 7 and three choices for the neighbour of site 0.
The checker replays (5) with stored-edge transposition on all

```text
60 * 3^5 W-colourings * 3 site-0 colours * 3^2 K cells
  = 393,660
```

formal endpoint terms.  There are no sign, endpoint-order, or missing-pair
discrepancies.

## 3. Exact star tautology

For the star at 0, `L_(67,star0)` contains all nine cells on the ten residual
edges not incident with 0.  Those ten edges are exactly the pairs
`{a,b} subset W`.  Hence `K in ker L_(67,star0)` makes the right side of (5)
zero.  Contracting (3) by `K` gives

```text
                         b_c K_cc=0 for c=0,1,2.         (6)
```

At least one `b_c` is nonzero.  For such a colour, every `K` in the carrier
kernel has `K_cc=0`.  Finite-dimensional annihilator duality says precisely

```text
                         Kcc in rowspan L_(67,star0).    (7)
```

Thus the carrier is blocked by a diagonal form.  Site and colour transport
proves (7) for all

```text
28 cap pairs * 6 residual centres = 168 star carriers.
```

This uses normalized full `X5`, including the pure target coefficients.  It
does not hold on a mere `X4` truncation, so the six W40 star caps remain valid
positive controls.  They cannot occur on a hypothetical exact point.

Consequently, on normalized `X5`,

```text
all 728 star/triangle carriers blocked
             <=> all 560 triangle carriers blocked.     (8)
```

The fixed-star four-branch target in the earlier
[full-tail entry report](../unaudited-codex-full-tail-entry-incidence-2026-08-22/REPORT.md)
has been corrected and retired.

## 4. Why a triangle is non-tautological

Take the canonical triangle `S={0,1,2}` with cap pair `{6,7}`.  Its outside
matrix has 12 residual edges and 108 coordinate rows.  Among the ten pairs in
`W`, a triangle-kernel `K` kills nine; the opposite edge `{1,2}` is allowed.
Equation (5) therefore becomes the exact source identity

```text
sum_c b_c K_cc e_c^0
             = Gamma_12,beta(R_12(K))
               for K in ker L_(67,{0,1,2}).             (9)
```

The right side is not forced to vanish.  Repeating the construction with
each `x in {0,1,2}` gives three identities, whose surviving response edges
are respectively `12`, `02`, and `01`.  Thus the five-set theorem routes the
target through the three allowed triangle edges; it does not put a diagonal
blocker in the outside row space.

This is the smallest non-tautological linear carrier.  A response support on
at most three residual vertices is pairwise intersecting; after stars are
retired, the only remaining case is a triangle.  There are

```text
28 * C(6,3) = 560
```

such carriers.

## 5. Full-tail entry and the canonical triangle flag

Let `I5` be the normalized full-`X5` ideal and `J` the ideal of all 168
cross-colour cells.  The certified block-diagonal theorem gives

```text
                              I5+J=(1).                  (10)
```

Thus a hypothetical exact point has a live cross cell.  A labelled flag
consists of

1. an oriented choice of its endpoints `(a,p)` and ordered endpoint colours;
2. an auxiliary cap endpoint `q`;
3. two further residual sites `{y,z}` making triangle `{a,y,z}`.

There are

```text
8*7 ordered (a,p) * 6 choices q * C(5,2) * 6 colour orders
  = 20,160 flags.                                        (11)
```

They form one `S8 x S3` orbit.  Hence one may use

```text
y0=A_06[0,1]!=0,
cap pair {6,7}, triangle {0,1,2}.                        (12)
```

This is an orbit representative, not an intrinsic selection by the source.
Each stored live cross cell lies in 120 flags: two choices of which endpoint
is the triangle vertex, six auxiliary cap endpoints, and ten opposite
triangle pairs.  Under the hypothesis that **every** triangle is blocked one
may choose any such flag and transport it to (12).  Without that hypothesis,
the live cell alone selects none of them.

The role of `y0` is only to enter the chart.  Identity (9) does not contain
`y0` on its surviving opposite-edge side, and no exact source identity found
here makes `R_12(K)` nonzero.  Therefore full-tail entry does **not**
canonically activate the selected triangle.

If all triangle carriers are blocked, the canonical carrier has one of four
memberships

```text
K00, K11, K22, or <K,A_67> in rowspan L_triangle.        (13)
```

The four are inequivalent on the live-cell flag: a diagonal blocker colour
may equal the colour at `a`, the colour at `p`, or the third colour, and the
direct blocker is a fourth orbit.  Encoding one membership with 108 row-span
witnesses gives the smallest source-faithful exact branches:

```text
variables: 252 source + 108 witnesses + 1 inverse = 361,
equations: 6558 mixed + 3 pure + 9 membership + 1 inverse = 6571,
branches:  4.                                             (14)
```

The frozen manifest contains all 252 source labels, all 6,558 word labels,
the 108 outside-response labels, the stored-edge coefficient constructor,
the four right-hand sides, and the 108 witness labels.  Per branch it records
688,590 mixed matching occurrences, 315 pure matching occurrences, and 1,944
source-monomial occurrences in the membership matrix.

Unlike the star version, none of these branches is a consequence of the
five-set contraction: (9) retains the allowed response edge.  No solve was
launched.

## 6. First cancellation-clean wider carrier

The first response support that is not pairwise intersecting lives on four
residual vertices.  Fix a four-set `S`.  Requiring all response edges outside
`S` to vanish uses 9 edges, hence an `81 x 9` outside matrix.  On `S`, impose
the named-slot quadratic tensor identity

```text
R_01 R_23 + R_02 R_13 + R_03 R_12 = 0.                  (15)
```

Its 81 coordinate equations say `r^2=0`; `r^3=0` is automatic because the
support has only four vertices.  Together with the four activity forms, this
is a sufficient cancellation-clean cap.  There are

```text
28 * C(6,4) = 420                                       (16)
```

four-set carriers.  For the canonical `S={0,1,2,3}` and the cut used above,
the five-set factorization retains the three response edges `12,13,23`, so
this carrier is also non-tautological.  It is nonlinear and does not replace
the simpler triangle target (14); it is the first wider-support family to add
if all triangle branches persist.

## 7. Terminal verdict and replay

The corrected global carrier route is

```text
normalized X5
  -> full-tail entry by I5+J=(1)
  -> one canonical live-cell triangle flag by symmetry
  -> four exact triangle blocker branches (14),
```

not the fixed-star system.  The precise remaining lemma is to exclude those
four branches, or to construct an active triangle (and only then consider the
420 quadratic four-set carriers).  There is no remaining star-carrier work.

Replay:

```text
python3 computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/audit_star_tautology_triangle_replacement.py --write-results
python3 -O computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/audit_star_tautology_triangle_replacement.py
python3 -I -S computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/audit_star_tautology_triangle_replacement.py
```

The three modes are byte-identical.  Logical SHA-256:

```text
dddd7f28956aec4db547e8de163f4f4dbe5e6750c16a0f238a1efa5dc8d84a87
```

Artifacts:

- [`audit_star_tautology_triangle_replacement.py`](audit_star_tautology_triangle_replacement.py)
- [`results_star_tautology_triangle_replacement.json`](results_star_tautology_triangle_replacement.json)
- [`canonical_triangle_incidence_manifest.json`](canonical_triangle_incidence_manifest.json)
