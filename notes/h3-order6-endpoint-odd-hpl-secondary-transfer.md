# The order-six `-delta` shadow is the physical secondary transfer

## Exact statement

Filter the complete bounded order-six operator module by the number of
coefficient-prolonging faces retained after endpoint recolouring.  The
filtration-zero map is literal output on the three quadratic source
products; the first map is the complete singleton Spencer face; the pair
projection is the second map.

The exact 343-term rational vector satisfies

```text
literal source output = 0,
first Spencer face    = 0,
pair projection       = -delta.
```

Therefore `-delta` is not merely the shadow of the earlier sparse
188-term choice.  It is a genuine secondary operation on the kernel of the
literal source and first-face maps.  In homological-perturbation notation it
is

\[
 D_2=-p\,\partial h\partial i,
 \qquad D_2[\Theta_6]=[-\delta],                       \tag{1}
\]

while `D1=p partial i` vanishes on the selected class.  The augmented HPL
lemma proves that (1) is well defined on `D1` homology; changing a first-page
representative changes `D2` only by a `D1` boundary.

This is a source-provenance result inside the actual 8,580-column physical
operator block.  The columns are quadratic-coefficient order-six operators
acting on the literal source products; no formal fourth-Hasse symbol has
been adjoined to obtain (1).

## Word and augmentation gluing

The secondary shadow has two nonzero fine-word components.  The endpoint
recolouring theorem proves that their operator shifts become one common
source-module degree after the natural pure/mixed word degrees are included.
The simultaneous tail-colour Weyl element exchanges those components.

The endpoint-odd Cartan theorem then gives

\[
 K=(1-s)H_w,
 \qquad dK+Kd=(1-s)(w-1),                              \tag{2}
\]

with four-corner boundary `-delta`.  Every endpoint-even augmentation kills
`K`; hence `D`, `W`, target, anchor incidence, and the pure-Eq aggregate are
zero without additional corrections.  The complete order-six tower also
commutes strictly with the ridge class `-dOmega_v`.

Together these facts remove three former ambiguities:

1. the first face is not an invariant obstruction;
2. the two word pieces are not in incompatible module degrees; and
3. target/anchor protection does not require the Weyl action itself to fix
   the GHZ tensor.

## The remaining comparison is narrower

The theorem does **not** identify the bounded filtered operator module with
the complete repeated `P3+K2` physical correction complex.  That comparison
must still send

```text
D2 = -delta                    -> labelled ordinary residue,
the commuting ridge -dOmega_v -> eta/sigma terminal packet,
all endpoint-even rows         -> zero.
```

Thus physical descent is now one chain-map problem.  It is no longer a
search for a source correction, a word homogenization, a target
cancellation, or a compatible terminal character: the source secondary
operation, total word degree, protected rows, and terminal ridge are all
fixed.

The most direct next construction is a filtered comparison from the
complete principal-parts resolution of the three quadratic source products
to the literal augmented Jacobian/correction module.  Its associated-graded
map is forced by (1).  Failure at the next page is one relative Ext class;
if the physical terminal detects it, it is the relative-generator branch,
and if the comparison exists it supplies the desired `M_v`.

## Scope and verification

This proves the secondary-transfer interpretation in the complete bounded
operator module.  It does not construct the final operator-to-correction
comparison, prove terminal zero-indeterminacy, or land the resulting carrier
at transverse rank.

Run:

```text
python3 computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py
python3 -O computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py
python3 -I -S computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py
```

Frozen ledger SHA-256:

```text
85887afc1e4d409d533005f4cd2de667301fc40fa0c88af31077829fa744311a
```
