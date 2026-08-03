# The denominator-marked escape forks on one undetermined datum

**Retraction notice.**  An earlier version of this note, titled *"The
denominator-marked escape is closed by half-integrality"*, claimed the
escape was closed.  That claim is **withdrawn**.  An independent audit
showed it rested on an unproved modelling hypothesis — that the denominator
face is chart-neutral — and that the cited four-cube note points the other
way.  What survives is the arithmetic, which does not close the escape but
isolates the single datum that decides it.

Krenn's conjecture remains open.  Nothing here changes the certified spine.

## 1. What is settled: the arithmetic

The literal no-go
[`h3-literal-full-nine-schur-polar-no-go.md`](h3-literal-full-nine-schur-polar-no-go.md)
leaves one escape: a denominator-marked two-edge cell, generator (18)
carrying a free sign \(\sigma\), whose tail contributes \(-I_5\).

A face built from one copy of the three-term marked polar \(h_v\) is

\[
 w(\alpha,\beta)=\alpha\,(h_v)_{pq,\mathrm{direct}}
                +\beta\,(h_v)_{pr,\mathrm{two\text{-}star}},  \tag{1}
\]

and since \(h_v\) has exactly three terms and \(\Lambda_v\) is \(\pm1/6\)
on them,

\[
 \Lambda_v\bigl(w(\alpha,\beta)\bigr)=\frac{\alpha-\beta}2.    \tag{2}
\]

The checker verifies (2) on the full integer grid
\(\alpha,\beta\in[-3,3]\) for all five deletion faces, and verifies that
each face pairs to zero against the other four cochains.  The repair value
\(-1\) therefore needs \(\alpha-\beta=-2\).

## 2. The fork

Everything now depends on the **chart decoration** the denominator face
carries.  The checker sweeps every integer coefficient in \([-4,4]\):

| decoration | value | reaches \(-1\)? |
|---|---|---|
| chart-neutral \((\alpha=\beta)\) | \(0\) | **never**, at any coefficient |
| single sector \((\sigma,0)\) | \(\sigma/2\) | yes, at \(\sigma=-2\) |
| chart-odd \((\alpha=-\beta)\) | \(\alpha\) | yes, at \(\alpha=-1\) |

No restriction \(|\sigma|=1\) is imposed.  The no-go's (18) leaves
\(\sigma\) free and nothing in the repo bounds it, so bounding it would beg
the question.  The earlier version of this note did impose it, and that was
one of the audited defects.

**The escape is closed under exactly one of the three decorations.**

## 3. Which decoration is it?  Not decidable here

This is the honest answer, and it is the useful content of the note.

* `computations/verify_h3_qzero_denominator_rees_four_cube.py` explicitly
  declines to give the symbol cap and ordinary-residue coordinates: *"This
  is a polynomial/output-word symbol.  Giving it cap and ordinary-residue
  coordinates requires the attaching map that is deliberately not declared
  by this checker."*
* Equations (11) and (22) of
  [`h3-qzero-denominator-rees-four-cube.md`](h3-qzero-denominator-rees-four-cube.md)
  give only the polynomial identity \(P_m\delta(d_{v,m_v})=h_vY_0\).
  Neither assigns the symbol a chart sector.
* The attaching chain is unconstructed everywhere in the repo.

So "the presentation does not mention \(p,q,r\), therefore the embedding is
diagonal" is a **non-sequitur**: an unlabelled symbol must be *assigned*
coordinates by the (missing) attaching map, and nothing fixes that
assignment.

**The available evidence points toward chart-odd, i.e. toward the escape
being open.**  Four-cube section 2 requires the denominator face to cancel
the reset commutator produced on the \(K_v\) side, and the Rees symbol of
that side is its equation (9),

\[
 (h_v)_{pq,\mathrm{direct}}-(h_v)_{pr,\mathrm{two\text{-}star}},
\]

which is **chart-odd**.  If the cancelling face inherits that decoration
then \(\alpha=-\beta\), (2) gives \(\Lambda_v=\alpha\), and \(\alpha=-1\)
delivers exactly the required \(-1\).

## 4. One model that is closed for an independent reason

The pure-face (\(Y_0\)-type) model — the symbol carried by the all-zero
colouring — pairs to zero under *every* decoration, because its monomials
are disjoint from those of \(h_v\) (which carry the \(m\)-colours).  The
checker verifies the disjointness and the vanishing across all three
placements and all coefficients in \([-4,4]\).

This matters for reading the no-go: its \(\Lambda_vB'=0\) holds by disjoint
support, **independently of how \(B'\) is placed**.  The no-go therefore
supplies no evidence for diagonality either.

## 5. Cross-face independence

The supports of \(h_v\) and \(h_w\) are disjoint for \(v\ne w\): a matching
of \(D\setminus\{v\}\) uses the site \(w\) and vice versa.  The checker
verifies all \(5\times5\) intersections.  So the five conditions cannot be
traded off against each other, and a face at one deletion site contributes
nothing at any other.

## 6. What this leaves

The escape stated in the no-go is **not closed**.  It reduces to a single
undetermined question:

> Does the denominator face of the attaching cell carry a chart-neutral,
> single-sector, or chart-odd decoration?

Answering it requires constructing the attaching map — the same missing
object the four-cube note declines to declare.  That construction, not more
arithmetic on the symbol, is the next step for this route.

## 7. Scope

1. Finite, \(h=3\), direct-free specialization
   \(x=0,\ D=(1,2,3,4,5),\ p=6,\ q=7,\ r=3,\ A_{pr}=0\), word \(m=12112\).
2. Equation (2) is a proof: it follows from \(h_v\) having exactly three
   terms and \(\Lambda_v\) being \(\pm1/6\) on them.  The grid is a
   confirmation.
3. The checker verifies a formula about a three-term marked symbol under a
   *stipulated* embedding.  It contains no \(Y_0\), no denominator column,
   and does not import the four-cube checker — the geometric content is
   confined to `build_polars()`.  It should not be read as a verification
   about denominator material as such.
4. This closes nothing.  It constructs no replacement comparison, changes
   nothing on the certified spine, and Krenn's conjecture remains open.

## 8. Verification

Run

~~~text
python3 computations/verify_h3_denominator_face_decoration_fork.py
python3 -O computations/verify_h3_denominator_face_decoration_fork.py
python3 -I computations/verify_h3_denominator_face_decoration_fork.py
python3 -S computations/verify_h3_denominator_face_decoration_fork.py
python3 -I -S computations/verify_h3_denominator_face_decoration_fork.py
~~~

The checker rebuilds the five marked polars from the literal eight-site
rows, re-derives their two-sector placement, verifies support disjointness,
verifies (2) on 245 grid points, sweeps all three decorations over every
integer coefficient in \([-4,4]\) and records which reach \(-1\), verifies
the pure-face model's disjointness and vanishing, and verifies cross-face
independence.  Its frozen ledger digest is

~~~text
b9471153580976ddf8417b8f95b26161f9d46431a70cffab518e368b8e4730a6
~~~
