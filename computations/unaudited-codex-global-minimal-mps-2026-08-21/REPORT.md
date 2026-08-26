# Global minimal matching automaton / MPS audit

Status: **exact bounded no-go for the output-only minimal-MPS route**.

For an ordered cut, the literal source automaton has basis `(S,alpha)`, with
`S` the processed unmatched sites and `alpha` their physical colours.  On
reading colour `c` at site `j`, a transition either opens `(j,c)` or closes
`i in S` with weight `A_ij[alpha(i),c]`.  Its cut factorization is exactly
`H_k=R_k O_k`; reachable/observable minimization therefore has dimension
`rank(H_k)` and gives the diagonal three-state copying automaton for GHZ.

The exact `n=4` GHZ source exposes the loss of matching geometry.  All three
internal ranks are three and the quotient transitions are diagonal, but at
the middle cut its three colour states have crossing-edge counts `(0,2,2)`.
This holds for all 24 site orderings.  Thus no ordering turns the canonical
three states into one common closed pair or uniform two-site deletion.

For the frozen `n=8` Laurent family, the generic cut ranks are

```text
3,5,5,5,4,4,3,
```

and the GHZ special fibre has rank three at every cut.  At cut two the pure
zero channel has forward/backward orders `(-N,+N)` after the allowed
valuation redistribution, while both mixed output channels have order `N`.
Normalizing the GHZ channel uses `diag(t^N,1,1)`, a state gauge singular at
`t=0`.  Exact controls at `N=1,2,7` show that minimalization loses arbitrarily
large source valuations and the two positive-order mixed channels.

Finally, adding the frozen invisible chord `02` to
`01|23|45|67` creates the cut-three reachable state `{1:0}`.  It is
unobservable, so both sources have the same output, essential states, and
rank-one minimal automaton.  The quotient erases exactly the literal edge
whose deletion gives support descent.

Consequently the canonical automaton does not control the remote idempotent
and does not itself force a cap, a uniform six-site matching quotient, or
identify a literal deletion.  A useful successor would have to prove a new
source-relative **kernel-lifting lemma**: every killed direction in a
support-minimal exact source lifts to either a deletable coordinate or an
active cap.  Minimal-MPS uniqueness alone supplies no such lift.

Standard, optimized, and isolated/no-site modes agree at logical SHA
`5d8113de212fb6c79f9084eab11afbfcf092466af3ccdddcec776f9306ff90f2`.

## Minimum-norm/block-normal upgrade: still negative

Minimum norm does delete the old invisible chord: its complementary
six-site tensor is zero, so the single-edge block equation forces the chord
itself to vanish.  This does not make the whole top-Hankel radical
block-affine.  For a cut `k`, a radical vector `r` satisfying `O_k r=0`
lifts to `ker L_E` only when all histories in `r` have a common remainder and
differ solely in one intersecting edge block `E`.  General partial-matching
history cancellations do not have that form.

The exact `n=4` GHZ source is already decisive.  It is a global norm minimum:
for each colour, Cauchy--Schwarz and AM--GM give source cost at least two from
the normalized pure Hafnian, and the displayed source attains total norm
squared six.  Every one of its four star maps and four triangle maps is
injective of rank `27/27`, so every block-normal equation is vacuous.
Nevertheless prefix `01` at the middle cut reaches the literal state

```text
{(0,0),(1,1)},
```

and every one of its nine suffix completions is zero.  The state is reachable
and unobservable, contains no edge coefficient, and cannot be a star or
triangle affine-kernel component.

The phased six-site smooth local-minimum model supplies an independent hostile
control.  It has injective star and triangle maps over `F_7`, while its exact
cut census `(reachable rank, Hankel rank, radical dimension)` is

```text
(3,3,0), (9,9,0), (27,25,2), (51,9,42), (15,3,12).
```

One cut-three radical is the image of

```text
4|012> + 6|022> + 5|110> + 2|112> + |120>  over F_7.
```

Thus exact minimum norm and all star/triangle block-normal equations still do
not upgrade the three-state GHZ quotient to a source-faithful clean-pair
detector.  They kill single-edge inactive material but not global
history-cancellation radicals.
