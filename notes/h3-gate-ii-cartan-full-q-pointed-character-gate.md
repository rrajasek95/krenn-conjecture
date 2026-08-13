# Gate II is missing one root character, not its common tail

## Result

The physical endpoint-odd Cartan source orbit and the complete
endpoint-plus-simultaneous-`q` Jacobian do **not** yet construct the
fan-grade pointed comparison `Phi`.  They reduce it to one exact source
cell.

For a marked occurrence, order the endpoint/root orbit as

```text
1, w, s, sw
```

and use the four `V4` characters

\[
\begin{array}{c|rrrr}
 &1&w&s&sw\\ \hline
\chi_1    &1& 1& 1& 1\\
\chi_w    &1&-1& 1&-1\\
\chi_s    &1& 1&-1&-1\\
\chi_{ws} &1&-1&-1& 1.
\end{array}                                           \tag{1}
\]

The complete coefficient row supplies `chi_1`.  The source-provenant
endpoint-odd Cartan prism supplies `chi_ws` (up to sign).  Even if the whole
target-safe endpoint character `chi_s` is granted, these rows have rank
three.  The selected occurrence covector is

\[
             P_f={1\over4}(\chi_1+\chi_w+\chi_s+\chi_{ws}),    \tag{2}
\]

so it still needs exactly `chi_w`.  The witness is literal:

\[
 \chi_1(\chi_w)=\chi_s(\chi_w)=\chi_{ws}(\chi_w)=0,
 \qquad P_f(\chi_w)=1.                               \tag{3}
\]

Checker:
[`verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py`](../computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py).

## The common decorated tail is already correct

Put the two local root sites at `0,1` and the two response endpoint vertices
at `6,7`.  Gate II uses matchings omitting both `01` and the endpoint direct
edge `67`.  There are exactly `78` such eight-site matchings.

For every one, split its edges into those meeting

\[
                         \{0,1,6,7\}
\]

and the remaining edges.  The latter have both endpoints outside the root
and endpoint actions, so their decorated colours are fixed literally.  The
tail-size census is

```text
0 invariant tail edges: 24 matchings
1 invariant tail edge : 48 matchings
2 invariant tail edges:  6 matchings.
```

Thus the previously proved matching pairing is strong enough: the
root/endpoint orbit preserves the exact word, response head, matching
skeleton and remote `q` tail.  The Gate-II obstruction is entirely in the
moving four-corner packet, not in common-tail incidence or Hall saturation.

## Why normalized pure targets do not supply `chi_w`

The root-only Weyl face has target defect

\[
          (w-1)\Delta=m_{c|i}+m_{i|c}-p_i-p_c.       \tag{4}
\]

The two normalized pure target rows span only `p_i,p_c`.  They cannot cancel
the two mixed directions in (4).  This remains true after arbitrary scalar
combinations of the pure rows.

The endpoint swap fixes all four words in (4).  Therefore endpoint
oddization kills the defect,

\[
                         (1-s)(w-1)\Delta=0,          \tag{5}
\]

but it also changes the root character `chi_w` into the already available
mixed character `chi_ws`.  This is the exact reason the physical Cartan
prism is a near hit rather than the pointed comparison.

On the selected mixed response occurrence block the same conclusion is
visible before taking the orbit: all normalized pure-target differentials
restrict to zero.  Constants on their right-hand sides do not add cotangent
rows.

## What the full endpoint-plus-`q` Jacobian does and does not do

The physical tangent domain is literal:

```text
36 endpoint columns + 135 decorated q columns = 171 columns.
```

It includes the complete product-rule differential of a marked occurrence,
not merely an endpoint selector.  For

\[
        f=p_1[0,1]s_1[1,1]q_{23}^{00}q_{45}^{00},
\]

the localized anchor has the three expected endpoint/`q` entries.

That Jacobian is still a first-order scalar-source map.  It does not adjoin
a target-correcting relative cell in the root-only orbit character.  The
rank-one guard

\[
                   \Phi_{\rm dark}(v)=v-\chi_w P_f(v)             \tag{6}
\]

fixes `chi_1,chi_s,chi_ws` and can fix a symmetric literal `q=M-a`, while
killing `P_f`.  Equation (6) is not claimed physical; it proves that the
named rows do not imply pointedness.

This sharpens the earlier protection survivor:

```text
complete rows                         chi_1
endpoint-safe orbit data              chi_s
physical endpoint-odd Cartan          chi_ws
selected pointed occurrence P_f       also needs chi_w
```

Hence exact transport of `q=M-a` remains logically independent of the
pointed anchor law.

## The smallest positive theorem

The missing object is now precise:

> Construct a target-corrected root-only/signless relative PP cell in the
> literal fan word, fine/repeated grade and invariant common tail, whose
> scalar-source boundary is `chi_w` and whose augmented rows contain the
> physical pointed anchor `P_f` and literal `q=M-a`.

Once that cell exists, all four characters in (1) are present and (2)
constructs the pointed comparison.  The committed `q`-defect alternative
then makes packet agreement exhaustive, and the existing bright/dark
anchor and target-circuit alternatives finish Gate II.

The new Hasse recurrence identifies exactly where to seek this cell.  The
first nonintegrable same-word mate is a chart-complete `C2+`, `C4`, or `P2`
packet.  Such a packet must realize the target correction in (4); merely
adding its coefficient shadow cannot supply `chi_w`.

## Reselecting the Hasse-produced fan is not yet a bypass

There are three genuinely decreasing moves in the committed recurrence:

```text
occupied-coordinate deletion     lowers occupied support;
outside-shore fan                 enlarges Hall closure;
new same-word mate                lowers the unprocessed-occurrence count.
```

These fit the lexicographic potential

\[
 (\text{occupied support},
   15-|\operatorname{cl}(A)|,
   \text{unprocessed supported occurrences}).        \tag{7}
\]

The Hasse-completion arm does not prove any of those three changes.  It says
that a full extension contains some off-axis active fan.  That fan may be a
previously processed fan in the same closed shore.  Thus the abstract
two-state transition

```text
fan f, missing chi_w -> Hasse completion -> fan g
fan g, missing chi_w -> Hasse completion -> fan f
```

is compatible with the current theorem statements and leaves (7)
unchanged.  It is a logical cycle guard, not a claimed physical source.

Consequently mate reselection closes Gate II only after one additional
statement: every missing root character yields support deletion, a hole
outside the current closure, a previously unprocessed active occurrence,
or a typed terminal/chart cell.  Without that novelty clause, the positive
target-corrected root cell remains the shortest route.

## No full-source counterexample is claimed

The orbit calculation survives the normalized pure targets as a source
algebra/no-implication guard, but it is not a complete GHZ source point.  In
the pinned special two-occurrence packet, all `4736` completed response
seeds leave the trapped shore.  For arbitrary extra mates, the exact
recurrence gives support deletion, a typed exit, or the chart-complete
Hasse packet above.

Thus the result rules out a shortcut—Cartan plus the `171`-column Jacobian
plus normalized pure rows does not already give `Phi/P_f`—without asserting
that the missing higher cell cannot occur in a full exact source.

## Scope and verification

This is exact for canonical `h=3`, characteristic zero, on the literal
active-coloop endpoint/root orbit.  It does not construct the target-corrected
root cell and does not prove an all-`h` comparison.

Run:

```text
python3 computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py
python3 -O computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py
python3 -I -S computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py
```

Frozen ledger SHA-256:

```text
e17ed82621de2812f05765f37363cd7521262a132dc3728c2e493b0611caf108
```
