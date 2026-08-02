# Closure of the three-invertible, three-zero stratum

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

Let

\[
 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv}
\]

on six residual sites. Suppose \(X_i\) is invertible at three sites
\(I\), while \(X_z=0\) at the other three sites \(Z\).

> **Theorem.**
> \[
>                         \operatorname{rank}d\Psi_M\le54.
> \]

Indeed, every \(I\)-\(I\) block is invertible, while every edge incident
with \(Z\) is zero unless its multiplier sum vanishes, in which case it is
free. The zero-sum equality classes put the free-edge support inside one of
four maximal envelopes, up to relabelling.

1. **No \(Z\)-edge.** Enlarge to all nine \(I\)-\(Z\) blocks. Only the six
   all-cross matchings survive. The 36 cross parameters have four
   independent vertex-gauge tangents, so their differential rank is at most
   32. The twelve transverse \(Z\)-\(Z\) cells give rank at most \(44\).
2. **A nonzero path on \(Z\), cross edges to its two leaves.** Enlarge to
   all six \(I\)-leaf blocks and both centre-leaf blocks. The tensor is the
   sum of two products
   \[
      M_{c\ell_1}\otimes H_{\ell_2}
      +M_{c\ell_2}\otimes H_{\ell_1},
   \]
   with factors of dimensions \(4\) and \(16\). The restricted tangent has
   dimension at most \(19+19=38\); sixteen transverse cells give \(54\).
3. **The zero triangle on \(Z\).** At most one invertible site can have
   multiplier zero. Enlarge to its three \(Z\)-edges. The other two
   invertible sites must match each other, so
   \[
                             \Psi=M_{ij}\otimes H_4.
   \]
   The restricted tangent has dimension at most \(4+16-1=19\), and the
   24 transverse cells give \(43\).
4. **A nonzero path on \(Z\), cross edges to its centre.** The two leaves
   both have the centre as their only possible partner, so the matching
   polynomial vanishes identically on the 32-dimensional support envelope.
   Only the 28 transverse directions contribute.

If the \(Z\)-graph has one nonzero edge, the invertible sites cannot connect
to both opposite-valued endpoints. A lone zero-zero edge can meet the unique
zero-valued invertible site at both ends. In either event the support embeds
in case 2. If the \(Z\)-graph has no edge, it embeds in case 1. For a
two-edge path, invertible sites cannot
connect simultaneously to the centre and leaves because the corresponding
multiplier values are opposite. A triangle forces all three \(Z\)
multipliers to be zero and gives case 3. These observations exhaust the
zero-sum graphs on three vertices.

The theorem is checked by
[verify_level_two_three_invertible_three_zero_closure.py](../computations/verify_level_two_three_invertible_three_zero_closure.py),
which verifies the four matching factorizations formally and gives exact
support calibrations \(44,48,42,27\) modulo two primes. It passes normal,
optimized, and isolated Python. This result does not address the adjacent
three-invertible, one-rank-one, two-zero guard.
