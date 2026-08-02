# The single degree-four Koszul cell still sees the full five-face star

Research reduction only.  This note does not construct a physical cap
homotopy, prove that the packet Tor classes have full-source provenance,
establish zero indeterminacy, or prove Krenn's conjecture.

## 1. Outcome

Restricting the universal reset problem to the one degree-four Koszul cell

\[
 K_m=H_mr_0-(H_0-u)r_m
     =H_mr_0+(u-H_0)r_m,
 \qquad m=01211222,
 \tag{1}
\]

does **not** compress its five denominator defects to one alternating or
Euler combination.  For the internal word

\[
                         \bar m=12112,
\]

the smallest coordinate presentation on which the literal reset in (1) has
a nonzero relation defect is

\[
 D_{\bar m}=\bigoplus_{v=1}^5R\,d_{v,\bar m_v}
   \mathop{\longrightarrow}^{\delta_{\bar m}}
 V_{\bar m}=\bigoplus_{w:\,w_v=\bar m_v\ \text{ for some }v}R\,e_w.
 \tag{2}
\]

It has five source columns and 211 word coordinates.  Coefficient extraction
at \(\bar m\) gives

\[
 \epsilon_{\bar m}\delta_{\bar m}(d_{v,\bar m_v})=h_v,
 \qquad v=1,\ldots,5.                                  \tag{3}
\]

The coefficient of \(r_m\) in (1) is \(u-H_0\).  Taking the coefficient of
the independent homogenizing variable \(u\) in the induced relation defect
therefore gives the labelled map

\[
 a_{K_m}:D_{\bar m}\longrightarrow
 W=R\langle\omega_1,\ldots,\omega_5\rangle,
 \qquad d_{v,\bar m_v}\longmapsto\omega_v.             \tag{4}
\]

Thus

\[
                         \boxed{\operatorname {im}a_{K_m}=W,}
 \tag{5}
\]

not a line in \(W\).  The reset is zero on the pure row \(r_0\), and the
\(H_mr_0-H_0r_m\) correction contains no \(u\), so it cannot cancel (4).
After dehomogenizing \(u=1\), the same statement is the lowest edge-degree
piece: \(h_v\) is quadratic, whereas the correction \(H_0h_v\) begins in
degree six.

Five labelled components are consequently forced for the literal
associated-grade reset of the single cell.  There is nevertheless an
important constructional compression.  The stabilizer of `12112` is

\[
 S_{\{1,3,4\}}\times S_{\{2,5\}}\cong S_3\times S_2.   \tag{6}
\]

The five faces split into two orbits, according to whether the deleted
letter is 1 or 2.  An equivariant physical construction therefore needs only
two seed formulas, one for each orbit, and then their five labelled
translates.  Two seeds are sharp; one stabilizer orbit cannot span \(W\).

The exact packet Tor images from commit `b15d1ad` do not change the universal
answer.  They cover rank four on the direct-free packet and rank three on
the tilted packet.  Packet-specifically, one and two face directions remain,
respectively.  Both Tor-to-face maps also have a four-dimensional kernel, so
these data alone do not certify zero indeterminacy.

## 2. Why (2) is the smallest active presentation

The complete odd denominator presentation is

\[
 \delta:R^{15}\longrightarrow R^{243},\qquad
 d_{v,a}\longmapsto e_a^{(v)}q^{[2]}.                  \tag{7}
\]

For a word \(w\),

\[
 [e_w]\delta(d_{v,a})=
 \begin{cases}
 \operatorname {Haf}(q_w|_{D\setminus\{v\}}),&w_v=a,\\
 0,&w_v\ne a.
 \end{cases}                                           \tag{8}
\]

The reset \(\epsilon_{\bar m}\) annihilates the ten columns with
\(a\ne\bar m_v\), so those columns are tautological for this one readout and
can be removed.  Each of the five retained columns is supported on the 81
words satisfying \(w_v=\bar m_v\).  Their union consists of every word which
agrees with \(\bar m\) somewhere.  Its complement chooses one of the two
wrong colours at every site, and hence has \(2^5=32\) words.  Therefore

\[
                       \operatorname {rank}V_{\bar m}=243-32=211. \tag{9}
\]

Every one of these coordinates occurs with a nonzero universal quadratic,
so no smaller coordinate span contains the image.  The five source columns
are independently necessary already before reset: for each \(v\), the word
which equals \(\bar m_v\) at \(v\) and is zero at the other four sites occurs
in column \(v\) and in no other selected column.  These five word rows give a
diagonal nonzero-polynomial minor.

This explains the structural point hidden by the phrase “one Koszul cell.”
The row \(r_m\) has one formal label, but its coefficient lives in a
presented odd module.  Tensoring one cell with that presentation retains all
relation generators incident to its selected coordinate.  It does not turn
their rank-five star into the boundary of a rank-one simplex.  In particular,
no alternating signs or face augmentation occur in (7); inserting such a
sum would be an extra, undeclared map \(R\to D_{\bar m}\).

## 3. The initial obstruction is genuinely five-dimensional

Write

\[
 h_v=\operatorname {Haf}(q_{12112}|_{D\setminus\{v\}}),
 \qquad
 g_v=\operatorname {Haf}(q_{00000}|_{D\setminus\{v\}}). \tag{10}
\]

At the pure output coordinate \(Y_0=e_{00000}\), the old target denominator
rows contribute the span of the five \(g_vY_0\).  Different deletion sites
give different four-site supports, so the \(g_v\) have rank five.  The
\(h_v\) use only colour labels 1 and 2, while the \(g_v\) use only colour
label 0.  Their monomial supports are disjoint, and exact sparse reduction
gives

\[
 \dim\langle g_1,\ldots,g_5\rangle=5,
 \qquad
 \dim\langle g_1,\ldots,g_5,h_1,\ldots,h_5\rangle=10. \tag{11}
\]

Consequently the mixed pure-output initial cokernel has rank five.  In the
single-cell boundary, the five classes are multiplied by \(u-H_0\).  The
\(u\)-coefficient is still the identity matrix (4), so the Koszul correction
does not lower that rank.

This proves a sharp no-go for a lower-dimensional **literal** lift: a chain
homotopy defined on only one chosen combination of the five columns does not
make the reset a chain map on (2).  A successful replacement can instead
come from new source-provenant rows, a full-source non-flat Tor kernel, or a
different corrected reset whose complete associated-grade chain identity is
proved.  None of those alternatives is excluded here.

## 4. Symmetry reduces five components to two seed constructions

Put

\[
 A=\{1,3,4\},\qquad B=\{2,5\}.
\]

Then

\[
 W=\mathbb Q[A]\oplus\mathbb Q[B]                     \tag{12}
\]

as an \(S_A\times S_B\)-permutation representation.  The orbit of
\(\omega_1\) is \(\{\omega_1,\omega_3,\omega_4\}\) and spans the first
three-dimensional summand.  The orbit of \(\omega_2\) is
\(\{\omega_2,\omega_5\}\) and spans the second.  Hence two seeds generate
all of \(W\).

They are also necessary.  The invariant plane is

\[
 W^{S_3\times S_2}=
 \left\langle
  \omega_1+\omega_3+\omega_4,
  \omega_2+\omega_5
 \right\rangle,                                        \tag{13}
\]

of dimension two.  For any single seed \(x\), the Reynolds average of every
vector in the orbit span \(\mathbb Q[S_3\times S_2]x\) is a multiple of the
one vector \(\operatorname {Av}(x)\).  That orbit span therefore has at most
one invariant direction and cannot equal \(W\).  A generic single seed has
the sharp orbit rank four; the checker verifies this exactly.

Thus the natural faster construction is not to search for five unrelated
formulas.  It is to construct

\[
 \widetilde\tau_{1}^{\,2112\to0000},
 \qquad
 \widetilde\tau_{2}^{\,1112\to0000},                  \tag{14}
\]

with full source provenance and equivariance, and transport them under (6).
This produces five labelled rows, but only two mathematical templates.  The
two invariant sums in (13) alone are not enough: they have rank two and miss
the three nontrivial permutation directions that (4) also forces.

## 5. Exact comparison with the packet Tor images

Let \(I_{\rm df}\) and \(I_{\rm tilt}\) denote the images of the denominator
Tor transgression in \(W\).  The exact calculation of `b15d1ad` gives

\[
\begin{aligned}
 I_{\rm df}&=\langle
 \omega_1,\omega_3,-\omega_2+\omega_4,
                         -2\omega_2+\omega_5\rangle,\\
 I_{\rm tilt}&=\langle
 \omega_1,\omega_3,-\omega_2+\omega_4\rangle.
\end{aligned}                                          \tag{15}
\]

Their ranks are four and three.  The missing directions are detected by

\[
 I_{\rm df}^{\perp}=\langle(0,1,0,1,2)\rangle,         \tag{16}
\]

and

\[
 I_{\rm tilt}^{\perp}=
 \langle(0,1,0,1,0),(0,0,0,0,1)\rangle.               \tag{17}
\]

In particular \(I_{\rm tilt}\subset I_{\rm df}\).  The common packet image
has rank three, and \(\omega_2,\omega_5\) form an exact complement to that
common image; adjoining them simultaneously completes both packet images.
Therefore:

1. the direct-free packet would need at least one additional face direction;
2. the tilted packet would need at least two; and
3. no single extra direction can complete both packet transgressions.

This is a specialization ledger, not a construction.  Neither packet is a
point of the full source scheme, and the sparse packets break the stabilizer
symmetry (6).  Their Tor images therefore do not supply three or four
physical rows in the universal problem.  The tilted entry here is precisely
the `12112` face-label guard computed in `b15d1ad`; it is not the `02012`
reset row used for the tilted packet's separate associated-grade symbol.

There is a separate indeterminacy warning.  The packet Tor spaces have
dimensions eight and seven, whereas (15) has ranks four and three.  Hence

\[
 \dim\ker\tau_{\rm df}=4,
 \qquad
 \dim\ker\tau_{\rm tilt}=4.                            \tag{18}
\]

Whenever a face vector has a packet Tor lift, its lifts form an affine space
over this four-dimensional cap-invisible kernel.  Equation (18) does not
prove that a later residue readout is nonzero on that kernel, but it shows
that the denominator calculation alone cannot prove zero indeterminacy.  A
physical proof still needs the downstream readout to annihilate (18), or a
canonical source-level section.

## 6. Consequence for the proof search

The denominator question now has a precise answer.

* Homologically, the literal single-cell reset requires the full rank-five
  space \(W\); there is no natural one-face sum hidden in \(K_m\).
* Equivariantly, those five components have only two seed types.  This is the
  genuine reduction in construction effort.
* Specialization Tor can lower the number of additional directions, but the
  two available guards leave ranks one and two and do not establish source
  provenance or zero indeterminacy.

The shortest credible next attack is therefore to search the full-nine
four-face equations for the two equivariant seed rows (14), while tracking
the cap-invisible kernel readout at the same time.  A search for one scalar
Euler combination is too small; a search for five unrelated rows ignores
the strongest available symmetry.

## 7. Exact verification and scope

The dependency-free checker
[`verify_h3_single_koszul_cell_face_star_no_go.py`](../computations/verify_h3_single_koszul_cell_face_star_no_go.py)
supports `all`, `subcomplex`, `symmetry`, and `packets` modes.  It constructs
the five universal selected denominator columns, counts their minimal
211-coordinate image support, freezes a diagonal five-column witness,
computes the rank-five mixed initial cokernel, and verifies the identity
matrix in the \(u\)-coefficient of the Koszul defect.  It then enumerates the
order-twelve stabilizer, proves that two orbit seeds span the five faces and
that a generic single seed has sharp rank four, and checks the packet images,
cokernel covectors, common completing directions, and four-dimensional lift
kernels.

The result is conditional only on retaining the literal associated-grade
reset \(-\kappa\iota_{00000}\epsilon_{12112}\) in the proposed cap identity.
It does not assert that the schematic \(d_{\rm cap}\) has already been
constructed, nor does it exclude a larger source syzygy which changes the
presentation while preserving the required final readout.

```text
1507a0b656924a44a4bd0f35c9609d232d700f36d63d851b784aa505066ab617
```
