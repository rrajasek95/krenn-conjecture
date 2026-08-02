# The direct full-symmetry quotient is large after three layers

## Bounded exact census

In the balanced degree-twelve, 24-port Macaulay component for the full
eight-vertex source, the target \(H_0H_1H_2\) has exactly 31 row orbits under
\(S_8\times S_3\).  The orbit sizes, reconstructed from exact stabilizers,
sum to

\[
                         105^3=1{,}157{,}625,
\]

so these 31 representatives exhaust the target rather than merely sample it.

Closing those target rows under the mixed-generator incidence relation gives
the following first three layers:

\[
\begin{array}{c|rr|rr}
\text{layer}&\text{new rows}&\text{new columns}
             &\text{total rows}&\text{total columns}\\ \hline
1&570&31&601&31\\
2&27{,}470&741&28{,}071&772\\
3&360{,}818&17{,}915&388{,}889&18{,}687.
\end{array}
\]

The computation uses canonical coloured port-graph codes, audits the target
stabilizers, and quotients both vertex and colour permutations.  Thus the
growth is present even after the full natural symmetry reduction.

## Meaning and scope

This is a bounded census, not a rank calculation and not an ideal-membership
result.  The component was stopped before the fourth layer: the third-layer
run used roughly 0.8 GB resident memory, and there was no useful bound on the
remaining closure.  A direct full-component enumeration is therefore demoted
behind the filtered Schur calculation and the local-standard-basis route.

The reformulation remains conceptually useful.  Balanced monomials are
perfect matchings of 24 vertex-colour ports, mixed generators are matching
sums on eight-port transversals, and the pure product is the sum over three
monochromatic matching layers.  A representation-theoretic contracting
homotopy for this incidence map could bypass the enumerated component.

## Reproduction

```sh
python3 computations/analyze_n8_full_s8s3_pure_product_membership.py \
  --max-layers 3
```

The three-layer cap is the default and its exact census is frozen.  Raising
the cap is exploratory and can be substantially more expensive.
