# The endpoint-chart scalar splits into a capped C4 and a block projector

## Exact coefficient reduction

For the representative chart put

\[
 A=Dq_{01},\qquad B=p_0s_1,\qquad C=p_1s_0,
\]

and

\[
 H=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.
\]

The pointed chart audit `d1b8ec4` identifies the first proper face as

\[
                    L_{01}=(2A-B-C)H.                 \tag{1}
\]

The same nine occurrences form the literal local response block
`R01=(A+B+C)H`. Therefore, coefficientwise,

\[
              \boxed{L_{01}=3AH-R_{01}}.              \tag{2}
\]

Checker:
[`verify_h3_h2_chart_scalar_capped_c4_augmented_gate.py`](../computations/verify_h3_h2_chart_scalar_capped_c4_augmented_gate.py).

This identity has a crucial scope guard. `R01` is only nine terms of the
complete 105-term response polynomial:

\[
                         R=R_{01}+R_{\rm rest},
 \qquad |\operatorname{supp}R_{\rm rest}|=96.          \tag{3}
\]

The checker works in all 105 literal occurrence coordinates. The three
vectors `R,L01,AH` have rank three, not two. Modulo the complete response,

\[
       [L_{01}]-3[AH]=[R_{\rm rest}].                 \tag{4}
\]

A separating covector puts `+1` on one local `B` occurrence and `-1` on one
outside occurrence. It kills `R` and `AH` but reads `-1` on `L01`. Hence a
capped symmetric-C4 section alone cannot land the chart scalar. Isolating
the nine-term block is an additional source operation.

## What a positive construction must do

Second Hasse restriction in the directions `(D,q01)` sends `AH` to `H`.
Consequently the lower column isolated by `dc7c7ef`,

```text
U_C4[D,Q01;2345]  ->  H,
```

is the correct lower seed. It is not yet the scalar chart-reset cell. One
must cap/reinsert it by the two removed factors. Write the required cell as

```text
Uhat_C4 = (D*q01) cap U_C4.
```

Its principal-parts differential has the literal Leibniz form

\[
 \delta((Dq_{01})U)=Dq_{01}\delta U
   +(\delta D)q_{01}U+D(\delta q_{01})U.              \tag{5}
\]

The first term gives `AH`; the latter two are independent proper faces. A
formal coefficient reinsertion simply discards them. A physical PP chain
map must cancel them in the same word/fine/repeated object. No pinned cell
does so.

Even after those two faces are cancelled, (4) leaves `Rrest`. Thus the
smallest positive datum is either

1. the capped `U_C4` together with a source-valid projector onto `R01`; or
2. one combined pointed endpoint-chart cell having boundary `L01` directly.

The second description is exactly the graph coordinate `u01` in
`d epsilon01=L01-u01` from `d1b8ec4`. The first description explains its
two logically independent pieces: symmetric-C4 reinsertion and occurrence
block isolation.

The unit case in `4e2ff27` is consistent with the lower half of this description: it
constructs the lower symmetric-C4 section only when the entire retained
core—including its direction/reinsertion data—has a same-grade inverse. In
the general flat branch the one Tor/colon line survives. It does not supply
the nine-term occurrence projector, so even its unit branch must still be
combined with that projector before (2) becomes a physical response-row
identity.

## Why target safety is not enough

The site permutation has zero GHZ target defect and (1) has occurrence
augmentation zero. Neither statement assigns the augmented values of the
new cap. Before `Uhat_C4` is a physical column, the following remain
independent:

```text
word/fine/repeated landing,
anchor/ainc and physical q,
W,
the labelled shifted ridge,
eta and sigma.
```

The response-KS audit shows a five-dimensional ambiguity already after the
unaugmented differential is fixed: `ainc/q`, `W`, labelled ridge, `eta`, and
`sigma`. The formal anchor relation does not remove that ambiguity.
Eta/sigma become unique contractions only after a labelled physical ridge
has been placed.

Thus the honest site permutation is a chain isomorphism between response
charts, but it is not a termwise PP endomorphism of the fixed augmented
chart. Its first failure is the pair consisting of the block projector and
(5), before a physical `q`, `W`, ridge, or terminal value is defined.

## Exact terminal scope

After a same-grade physical placement, `4373ae6` is decisive. If `mu_j` are
the induced values of a local dual on the four cap corners, its extension is

```text
q = ainc = Eq = 0,
target_j = -mu_j,
W_j      = -mu_j,
ores_j   =  mu_j,
ridge    = -sum_j alpha_j mu_j,
alpha    = (-1,1,1,-1).
```

On an exhaustive physical relative map there are then exactly two cases:
the placed scalar has a protected-zero filler, or the displayed extension
is an augmented terminal. There is no third branch.

This implication cannot be reversed. Before the cap/reinsertion is placed,
the coefficient dual `L01/18` lives only on the formal response output. A
formal `q` defect may then have no witness in the physical domain, so it is
neither a relative generator nor a Fredholm terminal. This is precisely the
premature-promotion counterguard in the pinned response-KS audit.

## Shortest remaining theorem

Construct one combined pointed cell which

- has lower boundary `H` and top boundary `AH`;
- cancels both proper faces in (5);
- isolates the nine-term `R01` block inside the complete response;
- retains the literal word/fine/repeated labels; and
- carries physical anchor/`q`, `W`, labelled ridge, eta, and sigma data.

Then (2) lands the chart scalar without treating `R01` as a source row, and
`4373ae6` closes it by filler or terminal. The current result is an exact
two-piece decomposition of that cell, not its construction.

Run normally, optimized, and isolated/no-site. The frozen ledger digest is
recorded by the checker.
