# A shared odd comparison closes packet disagreement, but not anchor visibility

## Exact composition

Assume the source-valid protected odd comparison has been constructed,

\[
 J_0\Phi=A J,
\]

and that both complete odd-packet readouts have their literal physical
typing `q=M-a`.  Then `7a3ad78` removes packet agreement as a live branch.
The single class

\[
                 [q-q_0\Phi]\in L^*/\operatorname {row}J
\]

is exhaustive: a nonzero class is already a protected-kernel physical
`q` witness (or the corresponding saturated typed exit), while a zero class
is removed by a protected-row correction.  In the latter arm the physical
signless row and corrected odd row give the two oriented rows `(S+D)/2` and
`(S-D)/2`.  There is no further packet-mismatch case.

This statement begins **after** `Phi` exists.  In Gate I, construction of
the shifted fifteen-label map carrying `K d(u_012)` is still the input-side
problem; the quotient theorem does not manufacture that primal map.

Checker:
[`verify_h3_shared_odd_comparison_anchor_visibility_gate.py`](../computations/verify_h3_shared_odd_comparison_anchor_visibility_gate.py).

## The smallest remaining anchor theorem

Restrict the oriented affine packet to its minimum target-circuit block
`A_D`, so

\[
                 \ker A_D=\langle k\rangle,
                 \qquad e_\tau^*(k)\ne0.
\]

The rectangular Cartan landing needs exactly

\[
                         h_{\rm phys}(k)\ne0.          \tag{1}
\]

Let `h_0` be the canonical physical anchor row.  The smallest comparison
statement that forces (1) is

\[
 h_{\rm phys}-\mu h_0\Phi=\lambda A_D,
 \qquad \mu\ne0,
 \qquad h_0(\Phi k)\ne0.                              \tag{2}
\]

Indeed, evaluating (2) on `k` gives

\[
             h_{\rm phys}(k)=\mu h_0(\Phi k)\ne0.
\]

Conversely, on the corank-one block, if both functionals are nonzero on
`k`, choose `mu` to make their values agree.  Their difference annihilates
the whole kernel, hence lies in `row(A_D)`.  Therefore (2), after
normalization, is not an unnecessarily strong naturality demand: it is
equivalent to the required visibility on the target circuit.

There are two load-bearing pieces:

1. physical anchor transport modulo protected rows; and
2. noncollapse of the marked target circuit under `Phi`.

For Gate I the latter should come from the marked top occurrence retained by
the filtered lift.  For the fan-coloop gate it should come from preservation
of the homogenizing target coordinate in the two oriented affine rows.
Neither implication has yet been proved at complete source level.

## Sharp counterguards

The actual scalar pivot of `e6b390a` can be completed to

\[
 A_D=
 \begin{pmatrix}
 4&-2&-1\\
 3&-2&0
 \end{pmatrix},
 \qquad k=(2,3,2).
\]

Take `Phi=I` and identical physical `q` rows.  Then the protected square and
the `q` comparison are exact.  Nevertheless the canonical target selector
`e_tau^*=(0,0,1)` reads `2` on `k`, whereas the physical row

\[
                         h_{\rm dark}=(4,-2,-1)
\]

lies in `row(A_D)` and kills `k`.  Thus the shared odd comparison plus the
quotient-defect theorem cannot imply (1).  This is the smallest guard using
the actual fan-pivot first row; it is an exact linear-algebra guard, not a
claim of a full Krenn source counterexample.

There is a second independent guard.  A protected comparison may collapse
the marked kernel line.  With `J=J_0=(1,0)` and

\[
                         \Phi=\begin{pmatrix}1&0\\0&0\end{pmatrix},
\]

the protected square commutes, but `Phi(0,1)=0`.  Even literal transport of
the pulled-back anchor then has zero value.  This is why (2) must include
`h_0(Phi k)!=0`, rather than only a row-space congruence.

## Exact frontier

After one complete physical odd `Phi` and literal `q=M-a` typing, packet
agreement is closed automatically by the quotient alternative.  The sole
remaining constructive row law is:

> On the minimum target circuit, transport the physical pure/target anchor
> modulo the complete protected rows and prove that the marked circuit is
> not collapsed; equivalently, prove `h_phys(k)!=0`.

If the intended proof instead wants to use the dark arm
`h_phys in row(A_D)`, it still needs a separate theorem typing that row
factorization as an existing Hall/Fitting exit.  Abstract row-space
membership alone does not provide such typing.

## Scope and verification

This is an exact composition and minimal counterguard.  It does not
construct the shared odd comparison, the shifted Gate-I label map, or the
physical anchor transport.

Run

```text
python3 computations/verify_h3_shared_odd_comparison_anchor_visibility_gate.py
python3 -O computations/verify_h3_shared_odd_comparison_anchor_visibility_gate.py
python3 -I -S computations/verify_h3_shared_odd_comparison_anchor_visibility_gate.py
```

Frozen ledger SHA-256:

```text
f74bfd6e0657ab983048d3c04f063b25109aafb9f9de97b417e6a5601eb6e0d9
```
