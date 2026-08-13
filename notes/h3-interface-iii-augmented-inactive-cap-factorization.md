# The inactive cap is one augmented row of Interface III, not a fourth generator

## Exact conditional factorization

The final `Yw -> W` obligation is logically independent of the projected
root-even equations, but it does not require a fourth source-generator
construction once Interface III is formulated as the complete augmented
comparison.

Work in one normalized repeated `P3 disjoint K2` fine grade.  The existing
physical cap combination is

\[
 B=r_0-T
   =(\operatorname {ridge}=0,\operatorname {Eq}=1,
     Yw=1,W=1,\operatorname {ainc}=-1,
     \operatorname {tgt}=\operatorname {ores}=0).     \tag{1}
\]

Here `Eq=1` denotes the coefficient of the conormal
`(H_0-u)e_Eq`; the unnormalized differential statement is the pinned
identity

\[
                       d(r_0-T)=Yw+(H_0-u)e_{\rm Eq}.  \tag{2}
\]

The normalized-C5 base-column theorem proves that the exact missing repair
relative to (1) is

\[
 A_v=(-r_v,-e_{\rm Eq},Yw=0,W=0,
       \operatorname {ainc}=\operatorname {tgt}
       =\operatorname {ores}=0).                      \tag{3}
\]

Consequently, if the completed root-even Interface III theorem constructs
(3) source-validly in the same endpoint, word, chart and repeated fine
grade, then

\[
 \boxed{P_v=B+A_v
   =(-r_v,0,Yw=1,W=1,\operatorname {ainc}=-1,0,0).}   \tag{4}
\]

This is exactly the physical augmented base column required by the
normalized rootless/inactive interface.  The old cap supplies `W=1` and
anchor incidence `-1`; the new root-even cell repairs the ridge and Eq
coordinates and is required to have zero cap/anchor/target/residue output.
Thus no additional source generator is needed for `Yw -> W`.

Checker:
[`verify_h3_interface_iii_augmented_cap_factorization.py`](../computations/verify_h3_interface_iii_augmented_cap_factorization.py).

## Why the cap row must still be stated

Forgetting the `W` row loses information.  The checker gives two repairs

\[
                         A_v,\qquad A_v-W              \tag{5}
\]

with identical ridge, reduced-Eq, `Yw` boundary, anchor, target and residue
coordinates.  Adding (1) gives respectively

```text
good: (Yw,W)=(1,1),
bad:  (Yw,W)=(1,0).
```

Therefore no proof of the projected Interface III equations can infer the
physical cap comparison.  `W(A_v)=0`, equivalently `W(P_v)=1`, is an
independent augmented output-row condition.  The correct theorem-counting
statement is:

> `Yw -> W` is not a fourth source-generator theorem, but it is a
> load-bearing row of the one Interface III source theorem.

If Interface III is published only after projecting away `W`, the cap
comparison remains a fourth logical hypothesis.  Packaging it into the
complete augmented map removes that artificial extra interface without
weakening the physical typing.

## C5 propagation

The five columns (4) satisfy

\[
                         P_v-P_{v+1}=E_v,              \tag{6}

\]

where `E_v` is the clean collision edge with zero `Eq/W/ainc/target/ores`
readout.  The edge lattice has saturated rank four, and one `P_v` raises it
to rank five.  Hence a single augmented Interface III base column
propagates around the entire normalized pentagon.  Its final consistency
condition is exactly `sum_v E_v=0`.

The primitive `W` covector still kills every edge and reads one on `P_v`.
This older separator proves that the edge family cannot manufacture the
base; it does not prove that the cap row needs a generator distinct from
the root-even repair plus the already existing chain (1).

## Normal jets

The same factorization persists through normal orders one, two and three.
The existing cap family has identical coefficientwise convolutions

\[
 \sum_{i=0}^k h_iYw[k-i],\qquad
 \sum_{i=0}^k h_iW[k-i].                              \tag{7}

\]

A Rees-linear Interface III repair has zero in both rows, so adding it
preserves their equality grade by grade.  The committed collision/reduced-
Eq family already prolongs functorially and creates no new `W`, target,
residue or anchor type.  Thus orders two and three introduce no new cap
generator theorem; they only require the seed Interface III comparison to
be genuinely Rees-linear and augmented.

This also sharpens the shared rootless/inactive interface: the derived
filler supplies `Yw`, while (1) is its canonical physical cap section.
The hard construction is the same-grade root-even ridge/Eq repair that
makes this section compatible with the physical base column.

## What Interface III must now say

The raw target-bearing signless cell `C_plus` is not yet (3).  The final
Interface III theorem must first combine it with its diagonal target
correction, reduced-Eq face, labelled ordinary-residue section, and
root/anchor comparison.  Its exact inactive output should then be stated in
either equivalent form:

1. construct the repair `A_v` of (3), including the zero `W` row, and add
   the existing `r_0-T`; or
2. construct `P_v` directly and prove the single augmented equality
   `Yw(P_v)=W(P_v)=1` together with the remaining rows in (4).

The first form makes the factorization transparent.  The second is shorter
in the final three-interface proof map.

This result does not construct the root-even comparison, its labelled
residue correction, or the separate `beta=0` protected membership.  It
only proves that a completed source-valid Interface III absorbs the inactive
cap obligation exactly, and that omitting its `W` row would be unsound.

## Verification

Run:

```text
python3 computations/verify_h3_interface_iii_augmented_cap_factorization.py
python3 -O computations/verify_h3_interface_iii_augmented_cap_factorization.py
python3 -I -S computations/verify_h3_interface_iii_augmented_cap_factorization.py
```

Frozen ledger SHA-256:

```text
bcfa7eb71274c5a1601858b414b89eb2ddd2a83068910c2ee8b11ece3cdc69ae
```
