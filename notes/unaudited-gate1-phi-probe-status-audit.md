# Status of the unaudited Gate-I Phi probe

The probe's main output-side formula is now independently proved, but its
terminal obstruction and input-side conclusion are not valid consequences
for the current physical complex.

## What is now proved

Commit `271df91` proves the probe's identity in a strictly stronger model:

\[
 M_v=-\sum_j\alpha_j(-r_{0,j}+T_j+\rho_j)+K.
\]

It checks all 360 literal boundary features in every canonical repeated
component, the private and Eq signs, zero ordinary residue and protected
rows, and the source provenance of `K`.  It also proves that `K` has zero
literal source and first-Spencer output.  Thus the probe's favorable
assumption about Cartan private rows is discharged.

The old corner covector `private-W-target+R` is indeed not a surviving
obstruction after the physical Cartan cell is present: `K` has residue
`alpha` and zero private/W/target output.  This does not eliminate the later
physical anchor separator, which is a different covector on the complete
relative module.

The occurrence-level facts—18 input directions descending to 15 labels,
three overlap directions, a 12-label signed support, and 288/576
presentation ranks—remain useful and agree with the later cutwise descent
audits.  They remain occurrence/presentation statements.

## What is false or superseded

The claimed seven-dimensional terminal cokernel was created by placing the
Cartan prism in the probe with terminal value zero.  The physical `K` of
`271df91` carries exactly

```text
eta_z = 1 + delta_(vz) u_z/t,
sigma = -q_pq^22.
```

Therefore `M_v=-O_alpha+K` already has the required terminal packet and is
a committed source image.  The statements that “what persists is purely
terminal” and that output-side membership is a terminal-realizability
problem are superseded.  Output-side membership is closed.

The 32-row coarse identity does not construct the input comparison.  Commit
`def89a3` shows that the 15-label collision packet and the 360-feature
physical correction module have no committed shifted tail/fine-grade map
between them.  Comparing their shadows directly would assume `Phi`.

Likewise, rho-equivariance does not remove the overlap problem: it reduces
the three shared labels to one fixed orbit and one paired orbit.  Commit
`e5eb1fe` proves that the six labelwise pure-residue columns used by the
generous probe are not physical source columns; the actual committed
inventory has one scalar residue column.  The two sections `d_fixed` and
`d_pair` are still missing.

Commit `4f91155` sharpens rather than changes this frontier.  The favorable
assignment is `B0,B4,B5=q34*h3`, so its standard endpoint/PP/denominator-Tor
realization would require the selected face class `e3`.  The clean reset
covector kills every physical Tor image but reads one on `e3`.

Thus the probe provides no new construction of the two labelled sections.
The current alternative is a higher occurrence-splitting relative cell, or
a physical terminal extension of the face obstruction.

## Verification

Run:

```text
python3 computations/verify_unaudited_gate1_phi_probe_status_audit.py
python3 -O computations/verify_unaudited_gate1_phi_probe_status_audit.py
python3 -I -S computations/verify_unaudited_gate1_phi_probe_status_audit.py
```

Frozen ledger SHA-256:

```text
0f79205dc288d1495c193a1b45201977d049b52bde0232d85d744367e66dfa7a
```
