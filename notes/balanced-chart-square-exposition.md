> **Expository edition** of
> [`notes/uniform-balanced-chart-square-master-obstruction.md`](uniform-balanced-chart-square-master-obstruction.md)
> (canonical, byte-frozen pin target). Content identical; editorial rendering only.

# The balanced chart square: one obstruction behind three frontiers

**What this note is.** The identification of the single class shared by the
program's three open frontiers — Gate II, the recurrent `C4` bistar core, and
the uniform Bianchi comparison — together with the statement of the one
theorem that would close it.

| claim | status |
|---|---|
| the identification: three frontier obstructions are one four-coordinate class | **[P]** — exact, checker-backed |
| balanced chart-square saturation (either branch) | **[O]** — open |

Context: [PROOF-SKETCH.md §6](../PROOF-SKETCH.md#6-the-remaining-statement)
states the same theorem in the sketch's register; the counterguards excluding
the obvious shortcuts are in
[`notes/h3-balanced-square-pointed-full-q-cone-gate.md`](h3-balanced-square-pointed-full-q-cone-gate.md).

Exact checker:
[`verify_uniform_balanced_chart_square_master_obstruction.py`](../computations/verify_uniform_balanced_chart_square_master_obstruction.py).

Two conventions are used throughout. A *chart* is one of the two endpoint
orderings carried by the doubled channel $A$ of the four-site residual window,
written $A_{[a|b]}$ and $A_{[b|a]}$; the other two channels of that window are
$B$ and $C$ (PROOF-SKETCH §6). A row, column, or cell is *source-valid* when it
is a literal consequence of the source equations with its physical labels
preserved — not merely a homologically admissible chain.

## 1. The identification

The three frontiers are the same four-coordinate character before physical
placement. In the ordered chart basis

$$\bigl(A_{[a|b]},\ A_{[b|a]},\ B,\ C\bigr)$$

put

$$z = (1,\,1,\,-1,\,-1). \qquad (1)$$

Then:

1. identifying the two ordered direct copies sends (1) to the Gate-II
   direction charge

   $$(2,\,-1,\,-1); \qquad (2)$$

2. (1) is the unique left-kernel charge of the balanced $K_{2,2}$ complete-row
   companion incidence from the recurrent common-bistar audit; and

3. (1) factors as

   $$(1,-1)_{\text{chart}} \otimes (1,1)_{\text{matching}}, \qquad (3)$$

   exactly the operation-sign class which survives every diagonal all-matching
   contraction in the uniform Bianchi audit.

Thus the proof does not have three unrelated missing lemmas. It has one
labelled family to construct or terminalize, stated in §4.

**Why the matching machinery cannot reach it.** Equation (3) gives the exact
two-chart interpretation. Global matching determinants and their Koszul
resolution act in the diagonal chart line. They can contract the matching
factor in (3), but not the chart-sign factor. This is why even the fully
contractible all-matching model leaves the tagged Bianchi class.

The coefficient identification is exact. This note does not construct the
physical family.

## 2. The flat square and the mate rows

The four formal primitive mate rows are

$$A_{[a|b]} + B, \qquad A_{[b|a]} + C, \qquad A_{[a|b]} + C, \qquad A_{[b|a]} + B. \qquad (4)$$

They have rank three. The vector (1) annihilates every row in (4), and
adjoining it raises the rank to four. Its normalized primitive dual is

$$\psi_z = \tfrac14 (1,\,1,\,-1,\,-1). \qquad (5)$$

This is precisely the coefficient $K_{2,2}$ shadow in the Gate-II joint-cobar
audit. The switch–Weyl product now constructs the required top decoration, so
(1) occurs literally in the remaining eighteen `Hasse[2](DQ/PS)` direction
faces rather than as a guessed representation.

### The exact complete-row projection criterion

For the smallest recurrent common-core component, write the four complete
rows (6):

```math
\begin{aligned}
 F_{A0} &= C + z_{00} + z_{01}, &
 F_{A1} &= C + z_{10} + z_{11},\\
 F_{B0} &= C + z_{00} + z_{10}, &
 F_{B1} &= C + z_{01} + z_{11}.
\end{aligned}
```

The companion incidence in (6) has rank three and left kernel (1). Since the
core coefficient row is $(1,1,1,1)$, its pairing with (1) is zero. There is
therefore no source-valid projection onto $C$. This failure is not merely
formal: the exact point

$$C = 1, \qquad z_{ij} = -\tfrac12 \qquad (7)$$

kills all four rows. If the second core coefficient is changed from one to
two, the pairing becomes one and the same kernel charge projects $C$ exactly.
Hence the correct projection ideal is the transported charge pairing, and the
sharp survivor is specifically the centered balanced component.

This supersedes an unconditional recurrent-core projection theorem. The
companion terms need not force an odd unit, deletion, or outside fan: (7) is an
internal, tail-saturated flat component.

## 3. The gauge to the augmentation class

Multiplying by the shore sign $\mathrm{diag}(1,1,-1,-1)$ turns the four
signless columns of the square into ordinary oriented incidence columns and
carries (1) to the constant vector $(1,1,1,1)$; since the oriented incidence
image is exactly the kernel of the vertex augmentation, the local problem
becomes the exhibition of one source-valid column of nonzero augmentation.
That reformulation, and the exact counterguards showing which columns do *not*
supply it, are the subject of the companion note
[`h3-balanced-square-pointed-full-q-cone-gate.md`](h3-balanced-square-pointed-full-q-cone-gate.md).

## 4. The open theorem

> **Balanced chart-square saturation theorem (open).** In every physical
> fixed-tail/fixed-window occurrence of (1), construct a source-valid
> relative cell whose boundary is the balanced charge tensored with the
> local `C4` tail, natural in restriction, reinsertion and chart overlap; or
> extend the normalized charge dual to the complete augmented physical
> terminal.

The two branches are the filler branch and the terminal branch, and either one
closes the program's remaining gap.

**What a filler buys.** A physical relative cell $d\Lambda = z$ has all three
desired consequences:

1. after ordered-direct projection it closes the Gate-II charge (2) and its
   eighteen same-grade relative-`C4` direction faces;
2. on a recurrent fixed bistar it kills the balanced complete-row projection
   obstruction; and
3. on overlapping pair charts it kills the Bianchi operation-sign class,
   allowing the two oriented four-cut primitives to descend to one carrier
   with

   $$d\Gamma = r - 2q. \qquad (8)$$

The strict all-moment construction is downstream of (8).

### Physical scope

The three occurrences of (1) currently live in different literal packets:

* Gate II uses one fixed residual window, the `DQ/PS` direction-pair
  idempotents, and the selected fan word/fine grade;
* the recurrent-core theorem produces fixed windows only after its boundary
  routing, with arbitrary companion complete rows; and
* the uniform Bianchi class is indexed by overlapping pair charts at every
  order.

Their character equality does not authorize a raw fold between these objects.
The positive theorem must be a natural family retaining the tail, window,
operation tag, repeated/Hasse grade, target, Eq, ordinary residue, physical
$q$, anchor, $W$, and shifted ridge. The negative theorem must extend (5) over
that same complete map. The committed augmented dual audit already fixes its
target/$W$/ordinary-residue correction and shows that the next untested faces
are exactly the selected `U_C4`, `db01`, eighteen direction terms, and the
downstream `0102` carrier.

### Shortest next attack

Work on (1) directly in the four-site relative chart square:

1. retain the presentation-safe switch coordinates rather than imposing
   equality of the old chart occurrences;
2. build one mixed-operation mapping cylinder for the two edges
   `DQ <-> P0S1` and `DQ <-> P1S0` on a fixed `C4` window;
3. totalize its first principal-parts boundary with the existing signed-Weyl
   and relative response cells; and
4. run the exhaustive augmented rank test. Failure now has the unique dual
   (5), so it must either extend to the terminal or expose the first genuinely
   new physical column.

No further coefficient projector, global matching determinant, or
tag-preserving root bar can affect (1).

## 5. Verification

Run

```text
python3 computations/verify_uniform_balanced_chart_square_master_obstruction.py
python3 -O computations/verify_uniform_balanced_chart_square_master_obstruction.py
python3 -I -S computations/verify_uniform_balanced_chart_square_master_obstruction.py
```

The checker pins the four contributing audits, verifies the exact ranks, the
Gate-II projection, the operation-character factorization, the complete-row
projection criterion, the counterpoint (7), and the normalized dual.
