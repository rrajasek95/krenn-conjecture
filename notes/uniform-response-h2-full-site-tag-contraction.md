# Every response-H2 direction tag contracts under full site symmetry

## Uniform theorem

At response order `h`, expose the two response endpoints `P,S` and keep the
`2h` residual sites.  The standard block variables are exactly the edge
variables of the complete graph on these `2h+2` sites:

```text
d = PS,       p_i = Pi,       s_i = Si,       q_ij = ij.
```

Consequently the complete response polynomial is an ordinary hafnian on
`2h+2` sites.  A compatible second-Hasse direction is a two-edge matching
on a four-set.  Each four-set has three such matchings, while its complement
has `(2h-3)!!` perfect matchings.  Its direction-pair/lower-tail incidence
component is therefore

\[
                         K_{3,(2h-3)!!}.              \tag{1}
\]

The centered direction-tag space has dimension two per four-set.  The `S4`
stabilizer of the four-set acts transitively on its three perfect matchings;
indeed a transposition sends any chosen matching to either other matching.
Thus both centered differences vanish in coinvariants.  Over characteristic
zero, coinvariants for a finite group are exact, so

\[
 \boxed{\text{the full-site centered H2 tag module has zero coinvariants}}
                                                               \tag{2}
\]

for every `h >= 2`.

Checker:
[`verify_uniform_response_h2_full_site_tag_contraction.py`](../computations/verify_uniform_response_h2_full_site_tag_contraction.py).

The checker exhausts literal components, tails, incidences, local
transpositions, and full-site direction-pair orbits for `h=2,...,6`.  It
also imports and re-runs the exact `h=3` rank calculation.  The all-order
proof is the preceding four-set argument, not an extrapolation from these
finite audits.

## Relation to the fixed-response C4 survivor

If `P,S` are frozen, the available subgroup preserves the operation types
`DQ` and `PS`.  At `h=3` this leaves the apparent invariant

\[
                    2e_{DQ}-e_{PS,1}-e_{PS,2}.        \tag{3}
\]

Changing which physical sites are exposed as response endpoints mixes
these operation types.  One endpoint--residual transposition already raises
the action rank from `139` to the full `140`; (3) is therefore not a
full-site invariant.  Formula (2) is the uniform explanation.

## Exact physical boundary

The coefficient theorem does not by itself provide the required chain
map.  The exact `h=3` chart audit
[`d1b8ec4`](h3-h2-full-site-chart-swap-pointed-scalar-guard.md) sharpens
this caveat.  A physical endpoint--residual transposition is a target-safe
source-algebra isomorphism between two response-chart objects, not a
boundary in one fixed pointed source.  Raw folding changes the fixed-source
quotient; retained-label transport has zero boundary.  Its first proper
face is exactly

\[
 L_{01}=(2Dq_{01}-p_0s_1-p_1s_0)
        (q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}),
\]

the nine-term target-zero centered scalar isolated in `0d14815`.

Thus, to use (2), the principal-parts comparison must be

- defined termwise on the literal direction pair;
- source-valid in every response chart;
- natural when the two exposed endpoint sites change; and
- compatible with word, fine, repeated, protected, target, `q`, `W`, and
  ridge readouts.

Under that hypothesis the action-groupoid bar contracts every H2 direction
tag at every order.  Without it, folding response charts is exactly the
unproved physical comparison in different language.  At order three the
first missing comparison is no longer anonymous: it is the pointed chart
cylinder carrying `L01` with its literal word/fine/direction grade.  The
theorem removes an independent invariant-C4 generator; it does not construct
this proper face.

At `h=3`, the endpoint-even word-`0102` carrier appears only after the lower
restriction and is not part of the original direction-tag module.  It
remains the first concrete downstream landing test.  Uniformly, analogous
word-grade proper faces—not H2 tag coinvariants—are where further work must
now concentrate.

The checker runs normally, optimized, and isolated/no-site.  Its frozen
ledger digest is
`6c4a8cd9a0d1eec597ed716b5e91bd9c24a3128512be97275eef9f05facdd3b7`.
