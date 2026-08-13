# A fan coloop has finite Hall saturation, but still needs a physical lift

## Result

After `1ec750e`, every determinant-bright zero `001122` row supplies a
source-provenant active private-site fan.  Complete pure target supports
make that fan four-good unless one of its two physical edges is a literal
pure-colour coloop.

There are two different assertions after that point.

1. A coloop already placed in the exact endpoint/common-`q` target-coloop
   normal form is consumed by the committed `h=3` chain.  The old `C6/C8`
   labels and the sixteen punctured-C4 returns are not current residuals.
2. An arbitrary coloop edge in a private-site fan has not yet been placed in
   that normal form.  Its finite Hall shadow can be saturated without any
   possibility of cycling, but promoting the saturated shadow to complete
   physical source rows is still the missing theorem.

The second point is the exact normalization boundary.  It should not be
described as another `C6/C8` census or as an unsolved termination problem.

Checker:
[`verify_h3_active_fan_coloop_saturation_boundary.py`](../computations/verify_h3_active_fan_coloop_saturation_boundary.py).

## 1. The normalized target-coloop packet is already closed

Suppose first that the physical source typing required by the old
target-coloop route is present: a literal pure target matching through the
coloop, a compatible nonzero outside matching or exchange carrier, the
common residual `q` tail, the prescribed endpoint orientation, and the
complete unary/four-response rows.

The committed chain is then exhaustive.

* The four-distinct-hole `E2` exchange has nine tail pairs, with full-cycle
  histogram

  ```text
  C6       1
  C8       6
  C4+C4    2.
  ```

* The shared-edge hybrid row treats all 110 remaining normalized label
  packets.
* The later two-companion, diagonal-return, zero-face, and rainbow steps
  specialize the affine returns.  The punctured-C4 identity `5a01b0a`
  finally forces an alternate pure-one target matching or an offanchor
  offdiagonal exit.
* The conjugate double-coloop theorem closes its 270 packets by reselection
  or a distinct-head four-good wedge.

This corrects a possible misreading of `0556512`.  That intermediate note
landed a one-shared branch on the global multisite affine/Hall interface,
but the later normalized target-coloop chain supplies the missing companion
rows and consumes that exact packet.  There is no surviving normalized
`C6/C8` theorem or target-coloop label census.

## 2. Saturate the Hall shadow once

Now assume only that complete source rows have produced two nonempty
families `A,B` of **effective unordered endpoint holes**.  If no pair of
holes is disjoint, every edge of `A` meets every edge of `B`.  On the
fifteen physical edges of `K6`, define

\[
 T(A)=\{e:e\text{ meets every edge of }A\},\qquad
 \operatorname {cl}(A)=T(T(A)).                       \tag{1}
\]

This is a Galois closure:

\[
 A\subseteq\operatorname {cl}(A),\qquad
 \operatorname {cl}^{2}(A)=\operatorname {cl}(A),
 \qquad T(\operatorname {cl}(A))=T(A).                \tag{2}
\]

Thus one should take every source-certified exchange reachable from the
coloop at once and replace its hole family by `cl(A)`.  If a later complete
row produces an edge outside this closure, closing again strictly increases
the closed set.  The integer

\[
                         15-|\operatorname {cl}(A)|    \tag{3}
\]

strictly decreases.  A Hall/reselection cycle is therefore impossible.
Moves inside an unchanged closed set are not claimed to decrease support;
they are intentionally absorbed before duality is applied.

The exact six-site census is small:

```text
5,141 nonempty hole families have a nonempty cross-intersector;
  446 closed ordered Galois concepts;
    6 orbit types modulo S6 and exchange of the two shores.
```

Representatives for the six closed types are

| `A` | `T(A)` |
|---|---|
| triangle `01,02,12` | the same triangle |
| matching `03,12` | rectangle `01,02,13,23` |
| path `01,03,12` | path `01,02,13` |
| adjacent pair `01,02` | `01,02,03,04,05,12` |
| singleton `01` | all nine edges meeting `01` |
| full star at `0` | the same full star |

The familiar star, triangle, and strict `K2,2` descriptions are shadows of
this closed list.  Existing complete-row theorems already close the
co-located Hall-star lock.  Before arbitrary coloop normalization, the
sharp lower interfaces are the outer-centre anchor triangle and the
anchor-contained injective `M3` five-lock with no complementary wedge.

## 3. The exact missing complete-row lift

The combinatorial saturation begins only after an effective physical hole
has been produced.  An arbitrary fan coloop gives instead

\[
                         \Delta_{ef}C_f\ne0,            \tag{4}
\]

together with the statement that every nonzero pure-`c` matching contains
one fan edge.  The determinant factor in (4), its cofactor tail, and the
pure target coloop do not automatically form the endpoint/common-`q`
matching packet assumed by the normalized target-coloop theorems.

The remaining statement is therefore:

> **Active-fan coloop tight-set lift.**  From (4) and a literal
> pure-colour coloop, the complete mixed, unary, and four response rows must
> either give an anchor-safe complete-column dependence, a target-coordinate
> point in the sequential affine fibres, or a nonzero literal exchange
> outside the current Galois closure.  If none occurs, they must realize the
> closed Hall covector with one common `q` tail, the correct endpoint
> orientations and response heads, all fine output grades, and every
> selected mutual anchor protected.

The conclusions have their existing landings:

```text
complete-column dependence -> anchor-safe support deletion;
target-coordinate point    -> exact joint-kernel concentration;
new typed exchange         -> enlarge saturation or free active fan;
closed physical covector   -> star/triangle/K2,2 source theorem;
normalized target coloop   -> committed h=3 closure chain.
```

Pure matching matroids prove none of the word, tail, orientation,
fine-grade, or anchor-protection clauses in the boxed lift.  The sharp
matching-support/private-site guard in `1ec750e` shows why a matroid-only
augmenting path cannot replace it.

## 4. Theorem-level scope

Finite `K6` saturation settles only the local Hall shadow and its
termination.  It does **not** by itself:

* lift arbitrary Theorem-A frame circuits into complete endpoint columns;
* normalize an arbitrary active-fan coloop;
* prove affine target-line hitting;
* handle repeated-site or determinant-dark source entry; or
* force dependence in the injective `M3` five-lock.

Consequently this result does not close global entry.  It removes one
logical burden from the missing theorem: once the complete-row lift is
proved, no separate well-founded Hall/reselection potential remains at
`h=3`.  Saturation and one tight-set dual are enough.

Run:

```text
python3 computations/verify_h3_active_fan_coloop_saturation_boundary.py
python3 -O computations/verify_h3_active_fan_coloop_saturation_boundary.py
python3 -I -S computations/verify_h3_active_fan_coloop_saturation_boundary.py
```

Frozen ledger SHA-256:

```text
769aba0337aa62354adb9353057f7eebff20a8dc29900a575ac5f8fbe321d4bb
```
