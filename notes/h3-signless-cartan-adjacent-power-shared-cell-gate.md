# The signless Cartan comparison needs a root-even adjacent-power companion

Research gate on the generic `beta != 0` branch.  This does not construct
the companion, prove inactive routing, or prove Krenn's conjecture.

## Result

On the balanced six-site word `001122`, let

\[
 \rho=(1\ 4)
\]

and let `w` be the simultaneous `0 <-> 2` Weyl action at sites `1,4`, with
the diagonal torus signs normalized so that the selected word is fixed
literally.
The two operations commute, `rho*w` fixes `001122`, and the collision lower
face is anti-invariant under `rho`.  This is the exact two-root geometry
behind the cut-swap comparison.

The endpoint-odd Cartan prism

\[
                    K_-=(1-\rho)H_w
\]

is target-safe.  The signless companion has

\[
 (1+\rho)(w-1)\Delta=2(w-1)\Delta.                 \tag{1}
\]

Correcting (1) inside the natural two-dimensional span
`<H_w,rho H_w>` cannot retain a signless comparison.  Since the Weyl defect
is `rho`-invariant, `a H_w+b rho H_w` is target-safe exactly when `a+b=0`.
In particular,

\[
              (1+\rho)H_w-2H_w=(\rho-1)H_w,          \tag{2}
\]

which is the odd prism again.  Therefore the fixed-word/signless comparison
requires an independent relative target-cone direction.

Checker:
[`verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py`](../computations/verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py).

## The literal diagonal rows do not supply that direction

For the generic diagonal branch, the two literal cap rows have targets

\[
 hT(J_1)=h(\beta,-\alpha,-\alpha),\qquad
 hT(J_2)=h(-\beta,-2\alpha,-2\alpha).                 \tag{3}
\]

Both live entirely on the three monochromatic GHZ target coordinates.  So
does every pure-colour coloop row and every global site/colour transport of
such a row.

By contrast, `(w-1)Delta` has two unavoidable mixed target words:

```text
020020, 202202.
```

The exact target-space rank is

```text
all pure target rows plus J1,J2     3
after adjoining (w-1)Delta         4.
```

Consequently neither `J1/J2`, an `alpha`-weighted pure-colour coloop row,
nor a global colour symmetry can cancel (1).  The scalar identity
`alpha U_i-d_i V_i=alpha` types a pure/mixed omit-coloop carrier, but it does
not create the local-root-decorated target coordinate required here.

This also answers whether the missing adjacent-power cell is already the
physical `M_v`.  The two objects have the same **two-local-root mapping-cone
architecture**, but are different parity components:

```text
M_v / K_-       rho-odd,  target zero;
new C_plus      rho-even, target-bearing correction to 2(w-1)Delta.
```

They are not the same literal column.

## Exact shared construction theorem

For one chosen generic row `J=J1` or `J2`, the diagonal route needs a
relative cell `C_J` whose upper face is `-hT(J)` in the `lambda A` grade and
whose lower face is zero.  Then

```text
P(J)+C_J:
    target = 0,
    normalized lower residue = J_cc * Ybar_c.
```

The signless route needs an even cell `C_plus` with upper face
`-2(w-1)Delta`.  A single source construction can serve both roles exactly
under the following comparison statement:

> There is a source-labelled, Hasse/Rees-linear two-root comparison which
> identifies the chosen diagonal upper face `hT(J)` with the root-decorated
> face `2(w-1)Delta`, carries the lower `p t_c B` face to the marked
> collision/repeated-grade output, and is equivariant for `rho`.

This theorem would simultaneously provide:

1. the root-even companion which turns the collision cut-swap shadow into a
   physical fixed-word comparison;
2. the target-cancelled adjacent-power diagonal cap used by inactive
   routing; and
3. the two-root target correction suggested by the trapped-coloop carrier.

The existing endpoint-odd `M_v` then supplies the protected rootless
comparison.  The new theorem is genuinely smaller than three unrelated
cells, but it is not a consequence of the committed inventories.

## Eta/sigma are a separate commuting factor

The diagonal cap module has no `eta_z` or `sigma` readout.  The physical
terminal packet

\[
 d r_v(\eta_z)=1+\delta_{vz}u_z/t,
 \qquad \sigma=-q_{pq}^{22}
\]

comes from the Kähler ridge `-dOmega_v`.  The complete order-six audit proves

\[
                    [\Theta_6,-d\Omega_v]=0.           \tag{4}

Thus the ridge may be tensored/glued after the physical two-root comparison
is constructed, but the adjacent-power target cell does not naturally
supply those terminals itself.  This is the rigorous part of the untracked
Gate-I probe's “terminal-only” suggestion: its terminal conclusion agrees
with the committed ridge typing, while its projected membership claim is
not used here.

## Minimal missing datum and scope

The first missing column is the root-even, root-decorated adjacent-power
companion with

```text
rho parity          even,
upper target        -2(w-1)Delta,
lower comparison    chosen p t_c B face,
Hasse/Rees law      linear and rho-equivariant,
eta/sigma           absent until tensoring with -dOmega_v.
```

Equivalently, on the diagonal side it is `C_J` with upper face `-hT(J)` and
zero lower correction, together with the label map identifying those two
upper faces.  The old physical adjacent-power inventory reaches the needed
cap boundary only in the prolonged fourth-Hasse cone and retains the
independent `(H_0-u)e_Eq` descent defect.  The present theorem does not remove
that source-validity condition or the separate truncated Rees class in
`ker(epsilon)/N_lit`.

The trace collision `beta=0` is excluded.  There the two diagonal rows
collapse, the selected target first occurs at order `h`, and the unary-jet
or complementary-survival branch remains separate.

Run:

```text
python3 computations/verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py
python3 -O computations/verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py
python3 -I -S computations/verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py
```

Frozen ledger SHA-256:

```text
90ab61ba0839e56bfc012a727ffbc5da1bc6f08b6b209d1c5410273f38bade0d
```
