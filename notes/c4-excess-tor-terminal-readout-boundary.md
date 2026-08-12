# Site gauge does not make the flat $C_4$ excess terminal-invisible

## Result

At the normalized ternary vertex-gauge point, the two balanced Segre
tangents are

$$
 T_A=\{f_{01}+g_{45}\},\qquad
 T_B=\{f_{05}+g_{14}\}.                               \tag{1}
$$

Their intersection is the nine-dimensional site-gauge tangent
$T_Z=\{u_0+u_1+u_4+u_5\}$. Their sum has dimension 25, so the excess
conormal

$$
 E=T_A^\perp\cap T_B^\perp=(T_A+T_B)^\perp            \tag{2}
$$

has dimension $81-25=56$. Passing from each balanced tangent to its quotient
by $T_Z$ removes no part of (2). Thus vertex-gauge normalization does **not**
make the geometric excess Tor disappear.

There is an exact readout criterion. A linear terminal readout $\epsilon$
is automatically invisible on the geometric excess precisely when its
representative belongs to $T_A+T_B$:

$$
                 \epsilon(E)=0
      \quad\Longleftrightarrow\quad
                 \epsilon\in T_A+T_B.                 \tag{3}
$$

The full scalar/all-word augmentation has this property. A marked-coordinate
projection does not: an explicit quadratic excess class is detected with
coefficient one. Consequently neither site-gauge quotient nor E2/E3
coherence proves zero indeterminacy for a marked terminal sector.

This is a theorem about the geometric Segre Tor. It does not identify that
Tor with the physical hafnian-source $H_1$, the chart-26 primitive colon
class, or the rootless pentagon classes $h_v$.

## 1. The complete excess decomposition

At one site write the function space as

$$
                         k^3=\mathbf1\oplus W,
 \qquad W=\{(z_0,z_1,z_2):z_0+z_1+z_2=0\}.             \tag{4}
$$

For $S\subseteq\{0,1,4,5\}$, let $V_S$ be the tensor sector with a $W$
factor exactly at the sites in $S$ and a constant factor elsewhere. A
sector is orthogonal to $T_A$ precisely when $S$ is contained in neither
$\{0,1\}$ nor $\{4,5\}$. It is orthogonal to $T_B$ precisely when $S$ is
contained in neither $\{0,5\}$ nor $\{1,4\}$.

Therefore

$$
\begin{aligned}
 E={}&(W_0\otimes W_4)\oplus(W_1\otimes W_5)\\
 &\oplus\bigoplus_{|S|=3}V_S
 \oplus(W_0\otimes W_1\otimes W_4\otimes W_5).        \tag{5}
\end{aligned}
$$

The respective dimensions are

$$
                 8+32+16=56.                           \tag{6}
$$

The first two terms in (5) are the two orientations of the third physical
matching $(04)(15)$. In particular, the excess begins in quadratic degree;
it is already disjoint from the constant and linear site-gauge sectors.

## 2. A marked readout detects excess

Let $r=(1,-1,0)\in W$ and define

$$
             \theta=r_0\otimes\mathbf1_1
                         \otimes r_4\otimes\mathbf1_5. \tag{7}
$$

Every $(01)$, $(45)$, $(05)$, and $(14)$ pair marginal of $\theta$ is zero,
so $\theta\in E$. Every one-site marginal is zero as well, so it remains
after quotienting site gauge. But

$$
        \sum_{i,j,k,\ell}\theta_{ijk\ell}=0,
        \qquad \theta_{0000}=1.                        \tag{8}
$$

Thus the full scalar augmentation kills this class, while the marked word
`0000` detects it. By permuting colours, the same statement holds for every
single word. Equation (8) is the smallest exact counterguard to

```text
vertex gauge + flat C4 coherence => every terminal readout kills Tor1.
```

The correct implication requires the actual physical readout to factor as
a sum of the two balanced tangent forms in (1), or an independent source
proof that it annihilates the image of physical $H_1$.

## 3. Relation to source saturation

The geometric excess $E$ and the source-relative correction homology are
different objects. A polarized source resolution and its physical diagonal
would have to identify the relevant subquotient of
$H_1(C_{\rm phys,flat})$ with a subquotient of $E$ before (3) could be used
on source classes. No such comparison is supplied merely by the ordinary
Segre intersection. Conversely, physical source homology
may contain primitive colon classes which are absent from $E$. The exact
chart-26 primitive-colon audit is such a surviving source warning; its
terminal pairing has not been computed by the geometric model.

Hence the flat $C_4$ theorem now has a sharp stopping rule:

* the full scalar augmentation is automatically invisible on geometric
  excess;
* a marked or partial readout is not automatically invisible;
* the physical theorem must prove
  $\varepsilon(H_1(C_{\rm phys,flat}))=0$ directly, or exhibit a terminal
  class on which it is nonzero.

## 4. Relation to the non-Euler rootless jet

The non-Euler rootless construction produces a genuine physical corrected
jet whose marked sector is $h_v=\sum_Nq_{v,N}$, while the complete mixed row
vanishes after adding the other 87 terms. Selecting $h_v$ is therefore a
marked-sector projection, not the full scalar augmentation in (8).

The class $\theta$ does **not** prove that $h_v$ detects a physical C4 Tor
class: the four-word Segre module and the five-face pentagon module have
different provenance and fine degrees. It proves only that vertex gauge
cannot make this projection zero-indeterminate automatically. The rootless
branch still needs the source-labelled terminal map which kills the
completion terms and satisfies

$$
           \varepsilon(H_1(\text{correction kernel}))=0. \tag{9}
$$

That is exactly the remaining hypothesis required to turn the non-Euler
marked jet into the physical pentagon map $P$.

## Verification

Run

```text
python3 computations/verify_c4_excess_tor_terminal_readout_boundary.py
```

The checker verifies (5)--(8), the tangent and gauge ranks, the exact
criterion (3), and pins the geometric/source dependencies. It is a sharp
geometric counterguard, not a physical source counterexample.
Its frozen ledger digest is
`7c3e8e99d74e41a344564b0dc064c6391a9bb5e30e55e2beb86b377aebe9f0c1`.
