# Linear L0 excludes the displayed dense transverse-column guard

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

The exact rank-\(55\) packet from the
[transverse-column potential boundary](level-two-two-invertible-transverse-column-potential-boundary.md)
has no completion to the full L0 equations. If

\[
                              D=d\Psi_M,
\]

then its exact incidence ranks over
\(\mathbf Q,\mathbf F_{101},\mathbf F_{32003},\mathbf F_{1000003}\) are

\[
\begin{array}{c|c}
\text{matrix}&\text{rank over all four fields}\\ \hline
D&55\\
D_{\mathrm{mixed}}&55\\
[D\mid e_{0^6}]&56\\
[D\mid e_{1^6}]&56\\
[D\mid e_{0^6}\mid e_{1^6}]&57.
\end{array}                                                     \tag{1}
\]

Thus neither pure L0 target lies in \(\operatorname{im}D\), and their
cokernel classes are independent. This is a fixed-packet obstruction. It
does not exclude other choices of the eight free core-to-zero blocks on the
dense transverse potential ray.

## Why the pure targets must lie in the tangent image

For every binary endpoint completion, partitioning the eight-site perfect
matchings according to their endpoint behavior gives, on each endpoint
slice \((s,t)\),

\[
             T_{st}=W_{st}\Psi(M)+D(N^{st}).                   \tag{2}
\]

The matching tensor is cubic in the residual packet, so Euler's identity is

\[
                              D(M)=3\Psi(M).                    \tag{3}
\]

Consequently every slice in (2) belongs to \(\operatorname{im}D\). The two
pure L0 slices are the nonzero coordinate targets \(e_{0^6}\) and
\(e_{1^6}\), but the last three rows of (1) show that neither target belongs
to the image. Hence the displayed guard has no full L0 completion.

Equivalently, deleting the two pure output rows must lower the differential
rank of a rank-\(55\) full solution from \(55\) to \(53\). For this packet
the mixed-row rank stays \(55\), giving the same contradiction.

## The exact packet remains a valid pre-L0 guard

The obstruction re-audits every earlier property of the packet:

* all 60 normalized transverse generic-kernel scalars;
* all 64 selected level-two rows, with matching-tensor support \(48/64\);
* differential rank \(55\) over the rationals and two prime fields;
* five independent trace-zero vertex gauges;
* literal R2 witnesses at all six residual roots; and
* invertible residual spokes to both zero sites.

The potential is

\[
                    \nu=\tfrac12(1,1,1,1,-1,-1).               \tag{4}
\]

The six positive-multiplier core blocks are determined by the transverse
endpoint normal form, and \(M_{45}=0\). The only residual freedom lies in
the eight zero-multiplier blocks

\[
                 04,\ 05,\ 14,\ 15,\ 24,\ 25,\ 34,\ 35,       \tag{5}
\]

containing 32 scalar cells. The present calculation fixes those cells to
the displayed guard values. The other 192 ternary edge cells lie outside
the residual differential \(D\) and cannot repair this fixed packet.

## Exact audit and scope

The standard-library checker
[verify_level_two_two_invertible_transverse_column_l0_obstruction.py](../computations/verify_level_two_two_invertible_transverse_column_l0_obstruction.py)
verifies the universal 256 matching-slice identities, Euler's identity,
all five rank quadruples in (1), the \(6+8+1\) determined/free/zero block
partition, and every generic-kernel, selected-row, rank, gauge, R2, and
invertible-spoke guard audit. It passes normal, optimized, and isolated
Python.

Since linear L0 already fails, no factored-L0 or overlapping-L1 claim is
needed for this packet. The dense transverse normal form as a whole remains
open. The subsequent
[incidence survivor](level-two-two-invertible-transverse-column-l0-incidence-survivor.md)
exhibits a different choice of the 32 free scalars on the necessary locus

\[
 \operatorname{rank}[D\mid e_{0^6}\mid e_{1^6}]
     =\operatorname{rank}D,\qquad
 \operatorname{rank}D_{\mathrm{mixed}}=\operatorname{rank}D-2. \tag{6}
\]

That survivor fails literal R2 at one invertible root, so it does not
supersede the fixed-packet obstruction here.
