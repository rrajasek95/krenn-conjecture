# The arbitrary tilted kernel reduces to one target-coordinate pair plus a residual

## 1. Result

Let

\[
 K=\ker\Phi,\qquad
 \pi_t:K\longrightarrow \mathbb C^5
\]

be target-coordinate projection: the `x`-th coordinate of `pi_t(U)` is
the coefficient of `e_t` in the local row `U_x`.  The finite Rees unit in
[`shared-reciprocal-two-bad-mixed-two-hole-rees-unit.md`](shared-reciprocal-two-bad-mixed-two-hole-rees-unit.md)
excludes a kernel row whose target projection has three nonzero entries.
Linearity turns that pointwise statement into a fixed-pair theorem.

> **Target-projection pair theorem.**  There is one subset
> `S subset {0,...,4}`, `|S|<=2`, such that
>
> \[
>                  \pi_t(K)\subseteq\mathbb C^S.        \tag{1}
> \]
>
> In particular `dim pi_t(K)<=2`.

This does not say that every kernel row is supported on two sites.  It says
that all of their **target components** use the same two sites.  Arbitrary
non-target components may occur at all five sites.

Those extra components cannot be discarded in the common-cofactor
cokernel.  They admit, however, one canonical isolation.  Put

\[
 N=\ker(\pi_t|_K)
\]

and let

\[
 \mathcal R_{nt}=
 \operatorname{im}\bigl(A_1\otimes(N\cdot K)
       \xrightarrow{\ \mathcal T\ }\operatorname{coker}\Phi\bigr), \tag{2}
\]

where `N*K` denotes symmetric products having at least one target-free
kernel factor.  Then, modulo `R_nt`, the kernel-product map factors
canonically through

\[
       A_1\otimes\operatorname{Sym}^2(\pi_tK),          \tag{3}
\]

whose symmetric-square factor has dimension at most three.  Thus the full
arbitrary-centre problem is exactly a fixed two-hole target-projection
packet plus the named target-free residual (2).

## 2. Why the coordinate pair is fixed

Let `W=pi_t(K)`.  Suppose the union of the coordinate supports of vectors
in `W` contains at least three sites.  For every coordinate `i` in this
union, restriction of the `i`-th coordinate functional gives a nonzero
linear form `ell_i in W*`.  Hence

\[
                         \prod_i\ell_i                 \tag{4}
\]

is a nonzero polynomial on `W`.  Over the infinite field `C`, it is
nonzero at some point of `W`.  That point has every coordinate in the
union nonzero, hence support at least three, contradicting the Rees unit.
Therefore the union itself has size at most two, proving (1).

The infinite-field hypothesis is load-bearing.  Over `F_2`, the span of
`110` and `101` is

```text
{000,110,101,011};
```

every vector has support at most two although the union of supports has
size three.  The checker freezes this mutation guard so the complex-field
argument is not silently promoted to all fields.

## 3. The canonical target-free residual

The target projection gives an exact sequence

\[
 0\longrightarrow N\longrightarrow K
  \longrightarrow W\longrightarrow0.                  \tag{5}
\]

Choose any linear section `s:W->K`.  If `s'` is another section, then
`s'(w)-s(w) in N`.  Bilinearity gives

\[
 \mathcal T(P,s'(w),s'(w'))-\mathcal T(P,s(w),s(w'))
       \in\mathcal R_{nt}.                              \tag{6}
\]

Consequently

\[
 (P,w,w')\longmapsto
 [\mathcal T(P,s(w),s(w'))]\pmod{\mathcal R_{nt}}
                                                               \tag{7}
\]

is independent of the section and factors through `Sym^2(W)`.  This is a
formal bilinear identity, not a choice of support normal form.  The checker
audits all three products `w0^2,w0*w1,w1^2` under a generic section change.

For the two-bad quotient equation

\[
 [X_t]=[\mathcal T(P,U,V)]\ne0,                         \tag{8}
\]

(7) yields the canonical reduced equation

\[
 [X_t]=\overline{\mathcal T}
       (P,\pi_tU,\pi_tV)
 \quad\text{in }\operatorname{coker}\Phi/\mathcal R_{nt}. \tag{9}
\]

Both projected rows in (9) live on the same fixed coordinate pair `S`.
This is the precise sense in which the remaining target part is a Hubble
fixed-two-hole packet.  The full rows need not be two-centre rows; their
non-target tails have been placed in the invariant residual.

## 4. Why target-free factors cannot simply be dropped

If `N in ker(pi_t)`, then every literal term of
`T(P,N,V)` has zero raw `X_t` coefficient: the inserted `N` factor has no
target entry at its chosen site.  This observation alone is insufficient
modulo `im(Phi)`.  A tensor with zero raw `X_t` coefficient may still
represent the pure target class after an image correction.

The pinned rational Pythagorean common-power packet makes the distinction
exact.  Reconstructing its full five-site map gives

```text
rank Phi                         11
dim ker Phi                       4
dim pi_t(ker Phi)                 1
dim N                             3
rank of target-free products      6
rank(im Phi + R_nt)              16
```

Thus `R_nt` contributes five genuine cokernel dimensions: it is not zero
and is not absorbed by `im(Phi)`.  In this exact guard,

\[
 (\operatorname{im}\Phi+\mathcal R_{nt})
 \cap\langle X_a,X_c,X_t\rangle
       =\langle X_a,X_c\rangle,                         \tag{10}
\]

so it still does not produce `X_t`.  Equation (10) is a bounded guard, not
the missing general theorem.

## 5. Remaining proof dependency

The arbitrary-centre `T=0` boundary is now split into two exact pieces:

1. the fixed-pair equation (9), on a target-projection space of dimension
   at most two; and
2. the **target-free residual pure-grade problem**

   \[
       [X_t]\stackrel{?}{\in}\mathcal R_{nt}
       \quad\text{or, more generally,}\quad
       [X_t]\stackrel{?}{\in}
       \mathcal R_{nt}+\operatorname{im}\overline{\mathcal T}. \tag{11}
   \]

Existing Hubble private-row and two-kernel repairs attack minimal
realizations of the first piece.  They do not prove that `R_nt` vanishes.
A theorem completing this lane must either exclude the pure target grade
from (2), or couple (2) to (9) by additional common-hafnian rows.

## 6. Reproduction

```sh
uv run python computations/verify_shared_reciprocal_two_bad_target_projection_pair_reduction.py
uv run python -O computations/verify_shared_reciprocal_two_bad_target_projection_pair_reduction.py
```

The checker pins both source dependencies, audits the fixed-pair and
section-independence arguments, reconstructs the rational target-free
residual, and freezes ledger SHA-256

```text
ac60460e15ee82ff95d0abba8ff1cd9f0efe114aa30e40a6e4a582edc929625e
```
