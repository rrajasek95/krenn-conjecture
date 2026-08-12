# The first bright target coefficient forces a two-decoration unary mate

## Result

Start from the rational silent-C6 zero fibre in `69e2417`. Normalize one
pure-colour matching in each missing bright cofactor:

```text
X1 in H_01:  23|45, 24|35, or 25|34,
X2 in H_34:  01|25, 02|15, or 05|12.
```

Every one of these six matchings contains an edge $e$ whose deleted
pure-zero cofactor in the common $q$ is nonzero. Consequently the unary
coefficient whose word has the bright colour exactly at the endpoints of
$e$ is nonzero. Since the target unary tensor is pure $X_0$, a full source
completion must supply a distinct cancelling matching omitting $e$.

Every such matching has exactly two off-diagonal decorated cells. Thus the
first bright layer gives the exact split

\[
\boxed{\text{a missing chord }q_{04}/q_{13}
       \quad\text{or a distinct two-decoration unary mate}.}       \tag{1}
\]

It does not force a chord or a same-star kernel individually: every active
edge has chord-avoiding mate topologies. Among the nine simultaneous bright
matching pairs, the pair

```text
X1 = 25|34,       X2 = 01|25
```

keeps both crossed response tensors zero before its forced unary mates are
added. This is the sharp first-layer residual.

Checker:
`computations/verify_h3_silent_c6_first_bright_unary_escape.py`.

## Literal coefficients

For a bright edge $e=uv$ of colour $c\in\{1,2\}$, let $w(e,c)$ be the
six-site word equal to $c$ at $u,v$ and zero elsewhere. With only the
normalized bright cell on $e$, its unary coefficient is

\[
[w(e,c)]q^{[3]}=q_e^{cc}H_e^{00}.                       \tag{2}
\]

On the frozen rational common $q$, the deleted cofactors on the six choices
are:

```text
X1 23|45: H23=-5, H45= 3
X1 24|35: H24=-1, H35=-1
X1 25|34: H25=-7, H34= 0

X2 01|25: H01= 0, H25=-7
X2 02|15: H02=-1, H15= 1
X2 05|12: H05= 5, H12= 3.
```

Hence every matching has at least one nonzero coefficient (2). These values
are complete two-edge hafnians, not selected matching terms.

If a perfect matching $N$ omits $e$, the two sites of $e$ must be paired to
two zero-coloured sites. Therefore $N$ contains exactly two $c0/0c$
decorations; its third edge is `00`. This parity statement proves the
two-decoration conclusion in (1) without a support census.

For regression, the checker enumerates all twelve matchings omitting each
active edge. Seven or eight of them, depending on $e$, avoid both physical
chords `04` and `13`. Therefore the unary equation alone cannot strengthen
(1) to “one missing chord is nonzero.”

## Simultaneous bright-pair audit

The checker adjoins each of the three $X_1$ and each of the three $X_2$
matchings to the same rational zero fibre and expands both crossed response
tensors. Eight of the nine pairs immediately have a nonzero crossed
coefficient. The sole crossed-dark pair is

```text
X1 = 25|34,       X2 = 01|25.
```

It still has the nonzero unary coefficient $H_{25}^{00}=-7$ in both bright
colours. Thus even the crossed-dark case must acquire a distinct
two-decoration unary mate. Routing those new decorated cells to a
same-star dependence, an off-anchor carrier, or a later decorated-anchor
exchange is the next source-provenance step.

## Scope

- The result is exact for the first bright completion coefficient over the
  rational guard of `69e2417`.
- It uses the full unary target, not an aggregate support inference.
- “Distinct mate” means a new decorated matching monomial in the unary
  coefficient. Its physical edges may still lie in an anchor union; no
  off-anchor landing is claimed here.
- The result neither constructs a full one-bad packet nor claims that the
  first mate alone completes the five-lock kernel/wedge alternative.

## Verification

```text
python3 computations/verify_h3_silent_c6_first_bright_unary_escape.py
python3 -O computations/verify_h3_silent_c6_first_bright_unary_escape.py
python3 -I -S computations/verify_h3_silent_c6_first_bright_unary_escape.py
```

Frozen ledger SHA-256:

```text
cffcaf1f7946df044e889d9dee25304da93eb3d15eaaf0889fcb970625076c3e
```
