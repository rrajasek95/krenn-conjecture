# The two lower packets map to `delta+` coefficientwise, but leave a rank-two mixed target face

This note pins the exact common interface between the order-two lower
packets and the six-output root-even packet.  The accompanying checker is

```text
computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py
```

## Exact coefficient map

For either four-site cut, let `V` be the twelve-dimensional module on
ordered endpoint occurrences

\[
                 (p,s;\text{the complementary residual edge}).
\]

Let `S` reverse the endpoint roles and let `B_occ` replace one endpoint by
one residual site.  Forgetting endpoint order gives the six-dimensional
module on unordered endpoint holes.  Write this quotient as

\[
                       \pi:V\longrightarrow \mathbb Q^6.
\]

It is an exact intertwiner:

\[
       \pi S=\pi,\qquad \pi B_{\rm occ}=B_{\rm ep}\pi.       \tag{1}
\]

Thus it kills every endpoint-odd vector and preserves the full `B-4`
factorization on the even part.

Use the six-hole order

```text
B0=02, B1=01, B2=03, B3=13, B4=23, B5=12.
```

There are four K4 relabels sending a prescribed marked hole to any fixed
target hole.  Choose

```text
0112 cut, sites 0,1,4,5:  0->0, 1->1, 4->2, 5->3;  marked -> B1,
0121 cut, sites 0,1,2,3:  0->2, 1->3, 2->0, 3->1;  marked -> B4.
```

If

\[
 c_a^+=6(e_a+e_{Sa})-\mathbf1_{12},
\]

then the two quotients satisfy

\[
 \pi_{23}c_{23}^+=2c_1^+,
 \qquad
 \pi_{45}c_{45}^+=2c_4^+.
\]

Consequently

\[
 \boxed{
 {\pi_{23}c_{23}^++\pi_{45}c_{45}^+\over16}
 = {c_1^++c_4^+\over8}
 =\delta_+.}                                               \tag{2}
\]

After clearing the normalization by four, the left side maps to the
integral debt

\[
                  D_6=4\delta_+=(-1,2,-1,-1,2,-1).          \tag{3}
\]

This proves the desired map in the endpoint association module.  It also
shows that no further coefficient identity is missing.

## Why this is not yet a physical relabel

The maps in (2) relabel the K4 endpoint-hole graph.  They do not relabel
literal decorated source monomials.  The lower basis retains an ordered
`p/s` occurrence and its residual `q` edge, whereas the six `B_i` are
complete pure-`q` multiplier columns.  Site, colour, and repeated-edge
relabeling preserve operation type, so they cannot turn the former into the
latter.  A response/Cartan/Hasse comparison is needed to promote (2).

The natural promotion has a sharp first boundary.  In the `0112` cut, the
site swap carrying an endpoint to a residual site must be accompanied by a
two-root Weyl path whenever the two site colours differ.  Applied to the
exact `B-4` preimage, its primitive target normal has eleven full-word
coordinates.  The mixed covector

```text
X_00211122^*
```

kills the local diagonal target line and reads `2` on this normal.  The
`0121` cut has the transported primitive normal, detected by

```text
X_00111222^*
```

with the same value.  The physical word stabilizer

\[
                       \sigma=(2\ 5)(3\ 4)                    \tag{4}
\]

exchanges the two cuts and their two normals.

The two local diagonal lines have rank two.  Adjoining the two natural
mixed normals raises the rank to four.  Equivalently, their classes have
rank two modulo the granted diagonal target corrections, with pairing

\[
 \begin{pmatrix}
 X_{00211122}^*\\ X_{00111222}^*
 \end{pmatrix}
 (N_{23},N_{45})
 =
 \begin{pmatrix}2&0\\0&2\end{pmatrix}.                       \tag{5}
\]

In particular the `sigma`-even sum `N23+N45` is nonzero; the two cuts do
not cancel each other's target defect.  Thus the minimum physical repair is
one `sigma`-covariant two-object orbit of occurrence-local mixed-target cone
sections, totalized with the one-endpoint product-rule/Hasse faces.  Before
imposing covariance it has two independent target restrictions; covariance
identifies them as one cell type.

This is exactly the missing lower restriction of the independently isolated
root-even `C_+` orbit.  The result is therefore a positive coefficient
construction plus a minimal physical obstruction, not another unexplained
six-output debt.

## The beta-zero payoff is conditional on the full comparison

The quotient (2) is beta-independent.  Its literal special-fibre signature
is

```text
lower landing          delta+
mixed target           N23 and N45, still nonzero
selected D0            0
lower-column Bockstein 0.
```

Indeed, for a beta-independent integral closed lower column `x`,
`dx=0=beta*0`, so its connecting image is zero.  Beta-independence by itself
does not manufacture the selected `D0` proper face or prove beta-saturation.

There is an important stronger conditional statement.  If (2) and the
mixed-target repair extend to the **pointed** `k[beta]`-linear chain
comparison on a source generator satisfying

\[
                            ds=\beta y,                       \tag{6}
\]

then chain-map naturality gives

\[
 d\Phi(s)=\beta\Phi(y),\qquad
 \delta_\beta[\Phi(s\bmod\beta)]=[\Phi(y\bmod\beta)].        \tag{7}
\]

At that stronger level the generic even face and the `D0` Bockstein really
are consequences of one integral comparison.  The lower association map
does not yet supply (6).  The remaining beta-zero condition is precisely
beta-saturation of the complete augmented physical image, or the completed
`D0` terminal dual.

## Exact frontier

The shortest remaining theorem is now:

> Construct one cut-covariant, source-labelled mixed-target/Hasse cone orbit
> whose restrictions are the two natural `B-4` normals in (5), whose lower
> coefficient map is (2), and whose pointed `k[beta]` extension contains the
> proper face (6).

The first two clauses construct physical generic `iota`; the third is what
makes the beta-zero Bockstein automatic.  Omitting the third leaves `D0` as
an independent saturation/terminal obligation.

Run:

```text
python3 computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py
python3 -O computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py
python3 -I -S computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py
```

Pinned ledger SHA-256: `358b02641badab180817493d846e73282b1b3adc1d666f5f5a21bf6899b13bbc`.
