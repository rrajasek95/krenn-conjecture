# The physical E3 landing has a one-sided linear response route

## Result

After 54c1be7, the single-C6/C8 target-coloop packet always acquires a
third unary/direct matching base. There is also an exact one-sided
alternative already present in the two response bases.

Let the selected diagonal colour be i and the other bright colour be j.
A crossed response has endpoint labels (i,j) or (j,i). Exactly one outer
endpoint retains label i. At that endpoint the target-skeleton port and the
outside port are two literal components of the same source row:

    (i,j): compare two components of p_i;
    (j,i): compare two components of s_i.

Hold q and every opposite-endpoint row fixed. If C_tar,C_out are the two
complete output columns, target coloopness gives

\[
 C_{\rm tar}(t)\ne0,\qquad C_{\rm out}(t)=0.           \tag{1}
\]

Therefore:

1. if C_out=0, delete only the outside component exactly;
2. if C_out=lambda C_tar, equation (1) forces lambda=0, so this is the
   same deletion branch;
3. at a support-minimal source C_out is nonzero, hence the columns are
   nonproportional and some source-valid same-star 2 by 2 minor is nonzero.

Checker:
computations/verify_h3_axis_target_coloop_one_sided_column_route.py.

## Why this is not the bistar Hessian

The operation changes one p_i row, or one s_i row, while the opposite
endpoint and common quadratic are fixed. The response tensor is exactly
linear in that row. The mixed second difference that obstructs a
simultaneous change at both endpoint stars does not occur.

The deletion is anchor-safe. The outside component has endpoint label i,
so it is not a pure anchor of the other bright colour or the unary direct
anchor. Target-coloopness excludes it from a nonzero selected colour-i
pure target matching. Only the outside component is removed; the
target-skeleton component is retained.

This yields a genuine same-star minor, but the present result does not
identify that minor by itself with the downstream four-good or clean
interface.

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

    9a4760098cd0bd2ab06d3dec10554a549c0fc8a8830dac7b2e37d954d49d7c91
