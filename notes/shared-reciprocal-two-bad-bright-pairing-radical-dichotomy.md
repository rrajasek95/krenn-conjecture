# The full bright rows force one radical line on the fixed target pair

## 1. Result

Continue with

\[
 K=\ker\Phi,\quad W=\pi_tK,\quad
 N=\ker(\pi_t|_K),\quad
 \mathcal C=\operatorname{coker}\Phi/\mathcal R_{nt}.
\]

The target-projection theorem gives `dim W<=2`, supported on one fixed
coordinate pair.  Modulo the target-free residual, the kernel-product map
is a symmetric bilinear map

\[
 \beta_P:\operatorname{Sym}^2W\longrightarrow\mathcal C. \tag{1}
\]

The complete nine common-hafnian rows force a sharp trichotomy.

> **Bright-pairing radical dichotomy.**  Put
>
> \[
> \alpha=\pi_t(Q_a),\quad u=\pi_t(Q_t),\quad
> \rho=\pi_t(R_c),\quad v=\pi_t(R_t),
> \]
>
> and let `x` be the image of `[X_t]` in `C`.  Then at least one of the
> following holds:
>
> 1. `x=0`, equivalently `[X_t] in R_nt`;
> 2. `alpha=0` or `rho=0`; or
> 3. `W` is two-dimensional, `alpha` and `rho` span the same line `L`,
>    `L` is the radical of `beta_P` on the displayed rows, and `beta_P`
>    factors through the one-dimensional quotient `W/L`.

The third branch is not contradictory.  There is an exact linearized
common-hafnian quotient normal form satisfying both old bright image labels
and all nine product rows.  Therefore the next proof must use the fact that
the rows arise from one quadratic `q_C`, not only their image/kernel labels.

## 2. The four load-bearing rows

The literal common-hafnian equations are

\[
 P_t(D_{jk}K+Q_jR_kq_C)
    =\delta_{jt}\delta_{kt}X_t.                         \tag{2}
\]

Modulo `im Phi`, the chord term vanishes.  Modulo `R_nt`, a product of
kernel rows depends only on their target projections.  Four entries of (2)
therefore give

\[
 \beta(\alpha,\rho)=0,\qquad
 \beta(\alpha,v)=0,\qquad
 \beta(u,\rho)=0,\qquad
 \beta(u,v)=x.                                         \tag{3}
\]

The checker pins and reconstructs all `2,187` literal rows of (2), so (3)
is not an abstract pairing imposed after forgetting matching provenance.

## 3. The two-dimensional argument

Assume `x!=0` and `alpha,rho!=0`.  If `alpha` were proportional to `u`,
the second and fourth equations in (3) would contradict each other.
Therefore `(alpha,u)` is a basis of `W`.  Similarly `(rho,v)` is a basis.

The first two zero equations now say

\[
                         \beta(\alpha,W)=0,
\]

while the first and third say

\[
                         \beta(W,\rho)=0.
\]

Thus both `alpha` and `rho` lie in the radical.  If they were independent,
the radical would be all of `W`, contradicting `beta(u,v)=x!=0`.  Hence

\[
                  \langle\alpha\rangle
                    =\langle\rho\rangle=L.             \tag{4}
\]

In a basis `(ell,h)` with `L=<ell>`, the surviving form is

\[
 \beta(\ell,W)=0,\qquad \beta(h,h)=g,
 \qquad x=v_1g.                                        \tag{5}
\]

This is a rank-one quotient in the `W/L` direction.

## 4. Compatibility with the old bright images

Let `Cc,Aa` denote affine classes with

\[
                    \Phi(Cc)=X_c,\qquad\Phi(Aa)=X_a.
\]

In the four-dimensional linearized space with basis

```text
ell, h, Cc, Aa
```

take

```text
(Q_a,Q_c,Q_t) = (ell,Cc,h),
(R_a,R_c,R_t) = (Aa,ell,h),
beta(h,h)=x,
all other displayed pairings zero.
```

The resulting `3 x 3` matrix is exactly

\[
 \begin{pmatrix}
 0&0&0\\0&0&0\\0&0&x
 \end{pmatrix}.                                       \tag{6}
\]

Thus the diagonal bright equations `Phi(Q_c)=X_c` and `Phi(R_a)=X_a` do
not by themselves kill the common-radical branch.  This is an exact
quotient counterguard, not a common-provenance quadratic packet and not a
Krenn counterexample.

## 5. Why a universal colour multigrading cannot finish the proof

Assign an additive weight `g_(x,i)` to colour `i` at site `x`.  Homogeneity
of an arbitrary full `3 x 3` block on edge `xy` requires

\[
                    g_{x,i}+g_{y,j}=h_{xy}
                    \quad\text{for all }i,j.            \tag{7}
\]

The exact `90 x 25` system has rank `20` and a five-dimensional kernel.
Every kernel vector is colour-blind at each site:

\[
                  g_{x,0}=g_{x,1}=g_{x,2}.              \tag{8}

Hence every five-site output word has the same weight.  No universal
additive colour grading compatible with arbitrary mixed blocks can
separate `X_t` from `R_nt`.  A successful covector must depend on the
actual `q_C` equations or on a further rank/flag degeneration.

## 6. Remaining source-level branches

The target-free problem is now partitioned without overlap:

1. **residual-pure branch:** `[X_t] in R_nt`;
2. **projection-degenerate branch:** `pi_t(Q_a)=0` or `pi_t(R_c)=0`;
3. **common-radical branch:** the normal form (4)--(5), which must be
   tested for compatibility with one literal quadratic `q_C` and the
   affine bright equations.

The quotient normal form proves that another argument using only the nine
row labels cannot close branch 3.  The next load-bearing calculation is a
common-provenance lift or obstruction for (5), with branches 1 and 2 kept
separate.

## 7. Reproduction

```sh
uv run python computations/verify_shared_reciprocal_two_bad_bright_pairing_radical_dichotomy.py
uv run python -O computations/verify_shared_reciprocal_two_bad_bright_pairing_radical_dichotomy.py
```

Both modes freeze ledger SHA-256

```text
1d13558c8fb3fca947702ca346a022aa4b286baa39a6ea1af3492a6d541dd555
```
