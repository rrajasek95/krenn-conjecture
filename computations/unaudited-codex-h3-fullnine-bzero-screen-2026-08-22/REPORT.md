# Minimal-`q` full-nine ordered-channel screen

Status: **UNAUDITED bounded exact finite-field PASS**.  This is a corrected
replay of the smallest six-site common-power stratum; it is not a
characteristic-zero emptiness proof.

## Result

Normalize the selected ordered channel to `(a,b)=(0,1)`.  Let `q` have two
unit diagonal edges in each physical colour, and let each of the six endpoint
stars have projective support on at most two decorated ports.  The valid
symmetry is `S6` together with endpoint swap followed by the physical/channel
colour swap `0<->1`; a free `S3` colour quotient is unsound after selecting
`01`.

The corrected quotient has exactly 100 ordered `q`-support orbits, not the
48 recorded by the stale pre-correction result.  Exhaustive screens give

```text
field    ordered q orbits    compatible six-star sextuples
F5              100                         0
F7              100                         0
```

The failure occurs before testing `r^[3] != 0`: no choice of endpoint stars
simultaneously realizes the six off-diagonal common-power rows and the three
separately labelled diagonal anchors.  Of the 100 supports, 42 have
`q^[3]=0` and 58 do not; both classes are excluded by the nine-row
compatibility incidence.

Conceptually, the nine equations ask whether the bilinear response tensor

```text
beta_q(p,s) = (p*s) q^[2] mod <q^[3]>
```

contains the labelled diagonal restriction
`beta_q(p_i,s_j)=delta_ij X_i`.  The finite screen is therefore a sparse
tensor-restriction test, not an unstructured coefficient brute force.  A
global proof would classify the corresponding Segre/linear-section
incidence over an algebraic closure; absence of `F5` and `F7` rational points
alone does not do that.

## Scope and replay

The result covers exactly the displayed minimal diagonal-`q`, two-port-star
stratum.  It neither bounds arbitrary star support nor excludes solutions
over finite extensions or characteristic zero.

```sh
python3 computations/unaudited-codex-h3-fullnine-bzero-screen-2026-08-22/screen_minimal_q_fullnine.py --write-results
```

Corrected logical SHA-256:

```text
72cc1c6f6e38c11efddff31439e79480753a9123f74a653f91b9c34201d4b271
```
