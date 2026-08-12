# The normalized clean C5 leaves exactly one augmented comparison column

## Exact conclusion

On the target-preserving slice of `7c6d431`, impose the exact C5
specialization

\[
                         R_1=\cdots=R_5=0.
\]

Then every face coefficient is \(h_v=1\). The five physical
principal-parts collision edges are source-valid and have

\[
 dE_v=-r_v+r_{v+1},\qquad
 (W,\operatorname{ainc},\operatorname{tgt},
       \operatorname{ores})(E_v)=(0,0,0,0).            \tag{1}
\]

They form the saturated oriented incidence lattice of \(C_5\): their rank
is four, their sum is zero, and a four-by-four minor is a unit. Thus the
reduced pure-Eq collision correction which was missing before normalization
is no longer needed on this specialization.

The derived fillers of `0373033` now have

\[
 d n_v=Yw,\qquad
 (\operatorname{tgt},\operatorname{ores})(n_v)=(0,0),
 \qquad \operatorname{chart}(n_v)=-S_v,                \tag{2}
\]

with marked chart value \(-1\). Equations (1)--(2) expose one exact
remaining datum: a physical augmented comparison image \(p_v\) with

\[
 p_v=(-r_v,\ W=1,\ \operatorname{ainc}=-1,
                \operatorname{tgt}=0,\operatorname{ores}=0)           \tag{3}
\]

in the same endpoint/midpoint fine grade. Formula (3) is a required typed
signature, not a declaration that the formal chart label \(-S_v\) already
is physical anchor incidence.

One such column is necessary and sufficient for the whole pentagon. With
the orientation of (1),

\[
                         p_v-p_{v+1}=E_v,               \tag{4}
\]

so one base column propagates around the cycle; its final consistency is
exactly \(\sum_vE_v=0\). Conversely every clean edge has \(W=0\), while
the base column has \(W=1\). The primitive covector selecting the \(W\)
row kills the full collision-edge lattice and detects (3). Therefore no
combination of the normalized collision edges constructs the base column.

The target-preserving étale gauge removes the Eq defect but does **not**
identify derived \(Yw\) with physical \(W\). It descends a comparison once
one is constructed; it does not create that comparison.

## Fredholm status

Fredholm cannot yet be invoked: without one physical column (3), the five
augmented polar classes \(P(e_v)\) are not defined in a common physical
cokernel.

Once one source-valid column (3) is constructed, (4) defines the other four
and the alternative of `0373033` applies immediately:

* if physical anchor incidence kills the correction kernel, the five-column
  polar map is zero-indeterminate and Fredholm gives the generator or the
  annihilator;
* if it does not, a normalized kernel element is already the primitive
  relative anchor generator.

Accordingly, on this exact specialization the primitive anchor is not an
additional input needed before invoking the alternative. It is one possible
output. If one insists instead on directly completing the positive
pentagon mapping cone, the primitive anchor column isolated by `2304c4a`
is of course still required.

This is the sharp change from the general chart. There the extra
\(R_v-R_w\) companions must first be cancelled. Here they vanish, so the
sole remaining construction gate is the one-column physical comparison

\[
        (Yw,-S_v,-1,0,0)
          \longmapsto (W,-r_v,-1,0,0),                 \tag{5}
\]

preserving source boundary, target, ordinary residue, fine grade, and
physical anchor incidence.

## Scope

The statement is confined to the selected nonzero C5 torus after the exact
specialization \(R_v=0\). It neither covers the general residual-tail chart
nor constructs (3). In particular it does not formally rename chart
\(-S_v\) as physical `ainc`.

Run:

```text
python3 computations/verify_h3_rootless_normalized_c5_augmented_comparison_gate.py
python3 -O computations/verify_h3_rootless_normalized_c5_augmented_comparison_gate.py
python3 -I -S computations/verify_h3_rootless_normalized_c5_augmented_comparison_gate.py
```

The checker pins `7c6d431`, `2304c4a`, and `0373033`; reconstructs the
saturated collision lattice; verifies (4), one-column propagation, all
augmented zeros, and the primitive \(W\) separator; and records the exact
Fredholm dependency.

Frozen ledger SHA-256:

```text
2aa83dd425550fbcd632d0f1c18063ba3e940e0904517e3344fe0a80be469ad2
```
