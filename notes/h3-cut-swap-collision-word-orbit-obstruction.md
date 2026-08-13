# The cut-swap symmetry is a collision shadow, not the missing physical comparison

## Result

For the complete determinant-dark lower packet

\[
                         P_{024}-P_{012},
\]

there is a useful exact symmetry.  Let `rho=(1 4)` be the site
transposition.  On the fifteen physical `(matching,repeated-edge)` collision
labels, `rho` carries the nine labels of the `012` tangent cube bijectively
to the nine labels of the `024` cube.  If `u_012` is the unsigned nine-term
lower face, then

\[
                 u_{024}-u_{012}=(\rho-1)u_{012}.       \tag{1}
\]

The fifteen labels split into seven two-cycles and one fixed point.  Six of
the two-cycles support the twelve nonzero coefficients in (1).  The three
shared labels are one fixed point and one two-cycle.  Therefore a genuinely
`rho`-equivariant cutwise construction would satisfy all three overlap
coherences automatically.

Equation (1) is not yet a source construction.  The selected mixed word is
`001122`.  Its colour histogram on `012` is `(2,1,0)`, while on `024` it is
`(1,1,1)`.  A physical monomial symmetry of the GHZ target consists of a
site permutation and one common global colour permutation; it preserves the
unordered cut histogram.  Exhausting the full 48-element stabilizer of the
word finds no element mapping `012` to `024` or its complement.

The checker is
[`verify_h3_cut_swap_collision_word_orbit_obstruction.py`](../computations/verify_h3_cut_swap_collision_word_orbit_obstruction.py).

## The first exact obstruction

The bare transposition sends

```text
001122  ->  021102.
```

It must be repaired at sites `1` and `4`.  More generally, among every site
permutation/global-colour map carrying the unoriented cut `012|345` to
`024|135`, the minimum word distance is two.  Hence no alternative physical
relabeling avoids the same obstruction.

The two required repairs are local colour operations, not a common global
colour permutation.  Applied to a pure GHZ word, they make it mixed, so they
do not preserve the target.  Consequently neither `rho_*` nor a formal bar
symbol `[rho]` is the protected comparison `Phi`.  The smallest possible
source type is now precise:

> a two-local-root word-changing Cartan/Spencer attachment, or an equivalent
> relative mapping-cone cell, whose target defect cancels and whose image in
> the canonical repeated `P3+K2` grade is the literal equivariant `M_v`
> family.

This cell must realize the six anti-invariant collision pairs.  Once its
base image is source-provenant and equivariant, the one fixed and one paired
overlap orbits remove the three separate coherence choices.

This rules out a tempting shortcut but improves the construction target:
the input-side problem is not fifteen unrelated images.  It is one
two-root word-changing image plus equivariance.

## Relation to the literal output gate

The output remains the exact cell isolated by `9ab5fa1`/`e8838b7`.  For one
face, `M_v` must have

```text
literal boundary       sum_j alpha_j B_j       (360 terms),
Eq corners             alpha=(-1,+1,+1,-1),
ordinary residue       0,
D,W,target,ainc         0,
eta_z                  1+delta_(1,z) u_z/t,
sigma                  -q_pq^22.
```

The old two-chart and polynomial repeated modules do not contain this
direction.  The cut-swap result does not reverse that private-pivot theorem:
it classifies the source operation which must create the new direction.

There is a small positive anchor statement.  The collision packet lies in a
mixed word and the required `M_v` signature has `ainc=0`.  Thus the lower
correction transports physical anchor incidence by the zero law.  The known
four-corner alpha aggregate is also killed by the physical six-term
covector `sum_6 matching-ainc`.

That is not the same as proving that the completed determinant-dark
top-plus-lower kernel is seen by the physical pure/target anchor.  The latter
is an independent law only if the completed kernel is to feed the
constructive rectangular/active branch.

## Exact effect on the global proof

The roles of the comparison and the anchor/cap laws should be kept
separate.

### Rootless Component III

For the rootless terminal branch, a physical `Phi` on the complete relative
domains is enough.  Commit `7efd10d` gives the final dichotomy without a
separate `h_phys` hypothesis:

* a nonzero defect of `q=sum_6 matching-ainc` yields a physical kernel class
  on the source or canonical side and hence the normalized relative
  generator;
* a zero defect transports `q` modulo protected rows and gives the Fredholm
  alternative.

Therefore constructing the two-root/equivariant `M_v` family closes the
local rootless Component-III comparison.  A separate physical anchor
pairing is needed only to reroute the same determinant-dark lift through
the rectangular/active construction.

### All-inactive Component IV

The same base family is a candidate for the first face-open inactive cell,
but it does not close Component IV by itself.  The shared interface
`9b768fe` requires the comparison to identify two additional physical
readouts:

```text
-S_v        -> primitive pentagon anchor incidence,
derived Yw  -> physical inactive cap W.
```

On `D(h_v)`, the existing derived filler `(kappa/h_v)n_v` then supplies the
first invisible cap.  The complete order-one through order-three weighted
normal companions already exist, so a comparison natural in the normal
grade would extend the same base cell over those strata by triangular
subtraction.  That naturality is not yet proved.

The simultaneous face-zero/cyclotomic locus is still separate.  Its
chart-level Rees chain lifts to all orders, but the primitive physical
separator

\[
                       E+W+T-O
\]

reads one on the missing cap.  One must still map the completed chart-odd
class to physical `W`, then finish the horizontal and diagonal inactive
Rees routing.  Thus Component IV reintroduces an independent physical cap
law (and, in the collision presentation, its separate primitive anchor
cell); it is not a formal consequence of the rootless `q` dichotomy.

The dependency chain is therefore

```text
two-root/equivariant M_v construction
        |
        +-- rootless III: physical Phi -> q defect/generator or q transport/Fredholm
        |
        `-- inactive IV: derived Yw -> physical W
                         + normal-grade naturality
                         + cyclotomic completed comparison
                         + horizontal/diagonal inactive Rees routing
```

So a successful `M_v` construction closes only the local rootless gate
immediately.  It becomes the common first inactive comparison only after
the cap law is added; it does not eliminate the global inactive routing
theorem.

## Verification

```text
python3 computations/verify_h3_cut_swap_collision_word_orbit_obstruction.py
python3 -O computations/verify_h3_cut_swap_collision_word_orbit_obstruction.py
python3 -I -S computations/verify_h3_cut_swap_collision_word_orbit_obstruction.py
```

Frozen ledger SHA-256:

```text
e12adf64d6bee8595a059f4ad2fb3f5b7af6b6c532a86798d9d9db0f3069ac42
```
