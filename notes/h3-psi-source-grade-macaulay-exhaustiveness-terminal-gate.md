# Exact source-grade exhaustiveness needed to promote `Psi`

## Outcome

At the canonical `h=3` cap grade, every currently typed source and
higher-cell family outside the response-to-`AugP2` mixed-incidence orbit is
`chi`-dark for a structural reason:

- its word, fine, repeated-edge, operation-parent, or occurrence tag puts it
  in a different direct-sum summand; or
- its literal cap projection lies in the exhaustive four-site image
  `ker(chi)`.

Here

\[
 \delta=(1,1,-1,-1),\qquad
 \chi=\delta\cdot(B-Eq),\qquad
 \Psi={1\over4}\chi.                                  \tag{1}
\]

The minimal unclassified list has one homogeneous source-generator type:

> the source-labelled response-to-`AugP2` mixed orbit/`K_Eq`
> mapping-cylinder two-cell `kappa_mix`.

The shortest augmented-`P2` schema has eight literal fixed-grade
instantiations.  Modulo the old cap rows, write

\[
 \Pi_{B/Eq}(\kappa_i)equiv\lambda_i(\delta,0),
 \qquad \chi(\kappa_i)=4\lambda_i,
 \qquad 0\le i<8.                                    \tag{2}
\]

Promotion to an accepted Macaulay terminal requires two genuinely missing
facts:

1. an exhaustive source-grade census proving that no other primitive
   cap-grade operation-changing generator exists; and
2. the eight finite equations `lambda_i=0`.

Under those facts, extending `Psi` by zero on every complete external row
gives the normalized global terminal.  Any nonzero `lambda_i` is instead
the unique projection-wise filler exit.

Checker:
[`verify_h3_psi_source_grade_macaulay_exhaustiveness_terminal_gate.py`](../computations/verify_h3_psi_source_grade_macaulay_exhaustiveness_terminal_gate.py).

## 1. The literal grade being exhausted

The relevant output block is not selected merely by polynomial degree.  Its
full tag is

```text
word        01211222
fine        t*q_(v,N) at the selected six P3+K2 occurrences
repeated    P3+K2
operation   AugP2 cap / mixed orbit
window      2345 with literal occurrence labels.
```

Call this tag `Gamma_*`.  Different words or operation parents remain
different direct-sum summands even if their undecorated matching shapes or
coarse polynomial degrees agree.  This is what makes the grading argument
strong enough: a coefficient shadow cannot be silently retagged as a cap
column.

The accepted source-grade block must be the finite physical map

\[
 J_{\rm phys,\Gamma_*}:C_{\rm phys,\Gamma_*}
                  \longrightarrow Y_{\rm phys,\Gamma_*}.            \tag{3}
\]

Its domain must contain:

- every primitive physical relation with an output face in `Gamma_*`;
- every monomial Macaulay multiple `m*r` satisfying
  `deg(m)+deg(r)=Gamma_*`;
- every PP, Hasse, Koszul, mapping-cylinder, and Tate generator with a
  `Gamma_*` face; and
- all source idempotent, operation-parent, word, fine, repeated, window, and
  occurrence labels.

Its codomain must retain:

- every private `B` and reduced-`Eq` occurrence row;
- target, `W`, ordinary residue, `M`, anchor incidence, physical `q`, and
  pointed `P_f`;
- word-resolved ridge, eta, sigma, and every protected terminal row.

Without both censuses, a local cokernel vector is a bounded separator, not
a Fredholm/Macaulay terminal.

## 2. Exact dark-family classification

The exhaustive four-site supermap has dimension `127`, rank `126`, and
one-dimensional cokernel.  Its image is exactly the local `chi`-kernel.  In
the aggregated cap block, the four diagonal and four signless companion
columns have rank seven in dimension eight, again with kernel detector (1).

The currently known families divide as follows.

| family | literal reason for `chi=0` |
|---|---|
| exhaustive four-site response/target/PP supermap | image is the complete local `chi`-kernel |
| 25 named `AugP2` cap columns | diagonal, signless shore edge, tied `B=Eq`, or external row |
| 121 named response/intermediate columns | response word/fine/operation summand |
| selected six `db01` terms | strict response first-PP grade, zero cap projection |
| eighteen `dL01` terms | strict fixed-window response grade, zero cap projection |
| collision tops, one-hole/unary, `C2+/C4/P2` repairs | off-grade, signless shore edge, or old local image |
| six sibling `3K2` faces | repeated grade `3K2`, not `P3+K2` |
| `(A+B)H` and `(A+C)H` response switches | word/fine still `11:110000` |
| word-`0102` section and `dq23` reinsertion | lower-word block until a cross-word placement exists |
| pointed conormal `P_f` | anchor/conormal coordinate outside `B/Eq` |
| primitive cap `p` and target/residue cap graph | `Q`, target, and ordinary-residue rows outside `B/Eq` |
| `gamma=-dOmega`, eta, sigma | shifted Kähler/external rows |

This advances the earlier global-gluing criterion in two ways.  Bare
`db01` and `dL01` are now proved dark rather than left undefined, and the
`d^2` audit proves that no augmentation value follows from the primitive
square boundary.  All remaining uncertainty is localized to (2).

## 3. Why ordinary higher cells stay dark

The higher-operation argument is an induction on construction length.

1. Monomial Macaulay multiplication adds a nonnegative fine exponent vector
   and preserves word, operation tag, source parent, and occurrence labels.
2. PP/Hasse/Koszul faces record a differentiated or removed literal slot but
   retain the word block, operation parent, and source idempotent.
3. Matching restriction/reinsertion returns to the same labelled occurrence
   and preserves a `B=Eq` tie, signless shore edge, or local-kernel vector.
4. Cartan, ridge, eta, and sigma completion changes only external rows unless
   it is carried by a cross-word mixed comparison.

The fixed polynomial degree is three.  The finite relation/multiplier degree
possibilities are

```text
(relation degree, multiplier degree) = (0,3),(1,2),(2,1),(3,0).
```

Positive multiplication can therefore complete a lower polynomial degree,
but it cannot change a response source parent into an `AugP2` source parent.
A cap-internal multiple factors through the projection-complete local map;
a response multiple remains outside the cap operation block.  Linear sums
within a fixed grade preserve `ker(chi)`.

Consequently:

> every Macaulay, PP, Hasse, Koszul, or Tate descendant of a classified dark
> seed remains dark unless its construction uses a primitive
> response-to-`AugP2` mixed-incidence generator.

This is an exact closure theorem for the listed operations.  Its remaining
global hypothesis is a source-presentation census: one must prove that the
physical source has no exotic primitive generator at `Gamma_*` outside this
closure and the mixed orbit.

## 4. The minimal unclassified finite list

The enriched `AugP2` schema separates seven homogeneous face directions.
Pointed conormal, primitive cap, central descent, labelled residue,
reinsertion, and shifted ridge directions are individually typed; only the
mixed orbit/`K_Eq` square direction can carry an unclassified `B/Eq`
augmentation.

There is one generator type and eight canonical instances:

```text
kappa_0, kappa_1, ..., kappa_7.
```

The old cap image has rank seven.  Therefore each instance has the unique
normal form (2).  Exact row reduction gives

```text
all lambda_i=0       B/Eq rank remains 7, Psi survives;
some lambda_i!=0     B/Eq rank becomes 8, unique quotient filled.
```

The mandatory proper faces do not enlarge the type list when the source is
presented by one totalized augmented comparison:

- physical reduced-`Eq`/cap descent is a face of `kappa_mix`;
- the word-`0102` section and `dq23` reinsertion are strictly off-grade by
  themselves, and their cap augmentation belongs to the same boundary
  orbit;
- the six `P3+K2` placements belong to that orbit, while the six sibling
  `3K2` faces are repeated-grade dark outside it; and
- the shifted ridge is an independent homogeneous face but has zero
  `B/Eq` projection.

There is one qualification.  If the actual source presentation treats any
cap-grade proper face as an independent generator rather than a face of one
of the eight `kappa_i`, the census must either identify it with the orbit or
append it to the finite test list.  This is precisely why the generator
census, not just a boundary sketch, is required.

## 5. Exact terminal-promotion theorem needed

The missing source-grade theorem can be stated without mentioning any
candidate construction:

> **`Gamma_*` source exhaustiveness.** After quotienting
> `C_phys,Gamma_*` by all generators whose literal `B/Eq` image lies in
> `ker(chi)`, the quotient is spanned by the eight classes
> `kappa_0,...,kappa_7`.  No other primitive cap-grade operation-changing
> generator occurs.

Together with that theorem, the remaining computation is finite:

\[
                         \chi(\kappa_i)=0
                    \quad(0\le i<8).                   \tag{4}
\]

If (4) holds, define `Psi_tilde` to be (1) divided by four on `B/Eq` and
zero on every other complete physical output row.  Then

\[
 \widetilde\Psi J_{\rm phys,\Gamma_*}=0,
 \qquad
 \widetilde\Psi((B,Eq)=(\delta,0))=1.                 \tag{5}

Equations (3)--(5), with the literal balanced comparison/RHS identified,
are the accepted finite Macaulay nonmembership certificate.  Because the
map contains physical `q` and all protected rows, the existing
kernel-generator versus Fredholm alternative is then eligible; no local
occurrence dual is being promoted before landing.

If (4) fails, a first nonzero `lambda_i` raises the projected rank from
seven to eight.  That column is the physical filler candidate, and its
target, `q`, anchor, residue, word, and ridge faces must be closed in the
same totalization.

## Sharp frontier

What is now proved:

```text
local four-site source closure             exhaustive, cokernel one
all named cap/response/collision families  chi-dark
bare db01 and dL01                         chi-dark
ordinary higher closure without cross mix chi-dark
unclassified homogeneous generator types  one
unclassified literal instances            eight
```

What is not proved:

```text
global Gamma_* generator census            open
absence of exotic cap-grade primitives     open
lambda_0=...=lambda_7=0                    open
literal comparison to final RHS convention open
```

This is the shortest negative/terminal lane.  It replaces an open-ended
search through higher faces by one source-presentation census and eight
exact scalar tests.

## Verification

Run all logical modes, or the complete audit in normal, optimized, and
isolated/no-site interpreters.  The frozen all-mode ledger digest is printed
by the checker.
