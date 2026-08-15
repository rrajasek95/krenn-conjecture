# Permanent triangles persist through exactly rank-one cofactor reinsertion

## Outcome

The support-28 three-row unit has a uniform all-order extension with an
arbitrary common cofactor tail.  The extension is source-labelled and stable
under terminal-ear or tight-cut reinsertion precisely when the boundary
transfer is rank one in the three permanent-triangle rows.  A nonzero common
tail then preserves the Laurent contradiction.

Neither a terminal ear nor a tight cut forces this rank-one condition.  A
labelled `C6` is the smallest exact tight-cut counterguard: three words agree
on the whole odd shore, but the cut exposes two independent near-perfect
cofactor states.

The exact checker is
`computations/verify_uniform_permanent_triangle_common_tail_reinsertion.py`.

## 1. The arbitrary-common-tail minor lemma

Work over a field of characteristic different from two.  For a fixed word,
replace each aggregate edge matrix by its selected endpoint-colour scalar;
the word coefficient is then the ordinary weighted perfect-matching sum.
This retains the physical word and occurrence labels and applies whether or
not the original edge matrices were diagonal.

Suppose three literal global mixed rows have expansions

\[
\begin{aligned}
F_{xy}&=T\,u(ae+bd),\\
F_{xz}&=T\,v(af+cd),\\
F_{yz}&=T\,w(bf+ce),                              \tag{1}
\end{aligned}
\]

where the six rectangle cells and the three complementary-pair factors are
support units.  The cofactor tail \(T\) is arbitrary: it may have any number
of matching monomials and cancellations.  The three-row identity is

\[
c v wF_{xy}+b u wF_{xz}-a u vF_{yz}
       =2bcduvwT.                                  \tag{2}
\]

Therefore the three mixed rows cannot vanish simultaneously at a point where
\(T\ne0\).  Scheme-theoretically, their ideal becomes the unit ideal after
localizing the support cells and \(T\).  When \(T\) is itself a support
monomial this is the Laurent unit from the eight-site guard; no monomial
hypothesis on \(T\) is needed for the pointwise statement.

Here is the exact source-labelled condition behind (1).  For row \(i\), let
\(\mathcal L_i\) be its two local rectangle matchings and let
\(\mathcal M_i\) be its global compatible matching occurrences.  There must
be one labelled tail family \(\mathcal T\), independent of \(i\), and
weight-preserving bijections

\[
\mathcal M_i\ \cong\ \mathcal L_i\times\mathcal T
       \qquad (i=xy,xz,yz).                         \tag{3}
\]

Then \(T\) is the total weight of \(\mathcal T\).  Conversely, (3) is the
termwise restriction/reinsertion statement that makes a common cofactor
natural; equality of an aggregated projection is not enough.

The checker realizes (3) literally on twelve sites.  It takes the pair-chart
eight-site permanent triangle and reinserts a four-site all-colour-2 cofactor
with three matching monomials.  Direct enumeration of all twelve-site perfect
matchings gives six terms in every global row, exactly

\[
(\text{two local terms})(\text{three tail terms}).
\]

This verifies a genuinely nonmonomial tail, not only multiplication by a
selected matching.

## 2. Exact terminal-ear recurrence

Let \(H\) be the old graph with distinguished vertices \(x,y\), and add a
terminal odd ear

\[
P=xv_1v_2\cdots v_{2k}y,                             \tag{4}
\]

whose internal vertices have no other incident support edges.  Every perfect
matching of the enlarged graph has exactly one of two forms:

* the **internal channel** uses
  \(v_1v_2,v_3v_4,\ldots,v_{2k-1}v_{2k}\) and an arbitrary perfect matching
  of \(H\); or
* the **through channel** uses
  \(xv_1,v_2v_3,\ldots,v_{2k}y\) and an arbitrary perfect matching of
  \(H-\{x,y\}\).

For every fixed source word this is the exact coefficient identity

\[
F^+_i=A_iF^H_i+B_iF^{H-\{x,y\}}_i,                  \tag{5}
\]

where \(A_i,B_i\) are the labelled products along the two ear patterns; an
incompatible pattern simply contributes zero.  The checker exhausts all 64
graphs on four outside vertices for ears of lengths 3, 5, and 7, verifying
the disjoint matching bijection in all 192 cases.

Equation (5) gives the useful persistence theorem.  Suppose the marked
permanent triangle is disjoint from the ear and its endpoints, the three
words agree on the ear/tail labels, and both deletion states factor as

\[
F^H_i=u_iE_iT_0,\qquad
F^{H-\{x,y\}}_i=u_iE_iT_2.                           \tag{6}
\]

Then \(A_i=A\), \(B_i=B\), and

\[
F^+_i=u_iE_i\underbrace{(AT_0+BT_2)}_{T^+}.          \tag{7}
\]

Thus a terminal ear lying wholly in the common cofactor tail preserves the
three-row unit, provided \(T^+\ne0\) at the putative source.  The recurrence
can be iterated: every invisible terminal ear merely replaces the old common
tail by its two-channel transfer (7).

A concrete source-support condition implying (6) is that, in both outside
states \(H\) and \(H-\{x,y\}\), no compatible matching crosses between the
marked rectangle block and the tail.  Then restriction gives the Cartesian
products (3).  More generally, (6) itself is the sharp algebraic rank-one
condition; separation is only a convenient sufficient hypothesis.

There are two terminal failures:

1. if either deletion state contains companion matchings not divisible by
   the same local row \(u_iE_i\), the ear adds an inhomogeneous correction and
   the old triangle does not lift; or
2. if the common updated tail \(T^+\) vanishes, (2) has zero right side and
   gives no contradiction.

The second failure is why a pure-row or coordinate-separated tight-boundary
argument must prove the selected total cofactor nonzero; a nonzero tail
monomial by itself does not prevent cancellation in the total tail.

## 3. Exact tight-cut criterion

Let \(L|R\) be an odd tight cut.  Since every perfect matching uses exactly
one crossing edge, the fixed-word coefficient is exactly

\[
F_i=\sum_{uv\in\delta(L)}
 q^{(i)}_{uv}
 H^{(i)}_{L-\{u\}}
 H^{(i)}_{R-\{v\}}.                                  \tag{8}
\]

Assume the permanent triangle lies on the \(R\)-side.  Tight-cut reinsertion
supplies a common tail if its labelled boundary transfer has rank one in the
three row labels: for every compatible boundary occurrence there are scalars
\(C_{uv}\), independent of \(i\), such that

\[
q^{(i)}_{uv}H^{(i)}_{L-\{u\}}
H^{(i)}_{R-\{v\}}
     =u_iE_iC_{uv}.                                   \tag{9}
\]

Then (8) is (1) with \(T=\sum C_{uv}\).  A single common
coordinate-separated boundary occurrence is the strongest easy sufficient
case.  Multiple boundary edges are allowed, but only if their total transfer
still has the common rank-one factor and the resulting \(T\) is nonzero.

This states the exact extra compatibility missing from a graph-only
tight-cut or ear decomposition.

## 4. Smallest tight-cut counterguard

Take the six-cycle

\[
01,12,23,34,45,50
\]

and the odd shore \(L=\{0,1,2\}\).  Its cut is \(\{23,05\}\), and its two
perfect matchings each cross the cut exactly once.  Hence this is a connected,
matching-covered, nontrivial tight cut at the smallest possible order.

Give edges 01, 12, 23, and 05 colour-0 cells, and give 34 and 45 both
colour-0 and colour-1 cells.  The three source words

\[
000011,\qquad 000110,\qquad 000000                    \tag{10}
\]

agree identically on the whole shore \(L\).  Nevertheless their coefficients
are

\[
\begin{aligned}
F_{000011}&=q^0_{01}q^0_{23}q^1_{45},\\
F_{000110}&=q^0_{12}q^1_{34}q^0_{05},\\
F_{000000}&=q^0_{01}q^0_{23}q^0_{45}
            +q^0_{12}q^0_{34}q^0_{05}.               \tag{11}
\end{aligned}

\]

The `23` boundary state exposes shore cofactor \(q^0_{01}\); the `05` state
exposes the independent shore cofactor \(q^0_{12}\).  The first two rows are
coprime monomials, so no positive-degree common shore tail divides the three
rows.  The boundary transfer has rank two.

Thus even agreement of the three words on the entire tight shore does not
keep a common tail: the outside labels select different boundary endpoints.
Tightness controls the **number** of crossing edges in a matching, not the
boundary state.  This counterguard is not a Krenn source point; it refutes
only the proposed automatic reinsertion inference.

## 5. Consequence for the all-order route

The 96 affine-guard permanent triangles can propagate through any chain of
terminal ears or tight cuts satisfying the nonzero rank-one transfer
criterion.  This gives a usable all-order terminal-ear lemma independent of
the local comparison-map route.

What remains is structural, not algebraic: one must show that a terminal ear
of a minimal vanishing fibre is either invisible/rank-one for one of the
available permanent triangles, or produces a different exit (a singleton
fibre, active clean cap, or new local triangle).  The U7H matching-covered
core theorem supplies ears and tight cuts fibrewise, but it does not relate
the three source words' boundary states; the `C6` counterguard shows that this
missing cross-fibre compatibility cannot be omitted.

## Reproduction

```bash
python3 computations/verify_uniform_permanent_triangle_common_tail_reinsertion.py
python3 -O computations/verify_uniform_permanent_triangle_common_tail_reinsertion.py
python3 -I computations/verify_uniform_permanent_triangle_common_tail_reinsertion.py
```

The checker verifies the arbitrary-tail identity, an exact twelve-site
three-term cofactor, all 192 terminal-ear matching decompositions, and the
source-labelled tight-`C6` rank-two counterguard.
