# Unary exactness breaks the minimal disconnected four-base graph

## Result

On six residual sites, take the minimum disconnected matching-base graph

```text
A = 01 | 23 | 45,       B = 01 | 24 | 35,
K = 02 | 15 | 34,       L = 05 | 12 | 34.
```

Its physical edge union supports exactly these four perfect matchings, and
its C4 graph is

```text
A -- B       K -- L.
```

Attach the minimum diagonal endpoint block with selected holes `01` for the
colour-one response and `34` for the colour-two response.  In the normalized
one-bad equations

\[
 q^{[3]}=X_0,\qquad p_i s_jq^{[2]}=\delta_{ij}X_i,       \tag{1}
\]

the displayed four-base support is an ordinary three-row source unit.  On
arbitrary support, the same identity forces an additional pure-zero perfect
matching.  Its physical topology is either a C4 bridge joining the two old
components or one of two explicit C6 separators.

Concretely, the selected endpoint entries are `p1@0:1`, `s1@1:1`,
`p2@3:2`, and `s2@4:2`.  The five literal full-source coefficient words are

```text
top: 000000;  G11: 110000;  G12: 100020;
G21: 010200;  G22: 000220.
```

Their target coefficients are respectively `1,0,0,0,0`.  Thus all four
response rows are present in the packet; the short unit below happens to
need only `G11,G22`.

Checker:
`computations/verify_h3_four_base_disconnected_unary_bridge.py`.

## The three-row identity

Write `H_01` and `H_34` for the four-site hafnian cofactors after deleting
the selected diagonal holes, and use only the pure-zero coefficients.  The
two bright diagonal targets give

\[
              [0^4]H_{01}=[0^4]H_{34}=0.              \tag{2}
\]

Partition the fifteen six-site perfect matchings according to whether they
contain `01` or `34`.  Inclusion--exclusion gives

\[
 [0^6]q^{[3]}-q_{01}^{00}[0^4]H_{01}
                  -q_{34}^{00}[0^4]H_{34}
 =\sum_{M\cap\{01,34\}=\varnothing}q_M^{00}
                  -q_{01}^{00}q_{25}^{00}q_{34}^{00}. \tag{3}
\]

The last monomial is the unique matching containing both selected hole
edges.  In source-generator notation, (3) is

\[
 G_{\rm top}(0^6)-q_{01}^{00}G_{11}(0^4)
                  -q_{34}^{00}G_{22}(0^4)
 =\sum_{M\text{ avoids }01,34}q_M^{00}
                  -q_{01}^{00}q_{25}^{00}q_{34}^{00}-1. \tag{4}
\]

On the ten-edge union of `A,B,K,L`, every monomial on the right except
`-1` vanishes.  Hence

\[
 \boxed{1=q_{01}^{00}G_{11}(0^4)
             +q_{34}^{00}G_{22}(0^4)-G_{\rm top}(0^6).} \tag{5}
\]

This is integral and uses no localization, Gröbner basis, or crossed row.
Therefore the minimal disconnected common-q support is not a full-source
guard; unary exactness is already the missing bridge input.

## Every extension supplies a bridge or long separator

For an arbitrary full source, (4) equals zero.  Thus at least one of its
eleven matching monomials is nonzero.  They split exactly as follows.

- Nine are physically C4-adjacent to at least one of `A,B` and at least one
  of `K,L`; these are literal bridges between the two components.
- Two have C6 symmetric difference from all four old bases:

  ```text
  03 | 14 | 25,
  04 | 13 | 25.
  ```

  The second contains both selected crossed hole edges `04,13`, so its two
  tails enter both crossed response companions.  The first is invisible at
  those two holes and is the sole silent minimum separator.

The checker enumerates all fifteen matchings and verifies the complete
`9+2` split, including every C4 adjacency.

This is the first positive source-exhaustivity statement beyond the
conditional graph theorem of `8855f11`: the full unary row cannot leave the
two flat components isolated.

## Exact remaining typing gate

Physical C4 adjacency is not yet the certified typed common-tail carrier of
`f6ce8cc`.  The forced matching is selected in the pure-zero coefficient,
whereas the old bases also occur in bright response columns.  A companion
word must retain the common decorated tail and the opposite determinant
orientation.  Thus the next theorem is sharply smaller:

> For one of the nine forced C4 bridge matchings, the complete diagonal or
> crossed response rows either synchronize its decorations into a certified
> typed C4 edge, expose an off-anchor factor, or replace it by one of the two
> C6 separators.  For the silent separator `03|14|25`, a mixed unary or
> response word supplies a distance-three chord or Hall incidence.

Once a typed bridge is obtained, `8855f11` propagates the flat component;
a nonzero bridge minor is the active carrier, while a flat bridge joins the
components.  Conditional on source exhaustivity, `05a9d46` then removes the
arbitrary-column flat branch.  A C6 chord shortens by `ba94ab8`.

## Scope

- Equation (5) is a full-source contradiction on the exact minimum physical
  support.
- Equation (4) forces an additional nonzero **monomial**, not merely an
  aggregate support cell.
- The topology classification does not silently promote a physical C4 to a
  typed carrier or a C6 to Hall.
- Only unary and the two diagonal rows are needed for the unit.  The crossed
  rows remain available precisely for the final decoration/typing step.

## Verification

```text
python3 computations/verify_h3_four_base_disconnected_unary_bridge.py
python3 -O computations/verify_h3_four_base_disconnected_unary_bridge.py
python3 -I -S computations/verify_h3_four_base_disconnected_unary_bridge.py
```

Frozen ledger SHA-256:

```text
a6f88257313af83c37a80bfa64cdb63a969c7ca9dbf021be7ba99d4145d0d47a
```
