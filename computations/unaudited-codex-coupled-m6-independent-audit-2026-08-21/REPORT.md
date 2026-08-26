# Independent coupled-m6 column-star audit

The explicit column-star family is not an admissible GHZ/no-cap arc.

The checker rebuilds its 40 nonzero endpoint-ordered source cells over
`Q(w)[t]`, with `w^2+w+1=0`, and directly enumerates all 105 matchings for all
6,561 output words.  It imports none of the derived `E2/E3/E4` formulas.

There are 30 nonzero mixed coefficients below order six.  The first by
`(order,word)` is

`[t^2] H_00111000 = 4`.

Among the specifically omitted orders four and five, eight order-four and
four order-five coefficients are nonzero.  The lexicographically first word
is

`[t^4] H_00110111 = 2`.

The full 30-row packet and the complete order-4/5 packet are frozen in the
JSON result.  As a positive control, the literal pure replay reproduces
`[t^6]H_11111111=-12`; the other two pure amplitudes vanish.

All 72 carriers active with rank zero at the base were independently
recovered.  Their polynomial response ranks over `Q(w)(t)` range from one to
three.  All 288 memberships against `K00,K11,K22` and the literal direct-pair
blocker were tested.  Eighteen carriers remain active over `Q(w)(t)`, so the
family also fails the no-cap requirement independently of the mixed-word
obstruction.  For every nonmembership the result stores a lexicographic
augmented minor and its exact leading term; exact memberships are marked as
such.

Standard, optimized, and isolated Python runs agree on logical digest
`166c565d8091e63d120451eaa8e80b1ad525da4c093661fc10e043287f29290d`.

