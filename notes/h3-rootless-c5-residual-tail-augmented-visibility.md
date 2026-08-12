# A response-dark C5 tail is deletable or exports an active carrier

## The source-level dichotomy

Work at a synchronized minimum-support representative of the six-site
one-bad packet

\[
 q^{[3]}=X_0,qquad
 p_i s_jq^{[2]}=\delta_{ij}X_i
 \quad(i,j\in\{1,2\}),                                \tag{1}
\]

on the target-preserving normalized C5 chart.  Every monomial in a nonzero
residual difference \(R_v-R_w\) contains at least one nonzero off-cycle
decorated chord cell

\[
                         e=q_{ab}^{m_am_b}.             \tag{2}
\]

Form its complete five-tensor coordinate column

\[
 C_e=\left(D_eq^{[3]},
       D_e(p_i s_jq^{[2]})_{i,j=1,2}\right).           \tag{3}
\]

Hafnian matching polynomials are affine in one physical cell: a perfect
matching cannot use (2) twice.  Consequently setting its coefficient to
zero has the exact finite effect

\[
 F(q-q_e e,p,s)=F(q,p,s)-q_eC_e,                      \tag{4}
\]

with no quadratic or higher correction.

If \(C_e=0\), equation (4) deletes (2) while preserving all five tensors.
This deletion is mutual-anchor safe.  At each endpoint of the chord, the
selected C5 retains its two incident nonzero \(m\)-decorated cycle cells;
removing the chord cannot destroy a degree-one coordinate anchor.  It also
does not change the selected C5 itself.  Minimum support therefore excludes
\(C_e=0\).

Thus every nonzero residual tail exports a nonzero complete physical
column.  There are two exhaustive cases.

1. If the unary component of (3) is nonzero, one literal top matching uses
   the chord.  Its four-site complement consists of \(x\) and three odd
   sites, so every completion contains an external spoke \(q_{xr}\).  A
   spoke with decoration \(0m_r\) is the desired full-word accessibility
   occurrence; every other decoration is a translated/off-axis active
   carrier.  Since (2) has a nonzero colour, its top row is a zero-target
   coefficient and its cancellation mate is source-forced.

2. If a response component is nonzero, some literal oriented endpoint
   product, remaining q-edge, and chord product are nonzero.  When the
   remaining q-edge is the other edge of the original tail, the two holes
   are exactly \((x,v)\), so this is the response-hole input of `8771755`.
   Otherwise it is an alternate active hole/tail.  If its output is mixed,
   the zero row source-forces a mate and enters the same alternatives:
   source unit, same-tail one-sided deletion/Fitting minor, or different-tail
   C4 off-anchor/Hall routing.  A pure diagonal output is already a bright
   response carrier and needs no zero-row cancellation claim.

Therefore a nonzero \(R_v-R_w\) cannot remain a *bare* response-dark
internal class at a minimum-support full five-row source.  It is either
deleted or exported to a literal active unary/response carrier.

## Exact incidence audit

The ten residual occurrences split into five with one off-cycle chord and
five with two, giving fifteen chord occurrences.  For every occurrence:

* deleting one chord leaves four sites and exactly three top completions;
  all three contain an \(x\)-spoke;
* the response derivative has six choices for its remaining q-edge and
  hence six ordered-hole complements; and
* choosing the other edge of the original tail leaves the unique holes
  \((x,v)\).

The complete totals are

```text
15 chord occurrences
45 unary top completions
90 response q-edge/hole completions
15 original-tail forced-hole completions.
```

This uses literal matching and output-word provenance, not a bare-tail
quotient or support enumeration.

## Endpoint affine fibres

The result does not assert that the first active response component is
already a coordinate target-line point.  Fixing the opposite two endpoint
rows gives the exact affine map

\[
 L_s(k)=(ks_1q^{[2]},ks_2q^{[2]}).                    \tag{5}
\]

A one-star change in \(\ker L_s\) is a finite exact source modification;
there is no same-star second-order term.  The established affine theorem
then gives the sharp continuation:

* a zero/dependent complete column yields a support-reducing one-star move;
* a target-line point gives literal concentration;
* otherwise minimum support leaves the unique quotient circuit;
* a free nonzero circuit minor is the Fitting/active carrier, while an
  anchor-contained circuit is the star/triangle/\(K_{2,2}\) Hall gate.

The last rank promotion is not proved here.  In particular, a Fitting
carrier is not silently called four-good.

## Relation to the marked-unary guard

The five silent reset-word SCCs of `f3e4b01` do not falsify this theorem.
Their specialization sets the desired and translated \(0m\) spokes to
zero but retains the five marked \(q_{xv}^{00}\) spokes.  Those are literal
unary carriers in case 1 above.  The SCC theorem proves only that repeated
q-only re-pivoting does not change the reset word; it does not make the
complete augmented chord column vanish.

Thus the smallest surviving branch is no longer “nonzero residual tail
with every source attachment dark.”  It is an exported translated/top or
response carrier whose affine/Fitting/Hall rank landing is still open.

## Scope

This is an exact h=3 source theorem for (1), conditional on the upstream
minimum-support normalization.  It proves the requested
deletion-or-active-carrier alternative, not the final target-line hit,
four-good landing, or global termination.  It gives no Krenn
counterexample and constructs no new source point.

Run:

```text
python3 computations/verify_h3_rootless_c5_residual_tail_augmented_visibility.py
python3 -O computations/verify_h3_rootless_c5_residual_tail_augmented_visibility.py
python3 -I -S computations/verify_h3_rootless_c5_residual_tail_augmented_visibility.py
```

Frozen ledger SHA-256:

```text
85d75d8d4473ac94433228d17c8304ab3f18ad913561ade12beb025d84edea71
```
