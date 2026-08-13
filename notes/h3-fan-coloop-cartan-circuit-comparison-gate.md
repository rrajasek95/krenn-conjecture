# The fan-coloop pivot reaches the same protected comparison/anchor gate

## Result

The complete-row pivot from `32ce01c`,

\[
                 \alpha U_i-d_iV_i=\alpha,             \tag{1}
\]

does not by itself satisfy the hypotheses of the target-augmented Cartan
circuit theorem.  It is one evaluated response coordinate.  The aggregates
`U_i,V_i` are sums of matching occurrences in two complete word rows, not
independent complete columns of one protected affine map.

There is nevertheless a precise conditional composition.  Construct a
source-valid two-root comparison on the endpoints of the coloop edge which
transports the full `V_i` packet to the `U_i` packet, including every
protected row.  Take a minimum affine support in the resulting complete
target fibre.  Its target augmentation is then a circuit `k`, and the
theorem of `b6775b0` applies to the placed physical Cartan column.

* An internal Cartan column gives a normalized affine exchange or a
  homogeneous unit-Cartan connector.
* An external Cartan column gives a target-dark separator.
* The constructive two-rank landing occurs precisely when

  \[
                         h_{\rm phys}(k)\ne0.           \tag{2}
  \]

  On the corank-one circuit block, after normalizing the two nonzero
  functionals, this is equivalent to

  \[
                 h_{\rm phys}-e_\tau^*
                    \in\operatorname {row}(A_D).       \tag{3}
  \]

The new point is negative but simplifying: neither the pure-colour coloop
normalization nor the ambient Cartan prism proves the missing comparison or
the row congruence (3).  The trapped-carrier gate has reduced to the same
protected two-root comparison plus separate physical-anchor law already
isolated in Gate I.  It is not an independent Hall enumeration.

Checker:
[`verify_h3_fan_coloop_cartan_circuit_comparison_gate.py`](../computations/verify_h3_fan_coloop_cartan_circuit_comparison_gate.py).

## 1. Why the scalar pivot is not yet a circuit

At one exact numerical point take

\[
       \alpha=2,\qquad d_i=3,\qquad V_i=2,\qquad U_i=4.
\]

Then (1) holds, and the scalar augmented row

\[
                         (U_i,-V_i,-1)=(4,-2,-1)       \tag{4}
\]

kills `(alpha,d_i,alpha)=(2,3,2)`.  But (4) has rank one and a
two-dimensional kernel.  The displayed vector is not a circuit.  Indeed,
in a one-dimensional scalar codomain either nonzero old coordinate alone
already spans the target.

The actual affine problem is the complete protected response map.  Its
other word and response coordinates decide whether the scalar occurrence
extends to a target point or carries debts.  Thus applying `b6775b0` to
`[U_i,-V_i,-1]` would forget precisely the trapped-carrier theorem being
sought.

## 2. The two-root target defect has four word directions

Let `w` swap colours `c,i` at the two endpoints `u,v` of the coloop edge.
Write

```text
p_c, p_i       for the pure-c and pure-i target words,
m_(c|i)        for c at u,v and i elsewhere,
m_(i|c)        for i at u,v and c elsewhere.
```

On the GHZ target,

\[
                 (w-1)\Delta
                    =m_{c|i}+m_{i|c}-p_i-p_c.          \tag{5}
\]

These are four distinct output words at every even order at least four.
Let `s=(P S)` be the endpoint-orientation transposition, disjoint from the
two local root sites `u,v`.  It fixes each of the four words because their
`P,S` colours agree.  Therefore

\[
 (1-s)(w-1)\Delta=0,
 \qquad
 (1+s)(w-1)\Delta=2(m_{c|i}+m_{i|c}-p_i-p_c).          \tag{6}
\]

This explains the exact parity boundary.

* The endpoint-odd physical Cartan prism is target-safe, but its boundary
  is the orientation difference rather than the desired signless
  `V_i -> U_i` comparison.
* The signless prism has the desired orientation symmetry but carries the
  four-word target defect (5).
* The pure-`c` coloop row can alter only the `p_c` target direction.  Even
  both pure target rows span only `p_c,p_i`; neither can cancel the two
  mixed directions in (5).
* A common global colour permutation merely relabels the same four distinct
  words.  It cannot change this conclusion.

Hence the relation `alpha*C_c=1` does not target-correct the signless prism.
Retaining its signless boundary requires an independent relative target or
mapping-cone cell whose boundary contains the two mixed directions.  This
is exactly the protected two-root source type already isolated by the
determinant-dark cut-swap comparison.

### The canonical workaround avoids the signless no-go

There is a better composition, already successful in the canonical E14
packet.  Do **not** construct a signless Cartan homotopy.  The complete-row
pivot (1) is itself the physical signless source row.  Project one selected
endpoint-hole/tail orbit to its two `P/S` orientations and write

\[
\begin{aligned}
 S={}&\alpha(U_++U_-)-d_i(V_++V_-)-\alpha,\\
 D={}&\alpha(U_+-U_-)-d_i(V_+-V_-).                  \tag{7}
\end{aligned}
\]

Here `S` is supplied by the exact complete source combination
`alpha*G_pure-d_i*G_mixed`, while `D` is target zero.  If the target-safe
endpoint-odd Cartan prism has **exactly this complete protected projection**,
then

\[
\begin{aligned}
 E_+={S+D\over2}&=\alpha U_+-d_iV_+-{\alpha\over2},\\
 E_-={S-D\over2}&=\alpha U_--d_iV_--{\alpha\over2}.  \tag{8}
\end{aligned}
\]

Thus both orientations become physical target-bearing affine rows.  This
avoids the four-word target defect of a signless Cartan homotopy completely:
the signless object was already present as a source row, and only the odd
Cartan direction is newly attached.

The qualification in bold is the remaining comparison theorem.  Uniform
Cartan placement proves a nonzero marked coefficient in the right exact
word/tail/orientation/fine label, but it does not yet prove that every other
retained Cartan corner has the coefficient multipliers and protected
readouts of `D` in (7).  A single extra retained protected feature makes the
desired `D` independent of the span of `S` and the contaminated odd row.
Consequently the positive statement is:

```text
same complete protected S/D packet -> two oriented affine rows (8),
packet mismatch outside saturation -> literal typed exit,
packet mismatch inside saturation  -> the protected-comparison obstruction.
```

This narrows the missing comparison.  It need not manufacture a signless
homotopy or cancel its target defect; it only has to identify the projection
of the already target-safe odd Cartan prism with the odd part of the physical
pivot packet, modulo protected rows or a typed saturated exit.  After (8),
the remaining constructive input is the row congruence (3).

## 3. The ambient Cartan column does not prove the anchor law

The physical Cartan prism uniformly constructs an ambient target-safe
word-changing column `g`.  The rectangular theorem still has two independent
visibility conditions:

```text
[g] nonzero in coker(A_D),
h_phys nonzero on ker(A_D).
```

The checker completes (4) to the corank-one protected matrix

\[
 A_D=
 \begin{pmatrix}
 4&-2&-1\\
 3&-2& 0\\
 0& 0& 0
 \end{pmatrix},
 \qquad k=(2,3,2),
 \qquad g=(0,0,1).                                    \tag{9}
\]

The same scalar pivot and external Cartan column admit two row behaviours.

1. `h_dark=(4,-2,-1)` is already in `row(A_D)` and kills `k`.  Appending
   `g,h_dark` raises rank only from two to three.
2. `h_bright=e_tau^*=(0,0,1)` sees `k` and gives the full rank four.

Thus the pure target coefficient being normalized to one is not the
physical row congruence (3).  A target-bearing physical row can lie in the
protected row space and be completely dark on the circuit.  This is the
same sharp guard as in the target-augmented affine theorem, now with the
actual fan-coloop scalar pivot as its first row.

## 4. Exact composition with the two global gates

The remaining proof can use one source theorem schema.

> **Protected odd-Cartan packet comparison with anchor alternative.**  In
> every required fine grade, identify the complete protected projection of
> the target-safe odd Cartan prism with the odd part of the already physical
> signless pivot row.  Either its physical terminal/comparison
> defect is nonzero and gives the already typed relative or Hall/Fitting
> exit, or equations (8) give the two oriented affine rows.  On a minimum target
> circuit, either `h_phys(k)!=0`, giving rectangular Cartan landing, or the
> dual row-space failure is itself a physical saturated Hall/Fitting
> covector.

For Gate I this comparison descends the determinant-dark collision packet.
For the fan-coloop gate it upgrades (1) from one scalar response coordinate
to the complete `V_i -> U_i` protected comparison.  The word-change and
anchor-law mechanism is the same, although fine-grade transport between the
two packets still has to be constructed; the existing canonical comparison
cannot simply be declared uniform.

Once that comparison exists, the earlier results finish the remaining
linear alternatives:

```text
internal Cartan  -> affine exchange or homogeneous unit connector,
external Cartan  -> target-dark separator,
nonzero terminal/comparison defect -> relative generator or typed exit,
bright physical anchor -> rank-two localized source unit.
```

The six saturated Hall concepts need no further orbit-specific response
identity.  Their only role is to type a dual failure when every carrier of
(1) remains trapped.

## Scope and verification

This is an exact target-word and linear-algebra obstruction.  The numerical
row-space packet is not asserted to be a full Krenn source counterexample.
The theorem does not construct the protected two-root mapping-cone cell or
prove its physical anchor law.

Run

```text
python3 computations/verify_h3_fan_coloop_cartan_circuit_comparison_gate.py
python3 -O computations/verify_h3_fan_coloop_cartan_circuit_comparison_gate.py
python3 -I -S computations/verify_h3_fan_coloop_cartan_circuit_comparison_gate.py
```

Frozen ledger SHA-256:

```text
3448a7fd4d50a437574e718dd804f173bb25763fa2894c6d4c739c5ba0a49da5
```
