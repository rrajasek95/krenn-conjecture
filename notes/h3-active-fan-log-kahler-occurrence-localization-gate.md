# The logarithmic ridge works on a selected open, but selection is still not a physical operation

## Verdict

The committed shifted-Kähler connection does **not** supply the `30`
`Omega*dT` faces from the exact active-fan Cartan restriction after physical
labels are retained.  It differentiates ridge cells of type

\[
                         q_{0v}^{01}
\]

(and, under the strongest two-root grant, cells on the `01` block).  The
new debts differentiate the six remote colour-`11` cells

\[
 q_{23}^{11},q_{24}^{11},q_{25}^{11},
 q_{34}^{11},q_{35}^{11},q_{45}^{11}.                \tag{1}
\]

Kähler one-forms retain their coefficient-cell labels.  Consequently the
committed connection has rank zero after projection to the `30` debt
coordinates.

There is nevertheless a sharp local positive result.  If one physical
occurrence `f` has already been selected and is nonzero, its remote tail
`T` is a unit on `D(f)`, and

\[
       -{d(T\Omega)\over T}
           =-d\Omega-\Omega {dT\over T}
           =\gamma-\Omega\,d\log T.                  \tag{2}
\]

The logarithmic correction in (2) is eta/sigma dark.  What remains missing
is not a connection formula: it is a physical occurrence-labelled source
cell and its comparison with the shifted repeated-grade correction module.

Checker:
[`verify_h3_active_fan_log_kahler_occurrence_localization_gate.py`](../computations/verify_h3_active_fan_log_kahler_occurrence_localization_gate.py).

## Exact labelled debt inventory

The `78` omit-`01`, omit-`67` terms form `39` endpoint orbits.  Their remote
tail sizes are

```text
tail edges       0    1    2
endpoint orbits 12   24    3.
```

Before collection, the `27` nonconstant-tail orbits have `30` distinct
product-rule faces.  Each atom retains

```text
endpoint-orbit parent,
differentiated physical edge and colour 11,
Omega potential label,
tail-Leibniz/Hasse operation parent.
```

Every remote edge in (1) occurs exactly five times.  For a two-edge tail,
the required debt is the sum of its two labelled faces.  Hence the exact
fixed product-rule debt space has `27` independent occurrence-parent
vectors supported on `30` atoms.

The committed connection has four one-faces `-d(q_0v^01)` in the E14
packet.  Even granting the full two-root closure

```text
d(q_01^10), d(q_01^01), d(q_01^11)
```

does not change the projection: none is a differential in (1).  Thus

```text
rank(connection on tail-debt block)          = 0,
rank(connection plus required debt vectors) = 27.
```

The Hasse coproduct does contain the faces formally.  Its divided-power
Leibniz rule constructs `d(T Omega)` in the complete principal-parts source
resolution.  This is source-side product closure, not a column in the
literal physical augmented correction presentation.

## The selected-occurrence logarithmic shortcut

Take the first one-edge-tail orbit

```text
f+ = 02 | 16 | 34 | 57,
f- = 02 | 17 | 34 | 56,
T  = q_34^11.
```

Writing `f=T R`, localization at the nonzero occurrence gives the exact
algebraic inverse

\[
                         T^{-1}=R/f.                  \tag{3}
\]

No analytic logarithm or root extraction is used.  The root action at
`0,1` and the endpoint swap `6 <-> 7` fix `T`, so (2) is compatible with
the four-corner Cartan orbit.

For every `eta_z`, the only nonzero weights are at colour `0` on the
endpoint/auxiliary sites.  Sigma uses colour `2` at sites `6,0`.  The tail
cell `q_34^11` meets none of these weights.  Therefore

\[
             \iota_{\eta_z}d\log T=0,
             \qquad \iota_\sigma d\log T=0,           \tag{4}
\]

and the same holds for every remote tail in (1).  Thus the logarithmic
correction adds no eta/sigma debt.  On a tail-free selected occurrence,
`T=1` and it disappears altogether.

This reduces the ridge problem on one selected occurrence to at most two
labelled logarithmic faces.  It does not solve the global `78`-term packet:
the tails differ by occurrence, so there is no single common logarithmic
gauge.

## Why choosing a nonzero term is not yet selecting a source column

The active-fan pivot proves that some literal summand is nonzero and permits
support/Hall routing by cases.  That existential choice does not define an
endomorphism or idempotent on the complete physical source equation.

The exact Euler selector illustrates the gap.  Its top coefficient selects
one matching, but its first physical-source face is the nonzero `15`-term
normal `H_e`; the cube is only a relative Spencer/KS carrier.  In the
selected response word, the committed same-grade operations have only the
complete orbit-sum image and do not isolate an occurrence.  Thus using (2)
only on `f` assumes the occurrence comparison which Gate II still needs.

There is a second, independent check.  Homogeneous localization extends the
site grading to a group grading.  Dividing both ridge halves by the same
`T` subtracts the same tail degree, leaving

\[
                         e_6+e_7\ne e_0+e_1.          \tag{5}

\]

So localization does not manufacture the physical shifted `67/01` section.
Conditional on a physical occurrence selector, (5) is the next missing
comparison.

## First irreducible face and filler-or-terminal test

For the displayed orbit the first face is

```text
Omega*dlog(q_34^11)
parent: tail-Leibniz/Hasse
endpoint mate: 02|17|34|56
eta/sigma: 0/0.
```

Its coefficient-extraction dual kills every committed gamma/root-connection
column and reads `1` on the face.  Adjoining a correctly labelled filler
raises the projected rank `0 -> 1`.

For any selected occurrence `f`, let `g_f` be the sum of its one or two
labelled logarithmic debt atoms.  The exact test is

\[
 g_f\in\operatorname {im}(\pi_{\log}J_{\rm phys})
 \quad\Longleftrightarrow\quad
 \text{the selected logarithmic ridge has a physical filler}. \tag{6}

If (6) fails, linear duality gives a normalized covector killing the
projected physical columns and reading one on `g_f`.  To promote it to an
accepted terminal, extend it through boundary, `W`, target and residue and
physically identify its `q`/anchor value.  After that typing, the committed
zero-indeterminacy-or-relative-generator theorem is exhaustive.  The latter
promotion is not unconditional yet because it requires the same
occurrence/PP-to-physical comparison.

## Shortest constructive order

```text
physical occurrence-labelled source cell for the selected endpoint orbit
        -> localize at f, hence at its remote tail T
        -> use gamma - Omega*dlogT (eta/sigma dark)
        -> place the separate 67/01 shifted labels in the physical grade
        -> apply the existing q correction-or-generator alternative.
```

The first dependency is occurrence selection, not inversion of `T`.  The
next dependency is the localized principal-parts-to-physical shifted-grade
comparison.

## Scope and verification

This is exact for the `h=3` `01`-coloop/`67`-response packet, all `39`
endpoint orbits, all `30` labelled tail differentials, and the one-selected-
occurrence localization.  It is not an all-`h` theorem or a full GHZ source
counterexample.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
907cd25b4fb2c92ef2b2954da0e9c79f57bc35d5996bc837112a07ae89bcee95
```
