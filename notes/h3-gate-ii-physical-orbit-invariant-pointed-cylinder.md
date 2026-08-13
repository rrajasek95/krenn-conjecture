# Gate II is not a relabeling orbit; its minimal repair is one pointed mapping cylinder

## Result

The trapped Gate-II packet is not obtained by physically relabeling the
canonical endpoint-odd Cartan packet, even after the common-tail
normalization of `32ce01c` and the arbitrary-mate reduction of `c0853d3`.
The obstruction is not the remote matching tail.  It is the ordered
root/endpoint character.

Order the four corners of the root/endpoint orbit as `1,w,s,sw`, where `w`
is the two-root Weyl operation and `s` is the endpoint-role transposition.
Then

\[
 \chi_w=(1,-1,1,-1),\qquad
 \chi_{ws}=(1,-1,-1,1).                              \tag{1}
\]

The physical Cartan boundary `(1-s)(w-1)` is the mixed character
`-chi_ws`.  The occurrence-asymmetric direction required to reconstruct the
marked trapped carrier is the root-only character `chi_w`.

A physical site/colour relabeling conjugates a colour-root operation to a
colour-root operation and a site transposition to a site transposition.  It
therefore preserves the ordered eigenvalue pair

```text
                         (root sign, endpoint sign).
```

The two rows in (1) have signs `(-1,+1)` and `(-1,-1)`, respectively, so
they cannot be in the same physical relabeling orbit.  The remote common
`q` tail is fixed by both actions and has character `(+1,+1)`; multiplying
by it changes neither sign.

Checker:
[`verify_h3_gate_ii_physical_orbit_invariant_pointed_cylinder.py`](../computations/verify_h3_gate_ii_physical_orbit_invariant_pointed_cylinder.py).

## What does relabel physically

The negative statement is packet-level, not occurrence-level.  The pivot
of `32ce01c` proves that every omit-coloop carrier has a literal matching
skeleton, endpoint orientation, word/fine label, and invariant remote tail.
An individual carrier can be moved to the corresponding canonical matching
shape.

What cannot be moved is the complete protected parity packet.  The
canonical prism is odd in the endpoint transposition; the missing pointed
direction is even in it.  Relabeling positions does not change this parity.

There is a secondary support invariant for a wholly trapped nonzero packet.
The complete canonical endpoint-port skeleton realizes all `15` residual
holes.  The unions of the two shores in the six closed Hall types have
sizes

```text
3, 6, 5, 6, 9, 5.
```

Their hole graphs are proper and have different degree sequences from the
complete `K6` support.  This is not used to obstruct a single carrier; it
only confirms that a complete trapped support cannot be a permutation of
the complete canonical packet.

## The smallest formal mapping cylinder

The occurrence orbit has four character lines.  Complete rows, the granted
endpoint-safe line, and physical Cartan span

\[
                  \langle\chi_1,\chi_s,\chi_{ws}\rangle,       \tag{2}
\]

of rank three.  The marked occurrence is

\[
 P_f={1\over4}(\chi_1+\chi_w+\chi_s+\chi_{ws}),       \tag{3}
\]

so its residual modulo (2) is exactly `chi_w/4`.

The root-only face is not target safe.  In the word basis

```text
m_(c|i), m_(i|c), p_i, p_c
```

its target defect is

\[
              \delta=(1,1,-1,-1).                    \tag{4}
\]

The two normalized pure-target rows span only `p_i,p_c`.  Their rank is two,
and adjoining `delta` raises it to three.  Thus the mixed part of (4) is one
primitive target-cokernel class.

The smallest formal repair is the paired cylinder

\[
       X=(\chi_w,\delta),\qquad Y=(0,-\delta),\qquad
                         X+Y=(\chi_w,0).              \tag{5}
\]

Both faces are forced.  Without `X`, the occurrence rank remains three;
without `Y`, the two mixed target directions remain.  They may be two faces
of one relative PP/Spencer object, so (5) is one local construction theorem,
not two independent conjecture-level hypotheses.

Equation (5) is only a formal finite mapping cylinder.  Its missing physical
datum is exact:

> Realize `Y` by a source-labelled chart-complete `C2+`, `C4`, or `P2`
> Hasse/principal-parts cell in the same fan word, fine/repeated grade,
> endpoint orientation, and common tail as `X`.

The arbitrary-mate recurrence of `c0853d3` identifies precisely those Hasse
types as the first nondeletion face.  It does not yet prove that their target
face is the `-delta` in (5).

## The two augmented equations

The pointed anchor and the physical terminal must be recorded on the same
cylinder, but neither is a consequence of the other.

First, after quotienting by (2), the anchor equation is

\[
                         H=P_f,\qquad
             H-P_{\rm available}={1\over4}\chi_w.     \tag{6}
\]

Thus the same root face which completes the occurrence character table must
carry coefficient `1/4` in the marked anchor row.  A coefficient-only
`chi_w` face does not prove (6).

Second, on both complete domains

\[
                             q=M-a.                   \tag{7}
\]

For any comparison `Phi`, the root-character component of its defect is

\[
 \delta q=(M-M_0\Phi)-(a-a_0\Phi)=\delta M-\delta a. \tag{8}
\]

The common-tail matching pairing gives `delta M=0` once it is promoted to
the complete cylinder, so (8) becomes `delta q=-delta a`.  But `q`
transport alone does not imply (6): nonzero equal defects
`delta M=delta a` cancel in `q`.  Conversely, pointed-anchor transport with
nonzero matching defect leaves a `q` defect.

This independence is harmless after a physical `Phi` exists.  The pinned
physical-`q` quotient theorem consumes a nonzero `[delta q]` as a typed
kernel witness/generator, while a zero class is removed by a protected-row
correction.  The construction still has to make (6) physical.

## Updated Gate-II frontier

```text
arbitrary extra mates
        -> deletion / typed exit / complete C2+,C4,P2 face   [c0853d3]
        -> common-tail matching transport                    [32ce01c]
        -> canonical endpoint-odd Cartan chi_ws              [f746560]
        -> NOT a relabeling: endpoint parity differs
        -> construct paired cylinder (chi_w,delta)+(0,-delta)
        -> carry H=P_f and q=M-a on the same physical object
        -> q defect: witness, or protected correction
        -> existing Gate-II circuit/anchor alternatives
```

The highest-leverage next attack is therefore the source-labelled
mixed-target companion `Y` in (5), not another Hall-support census and not a
common-tail transport theorem.

## Scope and verification

This is exact at `h=3` for the physical root/endpoint orbit, all six closed
Hall support types, the four target words, and the displayed augmented
quotient equations.  It does not construct the chart-complete companion or
claim a full trapped GHZ source.

Run:

```text
python3 computations/verify_h3_gate_ii_physical_orbit_invariant_pointed_cylinder.py
python3 -O computations/verify_h3_gate_ii_physical_orbit_invariant_pointed_cylinder.py
python3 -I -S computations/verify_h3_gate_ii_physical_orbit_invariant_pointed_cylinder.py
```

Frozen ledger SHA-256:

```text
2b6becf27bf6755c5580d9fad63d90271c3d4ee6a42a8057b73369941a601c15
```
