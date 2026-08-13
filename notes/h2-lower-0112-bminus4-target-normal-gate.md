# The natural lower \(B-4I\) lift stops at a mixed target-normal face

## Outcome

In the marked lower packet

    sites       0,1,4,5
    word        0,1,1,2
    occurrence  f=(p=0,s=1;q=45)

the four endpoint-adjacency moves are

    p: 0 -> 4,   p: 0 -> 5,   s: 1 -> 4,   s: 1 -> 5.

For a move \(x\to t\), let \(\tau_{xt}\) exchange the two sites and let
\(w_{xt}\) be the simultaneous signed colour Weyl swap at those sites
between their two colours. The composite

\[
                         g_{xt}=\tau_{xt}w_{xt}        \tag{1}
\]

fixes the lower word and sends the selected occurrence to its formal
\(B\)-neighbour. If the two site colours agree, \(w_{xt}=1\). Otherwise
the Cartan path has target-normal boundary

\[
 (g_{xt}-1)\Delta_4=(w_{xt}-1)\Delta_4,               \tag{2}
\]

because site permutation fixes the GHZ target. Exactly one marked move,
\(1\to4\), has equal colours. The other three give

\[
\boxed{
 N_f=
 X_{1010}+X_{0101}+X_{2002}+X_{0220}
 +X_{1212}+X_{2121}-2\Delta_4.}                       \tag{3}
\]

Thus the natural occurrence-local Cartan/site lift of
\((B-4I)e_f\) is not target-safe. The pinned common \(H_0\) carrier has
zero target projection. Even artificially granting it the whole line
\(\mathbb Q\Delta_4\) would cancel only the last term of (3). The primitive reduced cap
\(p_{v,N}=(-Q_{v,N},-\operatorname{ores})\) has target zero and cancels
none of (3). A primitive mixed coordinate, for example
\(X_{1010}^{*}\), kills both granted corrections and reads one on \(N_f\).

The obstruction is not removed by the special rational preimage used to
fill the even centered class. For

\[
 c_2^+=6(e_f+e_{Sf})-\mathbf1,\qquad
 v=-{1\over24}(B+6I)c_2^+,\qquad (B-4I)v=c_2^+,       \tag{4}
\]

the natural target normal is still nonzero. After primitive scaling it is

\[
\begin{aligned}
 N_v^{\rm prim}={}&
 2(X_{0011}+X_{1100}+X_{1122}+X_{2211})-2X_{1111}\\
 &-(X_{0101}+X_{0220}+X_{1010}+X_{1212}
       +X_{2002}+X_{2121}).                           \tag{5}
\end{aligned}
\]

Hence common \(H_0\) and the primitive cap do not construct the physical
\(B-4I\) lift. The first positive object is an occurrence-local
mixed-target cone section, together with its one-endpoint Hasse
product-rule face. The mixed-coordinate covector is only a quotient dual;
it becomes a physical Fredholm terminal only if it extends across the
complete mixed-target, protected, and physical-\(q\) source map.

The independently audited shared-interface theorem identifies this source
type: coefficientwise it is the lower projection of the root-even,
target-bearing \(C_+\) orbit. That theorem does not supply the
source-labelled restriction map. Formulae (3) and (5) give the exact lower
target packet which such a map must carry.

Companion checker:
[verify_h2_lower_0112_bminus4_target_normal_gate.py](../computations/verify_h2_lower_0112_bminus4_target_normal_gate.py).

## 1. The four literal endpoint moves

Write target words in the site order \((0,1,4,5)\).

| move | neighbour | colour pair | target normal |
|---|---|---|---|
| \(0\to4\) | \((4,1;05)\) | \(0,1\) | \(X_{1010}+X_{0101}-X_{0000}-X_{1111}\) |
| \(1\to4\) | \((0,4;15)\) | \(1,1\) | \(0\) |
| \(0\to5\) | \((5,1;04)\) | \(0,2\) | \(X_{2002}+X_{0220}-X_{0000}-X_{2222}\) |
| \(1\to5\) | \((0,5;14)\) | \(1,2\) | \(X_{1212}+X_{2121}-X_{1111}-X_{2222}\) |

Their sum is (3). The signs do not depend on replacing an unsigned colour
transposition by the standard signed \(SL_2\) Weyl representative: each
changed monochromatic word is acted on at two sites, so its two signs
multiply to \(+1\).

After reinserting q23:21 and the spectator q67:22, (3) occupies the
literal eight-site target words

    +1: 10211022  01210122  20210222
        02212022  12211222  21212122
    -2: 00210022  11211122  22212222.

These are target-normal faces of the root-decorated path, not the original
top word 01211222. The Cartan root degrees make the total operator
homogeneous; simply identifying the displayed words would discard the
normal boundary rather than fill it.

## 2. Why the exact even combination does not become target-safe

On the six unordered endpoint holes, the two orientations of \(v\) have
equal coefficients

    01: -13/12
    04:   1/6
    05:   1/6
    14:   1/6
    15:   1/6
    45:   5/12.

For a hole \(h\), let \(N_h\) be the sum of the four two-site target
defects crossing from \(h\) to its complementary residual pair. The target
face of the natural lift of (4) is

\[
                         N_v=\sum_h2v_hN_h.            \tag{6}
\]

The checker computes (6) exactly. Its coefficients have denominator three;
multiplying by \(3/2\) yields the primitive integral vector (5). In
particular \(X_{0011}^{*}(N_v^{\rm prim})=2\), while
\(X_{0011}^{*}(\Delta_4)=0\). So the cancellation failure is present on
the actual combination which maps to \(c_2^+\), not merely on a convenient
basis generator.

The target normal has total coefficient augmentation zero. That does not
make it a common-response boundary. Its mixed-word part is independent of
the one-dimensional \(\Delta_4\) line, and the pinned primitive cap has no
target coordinate at all.

## 3. The remaining Hasse face

Let \(a_f\) denote the coefficient selecting an occurrence-local endpoint
path and \(H_{xt}\) its Cartan/site homotopy. The source differential obeys
the product rule

\[
 d(a_fH_{xt})=a_f(g_{xt}-1)+(da_f)H_{xt}.             \tag{7}
\]

The first term contains (2)--(3). Adding mixed target-cone generators can
cancel it only if they exist in the same word/fine/repeated grade. Their
second term must then cancel the occurrence-local one-endpoint cross face
\((da_f)H_{xt}\). Neither the common \(H_0\) line nor \(p_{v,N}\) supplies
that face:

- \(H_0\) is occurrence-constant and its pinned target projection is zero.
- \(p_{v,N}\) has only its labelled \(Q_{v,N}\) and ordinary-residue
  entries, with target and protected rows zero.

This identifies the minimal new source family:

> Construct one cut-covariant occurrence-local mixed-target cone section
> for the three root-decorated moves in 0112, totalized with their first
> Hasse cross faces and with q23:21 q67:22 reinsertion into the labelled
> repeated P3+K2 grade. Site symmetry then transports it to the 0121 cut.

Equivalently, construct the physical \(C_+\) orbit with this literal lower
restriction. The known equality of coefficient shadows is necessary but
does not identify the two source presentations.

This is strictly sharper than asking for an arbitrary physical \(B\)
operator. The coefficient action is already known; (3), (5), and (7) are
the first target-normal and product-rule data it must carry.

## 4. Scope

The computation proves the exact target boundary of the natural combined
site/Weyl realization of every marked \(B\)-edge, and of the full preimage
in (4). It uses the committed facts that site permutations preserve GHZ,
two-site Cartan paths have Weyl target defect, and the primitive cap has
target zero.

It does not assert that an occurrence-local group bar is already present
in the physical source resolution. That provenance is part of the missing
section. Nor does the mixed-coordinate dual yet define a physical
terminal: complete target-cone and augmented-source extension remains to
be checked.

## Verification

    python3 computations/verify_h2_lower_0112_bminus4_target_normal_gate.py
    python3 -O computations/verify_h2_lower_0112_bminus4_target_normal_gate.py
    python3 -I -S computations/verify_h2_lower_0112_bminus4_target_normal_gate.py
