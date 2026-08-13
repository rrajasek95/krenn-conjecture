# One three-cap family unifies the block projector, but leaves an endpoint PP face

## The combined construction

Put

\[
 A=Dq_{01},\qquad B=p_0s_1,\qquad C=p_1s_0,
\]

and

\[
 H=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.
\]

Suppose there were source-valid capped Hasse cells `C_A,C_B,C_C` for the
three pairings of the four endpoint sites. Their two natural combinations
would be

\[
 C_R=C_A+C_B+C_C,\qquad C_L=2C_A-C_B-C_C.             \tag{1}
\]

At degree zero, (1) has boundaries

\[
 dC_R=R_{01}=(A+B+C)H,
 \qquad dC_L=L_{01}=(2A-B-C)H.                        \tag{2}
\]

Thus the capped symmetric-C4 section and the nine-term block projector from
`abcce03` are not two unrelated generators. They are the unweighted and
centered projections of one covariant three-cap family. Constructing that
family is the shortest positive route.

Checker:
[`verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py`](../computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py).

## The exact first principal-parts face

The next face of `C_L` is the literal Kähler differential

\[
 dL_{01}=d(2A-B-C)H+(2A-B-C)dH.                       \tag{3}
\]

The checker expands (3) in the complete first-PP occurrence module. Its
support is exactly

```text
36 terms = 18 residual-tail derivatives + 18 direction-factor derivatives.
```

The residual half differentiates one of the two `q` edges in each term of
`H`. For every labelled residual edge, the three direction coefficients
sum to `2-1-1=0`. Hence every residual-`dq` marginal vanishes separately.
The pinned endpoint/matching projector sees precisely this kind of face:
its selected `p0*s1` fibre has the six tail terms

\[
p_0s_1(dq_{23}q_{45}+q_{23}dq_{45}+\cdots
       +dq_{25}q_{34}+q_{25}dq_{34}).                 \tag{4}
\]

Equation (4) is one third of the 18-term tail half. As the pinned audit
emphasizes, it is a source-faithful formula, not yet a boundary in the fixed
pointed source.

The other half differentiates the endpoint/direction factors. In the
label order

```text
dD, dq01, dp0, ds1, dp1, ds0
```

its occurrence marginals are

\[
                   (6,6,-3,-3,-3,-3)
             =3(2,2,-1,-1,-1,-1).                    \tag{5}
\]

Their total sum is zero, but none of the six labelled entries is zero. So
the target-zero scalar top does not make the first-PP cell protected. The
matching projector controls the tail half of (3); it does not cancel (5).
This endpoint-even direction conormal is the first exact proper face of the
combined chart construction.

## The complete-response guard persists one level up

The complete response has 105 occurrences and its first differential has
420 labelled coordinates. The local block has 9 occurrences and 36 first-PP
coordinates. Therefore

```text
R-R01      has  96 occurrence terms,
d(R-R01)   has 384 first-PP terms.
```

The exact identities are

\[
 L_{01}=3AH-R_{01},\qquad
 dL_{01}=3d(AH)-dR_{01}.                              \tag{6}

In the complete 420-coordinate module, `dR,dL01,d(AH)` have rank three.
Adding `dR01` does not raise it, but is required to exhibit (6). Modulo
`dR`, the residual is the 384-term `d(R-R01)`.

A literal separator puts `+1` on one local `B` direction derivative and
`-1` on one derivative outside `R01`. It kills `dR` and `d(AH)` but detects
`dL01`. Thus neither the complete response nor a single capped `DQ` section
silently supplies the first-PP chart comparison.

## Physical and terminal scope

An honest construction now has a precise shape:

1. build the three capped cells in their literal `DQ,PS,PS` Hasse objects;
2. glue their 18 residual-tail faces by the matching PP schema;
3. cancel the 18 endpoint/direction terms, in particular the six marginals
   (5), with one endpoint-even Spencer/cobar cell;
4. retain the 384-term complement coherently rather than projecting it away;
5. carry word/fine/repeated, physical `q`, `W`, and the labelled ridge.

Before this placement, physical `q`, `W`, and ridge values on the formal
cell are undefined. Eta/sigma are unique only after the labelled ridge is
physical. Therefore the coefficient separator and (5) are not yet accepted
terminals.

After the whole face is placed in an exhaustive same-grade augmented map,
`4373ae6` again gives the exact two-way outcome: protected-zero filler or
augmented terminal, with no third branch. This theorem identifies the first
proper face needed for that placement; it does not construct the endpoint
Spencer cell.

The checker runs normally, optimized, and isolated/no-site. Its frozen
ledger digest is recorded by the checker.
