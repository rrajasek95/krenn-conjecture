# The hidden root-even debt is not a Cartan/Mv endpoint bar

The physical descent of the generic even reduced-Eq face leaves the proposed
raw-cell debt

\[
 H=(\operatorname{lower},\operatorname{Eq},\operatorname{ores})
   =(-E,0,+E),\qquad
 E=2D_{\rm root}\otimes {B_1+B_4\over2}.
\]

The checker
[`verify_h3_cplus_hidden_debt_cartan_mv_root_bar_span.py`](../computations/verify_h3_cplus_hidden_debt_cartan_mv_root_bar_span.py)
tests whether physical Cartan, `M_v`, or a sigma-paired root-word bar can
supply this debt while retaining all 24 root-word/pure-label coordinates.

## A stronger-than-physical span

Grant independently in every one of the 24 coordinates both

\[
 K_u=(0,0,u),\qquad M_u=(u,u,0).
\]

This is stronger than granting all physically placed `K_alpha` and `M_v`
packets. Its span is exactly

\[
             \{(x,x,z):x,z\in\mathbf Q^{24}\}.              \tag{1}
\]

The boundary of a root-word bar between any two such endpoints is their
difference, so it remains in (1). The checker explicitly adjoins all
endpoint differences for the paired-root action and the physical cross-cut
transition

```text
(B0 B5 B3 B2)(B1 B4).
```

The rank stays 48. Thus neither endpoint parity nor coarse cancellation
enlarges the full-row span.

For each root word, put

\[
 \chi=(0,1,-1,0,1,-1),\qquad
 \lambda_r=(e_r\otimes\chi)_{\rm lower}
             -(e_r\otimes\chi)_{\rm Eq}.
\]

Every `lambda_r` kills (1) and every adjoined bar boundary. On `H`, their
pairings are

```text
+2, -2, +2, -2.
```

Therefore `H` raises the rank by one even after the universal endpoint
grant. This lower-minus-Eq obstruction is independent of the labelled
residue obstruction in `6c5303c`.

## Exact reduction, not a new operation type

Formally,

\[
                 H=-M_E+K_E+C_{\rm Eq},               \tag{2}
\]

where

\[
 M_E=(E,E,0),\qquad K_E=(0,0,E),\qquad
 C_{\rm Eq}=(0,E,0).
\]

Equation (2) is useful because it names the two actual obligations.

- `K_E` is precisely the root decoration of a pure
  `d_even=(B1+B4)/2` labelled ordinary-residue section. Commit `6c5303c`
  proves that Cartan parity does not manufacture this section.
- `C_Eq` is the clean objectwise reduced-Eq comparison. It is the pointed
  `K_Eq` comparison already isolated by the integral rho-orbit theorem.

So the attempted bar cancellation fails, but it exposes no third primitive
cell. The complete root-even descent reduces exactly to the existing
`d_even` labelled section and pointed `K_Eq` comparison. A bar on those
clean derived endpoints would be part of that comparison; a bar on the
already physical Cartan/Mv endpoints cannot construct it.

## Scope

The universal endpoint grant makes this a strict no-go for the proposed
Cartan/Mv/root-word-bar mechanism. It is not a no-go against an enriched
pointed comparison containing a clean Eq endpoint. Eta/sigma, ridge, target,
`W`, and anchor rows were generously omitted: restoring them can only shrink
the attempted endpoint span.

Run:

```text
python3 computations/verify_h3_cplus_hidden_debt_cartan_mv_root_bar_span.py
python3 -O computations/verify_h3_cplus_hidden_debt_cartan_mv_root_bar_span.py
python3 -I -S computations/verify_h3_cplus_hidden_debt_cartan_mv_root_bar_span.py
```

Frozen ledger SHA-256:

```text
18faa02b2b5fdab3862a91b62f117e010a12d89afdc1a4a7f15d1cd33bca6df1
```
