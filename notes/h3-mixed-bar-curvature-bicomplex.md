# The mixed bar–curvature square reaches the lowered endpoint but retains residue

## Outcome

Combine the normalized local-\(GL_3\) interval

\[
 dE=L-D,\qquad \epsilon(L)=\epsilon(D)=1,\quad\epsilon(E)=0              \tag{1}
\]

with the literal selected physical normal row

\[
 Uf+tH-Fg-yN-D_c v=\kappa z,\qquad \kappa=AU-BF.                         \tag{2}
\]

The resulting tensor square is a genuine unaugmented bicomplex. After every
Leibniz commutator is retained, it has a canonical Massey chain whose
boundary is exactly the desired lowered endpoint:

\[
 \boxed{\mathcal M=D(n)+\mathsf H(\kappa z),\qquad
        d\mathcal M=L(\kappa z).}                                         \tag{3}
\]

Here \(dn=\kappa z\), and \(\mathsf H\) is the normalized multiplicative
bar homotopy from \(D\) to \(L\). Thus the unwanted \(D\) endpoint really
does cancel. Extending the word change across all seven nonzero-labelled
sites also makes the physical target zero.

But (3) is not the missing invisible attaching chain. Under the only
committed split-cap landing, \(L(\kappa z)\) has

\[
 (q\text{-augmentation},\operatorname{tgt},
          \operatorname{ores})=(\kappa,0,\kappa),                         \tag{4}
\]

while every bar-edge correction has normalized augmentation zero. The
ordinary-residue component \(\kappa\) therefore survives. The mixed
bicomplex solves the word and target faces, but not the augmented face.

## Full tensor-square boundary

Let \(n\) denote the physical normal-row chain in (2). The degree-two mixed
cell has total boundary

\[
 d(E(n))=L(n)-D(n)-\mathsf H(\kappa z).                                  \tag{5}
\]

Applying \(d\) again gives

\[
 L(\kappa z)-D(\kappa z)
 -\bigl(L(\kappa z)-D(\kappa z)\bigr)=0.                                  \tag{6}
\]

Equation (3) is obtained by moving the last two faces of (5) together:

\[
\begin{aligned}
 d\bigl(D(n)+\mathsf H(\kappa z)\bigr)
 &=D(\kappa z)+L(\kappa z)-D(\kappa z)\\
 &=L(\kappa z).
\end{aligned}                                                             \tag{7}
\]

This is the positive chain identity supplied by the product. It is not a
declaration of a new generator.

## Every Leibniz commutator

For ordered products the normalized multiplicative homotopy is

\[
 \mathsf H(ab)=\mathsf H(a)L(b)+D(a)\mathsf H(b).                         \tag{8}
\]

The determinant face therefore expands as

\[
\begin{aligned}
\mathsf H(\kappa)
={}&\mathsf H(A)L(U)+D(A)\mathsf H(U)\\
 &-\mathsf H(B)L(F)-D(B)\mathsf H(F),                                    \tag{9}\\
\mathsf H(\kappa z)
={}&\mathsf H(\kappa)L(z)+D(\kappa)\mathsf H(z).                          \tag{10}
\end{aligned}
\]

The checker also expands (8) independently on all five literal correction
terms

\[
 Uf,\qquad tH,\qquad -Fg,\qquad -yN,\qquad -D_c v,                        \tag{11}
\]

using

\[
\begin{aligned}
 f&=Az+xy,&g&=Bz+xt,\\
 H&=Av+E_cy+Fx,&N&=Bv+E_ct+Ux,\\
 D_c&=At-By.
\end{aligned}                                                             \tag{12}
\]

Their homotopies sum exactly to (10); no correction term is discarded.

## Target and residue faces

For the endpoint-only change, the source labels are \((m_v,2,2)\). The
all-\(L\) target remains nonzero on the two faces with \(m_v=2\). The full
seven-site change has input word

\[
                         1211222,
\]

which contains both nonzero colours, so its all-\(L\) action on the ternary
GHZ target is zero. Every corner containing \(D\) is target-zero as well.
Thus the complete version of (3) clears the target face.

Normalized augmentation is different. It sends both endpoints to the same
coefficient and sends every \(\mathsf H\)-term to zero:

\[
 \epsilon L(\kappa z)=\epsilon D(\kappa z)=\kappa z,
 \qquad \epsilon\mathsf H(\kappa z)=0.                                  \tag{13}
\]

With the selected polar normalized by \(z\mapsto1\), (13) is precisely the
old-cap equality of \(q\)-augmentation and ordinary residue in (4). Keeping
the difference \(L-D\) kills residue but also kills the desired endpoint;
forming the Massey chain cancels \(D\) and necessarily restores residue
\(\kappa\).

Therefore the first uncancelled typed face is

\[
                         \boxed{\operatorname{ores}=\kappa.}              \tag{14}
\]

A successful construction still needs a reduced relative augmentation or
an independent physical residue correction. The bar–curvature product does
not force either one.

## Verification

Run

    python3 computations/verify_h3_mixed_bar_curvature_bicomplex.py
    python3 -O computations/verify_h3_mixed_bar_curvature_bicomplex.py

The checker pins both input artifacts, verifies (2) as a sparse polynomial
identity, expands (8) on every term in (11), checks (5)–(10), evaluates
three active rational curvature packets including the direct-free case, and
audits the endpoint-only and complete-word target ledgers.  Its frozen ledger
digest is

    63f0ed1a39231f581a498b8fb4d1fda41ef5eec791f1b0fb4e3bb46138def6f2
