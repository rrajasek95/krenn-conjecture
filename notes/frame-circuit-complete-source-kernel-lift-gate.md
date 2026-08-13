# The frame circuit needs a marked lift to the complete source kernel

## Result

The anchored minimum-support theorem does not yet supply the hypothesis of
the rectangular anchor--Cartan alternative.  It constructs a marked
primitive circuit

\[
                         Bc=0                         \tag{1}
\]

for the unsigned optical port-incidence map `B`.  The rectangular theorem
needs a vector with nonzero marked anchor coordinate in

\[
                         \ker M,                       \tag{2}
\]

where `M` is the **complete labelled source-incidence map**.  There is no
proved chain map identifying (1) with (2).

The common-tail theorem narrows the gap but does not close it.  On its best
branch the two sides of `c` become literal occurrences in the same output
word.  It explicitly leaves the other matching terms of the complete source
row as contamination.  Thus it constructs a candidate lift, not a kernel
vector of `M`.

The exact missing interface is a marked-coordinate-preserving relative
chain lift.  It replaces the proposed square corank-one zero-holonomy cover;
no such cover is needed once this lift exists.

Checker:
[`verify_frame_circuit_complete_source_kernel_lift_gate.py`](../computations/verify_frame_circuit_complete_source_kernel_lift_gate.py).

## Exact lift-or-separator theorem

Let `x0` be the candidate complete-source vector obtained from a marked port
circuit and let `h` be its physically typed marked covector.  Put

\[
 q=h(x_0)\ne0,\qquad d=Mx_0.                           \tag{3}
\]

Exactly one of the following holds.

1. There is a relative correction `z` satisfying

   \[
                         Mz=-d,\qquad h(z)=0.           \tag{4}
   \]

   Then `x=x0+z` lies in `ker M` and retains the nonzero marked value
   `h(x)=q`.
2. There is a row-space separator `lambda` satisfying

   \[
                  \lambda^T M=h,
                  \qquad \lambda^T d=q\ne0.            \tag{5}
   \]

The proof is elementary but load-bearing.  Appending `h` to `M` either
raises row rank or it does not.  In the first case `h` is nonzero on
`ker M`; scale a kernel vector to have marked value `q`, which solves (4).
In the second case `h` belongs to `row(M)`, giving (5).  The identity on the
defect follows from `d=Mx0`.

Thus the first obstruction is not “a connected component with the wrong
holonomy.”  It is the exact failure of the marked coordinate to survive in
the kernel of the complete source presentation.

## Sharp two-column guard

Take the parallel optical frame circuit

\[
 B=(1\;1),\qquad c=(1,-1),\qquad h=(1,0).              \tag{6}
\]

Then `Bc=0` and `h(c)=1`.  Three complete-source maps distinguish all cases.

* If `M=(1  1)`, the port circuit is already a complete-source kernel.
* If `M=(1 -1)`, the candidate has defect `2`, but `z=(0,2)` cancels it
  without changing the first coordinate.  The corrected kernel is `(1,1)`.
* If `M=(1  0)`, every complete-source kernel vector has first coordinate
  zero.  No marked lift exists, although the optical frame circuit is
  unchanged.  The separator `lambda=1` gives `lambda M=h` and reads `1` on
  the defect.

The last example is the minimal counterguard to the claimed implication

```text
marked optical frame circuit  -/->  marked complete-source kernel circuit.
```

It is a logical/source-typing guard, not a physical counterexample to the
possible lift theorem.

## When the separator is already a typed exit

If `h=e_s^*` is literally the coordinate covector of the marked source
occurrence, (5) becomes

\[
                         \lambda^T M=e_s^*.            \tag{7}
\]

This is a protected source-row combination with coefficient one at the
marked occurrence and zero at every other coordinate in the complete
packet.  Equivalently, the marked column is a coloop/pivot of the complete
source matroid.  Equation (7) is then a localized source-unit exit, not an
unclassified anchor-dark component.

If the physical anchor covector is not a literal coordinate row, (5) is
still an exact Fredholm separator, but it cannot be called a source unit or
active/Hall exit until its target, residue, terminal, and fine-grade readout
are physically landed.  This distinction is why one cannot simply assume
every connected component has nonzero anchor charge.

## Minimal positive theorem

On the squarefree common-tail branch, construct a lift `Lambda` into the
complete labelled source domain such that

\[
                         h\Lambda(c)=c_s\ne0.           \tag{8}
\]

It is enough to prove either the exact chain identity

\[
                         M\Lambda(c)=0,                \tag{9}
\]

or a relative nullhomotopy `K(c)` with

\[
             MK(c)=M\Lambda(c),\qquad hK(c)=0.         \tag{10}
\]

Then `(Lambda-K)c` is the marked complete-source kernel required by the
rectangular theorem.  This is strictly weaker than embedding the occurrence
in a square, corank-one, zero-holonomy bicycle block and is the shortest
current entry interface.

The known source trichotomy fits around it without change:

```text
protected-relative frame circuit
        |
        +-- no common tail ------> Tutte/Hall accessibility exit
        |
        +-- repeated site -------> principal-parts/Cartan-Spencer face
        |
        `-- literal common tail --> marked lift (8)--(10)
                                      |
                                      +-- corrected kernel
                                      `-- row-space separator (5)
```

Once the corrected kernel has nonzero anchor value, the rectangular
anchor--Cartan alternative applies to arbitrary `M`: an external Cartan
class raises rank by two, while an internal Cartan class gives a
unit-coordinate kernel after adjustment along this marked kernel direction.

## Shifted proof frontier

The global entry task is therefore no longer to manufacture an exhaustive
cover of square critical components.  It is:

> Lift each common-tail optical circuit to the complete labelled source
> presentation while preserving one marked coordinate, or identify the dual
> row-space separator as a physically typed terminal/source-unit exit.

The optical theorem and common-tail typing give the domain-side candidate.
What remains is a naturality/comparison theorem controlling its complete
source defect.  A larger enumeration of component supports would not prove
that comparison uniformly.

## Verification

Run:

```text
python3 computations/verify_frame_circuit_complete_source_kernel_lift_gate.py
python3 -O computations/verify_frame_circuit_complete_source_kernel_lift_gate.py
python3 -I -S computations/verify_frame_circuit_complete_source_kernel_lift_gate.py
```

Frozen ledger SHA-256:

```text
d1f2dcfb7b390a3d4476c71bb3dbbe2b68e2a60d154561e465ce3d8e6ebd5d27
```
