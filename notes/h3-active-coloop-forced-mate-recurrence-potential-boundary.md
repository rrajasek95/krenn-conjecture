# The forced-mate packet is one-shot; arbitrary coloop recurrence is not proved

## Outcome

The fourteen alternatives from `ab3e510` do not create a cycle inside the
literal `H_0[000011]` packet:

```text
2 diagonal mates     -> current coloop 01 is broken;
12 offdiagonal mates -> physical active fan -> four-good or literal coloop.
```

What is not sound is to take the last literal coloop, relabel it as a new
copy of the special two-occurrence guard, and restart.  The complete-row
normalization required for that transition is exactly the open fan-grade
physical comparison/pointed-`P_f` theorem.

Checker:

```text
computations/verify_h3_active_coloop_forced_mate_recurrence_potential_boundary.py
```

## Why Hall growth is not uniform

The eight endpoint-closable mates produce effective response holes

```text
01 twice, 04 three times, 14 three times.
```

All lie in the closed triangle

\[
                         A=\{01,04,14\}=T(A).         \tag{1}
\]

Thus all eight can be trapped without enlarging the Hall closure.

The four head-dark rectangles use precisely the active cross edges

```text
05, 15, 24, 34.
```

They all lie in the closed nine-edge shore

\[
 A=T(\{45\})=\{e:e\cap45\ne\varnothing\},
 \qquad T(A)=\{45\}.                                 \tag{2}

Indeed (2) is the unique closed shore containing all eight possible
offdiagonal physical edges from the full fourteen-mate packet.  Hence the
head-dark four cannot be declared outside-hole exits uniformly.  They still
enter the active-fan theorem; if that theorem returns a coloop, physical
normalization remains necessary.

## Edge and word do not supply a missing decrease

Every alternative belongs to the same unary coefficient `000011`.  Its
site/colour orbit consists of the 90 words with colour multiplicities
`(4,2,0)`.  Likewise all fifteen physical edges form one `S6` orbit.  A
fixed numerical ordering of coloop edges is not source invariant, and the
unary-word orbit does not change.  Therefore neither label can make a
trapped Hall step strictly decreasing.

This gives sharp counterguards to a proposed lexicographic potential based
only on

```text
(coloop edge, closed Hall shore, unary word).
```

## The sound well-founded protocol

Use the state key

```text
(unary word w, literal coloop edge e, closed shore cl(A))
```

and, within that fixed key only, the conditional potential

\[
       \Psi=\bigl(15-|\operatorname{cl}(A)|,
                    \mathbf1_{\rm mate\ packet\ unprocessed}\bigr) . \tag{3}
\]

Order (3) lexicographically.

- A certified hole outside the shore strictly lowers its first coordinate.
- If all holes are trapped, process the entire fourteen-way packet once;
  its phase changes from one to zero.
- At phase zero, four-good terminates.  A coloop already carrying the exact
  endpoint/common-`q` normal form enters the committed `h=3` closure chain.
  An arbitrary coloop is passed to the single fan-grade physical `Phi/q`
  comparison, equivalently the pointed-`P_f` normalization gate.

There is no permitted transition which resets the phase at a merely
relabelled coloop.  Such a transition is precisely what remains to be
proved.  Conditional on that physical normalization, (3) and the existing
Hall closure theorem give genuine termination; without it, claiming a
recurrence would be circular.

## Updated frontier

`ab3e510` therefore removes a new combinatorial recurrence question.  It
does not remove the source-placement question:

```text
first unary mate
  -> coloop escape or active fan
  -> four-good or literal coloop
  -> MISSING physical fan-grade comparison / pointed P_f
  -> committed normalized coloop closure.
```

The triangle and nine-edge guards are Hall shadows, not complete GHZ source
points.  Their role is to show exactly why neither outside-hole growth nor a
word/edge tie-breaker can replace the missing physical comparison.

## Verification

Run

```text
python3 computations/verify_h3_active_coloop_forced_mate_recurrence_potential_boundary.py
python3 -O computations/verify_h3_active_coloop_forced_mate_recurrence_potential_boundary.py
python3 -I -S computations/verify_h3_active_coloop_forced_mate_recurrence_potential_boundary.py
```

Frozen ledger SHA-256:

```text
0a0d767063e37b2398126592e132cf6225aaa89bd1794a8e576e724962bfe70d
```
