# Retaining the centered carrier reduces landing to one physical `W` equation

## Result

The relative occurrence graph can be extended one step farther without
changing the old physical fibre, but this does **not** construct the desired
promoted E14 comparison.

For the exact `P2` carrier combination write

\[
                         t=t_{z_{\rm priv}},           \tag{1}
\]

and let `w_E14` be the canonical twelve-tail target in the word-`000101`
unary/`G11` first-hit block.  Adjoin a slack carrier `r` and a degree-one
generator `psi` with

\[
                       d\psi=r-w_{E14}+t.              \tag{2}
\]

Equation (2) is monic in the new variable `r`, so with `r` retained it is a
presentation-safe mapping cylinder.  Its augmentation is

\[
                           r=w_{E14}-t.                \tag{3}
\]

Setting `r=0`, however, imposes

\[
                           w_{E14}=t,                  \tag{4}
\]

and lowers degree-zero homology by one.  Thus (2) carries the failure of
landing; (4) is exactly the missing physical `W` theorem.

Checker:
[`verify_h3_relative_occurrence_e14_w_carrier_landing_gate.py`](../computations/verify_h3_relative_occurrence_e14_w_carrier_landing_gate.py).

## 1. The first-hit obstruction is already exact

The selected E14 first-hit presentation contains 269 complete unary/`G11`
columns of exact rank 269.  Its canonical target `w_E14` has twelve terms and
is not in their span.  The pinned rational covector has support 22, kills all
269 columns and reads `-1` on `w_E14`; its primitive integral normalization
reads `-30`.

Take the direct sum with the relative occurrence graph.  The latter has rank
24 and belongs to the source word `01211222`, while the E14 target is based at
word `000101`.  Extending the first-hit covector by zero on the graph block
kills the old direct-sum image and still reads

\[
                       \lambda(w_{E14}-t)=-1.          \tag{5}
\]

Consequently the desired comparison raises the direct-sum rank

```text
24 + 269 = 293  ->  294.
```

This also states the exact limitation of the decorated-core match.  The
rootless term maps to the E14 factor

```text
u05_01*v34_10
```

and, after multiplying by `p1_0_1*s1_1_1*v24_11`, selects one monomial of the
canonical twelve-tail target.  The full physical object is the entire
unary/`G11` remainder.  A shared `2K2` monomial does not define a chain map
between the two source presentations.

## 2. Why the slack carrier is the sharp relative construction

Modulo the two old blocks, use coordinates `(t,w,r)`.  Equation (2) is the
single column

\[
                              (1,-1,1).                \tag{6}
\]

It has rank one in three coordinates and therefore leaves degree-zero rank
two, exactly the old independent `(t,w)` fibre.  Adding `r=0` gives the two
independent columns

\[
                           (1,-1,1),\quad(0,0,1),      \tag{7}
\]

and lowers degree-zero rank from two to one.  In other words, every
presentation-safe attempt may retain the comparison defect under another
name, but erasing it imposes (4).

This is the same phenomenon as the previous relative graph:

```text
z-u and t-Cz          presentation-safe, because z and t are retained;
t=0                   changes the physical fibre;
r-(w-t)               presentation-safe, because r is retained;
r=0                   changes the physical fibre by the W equation.
```

The constructive problem has therefore been reduced, not evaded.

## 3. The old physical `Yw -> W` cap is necessary but not this landing

The existing literal cap chain `r0-T` proves the physical output law

\[
                              Yw=W                    \tag{8}
\]

coefficientwise.  On the five normalized `C5` columns its physical-`W`
projection has rank one.  By contrast, the endpoint-even part of the retained
occurrence carrier has rank five.

More importantly, the cap theorem records no principal boundary in the E14
word-`000101` unary/`G11` block.  It supplies the load-bearing physical-`W`
**readout** once a same-grade comparison has been built; it does not supply a
column with boundary

\[
       \text{promoted E14 occurrence}-\text{marked `01211222` carrier}.
                                                               \tag{9}
\]

Thus these two appearances of `W` must not be conflated:

- `w_E14-t` is the occurrencewise endpoint-word-changing source comparison;
- `Yw=W` is the physical cap output row which that comparison must preserve.

## 4. The exact terminal alternative

Let `J_full` be the complete augmented source map in the selected
word/fine/repeated grade, including all later endpoint-word-change, `q`,
target, labelled-residue, anchor, physical-`W`, eta and sigma columns.  Let
`b_W` denote (9) together with every forced proper face.  Finite-dimensional
duality gives the exhaustive alternative

\[
\begin{array}{ll}
 b_W\in\operatorname {im}J_{full}
    &\Longrightarrow\text{the physical promoted-occurrence landing exists},\\
 b_W\notin\operatorname {im}J_{full}
    &\Longrightarrow\exists\Lambda:\Lambda J_{full}=0,
                      \quad\Lambda b_W\ne0.
\end{array}                                                   \tag{10}
\]

The current 22-support first-hit covector is the exact first seed for the
second arm.  It is **not** yet a physical terminal: it has only been checked
against the truncated 269-column unary/`G11` presentation.  The remaining
terminal theorem is to extend it over the full augmented map and identify a
survivor with an accepted exchange, relative generator or Fredholm separator.

## Shortest remaining active/centered chain

No further occurrence census is required.  The shortest theorem chain is:

1. the relative graph and its labelled two-root cobar are constructed;
2. construct the complete augmented landing `b_W` of (10), or promote its
   first full-map nonlift to a terminal;
3. include in the same totalization the primitive cap face `p`, the physical
   `K_Eq`/`B4,B1` label transport, and the shifted Kähler ridge;
4. then `dq` follows by the principal-parts product rule, `d_even` by the
   pinned cap/label formula, physical `W` by (8), anchor by conormal
   functoriality, and eta/sigma by the unique ridge contractions.

The highest-leverage next attack is step 2 at the **full augmented** level:
start with the explicit 22-support E14 covector and solve its extension
equations through the endpoint-word-change and `q` columns.  Either the first
new column kills it and gives the missing comparison coefficient, or the
extended covector reaches a named physical terminal.  More coefficient-only
projectors cannot decide this fork.

## Scope

This is exact for the twelve-occurrence relative graph and the selected
canonical E14 first-hit block.  It proves a rank-one source-presentation
obstruction and a presentation-safe relative cylinder.  It does not prove a
full-source counterexample, an occurrencewise E14 orbit map, or a physical
terminal.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
033c69f35205783459fcd1990c5e89b4f5b1c05b051ec24fffdca8917166e584
```
