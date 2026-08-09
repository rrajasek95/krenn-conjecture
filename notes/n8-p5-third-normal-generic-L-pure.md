# N=8 P5 third-normal generic-L pure coefficients

## Result

The dense generic $L=0$ component has the first verified P5 pure survivor in
the checked recursion.  On the twice-bent localized graph,

- H1 degree nine reduces exactly to zero;
- H0 degree ten has a nonzero 52-term normal form.

This does not yet give a counterexample.  The graph is certified only through
mixed strict order six, whereas the surviving pure coefficient is computed
one normal layer beyond that certificate.  The degree-nine mixed tails and
strict-order-seven compatibility must still show that the generic $L$ branch
lifts rather than acquiring a new obstruction.

The exact checker is
`computations/verify_n8_p5_third_order_generic_L_pure.py`.  Its frozen ledger
has SHA-256
`26f163baa17af989a52a32e6908fd6041cc64b8aa5d2580fdbeafa71d6090353`.

## Exact reduction

The checker reuses the identity-safe third-normal construction and the
symbolic two-bend generic-$L$ graph.  It first reconstructs the five-term
first-bend equation and the 109- and 98-term second-bend equations.  Singular
then reduces the new pure coefficients modulo

$$
(L,F,b^{-1}(R_{30}-R_{33})),
$$

on the chart

$$
z_{16}z_{41}z_{11}b\ne0,
\qquad b=z_{44}+z_{45}.
$$

All four chart factors are inverted explicitly.  The localized ideal is
nonunit, and both original second-bend equations reduce to zero.

Before localization, the canonical $L$-remainders are:

- H1 degree nine: 10 terms, SHA-256
  `35af1b49d0717da1ce1a2e05c76b5011bde66c16b17b8b689d422c0d5d136576`;
- H0 degree ten: 1,024 terms, SHA-256
  `3ee772f336acedcbcdb3c467b4508545a924538e972ac76c4b009d4de23c7de0`.

The first reduces to zero.  The second reduces to a nonzero 52-term normal
form.  Its factorization contains the open factors
$z_{16}^2z_{41}z_{11}b$ and two additional nonzero factors, so saturation by
the stated chart factors does not remove the survivor.

## Interpretation and frontier

Together with the coordinate-component checkpoint, H1 now has no witness
through degree nine on any of the three checked P5 components.  H0 continues
to vanish through degree ten on $z_{16}=0$ and $z_{41}=0$, but not on the
generic $L$ component.  Thus a blanket P5 pure-membership pattern has broken:
the dense component is now the unique promising P5 lane.

The next decisive calculation is mixed strict order seven.  A successful
lift would promote the H0 normal form from a finite-order candidate to a pure
survivor on a longer compatible formal branch.  A new mixed equation could
instead cut out its nonzero locus.  Even after a successful finite lift, an
all-orders Hensel argument and a nonzero H1 coefficient would still be needed
for an actual counterexample.
