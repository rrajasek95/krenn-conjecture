# The target-coloop affine gate is one diagonal-return lifting lemma

## Exact localized packet

Work at `h=3` over characteristic zero with the complete source equations

```text
q^[3] = X0,
p_i s_j q^[2] = delta_ij Xi,  i,j in {1,2}.
```

Assume the maximum-anchor/minimum-support normalization and the exact final
carrier data from the target-coloop route:

```text
K: pure 0, with direct PS:00,
L: pure 1, with ports P2,S3,
M: pure 2, with ports P0,S1,
05:02 and 14:02 nonzero and physical L-only,
00112200: PS:00 | 05:02 | 14:02 | 23:11 nonzero.
```

All external endpoint, external off-diagonal, decorated-anchor migration,
and already certified five-lock exits are excluded; otherwise the packet
has already routed.  By
[`h3-axis-target-coloop-p2-21-private-row-closure.md`](h3-axis-target-coloop-p2-21-private-row-closure.md),
the surviving packet also satisfies

```text
P2:21 = 0.
```

Checker:
`computations/verify_h3_axis_target_coloop_zero_face_affine_accessibility_reduction.py`.

## Two literal four-hole cofactors

At residual word `001122`, the `L`-port block `P2,S3` has

```text
C = x01^00*x45^22
  + x04^02*x15^02
  + x05^02*x14^02.
```

The terms are respectively diagonal return, external off-diagonal route,
and selected `L` tail.  The `M`-port block `P0,S1` has

```text
D = x23^11*x45^22
  + x24^12*x35^12
  + x25^12*x34^12
```

up to the residual-site mirror.  These are diagonal return, selected `M`
tail, and external off-diagonal route.  The checker reconstructs all six
literal matchings in each of the four records; no aggregate row is declared.

Modulo the already routed external terms, the four response coefficients
are exactly the sum of two rank-one shore blocks

\[
 E_{ij}=p_i s_j C+a_i b_jD,                            \tag{1}
\]

where `p,s` are the endpoint factors on `P2,S3` and `a,b` those on
`P0,S1`.  The zero-face result is `p_2=0`, while the selected cells make
`p_1,s_1,s_2` nonzero.

## The nonzero-`C` branch is linear

The following are literal polynomial syzygies of (1):

\[
\begin{aligned}
s_2E_{11}-s_1E_{12}&=a_1D(b_1s_2-b_2s_1),\\
a_2E_{11}-a_1E_{21}&=a_2p_1s_1C,\\
a_2E_{12}-a_1E_{22}&=a_2p_1s_2C.
\end{aligned}                                         \tag{2}
\]

If `C` is nonzero, all four source rows and the selected units force

```text
a2 = 0,
(b1,b2) proportional to (s1,s2)
```

at this common output covector.  The global complete columns then have the
standard exact dichotomy already pinned in the target-coloop route:

1. complete proportionality gives a finite one-sided joint-kernel
   deletion, anchor-safe under the `nu` normalization;
2. failure of complete proportionality gives a nonzero second covector;
   characteristic-zero common-covector synchronization supplies the active
   Fitting/lock carrier.

Thus no further matching classification is needed away from `C=0`.  The
point of (2) is not to claim that one coefficient proves complete-column
proportionality; it reduces the alternatives precisely to the already
audited complete-column test.

## The sole missing lemma

After the external middle term routes, `C=0` is the localized affine
relation

\[
 x_{01}^{00}x_{45}^{22}
       =-x_{05}^{02}x_{14}^{02}\ne0.                  \tag{3}
\]

The remaining theorem-strength input is the following source statement.

> **Common-q diagonal-return lifting lemma.** In the exact packet above,
> suppose (3) holds and `P2:21=0`.  Let
> \(\mathcal L_S(z)=(zs_1q^{[2]},zs_2q^{[2]})\) be the complete labelled
> response column of a component of `p1`.  Then either the complete column
> of `P2:11` lies in the span of the other occupied `p1` columns, or a
> literal common-q four-hole exchange term gives a nonproportional complete
> shore/offanchor active carrier.

In the first case, the corresponding exact finite kernel combination
deletes `P2:11` without changing any of the four responses; unary top and
the other endpoint rows are unchanged.  The row `p1` already has another
occupied component, so the deleted cell is not a mutual anchor.  The
preserved pure-one target supplies a new nonzero matching `L'`; reselecting
it makes at least one old L-only `02` cell nonanchor.  The second case is an
existing routed alternative.

This formulation is deliberately complete-column and source-provenant.
Equation (3) at one word does not by itself imply the span statement: the
aggregate full-five-row counterguard shows that such an implication needs
the literal common-q four-hole exchange.  Proving exactly this propagation
is the missing lemma; another endpoint-support or matching census cannot
replace it.

## Conditional affine-accessibility theorem

Assuming the common-q diagonal-return lifting lemma, every exact source in
the displayed `00112200` packet has one of the following outcomes:

```text
localized source unit;
pure-target reselection exposing an old 02 cell;
finite anchor-safe joint-kernel deletion;
nonanchor/decorated active carrier;
common-covector/five-lock landing.
```

The proof is now short: nonzero `P2:21` exits by its private row; on its
zero face, `C!=0` reduces by (2) to the complete-column dichotomy; `C=0`
is exactly the lifting lemma.  This is the global affine-accessibility
theorem needed for the final sixteen target-coloop slots.

## Scope

The checker proves the physical two-cofactor factorization and all three
syzygies in (2).  It does **not** prove the boxed lifting lemma or promote a
single coefficient relation to a complete-column dependence.

Run

```text
python3 computations/verify_h3_axis_target_coloop_zero_face_affine_accessibility_reduction.py
python3 -O computations/verify_h3_axis_target_coloop_zero_face_affine_accessibility_reduction.py
python3 -I -S computations/verify_h3_axis_target_coloop_zero_face_affine_accessibility_reduction.py
```

Frozen ledger SHA-256:

```text
67057359d8266b234a06cb50ec10bf009d482ecba0ba614da33e1741b7ad3f2a
```
