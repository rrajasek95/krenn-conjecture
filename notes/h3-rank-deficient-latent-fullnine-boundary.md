# The rank-deficient latent branch reduces to a literal dark-kernel boundary

## Result

Work in the six residual-site algebra and retain the complete physical pair
rows

\[
 a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
 \qquad 0\le i,j\le2.                                  \tag{1}
\]

Let

\[
 P,S:\mathbb C^3\longrightarrow({\cal R}_W)_1          \tag{2}
\]

be the two injective endpoint-star maps, put

\[
 k=\dim(\operatorname {im}P\cap\operatorname {im}S)>0,
 \qquad \dim(P+S)=6-k,                                  \tag{3}
\]

and let the canonical scalar-zero matrix `K_*` be invertible with
`r(K_*)^[3]!=0`.

The overlap supplies an intrinsic **ordinary** response-product kernel

\[
 {\cal K}^{\rm ord}_{P,S}=\ker\!\left(
  \operatorname {Mat}_3\longrightarrow\operatorname {Sym}^2(P+S)\right)
       \simeq\Lambda^2(\operatorname {im}P\cap
                                  \operatorname {im}S). \tag{4}
\]

Hence its dimensions for `k=1,2,3` are respectively `0,1,3`.  Every such
matrix also gives `sum M_ij p_i s_j=0` after the site-square-zero quotient.
For every `M` in this kernel, the **literal full-nine equations**, not merely
their target-span projection, give

\[
 \boxed{\quad
    \sigma(M)q^{[3]}=\sum_iM_{ii}X_i,
    \qquad \sigma(M)=\sum_{ij}M_{ij}a_{ij}.\quad}       \tag{5}
\]

Equation (5) is the exact rank-deficient trichotomy.

* If `sigma(M)=0` and some `M_ii` is nonzero, (5) is a literal source unit.
* If `sigma(M)` and all three `M_ii` are nonzero, then `M` is an active
  clean cap: its response is zero, so its canonical clean error is zero.
* If `sigma(M)!=0`, then (5) makes `q^[3]` pure.  One or two nonzero
  diagonal entries give an exact unary or binary residual matching source
  after projection and one-site normalization; three give the active clean
  case above, while no nonzero diagonal gives the separate zero-top branch.

Consequently a mixed coefficient of `q^[3]` forces

\[
          \operatorname {diag}M=0,\qquad\sigma(M)=0
          \quad\hbox{for every }M\in{\cal K}^{\rm ord}_{P,S}. \tag{6}
\]

This is the first genuinely source-labelled terminal: the whole intrinsic
ordinary kernel must be invisible both to the three fixed target diagonals
and to the actual direct block.  The condition is absent when `k=1`, is one
rank-two dark line when `k=2`, and is a three-plane condition when `k=3`.

The hypotheses `K_*` invertible and `r(K_*)^[3]!=0` do not remove these
strata by themselves.  Exact six-site star packets realize them together
with all nine formal response products.  Those packets are not physical
EqSystem sources: their proposed `q^[2]` and `q^[3]` violate the proved
common-power pure-lift theorem.  This sharply separates coarse bilinear
compatibility from literal full-nine/common-power compatibility.

The exact checker is
`computations/verify_h3_rank_deficient_latent_fullnine_boundary.py`.

## 1. Abstract channels versus the physical image

The abstract channel space is always

\[
             H=\mathbb C^3_P\oplus\mathbb C^3_S,       \tag{A}
\]

and an invertible `K_*` gives it a nondegenerate hyperbolic response form.
The physical endpoint stars define an evaluation

\[
       F=(P,S):H\longrightarrow L=\operatorname {im}P+
                                      \operatorname {im}S.     \tag{B}
\]

In the branch considered here, `dim ker F=k`.  The hyperbolic form remains
perfect on the abstract six-space `H`; it need not descend to a form on
the quotient `L`.  Thus invertibility of `K_*` does **not** make `F`
injective.  This is precisely why the rank-six involution theorem cannot be
applied to the overlap branch.

The guards in Section 5 show that even the three pure target products, and
indeed all nine formal response products, do not make `F` injective.  What
may still eliminate the branch is their realization by the same literal
quadratic powers `q^[2],q^[3]`; this common-power datum is absent from the
coarse guards.

## 2. The intrinsic kernel

Put `U=im P`, `V=im S`, and consider the ordinary symmetrized product map

\[
 \Phi_{P,S}:\operatorname {Mat}_3\simeq\mathbb C^3\otimes\mathbb C^3
       \longrightarrow\operatorname {Sym}^2(U+V),
 \qquad M\longmapsto PM S^{\mathsf T}+SM^{\mathsf T}P^{\mathsf T}. \tag{7}
\]

The kernel of `U tensor V -> Sym^2(U+V)` consists exactly of alternating
tensors whose two legs lie in `U intersection V`.  Therefore

\[
 \ker\Phi_{P,S}\simeq\Lambda^2(U\cap V),
 \qquad\dim\ker\Phi_{P,S}={k\choose2}.                 \tag{8}
\]

This statement precedes the site-square-zero quotient.  Thus every element
of (8) certainly gives the literal quadratic relation in (4); extra
same-site kernels, if present, only enlarge the supply of possible clean
zero-response directions.

The checker puts the pair in the normal forms

```text
k=1: P=(e0,e1,e2), S=(e0,e3,e4), dim(P+S)=5;
k=2: P=(e0,e1,e2), S=(e0,e1,e3), dim(P+S)=4;
k=3: P=(e0,e1,e2), S=(e0,e1,e2), dim(P+S)=3.
```

Exact rational row reduction returns kernel dimensions `0,1,3`.  In the
last two displayed charts the kernel bases are the expected skew matrices.

## 3. Literal full-nine contraction and the clean root

For any pair matrix `M`, use the physical definitions

\[
 \sigma(M)=\sum M_{ij}a_{ij},\quad
 r(M)=\sum M_{ij}p_is_j,\quad
 T(M)=\sum_iM_{ii}X_i.                                  \tag{9}
\]

Contracting all nine rows in (1) gives

\[
             \sigma(M)q^{[3]}+r(M)q^{[2]}=T(M).       \tag{10}
\]

If `M` lies in (4), then `r(M)=0`, and (10) is exactly (5).  No word,
endpoint order, direct coefficient, or pure target label has been
projected away.

The denominator-cleared clean error at `h=3` is

\[
 {\cal E}(M)=r(M)^{[3]}+\sigma(M)q\,r(M)^{[2]}.       \tag{11}
\]

It vanishes identically on the kernel.  Thus a kernel matrix is an active
clean cap precisely when

\[
       \sigma(M)M_{00}M_{11}M_{22}\ne0.               \tag{12}
\]

This proves the first two alternatives without a root calculation.  In the
third alternative, divide (5) by `sigma(M)`.  The residual quadratic `q`
has pure top power

\[
                  q^{[3]}=\sum_i{M_{ii}\over\sigma(M)}X_i.      \tag{13}
\]

Projecting unused colour axes and rescaling one site gives an exact unary,
binary, or ternary six-site matching source.  The ternary case is already
excluded by the arbitrary-complex six-site theorem; equivalently (12)
would also give clean two-site descent.  Unary and binary outputs are real
smaller-colour residual branches, not ternary contradictions.

If `q^[3]` has any mixed coordinate, the mixed coordinate of (5) first
forces `sigma(M)=0`; the three independent pure coordinates then force
`diag M=0`.  This proves (6).

The zero case needs care.  If `q^[3]=0`, equation (5) forces the kernel
diagonal to vanish but says nothing about `sigma`.  The general zero-top
branch is not excluded here.  The pure-lift theorem applies to the explicit
guards below because their proposed `q^[2]` is a sum of pure missing-pair
lifts; it is not silently applied to an arbitrary mixed `q^[2]`.

## 4. Exact terminal strata

### Intersection dimension one

Here (8) is zero.  Overlap alone supplies no zero-response cap at all.  The
rank-six involution test cannot be used, but there is also no alternating
kernel to contract.  The remaining literal branch is

```text
k=1, q^[3] non-pure or zero, with all nine common-power rows retained.
```

There is nevertheless a smaller exact interface.  Write the unique overlap
relation in the fixed physical bases as

\[
                 Pu=Sv=\ell,\qquad u,v\ne0.            \tag{14a}
\]

Contracting the nine rows along the two presentations of `ell` gives six
literal shared-linear identities

\[
\begin{aligned}
 p_i\ell q^{[2]}&=v_iX_i-(av)_i q^{[3]},\\
 \ell s_jq^{[2]}&=u_jX_j-(u^{\mathsf T}a)_j q^{[3]}.
\end{aligned}                                           \tag{14b}
\]

These retain the actual coordinate vectors `u,v`, the common direct block,
and every pure target label.  They are the correct starting point for an
occupied-cell/derivative deletion: one needs to prove that a source-minimal
component of `ell` makes one row in (14b) private, or that two rows supply a
smaller common-power packet.  No such privacy follows from `dim(P+S)=5`
alone; the Section 5 guard has `u=v=e0` and verifies all six rows formally.

Any closure needs site-labelled information beyond the dimension defect—an
occupied-cell derivative, a private response component, or a second word
whose overlap relation has a smaller support.

### Intersection dimension two

There is one intrinsic rank-two matrix `N`.  Unless (5) gives a unit, a
pure residual source, or an active clean cap, the mixed-top branch is
exactly

\[
                       \operatorname {diag}N=0,
                       \qquad\langle N,a\rangle=0.      \tag{14}
\]

This is a fixed-label condition: changing bases independently in the two
endpoint colour spaces changes the three diagonal readouts and is not a
physical symmetry of the GHZ target.

### Coincident three-planes

Write `S=PC` in the physical endpoint bases.  Then

\[
 {\cal K}^{\rm ord}_{P,S}={AC^{-\mathsf T}:A^{\mathsf T}=-A\}. \tag{15}
\]

If every member has zero physical diagonal, then `C` is diagonal: applying
the three coordinate skew matrices shows that column `i` of `C^{-T}` is
supported only at `i`.  If every member is also direct-dark, then

\[
                         aC^{-1}\text{ is symmetric}.  \tag{16}
\]

Indeed, the Frobenius pairing with (15) vanishes for all skew `A` exactly
when `aC^{-1}` has no skew part.  Thus the mixed-top `k=3` terminal is not
an arbitrary coincident star.  It is the literal colour-aligned locus

```text
S_i=c_i P_i for three nonzero c_i,
a C^{-1} symmetric.
```

If either alignment fails, a kernel direction leaves one of the activity
hyperplanes and equation (5) gives one of the exits above.

## 5. Sharp coarse guards and the common-power boundary

The checker constructs one guard for each `k=1,2,3` on the six physical
residual sites.  Let the three missing pairs be

```text
P0=01, P1=23, P2=45.
```

For `i<k`, take the shared endpoint form

\[
 p_i=s_i=e_i^{(2i)}+e_i^{(2i+1)},                    \tag{17}
\]

and for `i>=k` take the separated forms

\[
 p_i=e_i^{(2i)},\qquad s_i=e_i^{(2i+1)}.              \tag{18}
\]

Both triples are injective and their intersection dimension is exactly
`k`.  With `K_*=I`, the coefficient of `r(K_*)^[3]` on word `001122` is

```text
k=1: 2,   k=2: 4,   k=3: 8.
```

Take the symmetric direct block `a01=a10=-1`, all other entries zero.
Then `alpha=-1`, `trace(a)=0`, so the canonical scalar-zero matrix really
is `K_*=I`; the pairing is invertible.

Finally let the formal degree-four multiplier be

\[
 F=\sum_i\lambda_iE_i(P_i),\qquad
 \lambda_i=\begin{cases}1/2&i<k,\\1&i\ge k.\end{cases} \tag{19}
\]

Literal word enumeration verifies all nine products

\[
                         p_i s_jF=\delta_{ij}X_i.      \tag{20}
\]

The factors `1/2` compensate for the two endpoint orders in the square of
a shared form.  Thus injectivity, overlap, invertible `K_*`, nonzero
response top, and all nine response products are mutually compatible.

But (20) is not yet the EqSystem.  Promoting it with formal `Q=0` would
require one physical quadratic satisfying

\[
                         q^{[2]}=F,\qquad q^{[3]}=0.    \tag{21}
\]

The three active missing pairs in (19) are distinct and private.  The
uniform pure-lift private-edge theorem excludes (21), with arbitrary
complex cells and cancellation.  Hence these are exact guards to every
argument based only on the target-span shadow or the nine response
products, but they are not source-compatible counterexamples to (1).

This is the required separation:

```text
literal full-nine/common-power source
    => kernel contraction (5) and trichotomy;

coarse target-span or formal response products
    != literal common-power source.
```

No exact physical guard survives the full-nine/common-power test in the
displayed zero-top family.  The first unresolved literal families are the
`k=1` branch and the dark conditions (14), (16) with a general mixed or
zero top tensor.

## 6. Reproduction

Run all modes:

```text
python3 computations/verify_h3_rank_deficient_latent_fullnine_boundary.py --mode structural
python3 -O computations/verify_h3_rank_deficient_latent_fullnine_boundary.py --mode full
python3 -I -S computations/verify_h3_rank_deficient_latent_fullnine_boundary.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
ffdf0de29566a0de3a7bf6ffdd47281591b99e12c8aba2d220e8c8724289a143
```
