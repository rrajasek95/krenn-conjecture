# All-matching E2/E3 saturation does not remove the chart-operation tag

## 1. Outcome

The universal chart-odd carrier (t), equivalently the tagged Bianchi class
(\widehat\beta), does **not** factor source-validly through the presently
available undivided E2/E3 matching-exchange complex merely by summing all
perfect matchings.

This remains true after granting the strongest plausible matching-side
hypotheses:

1. use every base matching at a normalized pure word;
2. impose the exact pure relation
   
   \[
                         \sum_Mm_M(c)=H_c=1;             \tag{1}
   \]
3. replace the known E2/E3/E4 cells by the entire all-matching Koszul
   resolution; and
4. grant primitive common-core saturation, so no matching factor creates a
   colon obstruction.

Under (1), the matching complex is explicitly contractible.  Nevertheless,
the physical global exchange cells enter the two chart presentations
**diagonally**, while (t) lies in the chart-sign summand.  The diagonal
matching contraction kills every matching-direction class but leaves

\[
 \boxed{
 [t]=[\widehat\beta]\ne0
 \quad\text{in the first relative operation-tag group}.}       \tag{2}
\]

Thus the first obstruction is not another C4 identity and not common-core
Tor.  It is the missing **operation tag**: one source cell must remember
that a fixed global matching occurrence is direct in one pair chart and
two-star in the other.  A global E2/E3 determinant has no such odd tag.

The obstruction relates directly to the shortest moment theorem.  The two
oriented primitives formally satisfy

\[
 d\Gamma^\rightarrow=q-x,
 \qquad
 d\Gamma^\leftarrow=q-r+x.                              \tag{3}
\]

They can be added in one physical module only after their overlap
difference (\widehat\beta) is killed.  If one chart-odd cell (\Lambda)
is constructed with

\[
                         d\Lambda=\widehat\beta,         \tag{4}
\]

the two primitives descend to a common carrier and

\[
 \boxed{
 \Gamma=-(\Gamma^\rightarrow+\Gamma^\leftarrow),
 \qquad d\Gamma=r-2q.}                                  \tag{5}
\]

Then the strict Leibniz construction fills the entire Hilbert--Cauchy
moment tower.  Without (4), equation (5) is only a formal sum of chains in
different restriction complexes.

This note freezes a source-typing obstruction, not a Krenn counterexample.
It does not compute the full decorated source complex and does not prove
that (2) survives after a new relative/Rees, Hasse--Schmidt, or occurrence
cell is included.  It proves that existing global matching-exchange cells,
even after maximal matching saturation, cannot supply that cell.

## 2. The strongest all-matching contraction

Fix a normalized pure word (c^N), and let (\mathcal M) be the set of
physical perfect matchings.  Over the exact-source coefficient ring put

\[
                         a_M=m_M(c^N).                  \tag{6}
\]

The pure GHZ equation is precisely the unimodular-row identity (1).  Let

\[
 E=\bigoplus_{M\in\mathcal M}Re_M
\]

and let (K(a)=(\bigwedge E,\iota_a)) be the Koszul complex with

\[
 \iota_a(e_{M_1}\wedge\cdots\wedge e_{M_p})
 =\sum_{j=1}^p(-1)^{j-1}a_{M_j}
    e_{M_1}\wedge\cdots\widehat e_{M_j}\cdots\wedge e_{M_p}. \tag{7}
\]

Set

\[
                         u=\sum_{M\in\mathcal M}e_M.    \tag{8}
\]

Left exterior multiplication (h(\xi)=u\wedge\xi) satisfies

\[
 \boxed{
 \iota_a h+h\iota_a
   =\left(\sum_Ma_M\right)\operatorname {id}
   =\operatorname {id}.}                               \tag{9}
\]

Therefore the entire matching complex is contractible.  This is stronger
than the presently proved local data:

* its degree-one boundaries grant every matching-monomial contraction;
* its degree-two faces contain all pairwise Koszul/exchange relations;
* its degree-three faces contain the Bianchi coherences; and
* all higher coherences and every common-core saturation are included.

The actual E2/E3 determinants have additional physical response rows and
matching cores.  Replacing them by (7)--(9) is deliberately favourable to
the proposed factorization.  A no-go after this replacement cannot be
repaired by another identity involving only matching labels.

## 3. The operation-tag complex

Let

\[
 V_{\mathrm{op}}=R e_{pq}\oplus R e_{pr},
 \qquad
 e_+=e_{pq}+e_{pr},
 \qquad
 e_-=e_{pq}-e_{pr}.                                    \tag{10}
\]

At row level, both charts present the same global coefficient.  The
full-word theorem gives the common-coefficient map

\[
 e_{pq}\longmapsto1,
 \qquad
 e_{pr}\longmapsto1,                                   \tag{11}
\]

whose kernel is (Re_-).

The undivided matching-exchange cells are global polynomial identities.
They do not have a choice of deleted pair.  When their common global row is
displayed in the two pair charts, it therefore appears as the diagonal
operation tag (e_+).  Even after granting (7)--(9), the physical relative
presentation has the bottom of the complex

\[
 \mathcal C^{\mathrm{op}}_1=K_1(a),
 \qquad
 \mathcal C^{\mathrm{op}}_0=K_0(a)\otimes V_{\mathrm{op}},
 \qquad
 d_{\mathrm{op}}(\xi)=\iota_a(\xi)\otimes e_+.          \tag{12}
\]

The E3 and higher cells map into (\mathcal C^{\mathrm{op}}_1) with the
same diagonal tag.  They prove (d^2=0) and coherence, but do not enlarge
the image in degree zero.

Since (9) gives (\iota_a(K_1)=K_0=R), (12) has

\[
 \operatorname {im}d_{\mathrm{op}}=Re_+,
 \qquad
 H_0(\mathcal C^{\mathrm{op}})=Re_-.                    \tag{13}

The universal tagged comparison is

\[
                         t=1\otimes e_-.                \tag{14}

Equations (13)--(14) prove (2).

We call

\[
 \operatorname {Tor}^{\mathrm{op}}_1
      :=H_0(\mathcal C^{\mathrm{op}})                   \tag{15}

the **first operation-tag Tor group**, using the conventional one-step
relative shift: (\mathcal C^{\mathrm{op}}) is the relative presentation
cone placed with the chart rows in degree zero.  This notation is defined
by (12)--(15); it is not an assertion that (15) is ordinary Tor over the
unlocalized edge-coordinate ring.

The distinction matters.  Ordinary common-core Tor has already been set to
zero by the contraction (9).  The surviving class is caused by the
operation-tag functor which duplicates coefficient presentations without
duplicating the physical exchange cells.

## 4. Why duplicating E2/E3 would assume the answer

One might instead put two independent copies of the entire Koszul complex
in the two charts.  Their difference would contain

\[
                         u\otimes e_-                  \tag{16}
\]

and (9) would give

\[
                         d(u\otimes e_-)=e_-=t.         \tag{17}

This is indeed an explicit factorization of (t).  It is not supplied by
the global E2/E3 complex.  The two copies in (16) must remember which
physical restriction operation was applied before the global identity was
expanded.  Their difference is exactly the chart-odd relative cell being
sought.

Thus (16)--(17) are best read as the minimal positive theorem:

> **Chart-odd all-matching lift.**  Lift the pure-word matching contraction
> (u) separately and source-validly through the (pq) and (pr)
> restriction/insertion operations, preserving word, fine/repeated, target,
> anchor, terminal, physical-(q), and protected rows.  Prove that the
> difference of those lifts is an admitted relative cell.

If this theorem holds, (17) kills (t).  If it does not, the single global
cell has tag (e_+) and leaves (15).  Writing down two formal copies without
their physical operation labels would simply assume the missing descent.

## 5. Relation to the undivided E2/E3 formulas

For two matchings (M,N) and word states (c,d), the exact E2 identity is

\[
 b_cP^M_{cd}-a_cP^N_{cd}=\Delta^{MN}_{cd}H_c.           \tag{18}
\]

At a pure word (H_c=1), it contracts the exchange minor:

\[
                         \Delta^{MN}_{cd}
             =b_cP^M_{cd}-a_cP^N_{cd}.                  \tag{19}
\]

The E3 determinant and E4 tetrahedral relation make these contractions
coherent under changes of word state and matching base.  The exact (N=8)
audit verifies these identities in the full aggregate polynomial ring.

All terms in (18)--(19) are global matching polynomials.  Applying the two
chart partitions after the equality produces the same equality twice, so
its operation tag is (e_+).  The pure target turns the matching minor into
a boundary but does not change this tag.  Summing (19) over every matching
therefore implements the contraction (9) in the diagonal summand and stops
at (13).

The local primitive-colon obstruction is logically separate.  Without the
generous saturation grant, one must also prove that common matching factors
can be removed source-validly.  With the grant, (13) still survives.  Hence
the positive route requires all three independent inputs

\[
 \boxed{
 \text{chart-odd operation lift}
 \quad+\quad
 \text{common-core saturation}
 \quad+\quad
 \text{E2/E3 pure contraction},}                        \tag{20}
\]

and neither of the last two can replace the first.

## 6. Exact obstruction to (d\Gamma=r-2q)

Let (Q^\rightarrow,Q^\leftarrow) be the two oriented restriction
complexes.  The known local equations (3) live separately in them.  A
common physical carrier is descent data consisting of:

1. a common target complex (Q);
2. restriction/insertion comparisons from both oriented complexes to
   (Q); and
3. a relative homotopy on their overlap.

The difference between the two overlap representatives is the chart-sign
class (t=\widehat\beta).  In the mapping-cone convention of (12), a
relative homotopy is precisely (4).  If it exists, modify one overlap
representative by (\Lambda), identify the two carriers, and add (3).  The
exact sign calculation is

\[
\begin{aligned}
 d\bigl[-(\Gamma^\rightarrow+\Gamma^\leftarrow)\bigr]
   &=-(q-x)-(q-r+x)\\
   &=r-2q.                                               \tag{21}
\end{aligned}
\]

Conversely, a source-valid common (\Gamma) obtained by descending these
two oriented cells supplies an overlap comparison, so its descent data
must kill the corresponding class in (15).  Therefore, for this route,

\[
 \boxed{
 d\Gamma=r-2q
 \quad\Longleftrightarrow\quad
 [\widehat\beta]=0
 \text{ in the complete chart-operation relative complex},} \tag{22}
\]

with existence of the two local oriented cells understood.  Equation (22)
is an equivalence of descent obligations, not a claim that every arbitrary
primitive of (r-2q) must arise from those two cells.

Once (21) exists in a decorated (R[q,r])-module, the already proved strict
Leibniz theorem gives

\[
 d(\Gamma H_s)=(r-2q)H_s
 \qquad\text{for all }s\geq0                            \tag{23}
\]

and removes the entire based-loop moment problem.

## 7. What could kill or terminalize the class

The first viable positive columns are now sharply typed.

* **Separate restricted all-matching contractions.**  Construct (16) with
  all physical decorations; its difference gives (17).
* **Relative Hasse--Schmidt cell.**  At (h=3), the exact second polars of
  the mixed full-nine rows have the required degree-lowering chart-odd
  symbol.  They need a physical totalization and zero lower companions.
* **Occurrence-labelled chart switch.**  Retain the matching occurrence
  while changing its direct/two-star operation tag, with all insertion
  faces commuting.
* **Full decorated terminal.**  If the chart-odd class is not a boundary in
  the complete augmented complex, finite duality produces a signed terminal
  detecting it.

An E2, E3, E4, or higher determinant constructed only in the global
aggregate polynomial ring remains diagonal.  Another such cell cannot
change (13).

## 8. Exact scope

The counterguard uses physical facts at its interface:

* every pure matching monomial in (1) is an actual source occurrence;
* the E2/E3/E4 identities are undivided aggregate matching identities; and
* both pair charts are literal partitions of the same full-word row.

The maximal Koszul completion in Section 2 is a favourable algebraic
replacement, not a claim that every Koszul generator is already a physical
source cell.  It is used only to prove that even perfect matching-direction
exactness leaves the operation tag.

No full finite tensor satisfying all GHZ equations is built, and no
physical terminal is exhibited.  A complete source complex could contain
the missing chart-odd cell.  The theorem says exactly what that cell must
do and why it cannot be manufactured by summing existing chart-forgetting
matching exchanges.

## Verification

Run

```text
python3 computations/verify_uniform_chart_odd_matching_exchange_operation_tag_tor_gate.py
python3 -O computations/verify_uniform_chart_odd_matching_exchange_operation_tag_tor_gate.py
python3 -I -S computations/verify_uniform_chart_odd_matching_exchange_operation_tag_tor_gate.py
```

The checker pins the all-word signed-kernel gate, strict common-four-cut
moment theorem, exact local E2/E3/E4 audits, and the (h=3) full-nine
anti-diagonal computation.  It verifies the Koszul contraction (9) in every
exterior degree for matching widths two through seven, the diagonal/sign
rank calculation (13), the unique effect of adding one chart-odd cell, and
the sign in (21).  The exterior-algebra proof is uniform in the number of
matchings; the finite widths audit only its signs.
