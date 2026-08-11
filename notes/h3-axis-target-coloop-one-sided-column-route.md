# The physical E3 landing has a one-sided linear response route

> **Correction to 024463c.** The first version incorrectly used target
> coloopness to force a proportional outside complete column to be zero.
> The compared target-port cell is decorated by the selected mixed word and
> need not be the pure-target anchor decoration. Thus both columns may have
> zero pure-target coordinate. The exact statement is the absorption/lock
> dichotomy below, independently checked in the companion-boundary note.

## Result

After 54c1be7, the single-C6/C8 target-coloop packet always acquires a
third unary/direct matching base. There is also an exact one-sided
alternative already present in the two response bases.

Fix one selected mixed word with endpoint labels (i,j). At P the
target-skeleton and outside ports are components of the same p_i row; at S
they are components of the same s_j row. Work one endpoint at a time:

    P-only comparison: two complete columns in p_i;
    S-only comparison: two complete columns in s_j.

Hold q and every opposite-endpoint row fixed. If the complete columns obey

\[
 C_{\rm out}=\lambda C_{\rm cmp},                      \tag{1}
\]

then the exact finite update is

    x_out -> 0,
    x_cmp -> x_cmp + lambda*x_out.

It preserves every full response coefficient. It is anchor-safe and
support-reducing unless the companion decoration is protected and its
updated coefficient becomes zero. That exceptional event is the exact
anchor-contained lock. If the complete columns are nonproportional, some
source-valid same-star 2 by 2 minor is nonzero.

Checker:
computations/verify_h3_axis_target_coloop_one_sided_column_route.py.

## Why this is not the bistar Hessian

The operation changes one p_i row, or one s_i row, while the opposite
endpoint and common quadratic are fixed. The response tensor is exactly
linear in that row. The mixed second difference that obstructs a
simultaneous change at both endpoint stars does not occur.

The protected-companion cancellation must not be called a deletion
contradiction. Likewise, a same-star minor is not by itself identified with
the downstream four-good or clean interface.

## Forced-unary edge-union census

The checker enumerates the seven physical single-cycle response pairs and
all fifteen direct unary bases. Among the 7 times 15 = 105 unions:

    55 contain a crossed response perfect matching;
    50 contain no crossed response perfect matching.

The per-response counts are 5,8,8,8,9,8,9. This is only a physical
edge-union statement. It does not say the requisite decorated cells or the
crossed matching monomial are nonzero. Consequently it cannot replace the
one-sided complete-column argument.

Among the 50 no-crossed unions, the numbers of perfect matchings supported
by the whole union have histogram

    3:13, 4:17, 5:14, 7:6.

The smallest canonical residual supports exactly the three input bases:

    M = P0 | S1 | 23 | 45,
    N = 01 | P2 | S3 | 45,
    K = PS | 01 | 23 | 45.

There is no fourth perfect matching, crossed or otherwise, on this physical
edge union. Thus the sharp residual is this three-base web together with a
nonzero one-sided same-star minor. Routing that minor requires a complete
coefficient to introduce a new physical edge; cycle recombination inside
the displayed union is exhausted.

## Verification

Run:

    python3 computations/verify_h3_axis_target_coloop_one_sided_column_route.py
    python3 -O computations/verify_h3_axis_target_coloop_one_sided_column_route.py
    python3 -I -S computations/verify_h3_axis_target_coloop_one_sided_column_route.py

Frozen ledger SHA-256:

    4c2ad1df552a7230c14c8b4d74e5b38b07246bb88d2e07205cc90ec86d52eb5e
