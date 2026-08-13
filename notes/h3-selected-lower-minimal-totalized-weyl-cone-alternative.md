# The 341-edge Weyl bar is one formal cell; physical descent is one rank-one section

## Outcome

There is no contradiction between the complete-row Cartan descent theorem
and the new private-face obstruction. They concern different summands.

The Cartan theorem checks the Ward square on every complete 90-term matching
row. In the matching-occurrence factor this is the trivial vector

\[
\mathbf 1_X=\sum_{M\in X}e_M.
\]

It proves that root recolouring and the endpoint involution preserve the
whole-row physical source presentation. It does not construct a source
preimage of an individual \(e_M\), nor a section of the quotient in which
the selected private monomial \(\xi\) lives. Thus “source-provenant” in the
complete-row theorem applies to the complete Cartan chain; it cannot be
read as occurrence localization.

The smallest live physical datum is now exactly one right inverse for a
one-dimensional quotient. The formal 341-edge calculation itself can be
packaged as one normalized group-bar generator and need not be checked edge
by edge.

Executable certificate:
`computations/verify_h3_selected_lower_minimal_totalized_weyl_cone_alternative.py`.

## The exact occurrence quotient

Work in the literal monomial space \(V_\xi\) of the four fine grades
containing \(\xi,\bar\xi,s\xi,s\bar\xi\). Let \(B_\xi\) contain:

- the eight compatible complete 90-term endpoints;
- every normalized whole-row tail-Weyl boundary and endpoint-odd rectangle;
- the four direct-free Hasse-face bridges.

The exact calculation gives

```text
rank(complete endpoints)                         8
rank(endpoints + every whole-row bar)            8
rank(B_xi)                                      12
rank(B_xi + private endpoint-odd packet)         13
```

Hence

\[
Q_\xi=
\frac{B_\xi+\mathbb Q p_\xi}{B_\xi}
\cong\mathbb Q,
\qquad
p_\xi={4\over3}(\xi-\bar\xi-s\xi+s\bar\xi).
\]

The extended odd covector of the Weyl-bar audit vanishes on \(B_\xi\) and
reads one on \(p_\xi\). This is the precise quotient that the whole-row
Cartan theorem does not see.

If \(d_{\rm rel}:L^{\rm rel}_{1,g}\to V_\xi\) is the physical relative
boundary and \(\pi:V_\xi\to V_\xi/B_\xi\), the missing source theorem is a
section

\[
\boxed{
\sigma_\xi:Q_\xi\longrightarrow L^{\rm rel}_{1,g},
\qquad
\pi d_{\rm rel}\sigma_\xi=\operatorname{id}_{Q_\xi}.}
\]

One nonzero lift suffices because \(Q_\xi\) is one-dimensional.

## One totalized group-bar cell packages all 341 edges

Let \(\widetilde Z_0,\widetilde Z_1\) denote the two fine components with
their complete Hasse/Spencer faces included. In the source-side totalization
they are cycles, and the signed Weyl involution satisfies

\[
\tau\widetilde Z_0=-\widetilde Z_1.
\]

In the homotopy-orbit group bar, introduce the single chain-valued generator

\[
b=[\tau\mid\widetilde Z_0].
\]

Its differential is formal and exact:

\[
db=\tau\widetilde Z_0-\widetilde Z_0
  =-(\widetilde Z_1+\widetilde Z_0).
\]

Endpoint oddization gives

\[
b_\xi=(1-s)b,
\]

whose normalized bar augmentation is zero. The two-root GHZ target defect
is \(s\)-invariant, so its physical target is also zero. This is one
generator, not 341 independent generators: its chain-valued boundary
contains all 341 edges and the complete Hasse faces functorially.

This is a construction in the **formal group homotopy-orbit extension**.
The canonical algebra bar \(\operatorname{Bar}_R(R/I)\) does not
automatically contain this group-bar generator. Promoting \(b_\xi\) to the
physical relative source category is exactly the section \(\sigma_\xi\)
above. Merely adjoining a mapping-cone symbol would assume the theorem.

## Required physical readouts

The bare formal bar forces only:

```text
private first face        nonzero p_xi, with chosen orientation
normalized augmentation  0
GHZ target                0 after endpoint oddization
```

The physical capped comparison must define all other rows. In the selected
normalization its complete column must agree with the pinned \(M_v\) packet:

```text
literal boundary          360 seven-edge features
Eq                        (-1,+1,+1,-1)
ordinary residue          0
D,W,target,ainc            0
eta_z                     1+delta_(vz) u_z/t
sigma                     -q_pq^22.
```

Source naturality does not infer `D/W/ainc/Eq/residue/eta/sigma` on the bare
occurrence bar. Those values are part of the single augmented attaching-map
theorem. This is exactly why the polynomial Cartan square, although true,
does not finish Gate I.

## The positive relative-extension alternative

Let \(\widehat d\) be the complete physically typed augmented boundary in
this grade, including every admitted relative generator, and let \(m_v\) be
the desired complete column above. Finite-dimensional duality gives exactly
two cases.

1. If \(m_v\in\operatorname{im}\widehat d\), choose one preimage. It is the
   selected cell \(C\) satisfying
   \(J_3C=A J_{\rm col}(u_{024}-u_{012})\).
2. If \(m_v\notin\operatorname{im}\widehat d\), a functional on the full
   augmented cokernel kills every physical correction and reads one on
   \(m_v\). This is the separator branch once its physical terminal
   interpretation is made.

Two fillers in the first branch differ by the protected kernel. If the
physical terminal is nonzero on that difference, normalization gives the
relative generator. If the terminal kills the kernel, the comparison is
well-defined and the Fredholm separator alternative applies. There is no
third linear branch.

The explicit \(\lambda_\xi\) is the first associated-graded seed for the
cokernel case. It is not yet a final separator: it must extend across every
future relative generator and every augmented row. Conversely, the formal
group-bar generator is the exact seed for the boundary case, but becomes
physical only after \(\sigma_\xi\) and the single capped augmented column
are constructed.

Thus the shortest positive target is not a 341-edge table. It is one
occurrence-local principal-parts/Weyl-bar section in the exact grade,
followed by one complete augmented-column check.

## Correction: the fixed GHZ fibre is not root-equivariant

The standard factorization

\[
w=\exp(L_E)\exp(-L_F)\exp(L_E)
\]

does integrate the universal Cartan homotopy. It does **not** act on the
fixed GHZ fibre. This is already visible infinitesimally.

Let

\[
\Delta=\sum_{c=0}^2e_c^{\otimes8}
\]

and apply either root \(2\leftarrow1\) or \(1\leftarrow2\) at site 2 or
site 5. The four resulting tensors are four distinct mixed words, each
outside the line \(\mathbb Q\Delta\). Hence the span of these four root
directions meets the projective stabilizer of \(\Delta\) in zero.

Equivalently, in the target coordinate ring put
\(f_u=y_u-\Delta_u\). For a root vector field \(X\),

\[
X(f_u)(\Delta)=(X\Delta)_u,
\]

and this is nonzero for one of the four mixed-word coordinates. The point
ideal of \(\Delta\) is therefore not \(X\)-stable. So a root contraction is
not an endomorphism of the cotangent or Tate complex of the fixed fibre.
The phrase “connected two-root stabilizer of GHZ” is false for the roots in
this construction.

## The corrected equivariant object is the orbit-relative derived fibre

There is nevertheless a canonical positive construction one level up. Let
\(\mathcal O\) be the connected tail-root orbit of \(\Delta\), and form the
derived source family over \(\mathcal O\). Use its functorial simplicial
polynomial/bar resolution, followed by principal parts and Hasse
totalization. An arbitrary minimal Tate resolution is not canonical enough
for this step; the simplicial bar model is functorial and genuinely carries
the group action and Cartan homotopies.

The endpoint swap \(s=(0\;1)\) commutes with all tail-root operations and
fixes every tensor in \(\mathcal O\) pointwise: tail operations never alter
the equal endpoint entries inherited from \(\Delta\). Thus the two copies of
the unipotent path have identical base path. Their difference

\[
b_\xi=(1-s)[\tau\mid\widetilde Z_0]
\]

lies canonically in the relative homotopy kernel over \(\mathcal O\). The
private-face theorem computes its associated-graded boundary and shows that
its image in \(Q_\xi\) is nonzero. After the certified normalization,

\[
\pi d(b_\xi)=1\in Q_\xi.
\]

Therefore the orbit-relative derived model **does** canonically realize the
source-side section \(\sigma_\xi\). This is stronger than merely postulating
a mapping-cone symbol and avoids occurrence-by-occurrence integration.

It still does not finish the physical comparison. The remaining map is

\[
\Pi_{\rm phys}:C^{\rm orbit,rel}_{\rm PP/Hasse}
   \longrightarrow C^{\rm physical,aug}_{h=3}.
\]

It must preserve the exact word, fine degree, repeated grade, and protected
rows. Its value on \(b_\xi\) must be the literal capped column, not just the
private associated-graded packet. This is precisely the comparison functor
that the complete Hasse/Cartan naturality audit found absent.

The terminal burden can be weakened but not erased. Once both source and
canonical domains carry the physical readout

\[
q=\sum_{i=1}^6m_i-\mathrm{ainc},
\]

a nonzero \(q\)-transport defect already normalizes to a relative generator;
a zero defect gives the augmented comparison and Fredholm branch. Thus one
need not force an a priori exact \(q\) value on the derived lift. But the
exhaustive alternative does not manufacture \(q\): defining physical \(q\)
on the complete orbit-relative domain is still required. Likewise formal
commutation with the Kähler ridge does not by itself establish the literal
labelled repeated-grade terminal map.

The refined frontier is therefore:

1. source-side occurrence section: constructed canonically in the
   orbit-relative derived PP/Hasse model;
2. physical comparison on that one derived generator: open;
3. physical \(q\) typing: either transports or immediately gives the
   relative-generator branch.

## Why canonical transport back to the GHZ fibre kills the boundary

The fact that \(b_\xi\) is vertical over the orbit does not make it a chain
in the fibre over \(\Delta\). This distinction is exact even in the
four-endpoint model.

At the initial point label the two vertical endpoints \(v,sv\), and at the
terminal point label them \(wv,swv\). The difference of the path and its
\(s\)-translate has ambient endpoint boundary

\[
             -v+sv+wv-swv.                              \tag{*}
\]

Its base path is zero because the two source paths cover the same target
path. But equivariant parallel transport back to \(\Delta\) uses \(w^{-1}\):

\[
wv\longmapsto v,qquad swv\longmapsto sv,
\]

where the second equality uses \(sw=ws\). Under this canonical transport,
(*) becomes zero. Thus the orbit-relative cell does not yield a nonzero
fixed-fibre boundary.

This exposes a load-bearing choice:

- equivariant transport gives an honest chain in the fixed fibre, but
  identifies the Weyl-shifted fine labels and kills the private packet;
- retaining fixed physical word/fine labels keeps the private packet, but
  the chain remains in the orbit-relative cone.

Consequently the remaining issue is not merely that a preferred physical
presentation has not been proved quasi-isomorphic to the cotangent/Tate
fibre. An ordinary quasi-isomorphism to the fixed fibre forgets exactly the
relative path that supplies \(Q_\xi\). One must retain the orbit-relative
cone and construct an enriched filtered/augmented comparison, or provide a
nontrivial connection whose transport preserves the labelled boundary.

Nor can all physical readouts be moved to the canonical fibre for free.
The target and normalized bar augmentation are intrinsic. The literal
private rows, `Eq`, ordinary residue, `D/W/ainc`, the shifted ridge, and
especially \(q=\sum m_i-\mathrm{ainc}\) must be realized as compatible
cocycles on the retained orbit-relative model. A quasi-isomorphism only
transports their cohomology classes after such cocycles have been defined;
it does not manufacture them or preserve the physical fine/repeated
filtration automatically.
