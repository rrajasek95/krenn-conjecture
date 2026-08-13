# The complete response rows eliminate both sharp active-coloop traps

## Result

The closed triangle and nine-edge/singleton guards in `5ddaa7e` are not
complete unary-plus-response source packets.

Start with the literal coloop guard of `44cdd15`.  Its nonzero selected unary
monomials occur in the three mixed words

```text
000011: q01[00] q23[00] q45[11],
001100: q01[00] q23[11] q45[00],
001111: q01[00] q23[11] q45[11].
```

Impose all three zero unary coefficients and choose a cancelling matching mate
in each.  Of the `14^3=2744` choices:

```text
728   break the pure-zero coloop immediately;
288   add a literal occurrence to the pure-one R11 target row;
1728  use offdiagonal mates in all three words.
```

After retaining every cross-colour physical edge and every endpoint closure
certified by the existing `p1/s1` cells, `1580` of the last `1728` choices
leave all closed Hall shores.  The remaining `148` lie in a unique closed
nine-edge/singleton concept.  No closed-triangle packet survives the three
unary equations.

Checker:

```text
computations/verify_h3_active_coloop_closed_shore_complete_row_response_gate.py
```

## The hand identity behind the final response step

Put

\[
             a=p_1[0,1]s_1[1,1]\ne0 .
\]

The same fixed endpoint pair and the `23|45` tail occur in three target-zero
mixed response coefficients:

\[
\begin{aligned}
 R_{11}[110000]&=a\,q_{23}^{00}q_{45}^{00}+\text{other occurrences}=0,\\
 R_{11}[110011]&=a\,q_{23}^{00}q_{45}^{11}+\text{other occurrences}=0,\\
 R_{11}[111100]&=a\,q_{23}^{11}q_{45}^{00}+\text{other occurrences}=0. \tag{1}
\end{aligned}
\]

All three displayed products are nonzero in the pinned guard.  In every one
of the `148` trapped support packets, exhaustive inspection of the `729`
words in the unary and four response heads shows that the displayed term is
the **only** nonzero occurrence in its coefficient.  Consequently a full
source satisfying (1) must add at least one alternate response occurrence in
each row.  This uses only the elementary fact that a single nonzero monomial
cannot equal a zero target; it assumes no generic coefficients.

The structural response alternatives are small:

```text
R11[110000]: 2 alternatives,
R11[110011]: 8 alternatives,
R11[111100]: 2 alternatives.
```

For the first row the alternatives are the pure-zero tails `24|35` and
`25|34`.  With `alpha=q01[00]`, either supplies a second pure-zero target
matching through the literal coloop.  For the third row the same two tails
carry `10` decorations, hence are same-head two-cross response carriers
omitting `q01`.  In the middle row, two alternatives are the complementary
`01` two-cross tails at the same endpoints and six change the endpoint
occurrence.

This is the promised source-level asymmetry: each current row has one marked
occurrence, while its zero target forces a differently labelled occurrence.
It is deliberately not identified with the still separate pointed covector
`P_f`.

## The 32-way completion has no trapped shore

Select one required alternate occurrence in each line of (1).  There are

\[
                         2\cdot8\cdot2=32
\]

choices for every one of the `148` residual packets.  An alternate occurrence
certifies its `p1/s1` endpoint closure as an effective response hole; each of
its cross-colour `q` cells is an active physical hole.  These are precisely
the source labels used in `ab3e510` and in the pinned Hall-saturation theorem.

The exact `K_6` concept census gives

```text
148 * 32 = 4736 completed response seeds tested;
0 are contained in any of the 446 closed Hall shores.
```

If a coefficient has more than one alternate occurrence, choosing any one
from each row already yields this conclusion; extra certified edges cannot
restore containment.  Therefore every completion of a formerly trapped
packet forces strict Hall-closure growth.  It then enters the existing
outside-hole/active-fan descent.  No recursive reset at a relabelled coloop is
needed for this local packet.

## What this closes, and what it does not

The local recurrence now reads

```text
three mixed unary rows
  -> coloop escape / new pure-one target occurrence / all-offdiagonal packet
  -> all-offdiagonal outside growth, except 148 exact nine-edge shadows
  -> three private mixed R11 rows
  -> one of 32 labelled response seeds
  -> strict Hall growth in every case.
```

Thus the two sharp Hall traps from `5ddaa7e` are eliminated after the complete
rows are imposed.  The conclusion is an exact Hall/active-fan exit, not a
construction of the global fan-grade comparison or pointed `P_f`, and not a
claim that an intermediate Hall shadow alone is a full GHZ solution.

## Verification

Run

```text
python3 computations/verify_h3_active_coloop_closed_shore_complete_row_response_gate.py
python3 -O computations/verify_h3_active_coloop_closed_shore_complete_row_response_gate.py
python3 -I -S computations/verify_h3_active_coloop_closed_shore_complete_row_response_gate.py
```

Frozen ledger SHA-256:

```text
a9e19c224d7f6bd847ab964d30bec36da3a6cfaede72e8f9f301fb44fa9e0cec
```
