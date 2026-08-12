# Reciprocal response reaches the right grade but the wrong parity

## Verdict

The reciprocal response Hasse--Bianchi identity is a serious candidate for
the shared endpoint/rootless homotopy: its middle term has exactly the
operation degree

\[
                       (\deg p,\deg s,\deg q)=(1,1,2),
\]

of the E14 endpoint face.  Its quadratic proper face has degree `(2,2,1)`
and cancels under Bianchi antisymmetrization.  Thus this route does not fail
for lack of a common multiplier or a coarse degree match.

It nevertheless does not construct

\[
 A=E_+-E_-+\Omega_1-q_{1,23\mid45}.                  \tag{1}
\]

There are two exact reasons.

1. The literal reciprocal identity returns the signless diagonal response
   `E_+ + E_-`, not `E_+ - E_-`.
2. Any forced endpoint-odd refinement has zero ordinary residue under the
   committed endpoint-invariant residue law, while `A` combined with the
   rootless bar requires an endpoint-odd row of ordinary residue one.

So reciprocal curvature alone cannot be the missing attachment.  The first
possible positive object is an endpoint-oriented Kodaira--Spencer lift plus
an independent, source-labelled reduced-residue correction in the same
repeated grade.

## Exact response calculation

Write

\[
 Q=q^{[3]},\qquad R_{ij}=p_i s_jq^{[2]},\qquad
 K_{ij;kl}=p_i s_jp_k s_lq^{[1]}.
\]

The reciprocal Hasse identity is

\[
 D_{kl}E_{ij}=d_{ij}R_{kl}+K_{ij;kl},
 \qquad K_{ij;kl}=K_{kl;ij}.                          \tag{2}
\]

For a literal offdiagonal direct cell
`d=lambda E_ab` and a diagonal row `cc`, equation (2) gives

\[
 D_{cc}E_{ab}-D_{ab}E_{cc}
     =\lambda R_{cc}=\lambda X_c                     \tag{3}
\]

on the source equations.  After the pure target is put back, the
target-corrected row is simply

\[
                  \lambda(R_{cc}-X_c)=\lambda E_{cc}. \tag{4}
\]

Thus the reciprocal curvature has returned to an existing diagonal
response row.

The checker expands (R_cc) on six labelled residual sites.  On the
canonical matching tail

\[
                             24\mid35,
\]

the two endpoint assignments are

\[
\begin{aligned}
 E_+&=p_c@0\;s_c@1\;q_{24}^{11}q_{35}^{11},\\
 E_-&=p_c@1\;s_c@0\;q_{24}^{11}q_{35}^{11}.
\end{aligned}
\]

Both occur in (R_cc) with coefficient (+1).  Reversing the Bianchi
orientation changes them both to (-1).  It never changes only one sign.
The exact endpoint projection is therefore

\[
                             (1,1),                    \tag{5}
\]

and the endpoint-orientation covector `(1,-1)` reads zero.  The checker
verifies (5) for all eighteen choices of offdiagonal direct row and diagonal
target row, and verifies all eighty-one literal symmetries in (2).

## Why an oriented refinement still misses one face

Include target and ordinary residue after the four geometric features
`(E_+,E_-,Omega,qcomp)`.  With the signs of the committed rootless bar,

\[
\begin{aligned}
 B&=(0,0,-1,+1;0,1),\\
 A&=(1,-1,+1,-1;0,0).
\end{aligned}                                          \tag{6}
\]

Consequently the endpoint row which would complete the attachment is

\[
                 D=A+B=(1,-1,0,0;0,1).                \tag{7}
\]

The response/old-cap ordinary-residue functional is invariant under
transposition of the two endpoint sites.  On the two endpoint coordinates
it factors through

\[
                         \epsilon(e_+,e_-)=e_++e_-;   \tag{8}
\]

this is the pinned equality `qaug=ores` for the committed matching-face
landing.  Over characteristic zero every endpoint-odd row is killed by an
endpoint-invariant functional.  In particular,

\[
               \epsilon(1,-1)=0.                      \tag{9}
\]

Suppose, more strongly than the reciprocal identity proves, that a
Kodaira--Spencer refinement supplied the odd row

\[
                         O=(1,-1,0,0;0,0).
\]

Then

\[
 O-B=(1,-1,+1,-1;0,-1),                               \tag{10}
\]

which has precisely the four geometric coordinates of (1), but ordinary
residue (-1).  One further correction

\[
                         Z=(0,0,0,0;0,+1)              \tag{11}
\]

in the **same source word and repeated fine grade** would give

\[
                         O-B+Z=A.                      \tag{12}
\]

Equation (11) is a typed requirement, not permission to import a bare
ordinary-residue symbol from another source block.  Producing its
same-word copy (or an equivalent hidden even correction) is the reduced
relative attachment still missing.

The pure target on the right of (3) does not repair (10).  It has zero old
ordinary residue; cancelling it with the committed target cap changes the
target/cap rows but does not create (11).

## Common multiplication cannot change the verdict

Multiplication by a common tail acts equally on (E_+) and (E_-).  It
preserves both eigenspaces of endpoint transposition:

\[
 \mu(E_++E_-)\text{ remains even},\qquad
 \mu(E_+-E_-)\text{ remains odd}.                     \tag{13}
\]

It also preserves the invariant-residue equation (9).  Therefore a common
tail may place the reciprocal row in the desired repeated
`P3 disjoint K2` cell degree, but it cannot turn (5) into the required odd
row or make an invariant residue functional nonzero on that row.  The
obstruction is parity plus source typing, not polynomial homogenization.

## The relative-Ext/Fredholm alternative

This calculation identifies how a larger resolution could finish the
branch, but the bounded parity covector is not already a physical Macaulay
annihilator.

Let (J) be the **complete** augmented correction map in the fixed repeated
grade, retaining source boundary, (W), target, and ordinary residue.  Once
an oriented Kodaira--Spencer lift (O) is constructed, equation (11) is a
linear lifting problem for (J).

* If (Z) exists and its correction torsor has nonzero physical terminal
  indeterminacy, the normalized difference of two corrections is the
  relative generator of the `0373033` alternative.
* If the physical terminal functional kills (ker J), (Z) and hence (A) are
  well-defined; the clean cycle edges propagate the resulting comparison
  vertex and the pentagon Fredholm alternative applies.
* If (Z) does not exist, linear duality supplies a covector killing
  (im J) and detecting its missing class.  It becomes the physical
  Fredholm/Macaulay annihilator only after (J) is proved exhaustive and its
  terminal landing is source-provenant.

The current reciprocal packet supplies neither the oriented lift (O) nor
the exhaustive physical map (J).  Therefore its failure is a sharp
relative-Ext boundary, not by itself the positive generator or the global
annihilator.

## Verification

Run:

```text
python3 computations/verify_h3_reciprocal_response_rootless_attachment_parity_gate.py
python3 -O computations/verify_h3_reciprocal_response_rootless_attachment_parity_gate.py
python3 -I -S computations/verify_h3_reciprocal_response_rootless_attachment_parity_gate.py
```

Frozen ledger SHA-256:

```text
4a7b2e6287d2e00827bd21782de430580776c00003efb6494c3e8a341f7089e7
```
