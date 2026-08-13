# The protection survivor is not axis-pure; it needs one fan-anchor scalar

## Verdict

The sole full-`q` survivor

\[
          \Lambda\in\operatorname{row}(A),\qquad
          H\notin\operatorname{row}(A)
\]

is not eliminated merely by the presence of a literal offdiagonal
active-fan coloop.  In fact that fan prevents the proposed axis-pure exit:
its defining source-provenant cell is nonzero and offdiagonal, while the
axis-pure locus used by `22c2e5c` contains only `q_{uv}^{cc}` and endpoint
row-`c` coordinates.  Darkness of a tangent/readout class does not imply
that the nonzero base-point cell vanishes.

The exact residual is smaller than a new coloop theorem.  After the fan
comparison square and its physical `q=M-a` row have been supplied, the only
additional datum needed by this survivor is

\[
       \boxed{H-h_{\rm fan}\Phi\in\operatorname{row}(A)}.       \tag{1}
\]

On the physical affine chart `u=1`, one has `du=0`, so the selected pointed
conormal is

\[
                         P_f=df-du=df=H.              \tag{2}
\]

Thus on the sharp one-dimensional quotient, (1) is exactly the missing
pointed-`P_f` scalar (and in particular a noncollapse condition), not
another Hall branch.  The pinned two-occurrence `U`- and `V`-bright guards
show why the complete coloop pivot does not already supply it: internal
redistribution preserves each aggregate but is visible to `P_f`.

Checker:

```text
computations/verify_h3_protection_survivor_active_coloop_phi_gate.py
```

Frozen ledger SHA-256:

```text
e3a6281dec9746218e447d5e9b4263273fa6aa59245fa7ea1bbf5643e9407412
```

## The full 171-column counterguard

Use the literal fixed-right domain

```text
36 p endpoint columns + 135 decorated q columns = 171.
```

For the marked nonzero occurrence

```text
p1[0,1] s1[1,1] q23[0,0] q45[0,0]
```

the fixed `s1` anchor differential has three nonzero entries.  Localizing
the occurrence and passing to invertible logarithmic tangent coordinates
normalizes it to

\[
 H=e_{p_1[0,1]}+e_{q_{23}^{00}}+e_{q_{45}^{00}}.     \tag{3}
\]

Let `xi` be the vector equal to one in those same three coordinates and
zero elsewhere.  The checker takes the maximally constrained sharp guard

\[
 \operatorname{row}(A)=\xi^\perp.
\]

Concretely, `A` contains every non-anchor coordinate selector and the two
centered differences between the three anchor coordinates.  Hence

```text
rank(A) = 170,
dim X*/row(A) = 1,
H(xi) = 3,
H not in row(A).
```

In this sharp linear countermodel, basis-normalized representatives of the
six-term row `Lambda` and the fan `q` readout are put in the 170-dimensional
physical complement, exactly as required by the survivor branch.  This is
not an identification of the formula `q=M-a` with a coordinate selector;
it is the normal form of two covectors already assumed to lie in
`row(A)`.

Now use the rank-one projection

\[
                    \Phi_{\rm dark}=I-\xi H/3.       \tag{4}
\]

It fixes every row of `A`, `Lambda`, and the fan `q` row, but kills `xi`
and pulls `H` back to zero.  Therefore

```text
A Phi_dark = A,             (complete comparison square)
Lambda Phi_dark = Lambda,   (six-term transport)
q Phi_dark = q,             (fan q transport)
H - H Phi_dark = H notin row(A).
```

This is the sharp full-width version of the old three-coordinate linear
guard.  It proves that neither the chain square nor physical `q` transport
implies (1).  The identity comparison repairs exactly (1), so no smaller
quotient condition can distinguish the two packets.

## Why the coloop does not invoke axis-pure emptiness

The pinned literal fan guard has adjacent active edges `01,02`, a
colour-zero coloop on `01`, a colour-one coloop on `02`, distinct centre
heads, and the exact private-site identity

\[
                    q_e+\Delta_{ef}C_f=1-1=0.
\]

Retain its literal offdiagonal cell as `q_{01}^{01}=1`.  That coordinate is
not one of the 69 axis-pure coordinates.  Thus an actual source packet in
this arm is already outside the locus excluded by `22c2e5c`.

To use axis-pure emptiness one would first need a new theorem turning fan
comparison darkness into the vanishing of every offdiagonal source cell.
No current row-space theorem does this, and it would contradict the chosen
nonzero fan witness unless it simultaneously supplied a terminal exit.
Consequently the shortest route is the positive comparison law (1), not a
darkness-to-axis-pure reduction.

## Relation to Gate II

The existing fan-`q` quotient theorem explicitly exhibits zero `q` defect
with a nonzero anchor defect.  This note combines that independence with
the full-`q` protection survivor:

```text
literal active-fan coloop
        |
        v
fan-grade chain comparison + q=M-a transport
        |
        +-- anchor quotient law (1) holds
        |       -> H-visible protected kernel
        |       -> existing generator/separator landing
        |
        `-- anchor quotient law fails
                -> exact one-dimensional counterguard (3).
```

Thus the load-bearing restriction of the missing fan-grade `Phi` is
precisely anchor faithfulness on `[H]=[P_f]`.  The complete construction still
has to preserve word, fine/repeated grade, common tail, response heads, and
the augmented physical rows; the statement here identifies which one of
those rows is logically independent after the chain and `q` clauses.

## Scope

This is an exact compatibility/counterguard for all currently proved
linear and support data.  The literal fan packet pinned by the active-fan
checker is not asserted there—or here—to be a complete GHZ source point.
Accordingly the result proves that existing hypotheses do not force the
survivor into the now-empty axis-pure branch; it does not construct a
counterexample to the conjecture.  Constructing the physical fan-grade
comparison satisfying (1) remains the positive theorem.
