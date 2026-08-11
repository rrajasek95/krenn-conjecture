# The current source-constrained HPL packet fails before curvature

This is an exact counterguard for the present labelled source and cap
inventory.  It does not rule out an enlarged relative complex and does not
prove `SP-CLEAN-BRIDGE` or Krenn's conjecture.

## Result

The proposed algebraic-discrete-Morse/HPL route has two independent
necessary low-grade blocks.  Both already have a nonzero relative class.

First, the literal chart-25 fibre has physical rows

\[
                        A_1,A_2,A_3,A_4,D.
\]

Every actual mixed-source column incident to this fibre joins one (A_i)
to (D).  The four incidence types occur with multiplicities
((3,4,4,3)), and every labelled source boundary therefore obeys

\[
                         [D]=\sum_{i=1}^4[A_i].           \tag{1}
\]

Equivalently, the integral partial character

\[
                        \ell=(-1,-1,-1,-1,1)             \tag{2}
\]

annihilates every source column.  The desired quotient HPL packet
(-A_1-A_2-A_3+D) has (ell)-value (4).  A source lift is forced to add
(4A_4); after matching (A_4), the literal second transfer is consequently
(-3D), not (+D).  Gaussian elimination, Schur complementation, and
algebraic Morse cancellation preserve the one-dimensional cokernel detected
by (2).  Thus no choice or ordering of unit pivots inside the current
labelled mixed-source family manufactures the missing (4D) lower face.

Second, the old target-augmented cap block is

\[
 R\langle T,\rho\rangle\longrightarrow R\langle w\rangle,
 \qquad dT=-Yw,\quad d\rho=w,                            \tag{3}
\]

with physical target and ordinary residue

\[
 (\operatorname {tgt},\operatorname {ores})(T)=(1,0),
 \qquad
 (\operatorname {tgt},\operatorname {ores})(\rho)=(0,1).\tag{4}
\]

Hence

\[
 \ker(\operatorname {tgt},\operatorname {ores})=0,
 \qquad
 {Rw\over d\ker(\operatorname {tgt},\operatorname {ores})}=Rw. \tag{5}
\]

For five deleted faces this obstruction has rank five.  In particular an
augmentation-preserving contraction has no invisible degree-one chain with
nonzero (w)-boundary.  This is precisely the zero-indeterminacy failure:
it occurs before the curvature (d_2) can be formed.

Together, (2) and (5) refute an ADMT/HPL contraction built only from the
current physical mixed-source columns and the split cap generators.  The
minimal missing types are exact:

1. a source-labelled relative cell whose projected lower boundary supplies
   (4D); and
2. an invisible cap chain (n) with
   (dn=\gamma w), (operatorname {tgt}(n)=0), and
   (operatorname {ores}(n)=0).

The intrinsic single-edge cap theorem of commit `a67ec1d` weakens the
desired terminal critical cell, but it does not remove this obstruction.
The current cap block contains no invisible chain at all, so there is no
terminal response whose physical-edge support can yet be tested.  Once a
new chain of the second type is constructed, preserving scalar zero,
diagonal target labels, and the direct-sum grading by physical edge is the
correct weaker terminal requirement.

## Scope

The five-row statement is source-faithful: the dependency checker reruns all
56 actual mixed-source columns incident to the complete frozen partial
character, not an orbit-only incidence matrix.  The cap statement is
universal over the coefficient ring because (4) is a split identity map.

This does **not** prove that no larger anchored two-chart relative complex
can work.  It proves exactly what that enlargement must change.  Adding
ordinary source syzygies cannot change (2), and base change inside the split
cap block cannot change (5).  A positive construction must add a genuinely
new source-provenant lower face and a target/residue-invisible cap lift.

## Verification

Run

```text
python3 computations/verify_source_constrained_hpl_relative_counterguard.py
python3 -O computations/verify_source_constrained_hpl_relative_counterguard.py
```

The checker reruns the frozen literal-source and Reynolds-cap dependencies,
reconstructs the five-row source matrix and its integral separator, verifies
the relative augmentation rank obstruction at three rational
specializations, and pins ledger digest
`909cd81e09160255b99807063b392dda85189226eead2cc0ba56da4a5f4c9d96`.
