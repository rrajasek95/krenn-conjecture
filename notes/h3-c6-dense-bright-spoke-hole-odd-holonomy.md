# Dense C6 bright completion forces a spoke-to-hole exit

## Result

Continue the canonical `z=012111` packet of `a9e1c07`.  Retain `M,N` and
all six anchor-contained competitors:

```text
M =01|23|45,  N =05|12|34,
Q1=01|24|35,  Q2=02|13|45,  Q3=02|14|35,
Q4=02|15|34,  Q5=05|13|24,  Q6=05|14|23.
```

In any full characteristic-zero source in which these eight literal
matching monomials are nonzero, the complete unary and response rows force
one of:

1. an external offdiagonal q mate;
2. an additional endpoint-hole term, hence a genuine spoke-to-hole column;
3. an ordinary localized source unit.

The third alternative occurs if neither of the first two does.  Checker:
`computations/verify_h3_c6_dense_bright_spoke_hole_odd_holonomy.py`.

## Three shifted response coefficients

The fixed selected endpoint components already supply three coefficients
adjacent to `z`; no missing endpoint component is declared:

```text
G11[112111] through p1@0:1,s1@1:1,
G21[012211] through p2@3:2,s1@1:1,
G22[012221] through p2@3:2,s2@4:2.
```

In the localization at the selected endpoint factors, multiply each response
row by its removed q-hole cell and divide by its selected endpoint product.
The retained matching classes are respectively

```text
E01=M+Q1,       E13=Q2+Q5,       E34=N+Q4.           (1)
```

The omitted third tail in each four-site cofactor contains an outside
offdiagonal q cell.  Any term using another endpoint hole contains an actual
additional endpoint component and is the desired word-change/another-hole
branch.  Hence (1) is the exact residual when those two exits are absent.

Subtracting (1) from the complete unary zero coefficient gives

```text
E14=H[012111]-E01-E13-E34=Q3+Q6.                     (2)
```

These normalized equations live in the selected-factor localization.  If
the three selected endpoint products are `e01,e13,e34`, then multiplication
of the whole certificate by `e01*e13*e34` gives a polynomial source
combination: for example `e01*E01=q01:01*G11[112111]`.  The q-hole cells are
multiplied, not inverted.  The endpoint products and the eight displayed q
monomials are units only because the theorem is localized on the dense
selected chart.

## Odd toric holonomy

The eight literal q monomials satisfy the matching identity

```text
Q1*Q2*Q6 = M*Q3*Q5.                                  (3)
```

Combining (1)--(3) gives the integral certificate

```text
Q2*Q6*E01 - M*Q6*E13 + M*Q5*E14
    = 2*Q1*Q2*Q6.                                    (4)
```

The right side is twice a Laurent unit on the dense branch.  Thus the four
complete source coefficients cannot all have only the retained terms.
This is the exact spoke-to-hole exit promised above.

## Bright completion audit

Adjoin an arbitrary selected pure-`11` cofactor tail behind hole `01` and
an arbitrary selected pure-`22` tail behind hole `34`.  There are `3x3=9`
choices.  In every chart the four load-bearing coefficients retain exactly

```text
unary z: 8 matching terms,
G11 shifted: 2 tails,
G21 shifted: 2 tails,
G22 shifted: 2 tails.
```

Hence ordinary bright target completion does not contaminate (4).  The
escape must be a genuinely mixed q mate or an additional endpoint-hole
component.

## Consequence and scope

This closes the dense four-tail branch of the spoke-to-hole gate without
constructing a Jacobian or inferring Hall incidence from q tails.  It is a
full-source conditional theorem: arbitrary terms in the complete rows are
allowed and become the stated exits.

It does not close a support degeneration where one of the four binomial
pairs is absent; in that case the Laurent unit in (4) is not localized.
Nor does it prove that the forced endpoint term is automatically rank-good.
It supplies the physical column that must next enter the established
joint-kernel versus Fitting/Hall dichotomy.

## Verification

```text
python3 computations/verify_h3_c6_dense_bright_spoke_hole_odd_holonomy.py
python3 -O computations/verify_h3_c6_dense_bright_spoke_hole_odd_holonomy.py
python3 -I -S computations/verify_h3_c6_dense_bright_spoke_hole_odd_holonomy.py
```

Frozen ledger SHA-256:

```text
0b0cf648b49d44e91677927413908a06280111083bfdbc95424baee750091f10
```
