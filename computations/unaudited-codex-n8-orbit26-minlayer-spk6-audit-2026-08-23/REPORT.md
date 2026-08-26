# Orbit-26 minimum layers and the SP-K6 interface

## Source-faithful minimum-layer theorem

For a literal mixed word `w`, let `S(w)` be the chart-support cells whose
endpoint colours agree with `w`.  Those cells are site-disjoint.  If

```text
d = 4 - |S(w)|,
```

then the minimum normalized off-support degree of its Hafnian is exactly
`d`, and its complete minimum layer is the monic Hafnian on the `2d` sites
not covered by `S(w)`.  This was checked directly for all 6,558 mixed words.

```text
d                    0     1      2      3     4
mixed words          2   358   2298   3058   842
minimum-layer terms  1     1      3     15   105
```

The term counts are `(2d-1)!!`; they are not merely a numerical pattern.
Every minimum monomial is the literal matching on the unmatched named sites
with the endpoint colours from `w`, and every coefficient is one.

## Linear contraction through degree nine

The 358 degree-one words cover all 240 normalized variables.  A variable
has one, two, or three linear providers with histogram

```text
1 provider: 130 variables
2 providers:102 variables
3 providers:  8 variables.
```

For a row of positive `y`-degree `k <= 9`, select one of its variables and
a monic linear provider.  The source multiplier has `y`-degree `k-1` and
`t`-degree `9-k`, hence total degree eight.  Its unique lowest output is the
selected row; every other output has strictly larger `y`-degree.  Distinct
rows therefore have distinct pivots and the degree ordering is acyclic.

The frozen deterministic provider packet was replayed exactly.  It is not
itself stabilizer-equivariant (64 of 960 covariance checks fail), but an
equivariant section exists after changing 16 of its 240 choices.  It has 66
variable-orbit generators.  Thus symmetry is available, but it is separate
from the deterministic contraction proof.

## First coupled `N4` exchange layer

At `y`-degree ten the linear multiplier would need negative `t`-degree, so
degree-two minima are first.  The 2,298 source words yield 2,206 distinct
three-term blocks on 6,618 quadratic monomials.  Every block is exactly the
three perfect matchings of a decorated `K4`; different unmultiplied blocks
share no quadratic node.  There are 2,114 single-source blocks and 92
double-source blocks.  Consequently the base incidence rank over `Q` is
2,206 and its node kernel has dimension 4,412.

Under the order-four fixed-chart stabilizer the blocks have:

```text
517 orbits of size 4, source multiplicity 1
 23 orbits of size 4, source multiplicity 2
 22 orbits of size 2, source multiplicity 1
  2 fixed blocks,       source multiplicity 1.
```

This block decomposition does not automatically survive multiplication by
balanced degree-eight monomials: translated outputs can coincide.  No
block-diagonal claim is made for the 63,603,821-row degree-ten residual.

## Why the `y11` page is not SP-K6

The certified theorem `SP-K6` assumes one literal common system

```text
H6(A) = Delta_(6,3)
```

for arbitrary endpoint-ordered `3 x 3` blocks: all 729 word coefficients,
all mixed coefficients zero, and three nonzero pure coefficients.

For the canonical degree-two word `00000102`, its three-term `N4` minimum is
followed by 24 degree-three terms.  Source provenance splits those terms into
two 12-term punctured six-site fibres.  The positive attachment is exact:
the missing three terms are the same labelled `N4` triple, from the same
source word and under the same arbitrary outer multiplier.  For either
chosen outer support edge, the 15 matchings containing it are precisely
`3+12`; the other 90 matchings avoid that edge.

Closing the fixed-edge packet through the lower `d=2,1,0` pages also reaches
all 729 residual colour words.  Thus there is no omitted residual word orbit.
The obstruction is the target character.  Fixing a diagonal support cell
fixes the two deleted endpoints to one colour `c`.  Exactly 728 residual
words give mixed eight-site equations.  The omitted word is the original
pure word `c^8`, so the induced six-site target is only
`e_c^tensor6`.  The other two residual constant words are globally mixed
and have target zero.  In addition, extracting the 15 containing-edge terms
from each literal equation still requires cancelling its 90 avoiding-edge
terms.

So `SP-K6` cannot be invoked directly at `y11`, even after the genuine
`12+3` completion.  The smallest valid bridge must combine three active
endpoint-colour contractions on one physical pair and cancel the avoiding-
edge contamination, producing three nonzero pure residual coefficients for
one common set of six-site blocks.  This is exactly the missing source-
faithful active-cap/clean extraction.

## Scope and reproduction

This audit does not contract the full 224,319-row degree-six residual or
solve the translated degree-ten core.  It proves the minimum-layer theorem,
the triangular range, the unmultiplied `N4` decomposition, and the precise
failure of the direct certified-six-site attachment.

```sh
python3 computations/unaudited-codex-n8-orbit26-minlayer-spk6-audit-2026-08-23/audit_minlayer_spk6_interface.py --check-results
python3 -O computations/unaudited-codex-n8-orbit26-minlayer-spk6-audit-2026-08-23/audit_minlayer_spk6_interface.py --check-results
python3 -I -S computations/unaudited-codex-n8-orbit26-minlayer-spk6-audit-2026-08-23/audit_minlayer_spk6_interface.py --check-results
```

Hostile mode `--mutate` must fail.  Logical SHA:
`c87d42520f287fc10fbdf16a697812f0676f0567e113af310bcccb9f6fa728b8`.
