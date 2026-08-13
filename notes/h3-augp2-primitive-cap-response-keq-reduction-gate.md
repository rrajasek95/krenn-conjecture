# After `K_Eq`, primitive `p` is exactly one scalar-residue landing

## Verdict

Grant the pointed occurrence family, its centered complete-response gauge,
the physical invisible `K_Eq` lift, and the pure `d_even` section.  These do
**not** by themselves construct the primitive cap.  The reason is one exact
row, not another large occurrence obstruction.

For the selected even deletion-face aggregate

\[
                         y={e_3+e_5\over2},
\]

the primitive cap and invisible lift are

\[
 p_y=(-y,-\operatorname {ores}_{\rm cap}),\qquad
 n_y=(+y,0).
\]

Consequently

\[
 \boxed{z_{\rm cap}:=p_y+n_y=(0,-\operatorname {ores}_{\rm cap}),
        \qquad p_y=z_{\rm cap}-n_y.}                 \tag{1}
\]

Thus `K_Eq` removes the entire `Q` part of the construction.  The shortest
remaining primal theorem is one pure scalar ordinary-residue landing in
word `01211222`, fine degree `t q_(v,N)`, and repeated grade `P3+K2`.  Since
a coarse physical `d_ores` column already exists, this can equivalently be
formulated as one relative word/grade placement

\[
             d s_{\rm cap}=z_{\rm cap}-d_{\rm ores}^{\rm coarse}. \tag{2}
\]

Equation (2), followed by (1), constructs the aggregate primitive cap.  No
new `Q`-bearing cap generator is needed after the physical `K_Eq` lift.

Checker:
[`verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py`](../computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py).

## Why the centered response gauge does not already give (2)

The response-gauge identity used in the labelled `P2` repair is

\[
                       z\longmapsto z+{k\over8}{\bf1}_{12}.
\]

Here `z` is the coefficient of an **already granted same-labelled
`p_Q/p_ores` family**.  The change creates a complete-response `Q` row and,
through that granted family, a scalar-residue cost.  If `p` is absent, the
independent complete-response column has zero cap ordinary residue.  Using
the gauge to construct `p` would therefore be circular.

The other new faces do not help:

- `P_f=d(u_f-u)` is a pointed conormal and has zero cap residue;
- `n_y` and the `K_Eq` core have zero cap residue;
- `d_even=(B_1+B_4)/2` is a **labelled** residue row, independent of the
  scalar cap-residue row; and
- the committed aggregate `d_ores` is coarse.  No existing map places it in
  the cap word/fine/repeated summand.

In the direct-sum quotient retaining these row labels, scalar cap residue
annihilates every available column and reads `-1` on `p_y`.  Adjoining (2)
raises the old span by exactly one and then makes `p_y` a boundary via (1).

## Minimal cap/Tor source cell

The degree-four Hasse reset and the endpoint projector agree with this
reduction.  The reset produces the invisible transgression `n_y` only after
physical `K_Eq` descent; its five standard face differences are already
removed by the physical `C5` Cartan orbit.  What survives is not another
denominator syzygy but the one base-augmentation coordinate (1).

The minimal positive object can be stated in either equivalent way:

1. a source-valid pure `z_cap` cell, target/protected/anchor/terminal zero;
   or
2. the relative placement cell (2), transporting the already physical
   coarse scalar residue into the literal cap component.

It must preserve the full word, chart, fine and repeated grade.  Polynomial
multiplication does not supply this because it does not change a source word
idempotent.

## The dual alternative

Before (2), the primitive local covector is simply

\[
                 \epsilon_{\rm ores}^{\rm cap}
                 (z_{\rm cap})=-1.                    \tag{3}
\]

It kills `P_f`, the complete-response gauge, `n_y`, `K_Eq`, `d_even`, the
coarse `d_ores`, and every `C5` standard difference because all of those
have zero scalar residue in the cap summand.

This is not yet a physical Fredholm terminal.  Killing the endpoint bar

```text
(-Omega,+Q,+ores_cap)
```

while also killing `n_y=(+Q,0)` forces the Omega weight to equal the cap
residue weight.  The target-stabilizer kernel then pairs as

\[
                          -A(5+u_z/t),                 \tag{4}
\]

so no normalized extension survives with the currently typed terminal
rows.  The first terminal-promotion datum is the already familiar physical
Omega-to-rootless/ridge comparison whose readout on every `eta_z` is
`+(5+u_z/t)` and whose target, residue, and anchor readouts vanish.

Equivalently, once the complete physically typed cap-grade matrix `J_cap`
is assembled, the exact finite alternative is

```text
z_cap in im(J_cap)  -> p=z_cap-n is constructed;
z_cap not in image  -> lambda J_cap=0, lambda(z_cap)=1 is the terminal dual.
```

The present result identifies the primitive row and the first failed
extension square.  It does not overclaim the second branch as an already
constructed physical terminal.

## Scope

This is an exact aggregate `h=3` reduction.  It is conditional on the
physical `K_Eq` invisible lift and does not construct the relative placement
(2), the full augmented terminal extension, the beta-integral family, or
the all-`h` spectator transport.

Run:

```text
python3 computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py
python3 -O computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py
python3 -I -S computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py
```

Frozen ledger SHA-256:

```text
b28588d688abd0b90b2bac58373e9c37f342f3f9767f27af702a87d8f6f27824
```
