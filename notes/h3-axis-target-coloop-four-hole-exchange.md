# The first physical target-coloop exchange leaves one even-cycle boundary

## Result

At `h=3`, let `M` be the unique literal target-tail matching selected on a
target-coloop port, and let `N` be a literal matching summand in a nonzero
outside complete column.  Assume their two endpoint-hole pairs are disjoint.
Keep the five source-word labels, and write

\[
 a_c=\mu_M(c),\qquad b_c=\mu_N(c).
\]

If `c` is the pure target word, then `a_c!=0`.  There is an exact dichotomy.

* If `b_c!=0`, `N` is already an alternate pure target matching and breaks
  the coloop.
* If `b_c=0`, choose a word `d` on which the outside matching is active.
  Then

  \[
    \Delta^{MN}_{cd}=a_cb_d-a_db_c=a_cb_d\ne0.          \tag{1}
  \]

  The matching-base exchange identity from
  `hafnian-path-forest-straightening.md` gives the literal carrier

  \[
  b_cP^M_{cd}-a_cP^N_{cd}=\Delta^{MN}_{cd}H_c.          \tag{2}
  \]

On the exact target row `H_c=1`, its right side is nonzero.  Thus the
proportional alternative is not a new residual: if every target/outside
minor vanished, `b_c=0` and `a_c!=0` would force the entire outside
evaluation vector `b` to be zero.

The remaining issue is the physical topology of this nonzero E2 carrier.
The checker is
`computations/verify_h3_axis_target_coloop_four_hole_exchange.py`.

## The nine tail superpositions

Normalize the target holes to `0,1`, the outside holes to `2,3`, and the two
common residual sites to `4,5`.  Each four-site complement has three perfect
matchings, hence there are nine ordered tail pairs.  Their alternating paths
pair the four exposed sites in exactly three ways:

```text
internal          {01,23}: 5
endpoint-aligned  {02,13}: 2
endpoint-crossed  {03,12}: 2.
```

Restore endpoint sites `P,S` with target arms `P0,S1` and outside arms
`P2,S3`.  The symmetric difference of the two resulting full matchings has
cycle profile

```text
C6 plus one common matching edge : 1
C8                               : 6
C4 + C4                          : 2.
```

This is a complete combinatorial classification, not a support search.

## When recombination gives a new matching

In the two endpoint-aligned cases the two alternating components are
`C4+C4`.  Flipping only one cycle gives two new full matchings.  Their
endpoint ports are

```text
(P2,S1) and (P0,S3).
```

They are the two crossed recombinations of the old target and outside
ports.  If the induced decorations are pure, one is an alternate target
matching.  If they are mixed, they are literal physical exchange carriers.
Whenever a newly exposed physical edge lies outside the chosen three-colour
anchor union, the nonanchor theorem routes it to a good active pair.

The other seven cases contain a single alternating `C6` or `C8`.  Their edge
union supports only the original two perfect matchings, so a signless cycle
flip produces no third matching.  Identity (2) still supplies a nonzero
common-q exchange minor, but it remains an anchor-contained even-cycle
carrier until another complete coefficient row or an external edge breaks
the cycle.

## Sharp boundary

The aggregate counterguard `6b12677` is therefore substantially sharpened:
genuine common-q provenance always produces either an alternate target
matching or a nonzero E2 exchange carrier.  What is not yet automatic is
the landing of the latter.  Exactly two of the nine four-hole topologies
have a same-union recombination; the other seven form the first physical
even-cycle residual.

The result assumes four distinct endpoint holes.  Hole collisions belong to
the lower affine/Hall reselection strata and are not silently included.
It does not claim that an anchor-contained `C6/C8` carrier is four-good.

Run

```text
python3 computations/verify_h3_axis_target_coloop_four_hole_exchange.py
python3 -O computations/verify_h3_axis_target_coloop_four_hole_exchange.py
python3 -I -S computations/verify_h3_axis_target_coloop_four_hole_exchange.py
```

Frozen ledger SHA-256:

```text
948b396097dff3ab1a1f9d9b5297550adf3e4abedb21eb012efc8c7e03bd2127
```
