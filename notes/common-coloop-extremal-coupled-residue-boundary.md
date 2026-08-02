# Extremality removes zero top but leaves a dark common-coloop boundary

Research evidence only. Krenn's conjecture remains open, the dashed
clean-point implication is not proved, and the certified spine is
untouched.

## Outcome

Return the
[cross-row scalar coupling](common-coloop-cross-row-scalar-coupling-elimination.md)
to the actual source selected lexicographically by

\[
 \text{maximum mutual anchors, then minimum aggregate support}. \tag{1}
\]

On the curvature-selected chart, the physical pair is good, so both
endpoint-star maps are injective, and its direct block
\(a=(a_{ij})\) is nonzero. Under these inherited hypotheses:

1. **Zero top is impossible.** If \(Q=q^{[h]}=0\), the whole nonzero
   direct block contributes zero to every one of the nine physical rows.
   Deleting it preserves every old mutual anchor and strictly lowers
   support, contradicting (1).
2. **Each one-sided rank-one branch is scalar-compatible.** Its surviving
   coefficient \(a_{rt}\ne0\) or \(a_{ts}\ne0\) makes the tangent scalar
   map surjective, so every \(z\), in particular some \(z\ne0\), is
   attainable.
3. **The dark nonzero-top branch is conditionally scalar-compatible.**
   When both cross coefficients vanish, its scalar map is
   \[
                 \ell(L)=a_{rr}\eta_r+a_{ss}\xi_s.          \tag{2}
   \]
   If either displayed coefficient is nonzero, every scalar is
   attainable. If both vanish, the sole value is \(\sigma_0\), and the
   branch is relevant exactly when \(\sigma_0\ne0\).

The audit also corrects the preceding four-branch list. Besides local
rank at least two, there is a nonzero local-rank-one boundary with

\[
        a_{rt}=a_{ts}=0,\qquad H_t=G_t=0.                   \tag{3}
\]

It is not one-sided and is not covered by
\(\operatorname{rank}_xQ\ge2\). It has the same scalar and curvature
ledger as the dark branch, so the corrected post-extremal classification
has three families:

\[
 \boxed{\quad
 \begin{array}{c}
 Q\ne0,\ a_{rt}=a_{ts}=0,\ H_t=G_t=0
       \quad\text{(dark top of any local rank)},\\
 Q=u q_t,\ a_{rt}\ne0,\ H_t=-a_{rt}q_t,
       a_{ts}=0,\ G_t=0,\\
 Q=v q_t,\ a_{ts}\ne0,\ G_t=-a_{ts}q_t,
       a_{rt}=0,\ H_t=0.
 \end{array}\quad}                                          \tag{4}
\]

The remaining four literal rows do not close these families. They
determine an exact curvature rectangle. In particular the missing
diagonal becomes

\[
 \begin{array}{ll}
 \Gamma_{tt}=X_t-a_{tt}Q,
   &\text{dark top},\\[1mm]
 \Gamma_{tt}=X_t-(a_{tt}u-a_{rt}p_{t,x})q_t,
   &\text{left one-sided},\\[1mm]
 \Gamma_{tt}=X_t-(a_{tt}v-a_{ts}s_{t,x})q_t,
   &\text{right one-sided}.
 \end{array}                                                 \tag{5}
\]

Thus the source-provenance question is smaller but still open: the
literal curvature product
\(\Gamma_{tt}=\rho\bar p_t\bar s_tq_0^{[h-2]}\), together with the other
three entries of its endpoint-ordered rectangle, must be compared with
the same arm's \(D_{\bar K}(z)\)-image. Maximum-anchor/minimum-support
extremality alone supplies no further deletion once \(Q\ne0\).

## 1. Extremal deletion closes \(Q=0\)

Let the selected good physical pair be \(p,q\). Its complete fixed-label
rows are

\[
 a_{ij}Q+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\le i,j\le2.                                      \tag{6}
\]

Curvature selection provides a nonzero direct coefficient, so
\(a\ne0\). Suppose \(Q=0\). Then (6) is unchanged if the entire aggregate
block \(a=A_{pq}\) is replaced by zero. This gives another exact source.

It remains to check the lexicographic objective. Every nonzero direct
cell \(a_{ij}\) uses the coordinate endpoints \((p,i)\) and \((q,j)\).
Goodness makes both residual endpoint maps injective. Hence

\[
                         p_i\ne0,\qquad s_j\ne0,             \tag{7}
\]

so each endpoint of the direct cell is incident with at least one other
supported scalar cell. No cell in the deleted direct block is therefore
a mutual anchor.

Deleting cells cannot destroy a mutual anchor outside the deleted block:
its cell remains and its two endpoint degrees can only decrease. It may
create new anchors. Consequently the deletion either

* increases the number of mutual anchors, contradicting the first stage
  of (1); or
* preserves that number and strictly lowers support, contradicting the
  second stage.

Thus

\[
                \boxed{\text{the selected good chart has }Q\ne0.} \tag{8}
\]

The argument uses the global extremal source exactly once. It does not
assert that every arbitrary full-nine packet has nonzero top.

## 2. Exact attainable-scalar classification

Use the disjoint singleton normalization

\[
                      c=e_r,\qquad d=e_s,\qquad r\ne s,      \tag{9}
\]

and write

\[
                 L=e_r\eta^{\mathsf T}+\xi e_s^{\mathsf T}. \tag{10}
\]

The overlap entry \((r,s)\) has response
\(p_rs_sq^{[h-1]}=0\), since both endpoint factors occupy \(x\). Its
full-nine row is

\[
                              a_{rs}Q=0.                     \tag{11}
\]

Equation (8) gives \(a_{rs}=0\). Therefore the scalar functional on the
five-dimensional tangent space is

\[
 \boxed{\quad
 \ell(L)=a_{rr}\eta_r+a_{rt}\eta_t
              +a_{ss}\xi_s+a_{ts}\xi_t.
 \quad}                                                       \tag{12}
\]

If (12) is nonzero, its image over \(\mathbb C\) is all of
\(\mathbb C\). If it is zero, the affine fibre has the single scalar
\(\sigma_0\). Combining (12) with the cross-row theorem gives:

\[
\begin{array}{c|c|c}
\text{branch}&\ell&\text{nonzero scalar}\\ \hline
\text{left one-sided}&a_{rt}\eta_t+\cdots&\text{always attainable}\\
\text{right one-sided}&a_{ts}\xi_t+\cdots&\text{always attainable}\\
\text{dark top}&a_{rr}\eta_r+a_{ss}\xi_s&
 (a_{rr},a_{ss})\ne(0,0)\text{ or }\sigma_0\ne0.
\end{array}                                                  \tag{13}
\]

The last condition is exactly the pre-clean activity condition on the
affine coset. Hence every dark branch which actually reaches the active
completion problem already satisfies it; a dark fibre with
\(\ell=0=\sigma_0\) is discarded as scalar-inactive before the polar
cokernel is tested.

The maximum-anchor/minimum-support choice does not force
\((a_{rr},a_{ss})\ne(0,0)\). Exact rational row models realize both a
surjective dark scalar and a fixed nonzero dark scalar. It likewise does
not remove the one-sided branches: their nonzero cross coefficient is
part of a nontrivial cancellation against \(Q\), so the zero-top deletion
argument no longer applies.

## 3. The hidden rank-one dark boundary

The simultaneous cross rows say

\[
              a_{rt}Q+uH_t=0,\qquad
              a_{ts}Q+vG_t=0.                              \tag{14}
\]

When \(Q\ne0\) has local rank one, the previous note split off the cases
where one coefficient is nonzero. But (14) also allows

\[
                 a_{rt}=a_{ts}=0,\qquad H_t=G_t=0.          \tag{15}
\]

Both diagonal rows can coexist with (15). For example, in an abstract
exact local-tensor ledger take

\[
 Q=e_2^{(x)}\otimes y_2,\qquad
 u=e_0^{(x)},\quad H_r=y_0,\qquad
 v=e_1^{(x)},\quad G_s=y_1,                                \tag{16}
\]

and \(a_{rr}=a_{ss}=0\). The \(r,s\) diagonal rows are then exactly
\(X_r,X_s\), both cross rows vanish, and a fixed
\(\sigma_0\ne0\) makes the scalar active. This is a sharp row-elimination
guard, not a consecutive-power Krenn source.

Accordingly, local rank alone should no longer index the dark residual.
The source-faithful division is whether one cross coefficient survives:
dark top versus left or right one-sided top, as in (4).

## 4. The literal remaining curvature rectangle

The rows not used in the four-row cross elimination are the rectangle

\[
                              (s,r),(s,t),(t,r),(t,t).       \tag{17}
\]

Write \(p_{i,x},s_{j,x}\) for local endpoint components. Their exact
Taylor equations are

\[
 \begin{aligned}
 \Gamma_{sr}
   &=-a_{sr}Q-p_{s,x}H_r-s_{r,x}G_s,\\
 \Gamma_{st}
   &=-a_{st}Q-p_{s,x}H_t-s_{t,x}G_s,\\
 \Gamma_{tr}
   &=-a_{tr}Q-p_{t,x}H_r-s_{r,x}G_t,\\
 \Gamma_{tt}
   &=X_t-a_{tt}Q-p_{t,x}H_t-s_{t,x}G_t,
 \end{aligned}                                               \tag{18}
\]

where

\[
          \Gamma_{ij}=\rho\bar p_i\bar s_jq_0^{[h-2]}.      \tag{19}
\]

Substituting the three cases in (4) gives (5) and the corresponding first
three entries of (18). This is the smallest exact source-provenant
remaining-row ledger. The \(\Gamma_{ij}\) are not free tensors: all four
come from the same \(\rho,\bar p,\bar s,q_0^{[h-2]}\). Rational Taylor
guards can assign them to satisfy (18), but that does not provide the
common factorization (19). The latter is exactly the additional datum
which can still close a branch.

Modulo the multiplication image
\(V_x\otimes\operatorname{im}(\mathcal R_1A)\), all \(Q,H,G\) terms
vanish and (18) reduces to the already audited sole corner

\[
                 \overline\Gamma_{tt}
                    =e_t^{(x)}\otimes\overline Y_t.          \tag{20}
\]

Thus the remaining literal rows sharpen the representative of the corner
but do not annihilate its quotient class.

## 5. Polar residue after extremal routing

Put

\[
              \alpha=u\bar s_t,\qquad \beta=\bar p_tv.      \tag{21}
\]

For an augmented cokernel pair with \(\mu=-\nu\), the remaining equations
are:

\[
\begin{array}{c|c}
\text{dark top}&
 \alpha A=\beta A=0,\quad
 \Lambda(\alpha D)=\Lambda(\beta D)=0,\\[1mm]
\text{left one-sided}&
 \widetilde\alpha A=-Q,\quad
 \Lambda(\widetilde\alpha D)=\mu,\quad
 \beta A=0,\quad\Lambda(\beta D)=0,\\[1mm]
\text{right one-sided}&\text{endpoint transpose}.
\end{array}                                                  \tag{22}
\]

In every case the detector remains

\[
        \Lambda(C_{\bar K}(z))+\mu(z-\sigma_0)\ne0.          \tag{23}
\]

The checker supplies exact detecting linear ledgers compatible with all
equations displayed above. They prove sharpness only for the
source-row/Taylor elimination. They do not assert that arbitrary assigned
\(\Gamma\) entries have the consecutive-power factorization (19).

## 6. Exact checker and revised frontier

The dependency-free checker
[verify_common_coloop_extremal_coupled_residue_boundary.py](../computations/verify_common_coloop_extremal_coupled_residue_boundary.py)
verifies:

* all \(2^9-1=511\) nonempty supports of a good \(3\times3\) direct
  block: zero-top deletion never destroys an old anchor and always lowers
  support;
* exact local-tensor diagonal/cross rows for surjective and fixed-scalar
  local-rank-two models, the hidden rank-one dark model, and both
  one-sided models;
* the attainable-scalar criterion (12)--(13);
* every remaining curvature row in (18), including all three corrected
  forms in (5); and
* sharp augmented polar detectors on every nonzero-top residual.

Its frozen SHA-256 ledgers are

    63926fa96da270e677f503026753a14bfa2cf3c2ffc343589a012bafb34fecf7
    07cde234899a14f5b9d45d5398ce48720cb44115230a5df4e27527ed4c69d842
    d5f7ea021d04444ae3b52d7f7e7bd1a2fd1f037056730936ebe973bf671fe38f
    f9bba0e728d73c3a7fd2e9cb6f5188526d23b674e48c0894c908e6ee8ad42030

They are respectively the extremal deletion, scalar compatibility,
remaining curvature-row, and polar sharpness ledgers. The checker is live
under normal Python, -O, and -I -S.

The proved advance is one exact closure and one correction: zero top is
incompatible with the selected extremal good chart, while the dark
residual must include its local-rank-one boundary. The remaining frontier
is the common factorization (19) coupled to (22)--(23), not another free
local-rank census.
