# Fresh adversarial reconstruction of the global edge reduction

**Result: PASS for the stated research theorem and its load-bearing chain.**
Independent reviewer: `/root/audit_global_foundation`, 2026-09-20.
This review used the current repository texts and reconstructed the arguments;
earlier audit labels and missing `/tmp` receipts were not treated as evidence.
No canonical theorem was edited. This is mathematical research review, not
formal certification or a resolution of the remaining diagonal conjecture.

## Exact current texts

All filenames in this table are relative to
`../unaudited-codex-higher-common-power-bridge-2026-09-05/`.

| Text | Lines | SHA256 |
| --- | ---: | --- |
| `UNIFORM-GLOBAL-EDGE-MONOCHROMATICITY-AND-COFACTOR-INVERSE.md` | 229 | `4e140eb5cd74a4e0d9869f76e975ce2f7d46c8d7d1ba9be332a8128424082e89` |
| `UNIFORM-ALL-EVEN-OMISSION-PURE-RESPONSE-VANISHING.md` | 211 | `450f75c2c6280c601e2d012c1ae892d1f18f14f62aae8ec5dd448c3a157b7688` |
| `UNIFORM-THREE-ACTIVE-COLOR-HIGHER-PURE-RESPONSE-VANISHING.md` | 240 | `14811c0332c217e1a5520bd619482f641573b9456783404f48a93dbc3542b190` |
| `UNIFORM-ALL-ODD-DIAGONAL-RESPONSE-FACTORS-AND-NULL-PAIR-TRANSFER.md` | 230 | `3f75dcf21adffb42369985efe37ef947152b4db8f2ad8192bff36031fa3f612c` |
| `UNIFORM-ALL-ODD-TWO-COLOR-MIXED-VANISHING-AND-KERNEL-PENCIL.md` | 186 | `03edf88285ca2a0d1dda8354d266b5d3e329be05149129e8843b2bb2dd9a12e1` |
| `UNIFORM-RETAINED-VACUUM-PAIRING-AND-CUBIC-PALETTE-COFACTORS.md` | 161 | `b2cd2d28691d5d502bc24cc7be1bbe321053b2bedfcb1ada86e7a096c9d29997` |

The complete texts were read. The re-proved dependency scope is the reflection,
common-factor, finite-mean, and covariance machinery used by the global theorem;
unneeded null-extension, kernel-pencil, and cubic-core corollaries are not being
separately recertified. The previous author's challenge was also read as a
cross-check, not as a premise: `ALL-EVEN-OMISSION-COVARIANCE-ADVERSARIAL-RECHECK.md`,
177 lines, SHA256 `d50c57c450af70366a209ba9887345f0beef6ecac51d6d48b04f5ea27f90a279`.

## Independent reconstruction

1. **Wick realization and reflection.** For arbitrary complex edge coefficients,
   define Wick moments by summing pairings of labeled ordinary variables. Set
   covariance between physical variables equal to the actual quadratic, within
   each physical site to zero, and add an auxiliary `g` with covariance row `L`
   and self-covariance zero. With `d` copies of `g`, every copy must pair to a
   different physical variable; the `d!` assignments are exactly the factorial
   in the raw physical product `L^d`. Remaining pairings give the divided power
   of the original core. Positivity and covariance invertibility are unused.

   On two independent identical copies, the orthogonal reflection fixing the
   auxiliary linear combination `s g_1+t g_2` preserves the entire covariance.
   Its determinant is minus one, so it reverses each local two-column
   determinant, including when the chosen pair of colors varies with the site.
   At odd physical order, the product changes sign. The expectation is zero
   over `C(s,t)`, and coefficient extraction is legitimate because the original
   expectation is polynomial in `s,t`. Extracting `s^p t` gives the displayed
   contraction of `H_p(L)` with the full original response `Phi(L)`.

2. **Binary mixed words and common pure factors.** For a mixed word avoiding
   an active color `h`, use its own color and `h` as the local determinant pair.
   Among complementary words, only the pure `h` word is diagonal. Thus the
   reflection gives `f_h(L)[w]H_p(L)=0` as a polynomial on the actual row space
   `D`. Cancellation is in `C[D]`, so it includes rows with `f_h(L)=0`.
   Constant color pairs instead give `f_b t_a=f_a t_b`. Two independent linear
   target functions are relatively prime and force `t_h=f_h q_r` with one
   homogeneous `q_r`. This reasoning works on the given subspace `D`; it does
   not require surjectivity onto the entire diagonal-response space.

3. **Finite odd means force the common factors to vanish.** The shifted Wick
   moment on odd order is exactly
   `Psi(L)=sum L^(2r+1) R^[m-r]/(2r+1)!`. Its binary projection is
   `G(L)(f_a(L)P_a+f_b(L)P_b)` after choosing independent `f_a,f_b`; the third
   active color is used to eliminate the binary mixed words. Two identical
   ordinary replicas and a determinant-one rotation preserve their covariance
   and each local determinant. Therefore the binary contraction of two means
   is invariant under rotating `(L,M)`. Cancelling the nonzero polynomial
   `f_a(L)f_b(M)-f_b(L)f_a(M)` gives the multiplicative identity for `G` before
   specializing `M=0`. A 45-degree rotation gives
   `G(L/sqrt(2))^2=G(L)`. Here `G` is finite, even, and has constant term one.
   Positive degree would double on the left; hence `G=1`, so every higher
   odd response vanishes on each whole binary palette. The finite-polynomial
   condition and cancellation before specialization are both essential.

4. **The all-even omission bridge.** Write the literal omission as
   `R=Q+sum h_q V_h` and `L=U+sum d_h(L)h_q`, and put
   `E(U)=sum U^(2r) Q^[m-r]/(2r)!`, `F=E(0)`. Occupying the omitted site by
   either a row mean or a star edge gives exactly
   `[h_q]Psi(L)=d_h(L)E(U)+partial_(V_h)E(U)`. After binary projection this is
   `f_h(L)h^S`, by step 3. This retains the original omitted-site component.

   The same ordinary-replica argument at even order gives
   `B(E(U),E(U))=B(E(sqrt(2)U),F)`. Rotate `(U,U+tV)` and differentiate at zero.
   The derivative of `E` at zero is zero, so the exact other identity is
   `B(E(U),partial_V E(U))=B(F,partial_V E(sqrt(2)U))/sqrt(2)`.
   It holds for arbitrary `V`, including the original star row `V_h` outside
   `U(D)`. Substitution of the omitted-site equations at `L` and `sqrt(2)L`
   leaves `f_h(L) B(E(U)-F,h^S)=0`: both `d_h` and `f_h` scale, while `V_h`
   stays fixed. Because `|S|` is even, this pairing extracts the pure other
   color with positive sign. Polynomial cancellation, homogeneous-degree
   separation, and polarization give every stated same-family even identity.
   No replica rotation is performed in a site-square-zero quotient.

5. **Cofactor multiplication and inversion.** At a full source, the three
   original rows at each deleted root satisfy the required full rank-three
   diagonal response. Applying step 4 after any further omission gives EV1.
   For fixed receiving color `h`, define `C_h[r,q]` by deleting distinct
   `r,q`, with its diagonal set to zero, and define `B_ih[p,r]=A_pr(i,h)`.
   A diagonal entry of `B_ih C_h` is the full word with one `i` at `p` and
   `h` elsewhere, hence `delta_(i,h) tau_h`. At an off-diagonal entry `p,q`,
   terms `r=p,q` vanish. Vertex `p` remains in each other cofactor, so expand
   its hafnian at `p`. The resulting ordered `r,s` sum is exactly
   `[h^S] X_i^(p,q) X_h^(p,q) Q^[m-1]`, zero by EV1. There is no half factor,
   including `i=h`: both sides count both orders of the two occupied sites.

   Consequently `B_ih C_h=delta_(i,h) tau_h I`. Taking `i=h` makes `C_h`
   invertible over ordinary complex scalar matrices, then every `B_ih=0`
   for `i!=h`. No invertibility of a physical-algebra element was used.
   This proves every original off-color cell is zero, and
   `C_h=tau_h M_h^(-1)`. At `n=4`, the residual hafnian is the empty value
   one and the calculation is valid. At `n=2`, the even-omission premise
   is absent and the theorem does not claim applicability.

## Fresh exact convention checks

The sibling [check script](check_global_foundation.py), SHA256
`3ebf99ecfb526a95db8ae5c04a7a41adb1663831828009d2588595bb6c7c9f85`,
implements direct first-site mean-or-pair recursion with exact integer and
`Fraction` arithmetic. It assumes neither reflection nor covariance.
Run `python3 computations/unaudited-codex-diagonal-continuation-2026-09-20/check_global_foundation.py`
from the repository root. The recorded [results](global_foundation_exact_checks.json)
show:

- 58 reflection contractions at odd orders 3, 5, 7, using both constant and
  site-dependent color pairs and every admissible odd degree in both factors;
- six nonzero exact rational-rotation checks at even orders 2, 4, 6, plus
  54 homogeneous equal-mean and differentiated-covariance coefficient checks;
- 882 off-diagonal and 162 diagonal matrix-cofactor comparisons on arbitrary
  dense sources at orders 4, 6, 8; the raw two-row coefficient was computed
  by polarization of the independent mean-or-pair recurrence;
- the complete 81-entry unequal-weight K4 tensor and all 324 EV1 coefficients;
- a binary-only three-site negative control whose nonzero higher pure
  coefficients are `(-420,-630,0)`, demonstrating why the third-active-color
  premise cannot be silently dropped.

These finite checks challenge conventions; the reconstructed polynomial
argument is what supports the all-order result. No counterexample, sign error,
missing factorial, tensor-domain error, or omitted hypothesis was found.

## Consequence and limit

It is valid at research-proof level to use the global diagonal reduction for
every full ordinary complex ternary source of even order at least four.
The remaining equations are products of **hafnian sums** on color classes.
This review supplies no permission to replace cancellation of such a sum by
termwise support exclusion, and proves no all-order diagonal nonexistence.
