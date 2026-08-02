# The two-invertible incidence survivor fails a factored L0 cut

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

The exact (2I+2R+2Z) packet from
[the linear-incidence survivor](level-two-two-invertible-l0-incidence-survivor.md)
has no completion to two physical, shared endpoint stars.  It passes the
necessary linear L0 screen, but its pure-zero slice already violates the
rank-two condition on one residual cut.

Let (D=d\Psi_M), and solve exactly

\[
                         D K^{00}=e_{0^6}.
\]

The packet has rank (55), and its kernel is exactly the five vertex
gauges.  After absorbing the direct endpoint cell by Euler, any factored
pure-zero slice would therefore have the form

\[
 B_{00,ru}=K^{00}_{ru}+(\lambda_r+\lambda_u)M_{ru}
 =U_r^0(V_u^0)^{\mathsf T}+V_r^0(U_u^0)^{\mathsf T}.
\]

Across the cut

\[
                    \{0,1\}\mid\{2,3,4,5\},
\]

this is a (4\times8) matrix with rank at most two.  Consequently all

\[
                    \binom43\binom83=224
\]

cubic minors must vanish.  Exact degree-reverse-lexicographic elimination
of the 80 nonzero minors (the other 144 vanish identically) in the six
unrestricted variables
(\lambda_0,\ldots,\lambda_5) gives

\[
       \operatorname{std} I_{3}(B_{00})=(1)
       \quad\text{over }\mathbb Q
       \quad\text{and over }\mathbb F_{32003}.
\]

Thus no gauge representative of the pure-zero preimage has cut rank at
most two.  A different choice of (K^{00}) cannot repair this: any two
preimages differ by a vertex gauge, which is absorbed by translating the
six (\lambda_r).  The contradiction is a necessary single-slice
condition, so no mixed-support or larger shared-factor subsystem needs to
be solved for this packet.

This obstruction is packet-specific.  It does not exclude the full
two-invertible incidence locus or prove Krenn's conjecture.

The checker
[verify_level_two_two_invertible_factored_l0_cut_obstruction.py](../computations/verify_level_two_two_invertible_factored_l0_cut_obstruction.py)
reconstructs the committed packet, rechecks generic kernel, selected L2,
rank (55/53), pure-target incidence, and R2, computes (K^{00}) by exact
rational row reduction, constructs all 224 cut minors in memory, and
requires the two exact unit Groebner bases.  It uses standard-library
Python plus an external `Singular` executable.
