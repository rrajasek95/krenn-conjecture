# The collision cofactors do not yet form an `AugP2` source object

## Literal answer

No committed source object packages the six shear-collision `P3+K2` faces
with the shifted ridge.  The preceding calculation found a genuine
undecorated `SQQ/P2` graph match, but the literal word and fine grades are
different.

The response collision lies in

```text
head/word       11:110000  = 11110000 on P,S,0,...,5,
```

whereas the canonical cap object lies in

```text
word            01211222.
```

These words differ at `P,0,2,3,4,5`.  For example,

```text
undecorated face     s0*q01*q45
response decoration s0^11*q01^11*q45^00
AugP2 decoration    s0^12*q01^21*q45^22.
```

All six tail cofactors have different response and cap fine-degree vectors.
The same holds for `q23,q24,q25,q34,q35,q45` individually as listed by the
checker.

Checker:
[`verify_h3_shear_collision_augp2_packaging_map_gate.py`](../computations/verify_h3_shear_collision_augp2_packaging_map_gate.py).

## The existing root cube does not provide the missing arrow

The committed response `D4` cube starts at `11:110000` and changes only the
last four residual zeroes by `0 -> 1`.  Its sixteen full words have form

```text
11:11 epsilon2 epsilon3 epsilon4 epsilon5,
```

so `01211222` is not a vertex.  In particular, neither identity/relabeling
nor the existing moving-target orbit gives a degree-preserving map from the
collision cofactor to the cap object.  A new occurrence-local, word-changing
Cartan/Spencer/principal-parts arrow is the first required datum.

This is a literal grade obstruction, not an assertion that no larger root
path can exist.  Any such path must be built together with its target-normal
and Hasse proper faces.

## What survives after granting a word arrow

Even granting a word-changing arrow does not make the collision into the
whole augmented source object.  In the decisive quotient

```text
(hidden lower/P2, central Eq, mixed square incidence, shifted ridge),
```

the available pieces are

```text
collision P3+K2 cofactor       (1,0,0,0),
old clean K_Eq                 (0,1,0,0).
```

They span rank two.  The pointed response-word/`K_Eq` mapping square has a
primitive `H1 = Z`; filling it needs the already isolated mixed
mapping-cylinder/Tate two-cell, raising rank to three.  The labelled shifted
Kähler face raises rank to four.  Its primitive coordinate kills both the
collision cofactor and clean `K_Eq`.

Thus the collision supplies at most the hidden lower/P2 coordinate of the
conditional `AugP2` schema.  It does not supply:

1. the mixed naturality-square incidence;
2. the physical reduced-Eq/cap label descent;
3. the six sibling `3K2` faces in the boundary of the collision top; or
4. the shifted `pq/xv` Kähler placement.

The third item matters: the collision top has six selected `P3+K2` tail
cofactors and six selected `3K2` path cofactors.  A putative source top
cannot retain only the desirable half of its boundary.

## Ridge and terminal scope

The shifted ridge is

\[
                 \gamma_v=-d\Omega_v.
\]

The existing formal cap/ridge local system is flat once a physical bottom
`AugP2` section is granted.  Its one nonconstant root face is

\[
                 -d(q_{xv}^{01}).
\]

Therefore no new curvature theorem is needed after placement.  But the
placement itself must carry both shifted `pq/xv` halves of `gamma_v` and
this connection face in the labelled repeated module.  The response
collision has no `Omega`, ridge, eta, or sigma coordinate from which these
could follow.

Physical `q` is likewise undefined on the response/collision generator
before a protected augmented comparison exists.  The existing
generator-versus-Fredholm defect alternative applies after this placement,
not before it.

## Shortest positive object

The smallest positive construction is one pointed relative PP mapping
cylinder whose:

- collision boundary retains all six `P3+K2` and all six `3K2` selected
  faces;
- word-changing diagonal sends the six `SQQ` faces into the canonical
  `01211222 / t*q_(v,N)` occurrence packet;
- mixed two-cell carries the central reduced-Eq and cap-label descent; and
- relative Kähler face is `gamma=-dOmega` with connection
  `-d(q_xv^01)`.

Once that object exists, the committed formal flatness gives cap/ridge
coherence and eta/sigma, while physical `q` closes through its protected
defect alternative.  The current `AugP2` result states exactly this kind of
multi-face theorem conditionally; it is not an already constructed source
object.

The audit is exact for canonical `h=3` and the selected collision block.  It
identifies the first literal word/fine map and the next mixed-incidence
obstruction; it does not prove an all-resolution no-go.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
9095b2120fd787af031e4f830bfe3a42a838bb253e91290381e9823c700b4fec
```
