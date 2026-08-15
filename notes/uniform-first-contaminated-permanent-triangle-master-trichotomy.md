# The first contaminated permanent triangle does not yet close the master trichotomy

## Result

The first literal contamination of a permanent triangle has two clean local
\(C_4\) coefficient cores and one three-term \(K_4\) coefficient core, but
none is yet the active three-colour cap required by the proof.  This gives a
sharp intrinsic counterguard to promoting a local coefficient restriction
to the master trichotomy.  No protected `B/Eq` presentation is involved.

Use six sites

```text
rows r,s = 0,1; columns x,y,z = 2,3,4; hub h = 5
```

and write the colour-zero \(K_{2,3}\) cells as

\[
Q=\begin{pmatrix}a&b&c\\d&e&f\end{pmatrix}.
\]

The three colour-one hub spokes are \(p_x,p_y,p_z\).  The first
contamination consists of the two additional colour-zero cells

\[
g=q^0_{01},\qquad k=q^0_{23}.
\]

Literal enumeration of all \(3^6\) output words and all fifteen perfect
matchings gives only

\[
\begin{aligned}
F_{000011}&=p_z(ae+bd+gk),\\
F_{000101}&=p_y(af+cd),\\
F_{001001}&=p_x(bf+ce).                                    \tag{1}
\end{aligned}
\]

Thus the packet has no singleton internally: its complete multiplicity
histogram is

```text
0 terms: 726; 2 terms: 2; 3 terms: 1.
```

Nevertheless, deleting the forced spoke in each row gives, intrinsically,

```text
000011 / p_z -> full three-matching K4 core,
000101 / p_y -> clean C4 core,
001001 / p_x -> clean C4 core.
```

These are coefficient-core statements only.  All four endpoints in every
displayed core carry colour profile

\[
(\kappa_0,\kappa_1,\kappa_2)=(\ne0,0,0),
\]

so the three-colour activity product is zero.  The two local \(C_4\) cores
are not active clean caps in the sense required downstream.  Likewise the
three-term derivative is one four-site coefficient, not an exact smaller
GHZ source.

The exact checker is
`computations/verify_uniform_first_contaminated_permanent_triangle_master_trichotomy.py`.

## Pure normalization cannot stay in the killed reinsertion sector

Put

\[
H=ae+bd+gk.                                                  \tag{2}
\]

Since \(p_z\ne0\), the mixed equation in (1) gives \(H=0\).  Now inspect
the literal pure-zero coefficient.  Its fifteen matchings partition into
three which use the physical edge \(45=zh\), and twelve which avoid it.
The first three are exactly the three \(K_4\) parents reinserted by
\(q^0_{45}\).  Hence

\[
F_{000000}=q^0_{45}H+E,                                    \tag{3}
\]

where \(E\) is the sum of the twelve escape matchings.  Exact target
normalization and (2) imply

\[
E=1.                                                        \tag{4}
\]

At least one escape matching therefore has a nonzero monomial.

There is an exact finite classification of those twelve matchings.  Each
shares exactly one edge with a unique one of the three reinserted \(K_4\)
parents.  Their symmetric difference is one four-cycle.  Each parent is
selected by exactly four escapes.

Formally restrict the pure coefficient to terms containing that unique
common edge.  On the four remaining sites there are only three possible
perfect matchings:

- if the third is absent, the restriction has a clean local \(C_4\)
  coefficient core (still monochromatic and inactive);
- if the third is present, the restriction has the full four-site matching
  coefficient core (not a descended exact source).

Restricting the pure row at that common edge exposes two or three local
matching terms.  It does **not** prove an equation for that restriction:
equation (4) constrains the sum of all twelve escape terms, not the part
containing one chosen edge.  Even if the restriction is retained as a named
source operation, it transports only this cofactor row; it does not transport
the other eighty four-site output words or the three pure target
normalizations.  Thus it is not yet a source-natural descent to a smaller
exact GHZ tensor.

## The extra channel is not removable by cut-rank rhetoric

After factoring \(p_z\), use the shore

\[
\{r,s\}\mid\{x,y\}.
\]

The three terms in \(H\) occupy three distinct matching-connectivity
channels:

```text
ae : two-cross identity,
bd : two-cross swap,
gk : zero-cross separated channel.
```

At the all-unit contamination point

\[
a=b=c=d=e=g=p_x=p_y=p_z=1,\qquad f=-1,\quad k=-2,
\]

their coefficients are \((1,1,-2)\).  The scalar augmentation is zero, but
all three channel coordinates are nonzero, and deleting any one makes the
scalar sum nonzero.  Thus \(gk\) is not itself a removable kernel state.
Only the full three-channel combination lies in the augmentation kernel.

The GHZ target has cut rank three, but cut-rank equality alone supplies no
source-natural identification of this connectivity basis with the three
target-colour channels.  The valid conclusion from the literal mixed/pure
equations is only the escape identity (2)--(4), not that \(gk\) is redundant
or that a full tensor descends.

There is also no hidden linear permanent-ideal comparison.  The checker
writes the most general homogeneous linear relation among

\[
ae+bd,\qquad af+cd,\qquad bf+ce
\]

and obtains an exact \(30\times18\) cubic coefficient matrix of rank \(18\).
Thus the linear-syzygy kernel is zero.  Identity (2) of the preceding
permanent-triangle lemma is inhomogeneous, with monomial right side
\(2bcd\); it is a unit certificate, not an automatic source comparison cell.

## Minimal pure anchoring forces singleton rows

As a separate exact boundary, choose one of the fifteen perfect matchings
as a pure anchor in each colour and add only their diagonal cells to the
eleven-cell packet.  The checker exhausts all

\[
15^3=3375
\]

choices.  Every choice has a mixed singleton; the minimum is nine, attained
by four anchor triples.  This proves alternative (i) for every support-
minimal pure completion of the packet.

This census does not claim that the same singleton remains after arbitrary
additional repair cells.  Equations (2)--(4) still force an escape matching,
but they do not isolate its common-edge restriction as an exact output row.

## Master trichotomy and all-order interface

For the first contaminated permanent triangle, the present exact verdict on
the proposed alternatives is:

1. **Singleton/unit:** absent in the eleven-cell packet; forced for every
   support-minimal one-pure-matching-per-colour completion, but not proved
   persistent under arbitrary repairs.
2. **Active clean \(C_4\) cap:** not constructed.  Two clean local \(C_4\)
   coefficient cores exist, but their three-colour activity products vanish.
3. **Smaller exact matching source:** not constructed.  The forced-spoke
   factorization and common-edge restriction expose individual four-site
   cofactors but do not transport the full tensor or target normalization.

If the packet at order \(N>6\) carries a forced unit common tail, factoring
that tail first reduces the named coefficient rows verbatim to this six-site
calculation.  The remaining all-order recurrence input is now precise:

> either assemble the local \(C_4\) in all three colours with every required
> \(\kappa_{c,s}\ne0\), or prove a full-output restriction theorem carrying
> all mixed rows and pure normalizations to the smaller matching source.

Same-sector support alone is insufficient: it gives the coefficient core but
not three-colour activity or full tensor descent.  Global pure normalization
may also change the spectator tail, producing a larger alternating core.

## Scope

This is an intrinsic counterguard for diagonal, occurrence-labelled
coefficient rows.  It proves the local contaminated packet and the six-site
pure/reinsertion escape decomposition.  It does not construct an active
three-colour cap, an exact smaller GHZ source, the missing all-order
restriction theorem, or an identification of matching-connectivity channels
with GHZ colour channels solely from cut rank.

Run:

```text
python3 computations/verify_uniform_first_contaminated_permanent_triangle_master_trichotomy.py --mode structural
python3 -O computations/verify_uniform_first_contaminated_permanent_triangle_master_trichotomy.py --mode full
python3 -I -S computations/verify_uniform_first_contaminated_permanent_triangle_master_trichotomy.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
eafe44986bc6c75b6c05d6d840927689b6e5008d6063fd5e7742b860442ebc69
```
