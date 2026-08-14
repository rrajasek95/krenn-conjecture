# Actual-source primitive terminal reduction at `Gamma_*`

## Outcome

There is a positive finite reduction at the **boundary-image** level and a
sharp obstruction at the **source-cell** level.

Let (Y_{\Gamma_*}) be the pinned 127-row protected output and let (D) be
the image of the 138 literal local protected columns.  Exact elimination gives

\[
 \dim Y_{\Gamma_*}=127,\qquad \operatorname{rank}D=126,
 \qquad D=\ker\omega_{\rm Eq},
\]

where

\[
 \omega_{\rm Eq}=\frac1{12}\delta\cdot(B-\mathrm{Eq}).
\]

For the Eq-only balanced vector (e_{\rm Eq}),

\[
 \omega_{\rm Eq}(e_{\rm Eq})=-1,
 \qquad \operatorname{rank}(D,e_{\rm Eq})=127.
\]

Therefore every possible physical boundary column (y) in this exact
codomain has the universal decomposition

\[
 \boxed{y=d-\omega_{\rm Eq}(y)e_{\rm Eq},\qquad d\in D.}       \tag{1}
\]

The checker replays (1) on all 127 coordinate basis vectors.  Thus the 13,601
declared dark generator occurrences plus one nonzero Eq orbit are already
exhaustive for **boundary columns**.  No second protected obstruction line is
possible.

Executable certificate:
[`verify_h3_actual_source_primitive_terminal_reduction_gate.py`](../computations/verify_h3_actual_source_primitive_terminal_reduction_gate.py).

## What the actual source presents

The official `EqSystemN 8 3` presentation has 252 weight variables, 6,561
relation cells, and 105 perfect-matching monomials in every relation.  It
records only the eight-site word and polynomial degree.  It does not record
operation parent, fine occurrence, repeated shape, selected window, or
`AugP2` face type.  In particular, it has no source-defined
`Hom(response,cap)` primitive sort.

After the six external `Gamma_*` fine monomials are supplied, the coefficient
Macaulay part is genuinely finite: every squarefree cubic has eight
divisor/complement pairs, giving 48 slots with degree histogram
`6,18,18,6`.  This exhausts coefficient multiples.  It does not enumerate
enriched operation primitives, because those labels are absent from
`EqSystem`.

The current callable enriched registry contains 128 constructors:

```text
literal Gamma entries       25
Gamma image rank            23
B/Eq image rank              7
nonzero omega_Eq charges     0
operation-changing atoms     0
Hom^1(response,cap)          0.
```

This registry passes the terminal charge test but is explicitly not an
exhaustive model of the physical off-diagonal source.

## Why the direct official Macaulay/jet bypass stops

One can enumerate every native fixed-grade monomial differential pattern.
For the six squarefree cubic fine monomials this is exactly the same 48
divisor/complement list.  This yields a finite official coefficient jet
matrix.

It does **not** yield (J_{\mathrm{phys},\Gamma_*}).  The official rows know
the colour word and polynomial exponent data, but not

```text
B versus reduced Eq occurrence;
response versus cap operation parent;
P3+K2 repeated type;
fixed window or root path;
target/q/anchor/W/ores/ridge/eta/sigma augmentation.
```

In particular, \(\omega_{\rm Eq}\) is not a functional on the official jet
row space.  It reads a derived private-minus-Eq augmentation which that matrix
does not contain.

The checker freezes a finite two-completion guard.  Take the complete
48-dimensional native jet matrix.  One augmented completion gives every
native column charge zero.  A second has the identical 48-row restriction
and one extra kernel-of-forgetting column of charge one.  The official
matrices are identical, while the augmented ranks differ by one.  Therefore
no direct left-null certificate computed only from the official EqSystem jet
matrix can decide the physical terminal.

The minimal repair is `GammaJetEnrichment`:

1. an operation/fine/repeated/window-labelled fixed-grade jet domain;
2. a chain- and augmentation-preserving map into the pinned 127-row
   \(Y_{\Gamma_*}\); and
3. completeness for physical primitives killed by forgetting back to the
   official EqSystem.

After this enrichment the matrix is still finite, and the one-dimensional
quotient theorem reduces its full audit to the scalar tests (2).  This is the
same finite datum as `GammaPrimitiveCompleteness`, expressed as a direct
Macaulay/jet map rather than a hand-chosen cellular grammar.

## The single underived Eq orbit

The complete Hasse/Koszul audit produces one transported candidate orbit

\[
 h_v(H_0-u)e_{\rm Eq}
\]

over five deleted sites and three matchings.  Its initial universal
direct-free residual has 273 monomial terms; at the (q)-zero top it becomes
((H_0-u)e_{\rm Eq}).  Target and ordinary residue are already zero.

This is a single orbit with 15 labelled representatives, but two required
facts remain unconstructed:

1. an underived physical source cell whose differential contains this orbit;
2. a protected operation-labelled projection carrying it to a nonzero scalar
   multiple of `balanced_top(Eq)` modulo (D).

The derived cube cancels the commutator with its Boolean companions.  It does
not provide either missing fact.

## Minimal finite hypothesis

Full source-cell factorization through all 13,601 declared presentation
generators is stronger than the Fredholm argument needs.  The minimal API
contract is:

> `GammaPrimitiveCompleteness`: enumerate every indecomposable physical
> relative-(C^1) generator at `Gamma_*`; retain word, fine, repeated,
> operation, root and window tags; and emit its differential in the common
> 127-row protected codomain.  The physical degree-one domain is the
> semi-free cellular closure of this finite registry.

Given this contract, promotion is a finite calculation.  For every registry
entry (g), compute

\[
 \lambda_g=\omega_{\rm Eq}(dg).                         \tag{2}
\]

- If every (lambda_g=0), then every boundary lies in (D), the normalized
  dual annihilates the exhaustive physical map, and its value one on the
  literal balanced-private RHS gives the Fredholm terminal.
- If one (lambda_g\ne0), then (dg) spans the unique quotient line.  It is
  the physical Eq-orbit/filler candidate; no further rank search is needed.

Primitive checks suffice because a semi-free degree-one word contains one
degree-one indecomposable, while all coefficient complements at this fixed
fine grade are among the 48 Macaulay slots.

## Sharp counterguard

Even after naming the underived Eq orbit, the official source data do not
prove source-cell generation.  Two enriched completions can have the same
official `EqSystem`, the same coefficient/Macaulay rows, the same 128 callable
constructors, and the same Eq candidate orbit:

```text
completion A source quotient basis    E_underived
completion B source quotient basis    E_underived, z_exotic
source quotient ranks                 1, 2
protected boundary quotient ranks     1, 1.
```

The extra primitive has zero official-source/callable shadow.  Its protected
boundary cannot make a second obstruction, by (1); it is congruent to a scalar
multiple of the Eq orbit.  This refutes cell-level essential surjectivity from
the current data without manufacturing a second terminal direction.

The extra primitive is a presentation countermodel, not a physical GHZ cell.
The exact unresolved physical statement is simply whether a complete
`Gen_phys(Gamma_*)` registry has any nonzero charge (2).
