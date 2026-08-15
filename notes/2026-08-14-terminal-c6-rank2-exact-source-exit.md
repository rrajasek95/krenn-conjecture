# A closed rank-two `C6` transfer cannot carry the three pure source rows

## Outcome

The tight-`C6` counterguard in `bf8ccd3` does not survive the first exact
source obligations.  Its two labelled boundary cofactors are independent,
but its evaluated six-site tensor has Schmidt rank one across the displayed
odd cut, supports only the colour-0 pure row, and already has the two mixed
singleton rows `000011` and `000110`.  It is a valid guard against automatic
common-tail factorization, not an exact source packet.

There is a uniform local replacement for that negative example.  Let a
source-labelled diagonal terminal component have underlying support

```text
01 12 23 34 45 50
```

and suppose all compatible occurrences factor through its two perfect
matching channels

```text
A = 01|23|45,                 B = 05|12|34                 (1)
```

with one common nonzero cofactor tail.  If all three normalized pure rows
are carried by this component, then it has at least six mixed debts.  Each
debt is one of the following exact exits:

1. a `2+2+2` word, which is a singleton even after completing the local
   graph to `K6`; or
2. a `4+2` word, which is a singleton unless one of exactly two crossed
   `C4` mates is active.

Thus a genuine rank-two `C6` boundary transfer cannot be silently
contracted.  It either loses a normalized pure row, exposes a mixed
singleton, or forces a new `C4`/outside-tail transfer.  If the effective
transfer drops to a row-independent rank-one common tail, the reinsertion
lemma of `bf8ccd3` applies and the component can instead be collapsed.

The exact checker is
`computations/verify_uniform_terminal_c6_rank2_exact_source_exit.py`.

## 1. Why the literal guard is not a source

The six-cycle has the tight odd shore

```text
L = {0,1,2},                  delta(L) = {23,05}.
```

In the `bf8ccd3` support, each cut edge carries only its colour-0 diagonal
cell.  Direct expansion of all 729 words and all 15 perfect matchings of
`K6` gives

```text
pure multiplicities              (2,0,0)
mixed singleton words            000011, 000110
rank across 012 | 345            1.
```

The last rank is the ordinary evaluated tensor-flattening rank.  It does
not contradict the earlier statement that the labelled boundary transfer
has rank two: the `23` channel retains shore cofactor `q01`, while the `05`
channel retains the distinct cofactor `q12`.  Those are independent formal
occurrence states, but both displayed word tensors lie over the same left
word `000`.  The checker records both ranks explicitly so they cannot be
interchanged.

The ternary GHZ flattening across any nontrivial shore has rank three.  Hence
the literal guard, or any global packet factoring through only its evaluated
image, cannot be an exact source.  A contraction cannot repair this defect:
quotienting or deleting boundary states cannot increase flattening rank.
An exact source must add an independent transfer channel or abandon this
closed component.

## 2. Closed-`C6` pure-support theorem

For a cycle edge `e`, let

\[
                     S_e\subseteq\{0,1,2\}                 \tag{2}
\]

be its nonempty set of live diagonal colours.  Put

\[
 C_A=S_{01}\cap S_{23}\cap S_{45},\qquad
 C_B=S_{05}\cap S_{12}\cap S_{34}.                         \tag{3}
\]

A constant-colour occurrence exists in the closed component precisely when
its colour lies in \(C_A\cup C_B\).  Therefore the three pure normalization
conditions imply

\[
                      C_A\cup C_B=\{0,1,2\}.                \tag{4}
\]

By pigeonhole, one of the two channels contains at least two pure colours.
Suppose it is `A` and contains colours \(b,c\).  Since every one of its
three edges carries both colours, the Cartesian product

\[
                     \{b,c\}^3                              \tag{5}
\]

contains its two pure decorations and six mixed decorations.  The union of
the two matchings in (1) is connected.  A word compatible with both is
therefore constant.  Consequently all six mixed occurrences in (5) are
singletons inside the closed `C6`.

This proves the first exact dichotomy:

> If a nonempty diagonal `C6` has no mixed singleton occurrence, it supports
> at most two of the three pure colours.

The checker exhausts all

\[
                           7^6=117649                         \tag{6}
\]

nonempty cycle-cell supports.  Exactly 3,037 support all three pure words,
and every one has at least six mixed singleton occurrences.  The bound is
sharp.  There are six sharp supports, one orbit under `D12 x S3`, represented
by

```text
01:0  23:0  45:0,           05:12  12:12  34:12.            (7)
```

This is also the conceptual minimum: one channel carries one pure colour,
and the other carries the other two.

## 3. The only local mates are crossed `C4` flips

The preceding singleton statement concerns the closed cycle.  Full source
exactness can try to repair a mixed row by adding other six-site occurrences.
Their form is rigid.

If the three edge colours on one channel are all distinct, the word has
type `2+2+2`.  In the complete graph every colour class is a prescribed
pair, so its compatible perfect matching is unique.  No local support
augmentation can mate it.

Otherwise the word has type `4+2`.  Its minority-colour pair must occur in
every compatible matching.  On the four majority-colour vertices there are
exactly three pairings: the original channel pairing and its two crossed
pairings.  Hence there are exactly two possible mates.  Each retains the
minority edge and changes the other two edges on one primitive `C4`; in the
sharp support (7), each mate requires exactly two new live cells.

This classification is coefficient-independent.  A live singleton is a
nonzero product and cannot vanish.  If an exact mixed row cancels it while
retaining the same tail, at least one of the two labelled `C4` alternatives
must be active.  If the mate uses a different tail or crosses the component
boundary, that is instead an explicit outside-transfer channel, so the
`C6` was not terminal.

The forced local object is an active binary **matching face**: the selected
term and one crossed `C4` term.  Graph data alone do not identify it with the
previous complementary-colour clean-cap polynomial

\[
                K_{bb}K_{cc}+K_{bc}K_{cb}.                         \tag{8}
\]

In the `C6` debt, both flipped edges carry the majority colour.  Promotion
from this monochromatic `C4` face to the framed active-clean cap in (8)
still needs a response/anchor compatibility theorem.  This is the sharp
remaining hypothesis; calling every crossed matching pair a clean cap would
overstate the result.

## 4. The first complete repair layer remains open-ended

For the sharp representative (7), the six initial debts are

```text
111221  122111  122221  211112  211222  222112.             (9)
```

Each has two possible crossed mates.  Choosing one mate for each debt gives
64 minimal repair packets.  In every choice the six mates require twelve
distinct new cells; no two debts share a repair cell.  The complete labelled
mate ledger is

```text
debt     crossed mate 1       crossed mate 2
111221   01;1 25;1            02;1 15;1
122111   03;1 45;1            04;1 35;1
122221   13;2 24;2            14;2 23;2
211112   13;1 24;1            14;1 23;1
211222   03;2 45;2            04;2 35;2
222112   01;2 25;2            02;2 15;2.                   (10)
```

Complete expansion after the additions gives the new singleton-count
histogram:

```text
 6:3   8:6   10:6   15:8   17:12   18:1
19:6  23:6   24:7   28:3   30:6.                              (11)
```

In particular, all 64 minimal repairs still fail an exact mixed row, and the
best three still carry six singleton debts.  This is a finite monotonicity
check for the first mandatory face layer, not a claim that arbitrary later
support additions preserve the same debt count.

The independently committed diagonal-six-site support theorem in
`computations/verify_diagonal_n6_obstruction.py` rules out an entire exact
diagonal six-site source after all additions, using the full pure/cofactor
identities.  The present result is more local: it identifies precisely the
first occurrence-labelled exit forced by the `C6` boundary packet, without
importing that global terminal theorem.

## 5. Schmidt rigidity: what it proves and what it does not

Across a nontrivial cut, the GHZ tensor is

\[
 \Delta_3=e_0^{\otimes L}\otimes e_0^{\otimes R}
          +e_1^{\otimes L}\otimes e_1^{\otimes R}
          +e_2^{\otimes L}\otimes e_2^{\otimes R},                  \tag{12}
\]

so its flattening has rank three and its left and right images are the three
dimensional spans of the constant words.  This gives a useful necessary
condition: after quotienting true kernels, every exact boundary
factorization must retain effective rank at least three.

It does **not** force its individual internal states to equal the three
colour lines.  The checker takes

\[
 S=\begin{pmatrix}1&1&0\\0&1&1\\1&0&1\end{pmatrix},\qquad
 Q=S^{-1}S^{-T},                                                     \tag{13}
\]

and verifies exactly that

\[
                            SQS^T=I_3.                               \tag{14}
\]

Every column of `S` mixes two colour lines.  Thus even a minimal rank-three
factorization can be nonaligned.  Equation (14) is not claimed to be a
physical hafnian construction; it is a counterguard to deriving physical
colour alignment from Schmidt rank alone.  A source-natural contraction
must preserve the literal endpoint, colour, word, and cofactor labels, or
prove separately that the mixing in (13) is realizable by allowed source
operations.

## 6. Sharply scoped terminal-ear rank-drop lemma

Combining the common-tail theorem in `bf8ccd3` with the present audit gives
the following usable local rule.

> **Terminal-`C6` rank-drop rule.**  Consider a diagonal terminal `C6`
> transfer with a nonzero row-independent common tail.  If its two labelled
> matching channels become proportional after evaluation, contract the
> resulting rank-one common tail.  If they remain independent and the
> component is required to carry all three pure GHZ rows, then either a pure
> row is missing, a mixed singleton survives, or a literal crossed `C4`
> mate/outside transfer is active.  There is no occurrence-preserving silent
> contraction of the rank-two branch.

This is uniform in the size and internal matching complexity of the common
tail, because the tail multiplies every displayed local occurrence.  It is
not yet an arbitrary-ear theorem for noncoordinate edge blocks: a single
crossing `3 x 3` block can already have Schmidt rank three, and the
nonalignment guard (12) shows why a graph-only rank count does not recover
the physical colour channels.

## Reproduction

```bash
python3 computations/verify_uniform_terminal_c6_rank2_exact_source_exit.py
python3 -O computations/verify_uniform_terminal_c6_rank2_exact_source_exit.py
python3 -I -S computations/verify_uniform_terminal_c6_rank2_exact_source_exit.py
```

The checker audits the literal `bf8ccd3` tensor, the exact Schmidt ranks and
nonalignment factorization, all 117,649 closed-cycle supports, the unique
sharp support orbit, all twelve labelled first mates, and all 64 minimal
first-layer repair packets.
