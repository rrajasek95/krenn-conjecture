# The two budget-thirteen charts have 47,530 relative states

## 1. Outcome

The nine one-chart normal forms from
[`shared-reciprocal-fullspan-budget-frontier.md`](shared-reciprocal-fullspan-budget-frontier.md)
do not collapse to a literal table of only \(9^2\) coefficient packets when
two reciprocal pairs share an endpoint.  Their exceptional residual sites
are distinguished, and only five residual sites are common.  After
quotienting those five sites, simultaneous target-colour relabeling, and
exchange of the two charts, the exact compatibility census contains

\[
                         \boxed{47,530}
\]

relative incidence states.

The upper-triangular count table for one-chart form indices `0,...,8` is

```text
       0    1    2     3    4     5     6    7     8
0    578  285  522  1368  684  1224  2448  684  1224
1          70  150   372  248   336   636  188   336
2              162   684  352   624  1224  346   624
3                   1040  960  1764  3528  960  1764
4                         360   908  1764  482   908
5                               938  3384  886  1720
6                                   3540 1764  3384
7                                         283   886
8                                               938
```

Thus the nine-form theorem is a sharp one-chart reduction, but target-axis
incidence alone does not provide the hoped-for 81-case global closure.
Relative placement and the actual transverse line remain genuine data.

The first exact support-shadow packet occurs in form pair `(0,6)`, at pure
matching multiplicity `(2,2,2)`.  Its maximal coordinate support has 130
localized cells and passes every 6,561 full eight-site support fibre:

\[
 \#\text{supported matchings}:\quad
 0:2268,\quad 2:2835,\quad 6:648,\quad 9:810.
\]

It is nevertheless coefficient-empty over \(\mathbb C\).  Three of its
2,832 mixed binomial equations form an odd Laurent circuit on eleven
localized cells.  This is the first exact algebraic obstruction beyond the
support shadow.  It closes the maximal 130-cell torus, not every proper
sub-support of the relative incidence state.

No genuinely coefficient-feasible shared full-span packet is established
here.

## 2. Relative-state encoding

For the deletion of `pq`, write its six residual records on
`C union {r}`; for the deletion of `pr`, write them on `C union {q}`.
A record is a three-bit target-omission mask together with the optional mark
for the unique transverse enlargement.  A relative state consists of

1. the distinguished record at `r` in the first chart;
2. the distinguished record at `q` in the second chart; and
3. the multiset of five ordered record pairs on the common set `C`.

Sorting the five pairs quotients `S_5`.  The checker then minimizes under
the six simultaneous target-colour permutations and chart exchange.  It
also reconstructs the one-chart orbit of each side, so the 47,530 states
partition disjointly into the displayed 45 upper-triangular entries.

This census is support-faithful for the coordinate-span forms.  At a marked
transverse plane, the coordinate support envelope must allow all three rows:
a noncoordinate plane can have a nonzero entry in every coordinate.  The
actual projective direction is therefore not encoded by the Boolean mask.
That is precisely why a purely incidence-level curvature conclusion would
overclaim.

## 3. The first semantic packet

Use sites

\[
                    p,q,r,C_0,\ldots,C_4=0,1,\ldots,7.
\]

The first packet has exceptional records `(000,000)` and common record
pairs

```text
(000,000), (000,001), (001,110), (011,100), (110,011*)
```

where `*` marks the transverse plane.  It belongs to form pair `(0,6)`.
The reciprocal head labels are

\[
 (a,c,b,d)=(0,1,0,0),\qquad
 A_{pq}=E_{00},\quad A_{pr}=E_{01}.
\]

Common-core blocks use the intersection of the two endpoint envelopes;
`q-C` blocks use the second chart, `r-C` blocks use the first chart, and the
`p-C` and opposite-chord blocks remain arbitrary.  This reconstructs exactly
130 admissible cells.  Localizing all 130 gives the matching histogram in
Section 1, including exactly two pure matchings in each target colour and no
mixed singleton.

There are 4,293 nonzero coefficient generators: three pure trinomials,
2,832 mixed binomials, 648 six-term rows, and 810 nine-term rows.

## 4. The odd Laurent circuit

For a word \(w\), let its two matching monomials be \(M_w^0,M_w^1\), and
put \(d_w=\exp M_w^0-\exp M_w^1\).  The three frozen mixed words are

\[
 u=00001111,\qquad v=00001021,\qquad z=00000010.
\]

Direct matching enumeration gives exactly two supported monomials for each,
and the checker verifies

\[
                         d_u-d_v+d_z=0.             \tag{1}
\]

Their exactness equations are

\[
 M_u^0+M_u^1=M_v^0+M_v^1=M_z^0+M_z^1=0.             \tag{2}
\]

Every cell in these six monomials is among the eleven named localized cells.
Dividing (2) in the Laurent torus gives

\[
 x^{d_u}=x^{d_v}=x^{d_z}=-1.
\]

Equation (1) therefore reads

\[
                         1=(-1)^{1-1+1}=-1,
\]

which is impossible over \(\mathbb C\).  The characteristic-not-two scope
is explicit; no characteristic-two conclusion is claimed from this circuit.

## 5. Reproduction and remaining gate

Run

```bash
python3 computations/verify_shared_reciprocal_budget13_overlap_frontier.py
python3 -O computations/verify_shared_reciprocal_budget13_overlap_frontier.py
```

Both modes reproduce ledger

```text
631187d58b99962e61bc1a5cb52d90e805e73ba085762b705bc631117450a505
```

The checker is solver-free.  It pins the one-chart frontier, reconstructs
all 47,530 relative states, checks all 6,561 support fibres of the first
semantic packet, and audits the Laurent exponent identity directly from the
six source monomials.

The remaining proof-critical gate is no longer honestly described as a
bare `9x9` classification.  One needs either

- a projective compatibility lemma coupling the transverse directions on
  the five common sites and forcing curvature/cubicity; or
- an algebraic obstruction stable under deleting cells from the first
  semantic packet and transportable across its relative-state orbit.

Continuing maximal-support faces one at a time would not provide that
uniform statement.
