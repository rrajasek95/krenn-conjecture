# The special active-coloop packet terminates; arbitrary entry is still sparse extraction

## Exact local termination theorem

Compose the first mixed-unary mate theorem `ab3e510`, the one-shot recurrence
boundary `5ddaa7e`, the complete-response closure `2448528`, and finite `K_6`
Hall saturation.

For the literal two-occurrence packet of `44cdd15`, process the three mixed
unary coefficients

```text
000011, 001100, 001111
```

simultaneously.  The exhaustive branch count is

```text
14^3 = 2744 mate selections

728  destroy the named pure-zero coloop;
288  add a literal occurrence to the selected pure-one target-response row;
1580 all-offdiagonal selections immediately leave the current closed shore;
148  initially remain in one nine-edge/singleton shore.
```

The last `148` packets have the three private target-zero rows

```text
R11[110000], R11[110011], R11[111100].
```

Choosing one forced alternate response occurrence in each row gives
`148*2*8*2=4736` completions.  None is contained in any of the `446` closed
ordered `K_6` shores.

This is formal termination of the **special packet processor**: it has no
transition back to its original closed Hall state.  Its outputs are

```text
named-coloop destruction,
selected target-packet enlargement, or
empty Hall transversal / free cross-shore exit.
```

The first two are handoffs, not recursive calls to the same special packet.
In particular, the new pure-one response occurrence is not silently called
an endpoint/common-tail normalized coloop packet.

Checker:

```text
computations/verify_h3_active_coloop_literal_packet_termination_scope.py
```

## Why zero closed-shore survivors is the correct Hall conclusion

For an effective-hole family `A`, put

\[
 T(A)=\{e:e\text{ meets every edge of }A\}.
\]

The exact census checks, for all `2^15-1` nonempty edge families,

\[
 T(A)=\varnothing
 \quad\Longleftrightarrow\quad
 \text{no closed shore contains }A.                 \tag{1}
\]

Indeed, if `T(A)` is nonempty then `cl(A)=T(T(A))` is closed and contains
`A`; the converse is immediate.  Thus the zero closed-shore count in the
`4736` completions says `T(A)=empty`.  If `B` is the nonempty opposite fan
shore, it cannot satisfy `B subset T(A)`: some `a in A` and `b in B` are
disjoint.  This is exactly the free-Hall/four-good alternative used by the
pinned active-fan theorem.

Outside-shore additions before (1) strictly decrease

\[
                         15-|\operatorname{cl}(A)|,
\]

so no finite-saturation cycle remains either.  The new result is stronger on
the final trapped packet: its transversal is already empty, rather than
merely having grown one more time.

## Relabelling and scaling do not give arbitrary coloop entry

The special packet has a monomial pure-zero cofactor:

\[
 C_0=q_{23}^{00}q_{45}^{00},
 \qquad |\operatorname{supp}_{\rm match}(C_0)|=1.    \tag{2}
\]

An arbitrary normalized literal coloop can have several cofactor monomials.
The checker freezes the smallest guard

\[
\begin{aligned}
 q_{01}^{00}&=1,\\
 q_{23}^{00}q_{45}^{00}&=1,\\
 q_{24}^{00}q_{35}^{00}&=1,\\
 q_{25}^{00}q_{34}^{00}&=-1.
\end{aligned}
\]

Then every nonzero pure-zero perfect matching contains `01`, while

\[
 q_{01}^{00}C_0=1(1+1-1)=1.                         \tag{3}
\]

Hence `01` is a normalized literal coloop and its residual cofactor has three
nonzero matching monomials.  Site/colour relabelling is a bijection of
matching monomials, and multiplication by nonzero torus characters preserves
which monomials vanish.  The support counts `1` in (2) and `3` in (3) cannot
be related by relabelling/scaling.

The guard is not asserted to satisfy all GHZ equations.  It refutes only the
claimed formal orbit reduction from arbitrary coloop data to the special
two-occurrence packet.

## The exact missing arbitrary-entry theorem

What remains is the following narrower statement.

> **Closed-shore-private sparse two-occurrence extraction.**  Given an
> arbitrary source-provenant active fan, a literal pure-`c` coloop
> `alpha*C_c=1`, and the complete unary/four-response packet supplied by the
> uniform coloop pivot, either obtain an existing anchor-safe deletion,
> target-fibre point, typed outside-shore/four-good exit, or select one
> nonzero residual cofactor tail and one endpoint pair such that the three
> mixed tail-square response rows used by `2448528` are private modulo the
> current closed-shore span.

The extraction must preserve word, fine/repeated grade, response head and
orientation, common residual `q` tail, and all selected mutual anchors.
Literal equality with all zeros of `44cdd15` would be sufficient but stronger
than necessary: `2448528` only uses privacy of the three displayed response
rows.

Thus the updated scope is

```text
special two-occurrence coloop packet -> CLOSED local recurrence;
arbitrary active-fan coloop          -> missing sparse/private extraction;
finite Hall termination              -> already proved, not part of the gap.
```

## Verification

Run

```text
python3 computations/verify_h3_active_coloop_literal_packet_termination_scope.py
python3 -O computations/verify_h3_active_coloop_literal_packet_termination_scope.py
python3 -I -S computations/verify_h3_active_coloop_literal_packet_termination_scope.py
```

Frozen ledger SHA-256:

```text
aa8f091cda9fa8d7a90b338c65f68bc1595bbd19610d7f95f4939abccf93be88
```
