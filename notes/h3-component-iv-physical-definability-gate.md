# Component IV stops before a physical filtered differential

Research boundary only.  This note does not prove the unified overlap
theorem, `SP-CLEAN-BRIDGE`, or Krenn's conjecture.

## Outcome

The proposed (h=3) Component-IV radial-to-response (d_2) is not yet a
defined physical operation.  Two independent prerequisites fail in the
current repository.

First, the rational five-exposed calibration is not a point of the complete
eight-site ternary equation scheme.  Its direct-free packet fails exactly
six of the (9\cdot3^6=6561) coefficients:

\[
\begin{array}{c|c|c|c|c}
\text{residual word}&i&j&\text{value}&\text{target}\\ \hline
000000&0&0&0&1\\
012112&2&2&1&0\\
012212&2&1&1&0\\
012212&2&2&1&0\\
111111&1&1&0&1\\
222222&2&2&0&1.
\end{array}
\]

The tilted calibration fails seven coefficients.  Therefore neither can be
used as a physical basepoint, and its normalized scalar (Y=1) cannot be
declared to be an ordinary-residue coordinate on a full source.  In fact, an
exact (N=8,D=3) full-EqSystem point with the prescribed three pure targets
would itself be a counterexample to the conjecture.  Requiring such a point
before formulating the proof route is circular; the replacement must be a
universal relative construction over the full EqSystem coordinate ring.

Second, the needed relative chain does not descend from the currently typed
source columns.  Normalize the four physical readouts as

\[
 (E,W,T,O)=
 (u\,\mathrm{Eq}|_{\text{edges}=0},,Yw,,\mathrm{target},,Y\,\mathrm{ores}).
\]

The full cap basis and all 60 labelled denominator/lower-face candidates
span a saturated rank-three submodule.  The primitive integral covector

\[
                    \lambda(E,W,T,O)=E+W+T-O
\]

annihilates every one of those columns, while

\[
             K=(0,1,0,0),\qquad \lambda(K)=1.
\]

Adjoining (K) raises the rank from three to four with determinant
(\pm1).  Thus the missing datum is not a scalar normalization or a hidden
torsion class.  It is a genuinely new literal relative source generator
(n_c) satisfying

\[
 d n_c=\kappa Yw,\qquad
 \operatorname{tgt}(n_c)=0,\qquad
 \operatorname{ores}_c(n_c)=0.                         \tag{1}
\]

Equivalently, its normalized physical column must be (K), outside
\(\ker\lambda\).  This is the earliest source-level definability gate.

## Why the formal calculations do not supply (1)

The selected-row target-augmented complex is internally consistent.  Its
filtered representative is the cap graph

\[
             (-\kappa,-\kappa Y),
\]

which is killed by the common diagonal-anchor mode.  Deleting its target
coordinate would leave the desired response, but the pair
((0,-\kappa Y)) has boundary (-\kappa Yw\), so that deletion is not a
chain operation.

Upstairs, the fourth-Hasse construction reconstructs a 17-term formal
combination with boundary (kappa Yw) and zero target/residue.  It does not
declare a new generator.  Under diagonal projection to the physical module,
every available proper face lies in (ker\lambda), while the desired column
does not.  Hence the formal combination is a useful symbol for (1), but its
projection is not a source-provenant chain map.

This also explains why a Jacobian calculation at the rational calibration
would answer the wrong question twice: the calibration is off the full
EqSystem scheme, and the ordinary-residue map has no physical relative-chain
definition there.

## Exact scope and next theorem

The checker
[`verify_h3_component_iv_physical_definability_gate.py`](../computations/verify_h3_component_iv_physical_definability_gate.py)
replays the complete coefficient failure census, the selected filtered
square, the 17-term formal lift, and the saturated primitive cokernel of the
60 labelled physical lower faces.

It proves no global nonexistence of (1) in an unknown larger source
resolution.  The smallest honest next theorem is:

> Over the localized full-EqSystem coordinate ring of the two-chart packet,
> construct a literal relative generator (n_c) satisfying (1), with an
> ordinary-residue readout invariant under all source relations; or prove
> that the primitive covector (lambda) extends to every admissible
> full-source relative generator.

Only after that theorem is available is the target-augmented radial-to-
response (d_2) defined and eligible for a value or rank comparison.
