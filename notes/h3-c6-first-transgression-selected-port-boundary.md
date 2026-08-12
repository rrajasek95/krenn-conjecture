# The canonical C6 transgression reduces to one endpoint-word-change face

## Result

For the canonical shortening packet of `820c626`, put

```text
M=01|23|45,   N=05|12|34,   K=03|12|45,
t=111111, x=011111, y=112111, z=012111.
```

The four-face transgression has the exact factorization

\[
 D_K=K_t(M_z+N_z)-M_yK_x-N_tK_z.                    \tag{1}
\]

Indeed the nominal fourth face satisfies the literal monomial identity

\[
                         N_xK_y=N_zK_t.              \tag{2}
\]

Both remaining mixed products in (1) contain `q03:01`, the offdiagonal
decoration of the new shortening chord.  Thus, after the already identified
offdiagonal-chord route, the entire first-transgression problem is the one
class

\[
                              K_t(M_z+N_z).           \tag{3}
\]

Checker:
`computations/verify_h3_c6_first_transgression_selected_port_boundary.py`.

## The unary row does not isolate the chord

The complete unary coefficient at `z` gives

\[
 H_z=M_z+N_z+\sum_{Q\ne M,N}Q_z=0.                  \tag{4}
\]

Consequently (3) becomes `-K_t sum Q_z`, with thirteen competing matching
bases.  Relative to the old four-base union, seven competitors already
contain an outside offdiagonal cell.  Six remain anchor-contained:

```text
01|24|35, 02|13|45, 02|14|35,
02|15|34, 05|13|24, 05|14|23.
```

This is smaller than the original three-face obstruction, but it is not a
single-survivor identity.

## Exact source-typing obstruction

At the residual word `z=012111`, the four selected physical holes see

```text
hole 01: 01,   hole 04: 01,   hole 13: 11,   hole 34: 11.
```

The fixed one-bad endpoint block supplies instead

```text
G11@01: 11,   G12@04: 12,   G21@13: 21,   G22@34: 22.
```

Therefore none of the four selected-port response coefficients contains a
monomial at `z`.  The remaining complete tensors cannot eliminate the six
anchor-contained competitors without changing an endpoint word.  The first
new literal companion needs, for example, `p1@0:0` in the `G11` hole-01 row
or `p2@3:1` in the `G21` hole-13 row, together with the already selected
opposite endpoint component.

This identifies the first-transgression selection theorem precisely: it is
an endpoint-word-change/complete-column statement, not another punctured
hafnian identity.  A nonzero word-changed component may route through the
existing endpoint/Hall machinery; its absence leaves the displayed
six-base unary class.

## Scope

This is an exact symbolic theorem for the canonical C6 embedded in the
fixed-port minimum four-base packet.  It classifies all three mixed faces
and the complete selected-port visibility.  It is not a full-source guard:
arbitrary endpoint components or additional decorated q cells can provide
the missing response coefficient.

## Verification

```text
python3 computations/verify_h3_c6_first_transgression_selected_port_boundary.py
python3 -O computations/verify_h3_c6_first_transgression_selected_port_boundary.py
python3 -I -S computations/verify_h3_c6_first_transgression_selected_port_boundary.py
```

Frozen ledger SHA-256:

```text
cbcfb53638fd3170967224331fc06c200e8cb36b8d2e1da3702dcd330971ec10
```
