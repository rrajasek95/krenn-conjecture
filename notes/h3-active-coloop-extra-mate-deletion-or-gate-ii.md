# Extra same-word coloop mates reduce to support deletion or Gate II

## Result

At canonical `h=3`, an arbitrary larger same-word mate closure creates no
new physical comparison theorem.  There is a well-founded recurrence with
three stopping outcomes:

```text
exact occupied-coordinate direction -> strict support deletion;
private row with no trapped mate     -> offdiagonal exit or coloop destruction;
first Hasse/full-rank packet         -> full-source completion dichotomy.
```

The last dichotomy is

```text
all completed support axis-pure -> impossible;
some completed support off-axis -> source-provenant active fan
                                  -> four-good or Gate II.
```

Thus every arbitrary trapped-coloop packet either exits, becomes four-good,
loses the selected coloop, or reaches the one already open Gate-II datum:
the fan-grade physical `Phi/q=M-a` comparison.

Checker:
[`verify_h3_active_coloop_extra_mate_deletion_or_gate_ii.py`](../computations/verify_h3_active_coloop_extra_mate_deletion_or_gate_ii.py).

## The well-founded recurrence

Order states lexicographically by

\[
 \mu=(\text{occupied scalar support},
       \text{unprocessed supported matching occurrences}). \tag{1}
\]

Both entries are finite in the complete `h=3` source.

If an anchor-safe occupied-coordinate direction `xi` satisfies

\[
 J_xF(\xi)=0,\qquad F_{[r]}(x;\xi)=0\quad(r\ge2),     \tag{2}
\]

then multiaffinity gives `F(x+t xi)=F(x)` identically.  Choosing `t` to
kill a nonzero coordinate strictly lowers the first entry of (1).  This is
the exact affine deletion from `4f7f104`, not a tangent approximation.

At fixed support, revealing a mate already present in a complete row lowers
the second entry.  No cell is adjoined to the source and no support is
enlarged.  Hence this move also cannot cycle.

If (2) fails at its first higher coefficient, retain that coefficient as a
literal Hasse packet and stop the recurrence.  The double-point guard of
`c41ab89` shows why this stop is mandatory: a Jacobian kernel alone need not
integrate.

## The first quadratic stop

The complete second-Hasse census `1480f7d` leaves exactly

```text
QQ target       one-edge restricted face,
QQ response     C2+,
DQ or PS        C4,
PQ or SQ        P2.
```

There are `45` target and `630` response pair incidences.  Each retained
face keeps its sites, word colours, response heads, fine grade, and matching
complement.  Occurrence-incompatible pairs have zero second face; if every
varied subset is occurrence-incompatible, all higher faces vanish and (2)
returns to exact deletion.

Earlier maps treated a pure trapped `C2+/C4/P2` face as requiring a new
same-grade chart-complete Spencer cell before the coloop argument could
continue.  That is unnecessary for **entry**.  The lower cell may remain
useful for a constructive comparison, but the full-source branch can be
classified before filling it.

## Why the completion split is guard-independent

The proof behind `4c15d41` first analyzed one silent Hasse-pair seed, but its
completion step uses no coefficient special to that seed.  It asks only
whether the completed normalized source support is axis-pure.

- If it is axis-pure, the source belongs to the globally empty canonical
  `h=3` axis-pure five-tensor locus.  Adding anchor, physical `q`, ridge,
  residue, `W`, or eta/sigma equations only cuts that empty locus.
- Otherwise the completed source contains a nonzero off-axis physical `q`
  or endpoint cell.  The target-augmented private-site identity gives a
  source-provenant active fan.

Therefore the same split applies to an extra-mate closure, a `C2+`, `C4`,
or `P2` quadratic packet, and even a first cubic or quartic rowwise packet.
It also applies to a larger block whose relevant restriction is full-rank
and hence has no deletion direction.  The entire finite packet is retained;
no selected face is projected away.

This is the crucial replacement for a missing chart map:

\[
 \boxed{\text{full-source completion of the face}
        \Longrightarrow \text{impossible axis branch or active fan}.} \tag{3}
\]

## Landing map

The evaluated active fan has two outcomes.

1. `four-good`: the existing transverse landing applies.
2. A literal pure-colour coloop: an outside hole strictly grows the Hall
   shore, so saturation takes at most fourteen steps.  A trapped shore is
   precisely Gate II.

A diagonal alternate which creates a nonzero pure target matching omitting
the selected edge destroys the current coloop and exits this branch.  An
offdiagonal alternate is already in (3).

After saturation, the only unlanded datum is

\[
                         J_0\Phi=A J,
 \qquad q=M-a
\]

in the literal fan grade.  Packet disagreement, the anchor bright/dark
fork, target circuits, and finite termination are already exhaustive after
that comparison.  Extra mate closures do not create a second open theorem.

## Scope

This is an exact entry reduction for canonical `h=3`, characteristic zero,
and a maximum-anchor/minimum-support complete five-tensor source.  It does
not construct the Gate-II `Phi`, nor does it promote the global axis-pure
emptiness theorem to arbitrary `h`.  It also does not claim the lower
`C2+/C4/P2` chart cells are constructed; it proves that they are not needed
as independent prerequisites for reducing this branch to Gate II.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
stored in the checker.
