# The complete minimal silent-`C6` core-port envelope is a unit

## Result

Continue from the exact rational silent-`C6` zero fibre used in
`b4d8568`.  Choose any one of its three pure-`11` residual target tails
and any one of its three pure-`22` tails.  Now allow **every** colour
component of all four endpoint rows on the four core sites `0,1,3,4`:

```text
p1,p2,s1,s2 at each core site, with residual colour 0,1,2.
```

There are 48 endpoint variables.  Complete perfect-matching expansion of
all four response tensors is nevertheless inconsistent.  For every one of
the `3 x 3` bright-tail choices, a diagonal pure-target coefficient and a
mixed zero coefficient have proportional complete endpoint polynomials.
Writing their common normalized polynomial as `P`, the two source rows are

\[
                 aP-1=0,\qquad bP=0,\qquad a,b\ne0.       \tag{1}
\]

Therefore

\[
                 b^{-1}(bP)-a^{-1}(aP-1)=1.              \tag{2}
\]

This is an ordinary two-row source unit.  It uses no endpoint
normalization, no Fitting-to-rank promotion, and no support-minimality.

Checker:
`computations/verify_h3_silent_c6_full_core_port_unit.py`.

## Canonical certificate

For the first bright pair

```text
A1=23:11 | 45:11,      B1=01:22 | 25:22,
```

the complete pure-`2` target coefficient is

\[
 F_{222222}=
 p_{2,3}^{2}s_{2,4}^{2}+p_{2,4}^{2}s_{2,3}^{2}-1.       \tag{3}
\]

The mixed zero word `220220` has exactly the same endpoint polynomial:

\[
 F_{220220}=
 p_{2,3}^{2}s_{2,4}^{2}+p_{2,4}^{2}s_{2,3}^{2}.         \tag{4}
\]

Indeed, in (3) the residual cofactor is the selected pure-`22` matching
`01:22|25:22`, while in (4) it is `01:22|25:00`.  Both cells on physical
edge `25` are present with coefficient one in the fixed rational packet.
Subtracting (3) from (4) gives `1`.

The checker does not assume this orbit persists.  It reconstructs every
complete coefficient from the literal decorated matchings, groups the
resulting bilinear endpoint polynomials up to rational scalar, and finds at
least one target/zero pair in each of the nine bright charts.

## What this changes

The earlier selected-private-word audit `f5af6fd` found a reciprocal
two-port Fitting lock after arbitrary core-port endpoint components were
allowed.  That lock is real in the selected coefficient, but it is not a
survivor of the complete response packet on this fixed `q` support.  A
diagonal companion coefficient supplies (1) before any Hall/Fitting rank
landing is needed.

Thus the minimal silent-`C6` chain is now:

1. fixed ports: source unit or nonanchor active carrier (`b4d8568`);
2. arbitrary core-port endpoint mass on the same minimal decorated support:
   the two-row unit (2);
3. outside endpoint ports: the existing zero-column/free-active-arm theorem.

The canonical finite packet therefore leaves no endpoint-normalization
residual.

## Exact scope

The internal decorated support is fixed to

```text
the rational q00 silent-C6 zero fibre
+ one selected pure-11 tail
+ one selected pure-22 tail.
```

Extra internal decorated `q` cells can add matching terms to one or both
rows in (1), and are not included here.  Consequently this theorem removes
the minimal core-port obstruction but does not prove the uniform
multisite affine-accessibility theorem.  In the global attack, the first
unresolved `C6` branch is now an **internal-tail enlargement/source-
exhaustivity** problem, followed by the already named active-rank landing
and termination problem.

## Verification

```text
python3 computations/verify_h3_silent_c6_full_core_port_unit.py
python3 -O computations/verify_h3_silent_c6_full_core_port_unit.py
python3 -I -S computations/verify_h3_silent_c6_full_core_port_unit.py
```

The checker freezes its literal response inventory and a SHA-256 ledger.
