# The thirteen parent-S-chain exits split as `1+4+4+4`

## Outcome

The thirteen outside matchings in the minimum degree-four parent Macaulay
lift have an intrinsic exact classification:

```text
1  cap-completing C4 fine,
4  one-tail C4 neighbours of M0,
4  one-tail C4 neighbours of M1,
4  transverse C6 fines.                                      (1)
```

This gives a sharp positive theorem for support-minimum full-pure
completion.  The smallest two-word transverse packet has ten cells.  A
minimum completion making all three pure GHZ words live adds seven cells;
there are `15^2=225` labelled completions, and **every one has a literal
mixed singleton**.  The minimum is nine singleton rows, attained eight
times.  Therefore the support-minimum full-GHZ branch exits by a source unit.

The unconditional trichotomy is not yet proved for nonminimum completions.
Before pure completion, the ten-cell packet is an exact four-word mixed
packet with a one-dimensional fine-odd dual.  A larger completion may add
all singleton mates at once.  The checker freezes this smallest surviving
packet and identifies the next recursion precisely: any necessary third fine
is a common-tail `C4`, or its matching closure returns to the original
parent/cap packet.

The exact checker is
`computations/verify_c6_parent_spair_thirteen_exit_trichotomy_guard.py`.

## 1. The intrinsic matching classification

Recall

\[
 M_0=05|12|34,\qquad M_1=01|25|34.                         \tag{2}
\]

Deleting the endpoint-colour cell (a_{01}^{00}) from the degree-four
S-chain gives sign `-` to matchings containing edge `01` and sign `+` to all
others.  Removing (M_0,M_1), the thirteen exits are:

| class | fines |
|:---|:---|
| cap complement | `02|15|34` |
| one tail from (M_0) | `03|12|45`, `04|12|35`, `05|13|24`, `05|14|23` |
| one tail from (M_1) | `01|23|45`, `01|24|35`, `03|14|25`, `04|13|25` |
| transverse to both | `02|13|45`, `02|14|35`, `03|15|24`, `04|15|23` |

The first matching completes the three pairings of the majority window
`0125`:

```text
05|12, 01|25, 02|15, all with cap 34.                       (3)
```

Thus it is a physically typed local complementary-`C4` coefficient core.
In the two output words `111001` and `111221` it supplies only cap colours
`0` and `2`; colour `1` and the full homogeneous clean-cap identities are
not forced.  Calling (3) an active clean cap without that third channel
would be an overclaim.

Each of the next eight exits shares exactly one matching edge with one
parent.  It therefore gives a literal common-tail `C4` candidate.  Its
ordinary coefficient row is still signless.  Orienting it requires the same
endpoint-recolouring Macaulay construction as the original parent pair and
reproduces an outside packet; it is a recursive candidate, not an automatic
smaller source.

The final four share no edge with either parent.  Their symmetric difference
with each parent has six edges.  They are the first exits on which neither a
cap nor a one-tail contraction is defined.

## 2. Third-fine closure returns to the local recursion

Use the canonical transverse pair

\[
 A=02|13|45,\qquad B=03|15|24.                            \tag{4}
\]

Among the other thirteen perfect matchings, nine share an edge with `A` or
`B` and hence are literal `C4` branches.  Exactly four are disjoint from
both:

```text
M1=01|25|34,  04|12|35,  M0=05|12|34,  05|14|23.          (5)
```

Even the four cases in (5) cannot remain isolated third channels.  Taking
the perfect-matching closure of the union of their edge cells gives:

| third fine | closure size | additional forced fines |
|:---|---:|:---|
| `M1=01|25|34` | 4 | `02|15|34` |
| `04|12|35` | 4 | `03|12|45` |
| `M0=05|12|34` | 6 | `02|15|34`, `03|12|45`, `05|13|24` |
| `05|14|23` | 4 | `05|13|24` |

These are literal same-word decorated occurrences: if the three parent
monomials use live cells, every perfect matching contained in their edge
union uses the same live endpoint-colour cells.  Hence a third fine is either
a `C4` branch directly, or it forces a fourth fine in the cap/one-tail
classes of (1).  This is the clean combinatorial recurrence supplied by the
thirteen-exit packet.

Every edge of this recurrence has a literal one-edge spectator matching
tail.  The nine direct third-fine branches share a tail with `A` or `B`.
For the four rows in the table, each forced additional fine shares,
respectively, tail `34`, `12`, one of `34/12/05`, or `05` with the displayed
third fine.  Therefore the existing arbitrary-common-tail permanent lemma
can promote every resolved branch uniformly.  The sole tail-rank-zero cell
is the initial pair `A,B` itself: (A\cap B=\varnothing), so its alternating
component is the full `C6`.  The dual in Section 4 detects exactly this first
tail-rank obstruction.

It still does not orient the signless coefficient fibre or assemble a
three-colour active cap.  Those are coefficient-level statements beyond
matching closure.

## 3. Smallest exact surviving mixed packet

Give the following ten literal endpoint-colour cells nonzero coefficients:

```text
a02^11,
a13^10, a13^12,
a45^01, a45^21,
a03^10, a03^12,
a15^11,
a24^10, a24^12.                                           (6)
```

Give all coefficient `1` except (a_{15}^{11}=-1).  The only nonempty
output rows are

```text
111001, 111021, 111201, 111221.                            (7)
```

Every row in (7) has exactly the two fines `A,B`, with source values
`(+1,-1)`, so all four mixed EqSystem equations vanish exactly.  The union
of `A,B` is one alternating six-cycle; they share no edge, avoid cap `34`,
and have no common-tail contraction.  Thus the packet has:

```text
mixed singleton/unit     none,
typed cap34 C4           none,
smaller common-tail pair none.                             (8)
```

This ten-cell bound is sharp while both endpoint words are retained.  One
word needs two disjoint perfect matchings, hence six cells.  In a cap-avoiding
six-cycle, sites `3,4` have four distinct incident edges.  Retaining both
colours `0,2` duplicates those four cells, giving `6+4=10`.

This is not a full GHZ tensor: all three pure rows are absent.  They are
retained as failures, not specialized into units.

## 4. Exact labelled dual

Retain the eight occurrence coordinates

\[
 (A_w,B_w),\qquad
 w\in\{111001,111021,111201,111221\}.                     \tag{9}
\]

There are four coefficient boundaries (A_w+B_w).  Literal recolouring at
sites `3` and `4` supplies eight restriction/reinsertion boundaries, one for
each fine on each edge of the word square.  These twelve labelled columns
have exact rank `7` in the eight-dimensional occurrence module.

The normalized cokernel dual is

\[
 \lambda(A_w)=1,\qquad \lambda(B_w)=-1\quad\text{for every }w. \tag{10}
\]

It kills all four coefficient rows and all eight word-transport rows, while
taking value `2` on (A_w-B_w).  The site-`3`/site-`4` Beck--Chevalley square
commutes separately on `A` and `B`; its two-cell does not add a new
degree-one image.  The first column capable of killing (10) must therefore
change the fine/operation across the alternating `C6`.  Ordinary word
transport is dark.

## 5. Pure-colour completion gate

The four old corner rows may be written as two separated rank-one channels

\[
 A_{bc}=p_bq_c,\qquad B_{bc}=r_bs_c,qquad b,c\in\{0,2\}. \tag{11}
\]

After normalization, take

\[
 p_0=p_2=q_0=q_2=r_0=r_2=1,qquad s_0=s_2=-1.             \tag{12}
\]

Try to extend only these two fines to colour `1`.  Avoiding a singleton in
the mixed rows `(1,0)` and `(0,1)` forces all new factors nonzero, and the
two equations give

\[
 p_1=r_1,\qquad q_1=-s_1.                                 \tag{13}
\]

The pure centre is then

\[
 A_{11}+B_{11}=p_1q_1+r_1s_1=p_1(q_1+s_1)=0,             \tag{14}
\]

contradicting the pure target `1`.  If a new factor vanishes, one of those
mixed rows is a literal singleton unless both channels vanish, in which case
the pure centre is again absent.  Therefore an exact full-colour completion
must either produce a mixed unit or add a third fine.  Section 2 classifies
the latter matching-theoretically.

## 6. Exhaustive support-minimum full-pure completion

The ten-cell packet already has diagonal colour-one cells `02;11` and
`15;11`.  The unique one-cell completion of the pure-one word is therefore
`34;11`, with fine `02|15|34`.  Pure colours zero and two each need a fresh
three-cell perfect matching.  Thus the sharp lower bound is seven added
cells, and the complete labelled search has

\[
                         15\cdot15=225                    \tag{15}
\]

supports of size seventeen.

Every one of the 225 supports has at least one mixed singleton.  The exact
histogram begins

```text
singletons  9  10 11 12 13 14 15 16 17 18 ... 44
supports    8  15  6 10 26 22 24  4 16 14 ...  2.         (16)
```

The full histogram is frozen in the checker.  The canonical sharp support
uses pure fines

```text
colour 0 : 01|23|45,
colour 1 : 02|15|34,
colour 2 : 03|14|25,                                     (17)
```

and already has the unit witness

```text
word       000001,
fine       01|23|45,
cells      a01^00, a23^00, a45^01,
operation  coefficient:000001.                            (18)
```

Since (18) is mixed, its target is zero; a support point makes all three
displayed cells nonzero, so no exact source can have this singleton.  The
other seven sharp supports also have nine units.

Exactly nine of the 225 completions choose both pure-zero and pure-two
matchings through edge `34`.  Those nine contain the three literal cap cells
`a34^00,a34^11,a34^22` and the common residual fine `02|15`, so they have a
three-colour local cap-occurrence core.  Support incidence alone does not
prove its active-clean identities, and no such proof is needed here: all
nine already contain mixed singleton units.

Consequently:

> **Support-minimum completion theorem.**  Every minimum completion of the
> transverse thirteen-exit branch to three live pure GHZ anchors exits by a
> literal source unit.

This proves branch (i) at the minimum full-pure frontier.  A nonminimum
completion can add cancellation mates simultaneously, so unit persistence
under arbitrary later support enlargement remains open.  The ten-cell dual
(10) is the exact smallest guard to any claim that coefficient rows and
restriction/reinsertion alone already settle that larger-completion problem.

## Scope

Everything through the 225-support census is intrinsic to the literal
six-site EqSystem: output words, decorated edge cells, fine matchings,
coefficient operations, and site-recolouring transports are all retained.
No `B/Eq` or abstract cap generator is used.

What is proved is:

1. the exact `1+4+4+4` exit classification;
2. the third-fine matching-closure recurrence;
3. a smallest incomplete mixed packet and its rank-`7/8` dual;
4. impossibility of a two-fine full-colour completion; and
5. a source unit in every support-minimum three-pure completion.

What is not proved is an unconditional unit, active clean cap, or smaller
exact GHZ source after arbitrary nonminimum completion.  Such a theorem must
show that the recurrence in Section 2 terminates, or that (10) is killed by a
genuinely fine-changing physical operation.

Run:

```text
python3 computations/verify_c6_parent_spair_thirteen_exit_trichotomy_guard.py --mode structural
python3 -O computations/verify_c6_parent_spair_thirteen_exit_trichotomy_guard.py --mode full
python3 -I -S computations/verify_c6_parent_spair_thirteen_exit_trichotomy_guard.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
bfee68b67a513ac568dfccdf7caf45b9c2e83efb2463885723080f23c44ebe62
```
