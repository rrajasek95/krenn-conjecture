# The first forced `11`/`22` escape has an ordinary unit

## Exact theorem

Let $H$ be the fixed weighted fourteen-cell Segre--K4 quadratic from
`772290e`.  Add

- arbitrary pure-zero cells on all fifteen physical edges;
- exactly two disjoint `11` cells; and
- exactly two disjoint `22` cells.

No such quadratic can satisfy the mixed top equations together with even
one of the corresponding diagonal response anchors.  In particular it
cannot satisfy the unary top and all four one-bad responses.

This closes the minimal escape forced by `0533765`.  There is no
coefficient-feasible packet at this carrier layer.

## Literal unit identity

Fix one colour $c$.  Write $a_c,b_c$ for the coefficients of its two
disjoint `cc` cells, and let $u,v$ be the two uncovered response holes.
Because these are the only `cc` cells, the coefficient of the pure response
word is exactly

\[
 [p_c s_c q^{[2]}]_{c^6}
  =a_cb_c\bigl(p_c(u)s_c(v)+p_c(v)s_c(u)\bigr).
\]

Put the parenthesized two-hole pairing equal to $L_c$.  The diagonal
response equation is therefore

\[
                         R_c=a_cb_cL_c-1=0.            \tag{1}
\]

For every carrier placement, a literal mixed top word $w_c$ has coefficient

\[
                         g_{w_c}=\epsilon_c P_c,       \tag{2}
\]

where $\epsilon_c=\pm1$ and $P_c$ is one of $a_c,b_c,a_cb_c$.  Thus $P_c$
divides the full carrier product.  Equations (1)--(2) give the ordinary
polynomial identity

\[
 R_c-\frac{a_cb_c}{P_c}\frac{L_c}{\epsilon_c}g_{w_c}
                              =-1.                    \tag{3}
\]

There is no localization or radical inference in (3).  It is a literal
unit certificate in the source coefficient ring.

## Complete placement audit

Two disjoint edges on six sites leave a pair of holes.  Hence there are

\[
                    \binom62\cdot3=45
\]

placements for each colour and $45^2=2025$ paired charts.  The actual
decorated **weighted** stabilizer of $H$ is trivial, so no quotient was used.
The exact witness degrees are

| degrees $(\deg P_1,\deg P_2)$ | charts |
|---|---:|
| `(1,1)` | 1089 |
| `(1,2)` | 396 |
| `(2,1)` | 396 |
| `(2,2)` | 144 |

Every chart has a unit certificate for colour 1 and independently for
colour 2.  The checker
`computations/verify_n8_one_bad_segre_cube_first_mixed_escape_unit.py`
retains every site, physical matching, endpoint colour, top word, and sign.

## Consequence and scope

The pure-additive chart was already excluded by `76e5f56`, while `0533765`
showed that the responses force two disjoint carriers in each nonzero
colour.  The theorem here proves that adding exactly those four carrier
cells still cannot escape: a mixed top singleton (or carrier product) meets
the diagonal response in a unit.

This uses only a mixed top row and a diagonal response; the unary coefficient
and crossed-zero responses are unused.  It is exact for the fixed weighted
$H$, arbitrary pure-zero coefficients, and exactly four added pure nonzero
cells.  It does not exclude deformations adding further `11`, `22`, `12`,
or `21` cells, and it is not a proof of one-bad emptiness or Krenn's
conjecture.

