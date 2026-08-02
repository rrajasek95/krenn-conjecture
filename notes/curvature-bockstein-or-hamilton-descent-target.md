# Curvature Bockstein or Hamilton descent

Research target only.  This note does not prove Krenn's conjecture and does
not change the certified dependency graph.

## 1. The reversal suggested by the exact cells

The primitive alternating-\(C_4\) colon classes in chart 26 need not be
eliminated in order to prove the conjecture.  There are two logically useful
outcomes of a source-labelled path-forest straightening step:

1. the collision class is null-homotopic after physical label identification,
   so the straightening continues to a component-joining forest term; or
2. the class survives diagonal specialization, in which case its connecting
   homomorphism can be paired with the three pure anchors.

The second outcome is potentially an obstruction rather than a failure of the
method.  Chart 25 is the finite exact model: its four-row functional annihilates
every incident mixed-source column but has source-provenant Schur target
pairing \(1\).  (The older value \(3\) was a lower-raw plus leading-reduced
hybrid which counted the certificate tail twice.)  After its
common factor is removed, the support consists of three decorations of one
alternating \(C_4\) and the parallel-pair degeneration, with coefficient vector

\[
                             (-2,-1,-1,+1).                 \tag{1}
\]

The first three rows are the genuine matching-exchange circuit.  The last row
is precisely the diagonal collision missing from the ordinary three-row
determinant.  Thus (1) should be read as a local source-relative Bockstein
cochain, not merely as an awkward non-squarefree leading term.

## 2. Candidate local complex

Let \(\widetilde R\) be the ring in which every occurrence of a decorated edge
has its own source-slot label, and let \(L\) be the sequence of differences
which identify labelled copies of the same physical coordinate.  Let
\(\widetilde C_{\mathrm{pf}}\) denote the proposed polarized path-forest
complex.  Its fixed-matching pieces have the already proved Koszul simplices;
alternating-cycle determinants give the base-exchange faces before primitive
division.

The physical total complex is

\[
 {\cal D}=\operatorname {Tot}
       \bigl(\widetilde C_{\mathrm{pf}}\otimes K(L)\bigr).  \tag{2}
\]

For a collision face \(\xi\), the first nonzero label-diagonal differential
defines a connecting class

\[
               \beta_L[\xi]\in H({\cal D}).               \tag{3}
\]

The ordinary Bianchi identities only say that the two-dimensional faces of
(2) close.  They do not force (3) to vanish.  The elementary ideal
\((xy,xz)\) shows that all pairwise diagonal tests can pass while higher Tor
survives.  Consequently the desired construction must use the full Koszul
cube of label identifications, or an equivalent filtered contraction with
proved zero indeterminacy.

## 3. Curvature--Bockstein dichotomy

The useful theorem is weaker than global derived transversality and stronger
than a squarefree degeneration.

> **Target theorem.**  On the synchronized full-nine two-chart packet, every
> primitive critical forest face admits one of the following source-faithful
> resolutions.
>
> 1. **Forest continuation.**  Its class in (2) is a boundary, with a chosen
>    contraction whose leading term is a legal endpoint join and whose lift
>    indeterminacy is zero in the augmented target complex.
> 2. **Curvature obstruction.**  Its first nonzero connecting class has a
>    canonical local representative supported on three alternating-cycle
>    decorations and one parallel-pair degeneration.  Pairing this
>    representative with the pure augmentation equals
>    \(\kappa\) times the appropriate nonzero adjacent-power residue, where
>    \(\kappa\) is the selected physical curvature minor.
> 3. **Geometric split.**  A repeated physical coordinate gives the exact
>    closed/open decomposition \(x=0\) or \(x\ne0\); on both branches a
>    lexicographic defect statistic strictly decreases.

At an exact ternary source the mixed augmentation kills every source boundary.
The synchronized selection gives \(\kappa\ne0\), and activity plus the three
pure anchors must make the residue in alternative 2 nonzero.  Thus alternative
2 is a contradiction.  Alternative 3 terminates by the branch statistic.
Only alternative 1 can persist.

Repeated forest continuation decreases the number of even path components.
It therefore terminates at an alternating Hamilton path.  The two unmatched
endpoints of its join matching are the candidate clean pair.  The terminal
part of the theorem must identify its augmented coefficient with the physical
clean-cap readout and prove activity and zero lift indeterminacy.  The existing
exact clean-pair theorem then descends from \(N\) to \(N-2\).

The [exact terminal chart-26 audit](n8-chart26-terminal-hamilton-readout.md)
shows that none of these three words can be omitted.  The normalized physical
target has 5,596 degree-seven Hamilton rows with unique pure-matching
provenance, 5,388 of which have a support-unit direct endpoint edge.  However,
the 300 path terms in the first mixed-source degree-six cell have 10,173 legal
normalized terminal extensions and none belongs to the physical target.
Moreover, one physical target Hamilton row has an explicit active cap with
zero error on its coordinate face, but adding a single off-path spoke leaves
the terminal monomial and activity unchanged while making four cap-error
coefficients equal to two.  Thus the terminal map must be an augmented
source-chain map with a specified lift; equality of uncoloured Hamilton
skeletons does not define it.

### Exact full-class model for alternative 3

The two coarse signatures selected by the no-simple-path representatives in
the weighted chart-26 census now satisfy a refined form of alternative 3 for
every labelled pair; see
[the full branch-class audit](n8-chart26-branch-class-uniformity.md).  They are
not uniformly collision cells:

\[
\begin{array}{c|r|r}
 &\text{squarefree continuation}&\text{collision split}\\\hline
4\text{--}5&2{,}986&5{,}426\\
5\text{--}5&29{,}212&16{,}564.
\end{array}
\]

Every one of the 21,990 collision cells has exactly one repeated decorated
coordinate \(x\), but \(x\) ranges through eight coordinate fibres in the
4--5 class and twenty-nine in the 5--5 class.  On \(x=0\), the source
expression leaves exactly two restricted lower columns in type 4--5 and one
in type 5--5, reconstructing the closed cell term by term.  On \(x\ne0\),
division by \(x^2\) changes the repeated pivot into a squarefree Laurent pivot
of skeleton `P3+P2+P2+P1`.  No term of any \(xG\) gains a lower degree-four or
degree-five divisor.

None of the 32,198 squarefree leads is a simple even path forest: 25,908 are
branched, and 6,290 are decorated-squarefree but retain a physical parallel
edge.  They define a separate squarefree non-path straightening frontier, not
an already solved Hamilton continuation.

The old representatives at \(x=x_{02}^{00}\) remain the smallest explicit
instances: the 8,412-class representative reduces through the restricted
\(H_1,H_{730}\) rows, while the 45,776-class representative reduces through
\(R_{730,1459}\); their open pivots are 034bc6f4 and 044ec6f4.

The resulting local defect is

\[
 (\#\text{ undecided decorated coordinates},
   \text{ repeated excess after removing invertible coordinates}). \tag{4a}
\]

Both children decide \(x\), and the open child additionally drops the pivot
excess from one to zero.  This is well-founded if a decided coordinate is
never selected again.  The exact audit now proves the local descent uniformly
on the collision stratum of both coarse signatures.  What remains in the
target theorem is compatibility with future cells, the squarefree
non-path straightening, and the augmented physical-target readout.

## 4. Concrete construction by homological perturbation

There is a standard mechanism which can produce the required secondary map
without choosing reductions anew in every cell.  First construct an explicit
contraction

\[
  (\widetilde C_{\mathrm{pf}},d_0)
  \mathrel{\mathop{\rightleftarrows}^{p}_{i}} H,
  \qquad d_0h+hd_0=1-ip,                                  \tag{4}
\]

where \(d_0\) is the direct sum of the fixed-base Boolean/Koszul forest
differentials.  Put every base exchange and label-identification operation in
a filtration-raising perturbation \(\delta\).  The induced differential on
\(H\) is the finite homological-perturbation series

\[
 d_H=p\delta i-p\delta h\delta i
       +p\delta h\delta h\delta i-\cdots .                \tag{5}
\]

The series is finite on each forest because a legal branch has at most
\(h-1\) joins.  Its first term is the ordinary alternating-cycle exchange.
The first possible confluent correction is the second term
\(-p\delta h\delta i\): two distinct labelled exchanges can be identified at
one physical coordinate, producing the parallel-pair degeneration which a
single determinant cannot contain.  Formula (1) is therefore an exact test
for this transferred second differential.

A source-labelled contraction (4) would solve two problems at once.  The
perturbation lemma makes \(d_H^2=0\) automatically, supplying all higher
coherences, and the specified homotopy \(h\) removes the lift ambiguity which
currently prevents the adjacent-power/Bockstein comparison.  The genuinely
new statement is not the abstract perturbation lemma; it is the equivariant
contraction (4), compatible simultaneously with matching-base flips, the
three pure anchors, and physical label identification.  If a denominator
needed by (4) vanishes, that failure should be routed to the geometric split
in alternative 3 rather than silently localized away.

## 5. Why this may be shorter than a complete Groebner theorem

A global squarefree Groebner degeneration would require simultaneous
orientation and reduction of every source-labelled critical pair.  It would
also prove much more radicality than the conjecture needs.  The dichotomy
above only needs:

* one local confluent \(C_4\) connecting formula, including its parallel-pair
  term;
* a proof that its target pairing is the curvature-weighted adjacent-power
  residue with no choice-of-lift ambiguity;
* a decreasing measure for the collision splits; and
* the terminal Hamilton-path target readout.

The degree-six census has already compressed 2,925,805 critical pairs to the
two mechanisms which these clauses address: base-exchange curvature and the
refined squarefree/collision routing inside the two fully audited branch
signatures.  A proof of the four clauses would avoid completing the entire
normalized ideal.

## 6. Exact tests for the proposed theorem

Any candidate construction must reproduce all of the following without
changing source labels.

1. Before primitive division, the alternating-\(C_4\) three-row determinant
   and its tetrahedral row syzygies.
2. After primitive division, the two nonzero chart-26 degree-six colon
   classes rather than falsely reducing them.
3. On the chart-25 circuit, the exact cochain (1), annihilation of all 56
   actual incident columns, and Schur target pairing \(1\).
4. On the off-diagonal clean boundary, the required grade transport from the
   admitted adjacent-power source relation to the reciprocal clean
   coefficient, retaining the physical target.
5. Independence of every chosen primitive lift modulo the complete anchored
   relative kernel.
6. On the terminal chart-26 row `04237475b8cfea`, the clean coordinate-face
   cap and the one-spoke nonclean lift, together with a chain-level reason the
   latter ambiguity is zero at an exact ternary source.  It must also explain
   how a mixed terminal forest reaches a physical target row despite the zero
   intersection for all 10,173 first-cell terminal extensions.

The third and fourth tests are the same proposed secondary operation in two
different coordinates.  Establishing that identification would connect the
new path-forest computation directly to Components III--IV of the unified
two-chart overlap--jet saturation target.

## 7. Exact local consistency test and first-jet no-go

The chart-25 circuit admits a more precise matching factorization.  On the
ordered residual vertices `(1,3,5,6)`, put

\[
        A=(13)(56),\qquad B=(15)(36),
\]

and let $u=1111$, $v=2222$, $s=1212$, $t=2121$.  The four residual
rows are exactly

\[
\begin{array}{c|c|c}
\text{row}&\text{matching factorization}&\text{quotient value}\\ \hline
4c62bce5&A_uB_v&-2\\
4d62b8e6&A_sB_t&-1\\
4f5ebce8&A_tB_s&-1\\
5e62b8bc&B_uB_v&+1.
\end{array}                                                   \tag{6}
\]

The coefficient $-2$ is an invariant-quotient multiplicity, not a special
local HPL coefficient.  The four row-orbit sizes are $(8,4,4,4)$, so the
weights on the actual rows in these four orbits are

\[
                       (-1/4,-1/4,-1/4,+1/4).              \tag{7}
\]

This does **not** make $(-1,-1,-1,+1)$ a literal source-labelled local
packet.  On the fixed common-factor fibre the size-eight orbit of the first
row contributes a second actual row

\[
                        A_vB_u=505eb8e9                  \tag{7a}
\]

with weight $-1/4$.  The literal fibre therefore has four degree-two
$AB$ rows, all of weight $-1/4$, and one degree-four $B^2$ row of weight
$+1/4$.  The earlier four-entry sign packet exists only after invariant
quotienting.  This distinction is decisive for a source-labelled HPL; see
Section 8.

There is also an exact no-go theorem for replacing the second transfer by a
single confluent determinant.  If one matching row approaches the other as

\[
                         A_i(\epsilon)=B_i+\epsilon U_i,
\]

then

\[
 \epsilon^{-1}
 \det\!\begin{pmatrix}A_i(\epsilon)&A_j(\epsilon)\\B_i&B_j\end{pmatrix}
       =U_iB_j-U_jB_i.                                    \tag{8}
\]

Its projection to the $B_iB_j$ sector is identically zero.  Consequently
no first derivative of one alternating matching-exchange minor can produce
the parallel-pair row in (6).  A second transferred operation (or another
genuinely symmetric operation) is necessary.

The quotient-level HPL sign pattern is algebraically realizable in a formal
toy contraction.  Adjoin one acyclic pair $d_0u=v$, let $h(v)=u$, and
write $a,b,c,d$ for the four circuit rows.  Define

\[
       \delta x=-a-b-c+v,\qquad \delta u=-d,
       \qquad \delta v=\delta a=\delta b=\delta c=\delta d=0.
                                                               \tag{9}
\]

Projection kills $u,v$.  The transferred differential is then exactly

\[
 p\delta i(x)=-a-b-c,qquad
 -p\delta h\delta i(x)=+d,                                  \tag{10}
\]

and every higher term vanishes.  This proves only formal consistency after
the source orbit has already been collapsed.  It does **not** construct the
required $u,v,h$ inside the source-labelled hafnian complex, and the exact
actual-row audit below proves that this particular four-row toy cannot be
lifted there with zero indeterminacy.

The direct chart-26 test is negative in the useful sense.  Insert the same
four-term packet in the frozen exchange

\[
 M=(02)(13)(45)(67),\qquad N=(02)(13)(47)(56).
\]

After dividing the full common core `09094848` and normalizing the support
coordinates, its rows are

```text
- cae0f7  - cbe0e5fa  - cddcf8  + dce0e5.
```

Its weighted lead `cbe0e5fa` is irreducible by the complete degree-four
source layer.  Across all six ordered colour pairs and all four chart
support stabilizers, the 24 packets have 15 distinct leads, and none divides
either path-bearing colon lead

```text
0951acc6f4f4    0952acc6f4f4.
```

Replaying the complete degree-four/degree-five colon audit still gives both
nonzero normal forms.  Hence the confluent packet is not a missing ordinary
lower Groebner reducer.  The consistent interpretation is instead that the
second HPL term must be a source-labelled connecting operation: it may
*account for* the colon class or send it to the target obstruction, but it
cannot simply be adjoined as a new output polynomial.

Run

```text
python3 computations/verify_n8_confluent_c4_hpl_model.py
```

with ledger digest
`e637b076a0b447ecf68558cdda85fdbfbb7dac9a836bcbb3eab74ed46cbcfe4f`.
The 24-packet test is deliberately bounded to the frozen exchange and its
colour/support-stabilizer orbit; it is not a classification of every
source-labelled $C_4$ embedding.

## 8. Literal source HPL no-go and the missing relative cell

The complete individual-row audit changes the local picture.  Over the
common factor in (6), write

\[
 (A_1,A_2,A_3,A_4,D)
 =(A_uB_v,A_sB_t,A_tB_s,A_vB_u,B_uB_v).                  \tag{11}
\]

All 56 actual source columns incident to the 20-row lifted dual hit exactly
one negative $AB$ row and one positive $B^2$ row.  Their incidence graph is
four disjoint stars.  The star over the displayed $D$ has the four leaves
in (11), with source multiplicities $(3,4,4,3)$.  Hence every actual source
boundary obeys the coefficient equation

\[
                         [D]=\sum_{j=1}^4[A_j].           \tag{12}
\]

The naive quotient packet $-A_1-A_2-A_3+D$ violates (12) by four and pairs
with the actual dual by $1$.  Any source lift is forced to add $+4A_4$;
that hidden row contributes $-1$ to the corrected augmentation.

There is a literal acyclic pair on the five-row support quotient.  Choose
one of the three labelled columns over $A_4+D$, put $d_0u=A_4$ and
$h(A_4)=u$, and retain a different labelled column over the same edge in
$x$.  Requiring

\[
                         p\delta i(x)=-A_1-A_2-A_3       \tag{13}
\]

forces coefficient $+3$ on that second $A_4+D$ column, so the augmented-HPL
convention gives

\[
                       -p\delta h\delta i(x)=-3D,        \tag{14}
\]

not $+D$.  Equation (14) is exactly what (12) requires and its corrected
augmentation is zero.  The desired toy coefficient differs by the projected
incidence vector

\[
                                  4D.                    \tag{15}
\]

No combination of the known mixed-hafnian source columns can produce (15),
because each satisfies (12); its pairing with the source-annihilating dual
is nonzero.  The
[exact relative-cell audit](n8-chart25-relative-4d-obstruction.md) now closes
two further obvious possibilities.  Tensoring the frozen source complex
with an ordinary label-diagonal Koszul complex leaves the specialized
degree-zero boundary image unchanged: every positive-exterior boundary is
multiplied by a label difference and vanishes on the physical diagonal.
Reynolds averaging sends $4D$ to the coefficient-one sum of the four rows in
the $D$-orbit, whose invariant-quotient pairing is still one.  Thus neither
ordinary diagonal Koszul cells nor orbit transfer supplies (15).

There is a formal target mapping-cylinder cell.  If $\tau$ denotes the
target generator and $sD$ the shifted actual row, then

\[
                         d(4sD)=4D-\tau.                \tag{16}
\]

The audit constructs the full shifted cylinder on the 14 actual source
labels over this centre, checks all degree-two source coherences and
$d^2=0$ on their 1,145 output rows, and extends the augmentation by
$a(\tau)=1$.  But (16) only records $q\sim\tau$: it is obstruction
bookkeeping available for every augmented complex, not a hafnian source
correction.  A successful confluent construction must derive its target
component through a genuinely mixed source--diagonal transgression (for
example a non-flat coupled module or principal-parts/$A_\infty$ comparison),
not adjoin (16) by definition.  It also cannot obtain (15) from another raw
hafnian source column or from a zero-boundary source syzygy.

The three possible labelled choices for $h(A_4)$ have full boundary
differences supported on 180, 180, and 204 rows away from the local dual
support.  Thus even the valid $-3D$ contraction needs a specified global
lift; local monomial coefficients do not remove the chain-level choice.
The exact checker and the full incidence statement are in
[the literal HPL no-go note](n8-literal-hafnian-hpl-local-no-go.md).

## 9. The literal \(h=3\) polar fails the dual Schur lift

The chart-25 class itself is now exactly a lifted Schur cochain:
\[
 (-\mu,\lambda)=(-2,-1,-1\mid1),\qquad
 \lambda T=\mu A,\qquad
 \lambda c-\mu b=1.
\]
On its five-row fibre, solving the three displayed lower rows produces
exactly \(4D\), with normalized pairing one.  Thus the local obstruction has
the right scalar normalization for the curvature branch.

The first literal \(h=3\) full-nine realization does not yet inherit that
property.  Retain the ten individually labelled marked rows
\[
 r_v^{pq},r_v^{pr},\qquad v=1,\ldots,5.
\]
Their 90-term physical boundaries agree chart by chart, so the five
differences \(k_v=r_v^{pq}-r_v^{pr}\) form the complete lower kernel.  Their
marked Rees tails are \(h_v\) in the \(pq\)-direct and
\(pr\)-two-star sector copies.  The normalized antisymmetric polar cochains
\(\Lambda_v\) obey \(\Lambda_vB'=0\), but the exact connecting matrix is
\[
                   (\Lambda_vT')(k_w)=\delta_{vw}.       \tag{17}
\]
Therefore no \(M_v\) satisfies \(\Lambda_vT'=M_vA'\): all five bare polar
classes have nonzero connecting image.  Multiplying by the active
curvature/cap scalar gives \(\kappa YI_5\), which remains invertible on the
active open.  The target-side factorization
\[
 \lambda_{25}(4D)\cdot(-F,A)\binom BU\cdot Y
       =1\cdot\kappa\cdot Y
\]
is exact, but it is not yet a legal Schur pairing because the source lift
does not exist.

This identifies the next correction more rigidly: the
denominator-marked two-edge comparison cell must contribute \(-I_5\) on
the five lower-kernel vectors before any curvature/adjacent-power target
value is read.  A mapping-cylinder target cell cannot cancel (17).  The
complete source-labelled audit is in
[the literal full-nine Schur no-go](h3-literal-full-nine-schur-polar-no-go.md).
