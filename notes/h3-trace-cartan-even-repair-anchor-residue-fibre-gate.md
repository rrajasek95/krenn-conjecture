# The even `B1/B4` repair reduces to one labelled-residue section

## Result

Let

\[
                     v={B_1+B_4\over2}.
\]

The denominator-Tor route in `73ee225` conditionally gives a negative
reduced companion with the correct lower tail and positive ordinary residue.
There is an exact same-grade correction, provided the physical relative
source contains a pure multiplier-labelled residue section `d_v`:

\[
 (-A_v)+T_v+\rho_v-2d_v
       =(\operatorname{lower}=v,\operatorname{target}=v,
         \operatorname{ainc}=0,\operatorname{ores}=0).       \tag{1}
\]

The required pure `r0` image differs from (1) by exactly
`ainc=-1`.  Thus the anchor-fibre Fredholm alternative of `8e1f858`
applies without another coarse correction:

- if `ainc` is nonzero on the protected fibre kernel, normalize it to obtain
  the relative generator;
- if it vanishes there, it is the physical anchor separator, with the
  bordered Cartan refinement already proved in `8e1f858`.

Equivalently, writing `x_v=r0_v-T_v-rho_v+d_v`, the tempting decomposition

\[
 r0_v-(-A_v)=(r0_v-x_v-d_v)+(\operatorname{ainc}=-1)
\]

is exact, but does not remove an input: its first parenthesis is precisely
`T_v+rho_v-2d_v`, and `x_v` is source-typed only after the same labelled
`d_v` exists.  It is the cone identity (1), not an independent construction.

Checker:
[`verify_h3_trace_cartan_even_repair_anchor_residue_fibre_gate.py`](../computations/verify_h3_trace_cartan_even_repair_anchor_residue_fibre_gate.py).

## The first missing source cell is literal and label-sensitive

The conditional phrase in (1) cannot be removed using the present residue
inventory.  In the six target labels `(B0,...,B5)`, the strongest natural
lift of the scalar pure-`ores` column is the diagonal vector

\[
             \mathbf 1=(1,1,1,1,1,1).
\]

The physical endpoint-odd Cartan cell supplies only

\[
             c=(1,0,1,-1,0,-1).
\]

The primitive covector

\[
             \chi=(0,1,-1,0,1,-1)                     \tag{2}
\]

kills both `1` and `c`, but `chi(v)=1`.  In particular, it reads `-2` on
the `-2d_v` term required by (1).  The Cartan cone therefore cannot replace
the missing labelled residue section.

The minimal new cell is a rho-even relative chain `d_even` with

```text
ordinary residue = (B1+B4)/2,
lower = W = target = ainc = 0.
```

Fine grading matters.  Its homogeneous source pieces must live in the two
actual denominator routes:

```text
face 3, multiplier 34  -> B4,
face 5, multiplier 45  -> B1.
```

Equivalently, the stronger supply is a labelled pure-residue section in
each of those grades.  A single ungraded scalar `ores` column does not count.
This even section is not supplied merely by Gate I's current request for one
chosen fixed section and one paired section: the even repair uses both fixed
labels.

## The unaudited Gate-I probe does not change this gate

The probe's claim that only an output terminal packet remained is
superseded.  Commit `271df91` proves the full literal `M_v=-O_alpha+K`
composition, including its physical eta/sigma values.  Thus the old
output-side terminal problem is closed.

That result does not help (1).  Its exact composite has zero target, anchor,
and ordinary residue.  It supplies neither Gate I's `d_fixed/d_pair` source
sections nor the rho-even `B1/B4` section above.  The distinction is
input-side source labelling, not output-side terminal realization.

## Exact weighted condition away from the clean slice

For the direct selected face projection

\[
        y=(0,0,\tfrac12,0,\tfrac12),
\]

the universal reset-word equation is

\[
                         h_3+h_5=0.                    \tag{3}
\]

For its rho-evenized projection

\[
        y_+=(0,\tfrac14,\tfrac12,0,\tfrac14),
\]

it is

\[
                         2h_3+h_2+h_5=0.               \tag{4}
\]

Nonconstant weights do occur and both loci are nonempty in the normalized
`C5` coefficient chart.  Write the chord coefficients in order
`(13,14,24,25,35)`, with all cycle edges normalized to one.  Then

```text
(0,-2,0,0,0) gives h=(1,1,1,1,-1)  and satisfies (3),
(0,-4,0,0,0) gives h=(1,1,1,1,-3)  and satisfies (4).
```

But nonconstancy alone is not sufficient: a generic nonconstant `h` misses
both hyperplanes.  Nor is either scalar equation sufficient for the full
selected-column membership in the unselected denominator image.  Finally,
the two displayed coefficient specializations have not been certified to
belong to the global all-inactive physical branch; inactivity is a separate
condition.  Thus this result proves that the clean aggregate obstruction can
disappear off-clean, not that the desired denominator kernel has been built.

## Frontier

The even gate is now split sharply:

1. weighted denominator membership supplies the conditional `-A_v`;
2. a same-grade rho-even labelled residue section supplies the correction
   in (1);
3. the physical anchor fibre gives either the relative generator or a
   separator.

The first unresolved source object after the denominator tail is `d_even`.
The `beta=0` selected-colour branch remains independent.

## Verification

Run:

```text
python3 computations/verify_h3_trace_cartan_even_repair_anchor_residue_fibre_gate.py
python3 -O computations/verify_h3_trace_cartan_even_repair_anchor_residue_fibre_gate.py
python3 -I -S computations/verify_h3_trace_cartan_even_repair_anchor_residue_fibre_gate.py
```

The frozen ledger digest is
`7c869d6660a62bcdb6e2874d848b82fb6f0c2b5fc1540435dbd3583d9d4b9fc5`.
