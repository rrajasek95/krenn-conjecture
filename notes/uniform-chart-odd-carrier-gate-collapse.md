# Gate II and the Bianchi obstruction are one chart-odd carrier

## Outcome

The two mixed chart arrows isolated at the `h=3` Gate-II frontier are not a
new generator species.  They are exactly the two degree-zero switch carriers
in the already constructed presentation-safe relative matching graph.  The
uniform tagged Bianchi obstruction is the same carrier construction between
two overlapping pair-chart copies.

Consequently the local and all-order frontiers reduce to one physical
statement:

> **Chart-odd augmented saturation theorem (open).**  Land the universal
> relative switch carrier in the complete augmented physical complex and
> construct a nullhomotopy compatible with word, fine and repeated grade,
> every PP/reinsertion face, target, Eq, ordinary residue, physical `q`,
> anchor, `W`, and shifted ridge.

This is a genuine reduction of the proof frontier.  It does not construct
that nullhomotopy.

Exact checker:
[`verify_uniform_chart_odd_carrier_gate_collapse.py`](../computations/verify_uniform_chart_odd_carrier_gate_collapse.py).

## The universal relative graph

For one parent occurrence `u0` and one chart companion `u1`, add graph
coordinates `z0,z1,t` and degree-one generators

\[
 d\theta_i=z_i-u_i,
 \qquad
 d\phi=t-(z_1-z_0).
\]

The combination

\[
 \Gamma=\phi+\theta_1-\theta_0
 \quad\text{satisfies}\quad
 d\Gamma=t-(u_1-u_0).                              \tag{1}
\]

All equations are monic in new variables.  Eliminating them returns the old
occurrence algebra with no new relation among `u0,u1`; the carrier simply has
the forced value `t=u1-u0` in `H0`.  Setting `t=0` instead would identify the
two old occurrences and change the fibre.

## The `h=3` Gate-II class

Write the three residual `C4` charts as

\[
 A=Dq_{01}H,
 \qquad B=p_0s_1H,
 \qquad C=p_1s_0H,
\]

and let `tB=B-A`, `tC=C-A` be the two relative switch carriers.  Then

\[
 \boxed{,L_{01}=2A-B-C=-(t_B+t_C)\quad\text{in }H_0.\,} \tag{2}
\]

At chain level the exact identity is

\[
 L_{01}+t_B+t_C=d(\Gamma_B+\Gamma_C).                \tag{3}
\]

Thus the two missing arrows

```text
DQ <-> P0S1,
DQ <-> P1S0
```

are precisely the two graph carriers.  They are not site-root cobar edges;
that negative result remains correct.  What changes is the interpretation:
the source-safe relative graph already constructs their carrier object.
The still-open step is its map to the complete augmented cap grade.

If an augmented chain `EtaB+EtaC` has boundary `tB+tC`, then (3) gives

\[
 d(\Gamma_B+\Gamma_C-(\Eta_B+\Eta_C))=L_{01}.         \tag{4}
\]

The committed word-`0102`, `dq`, `Q/ores`, `d_even`, `W`, and ridge ladder
then begins exactly where the previous Gate-II audits place it.

## The uniform Bianchi class

Retain two tagged pair-chart copies `u_M^{pq},u_M^{pr}` of every global
matching occurrence.  The same graph gives

\[
 d\Gamma_M=t_M-(u_M^{pr}-u_M^{pq}).                  \tag{5}
\]

Summing over the matching occurrences in a fixed word identifies the tagged
Bianchi difference with the total chart-odd carrier:

\[
 \widehat\beta_{h,\omega}
       =\sum_M(u_M^{pr}-u_M^{pq})
       =\sum_Mt_M-d\sum_M\Gamma_M.                  \tag{6}

Every strict global-word readout assigns the same coefficient to the two
chart copies and zero to `t_M`.  It therefore kills both sides of (6) without
making either a boundary.  This recovers the all-word signed-kernel theorem
and explains why appending every pure and mixed target row does not help.

If a natural augmented saturation supplies `d Eta_M=t_M`, then

\[
 d(\Gamma_M-\Eta_M)=-(u_M^{pr}-u_M^{pq}),             \tag{7}

so the tagged Bianchi descent obstruction is filled.  With the chartwise
oriented four-cut primitives and triangle coherence already in place, (7)
is exactly the missing descent datum needed to put both orientations in one
common carrier.  The strict common-four-cut theorem then gives
`d Gamma=r-2q`, which kills the whole Hilbert--Cauchy moment tower.

## What remains physical

Equations (1)--(7) are presentation-safe and source-labelled, but they do
not define the augmented image of `t`.  The carrier is a literal
matching-exchange binomial, not a Pluecker relation.  Its image must still
carry all proper faces and terminal readouts.  At `h=3` those proper faces
are the named endpoint-even `C2+`, invariant `C4`, and `P2` packets; at
general order common-edge faces recurse and the four switch-cycle faces are
the same three species.

The shortest remaining attack is therefore no longer “construct two mixed
chart arrows” plus “kill a separate Bianchi kernel.”  It is:

1. land the universal chart-odd carrier once in the augmented physical
   complex;
2. show its common-core kernel is saturated, or extend its primitive dual to
   an accepted physical terminal; and
3. use the resulting common four-cut homotopy to kill every moment at once.

## Reproduction

```sh
python3 computations/verify_uniform_chart_odd_carrier_gate_collapse.py
python3 -O computations/verify_uniform_chart_odd_carrier_gate_collapse.py
python3 -I -S computations/verify_uniform_chart_odd_carrier_gate_collapse.py
```
