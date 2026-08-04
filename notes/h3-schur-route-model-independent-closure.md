# The h=3 Schur comparison is chart-blind, so every adjunction is inert

The literal \(h=3\) no-go
[`h3-literal-full-nine-schur-polar-no-go.md`](h3-literal-full-nine-schur-polar-no-go.md)
proves the five marked polar cochains \(\Lambda_v\) have source-relative
connecting matrix \(I_5\), so none lifts through the literal lower block.
Its scope statement leaves three escapes: the denominator-marked cell of
its (18), a larger source-provenant totalization, and "a different literal
operation whose added tail cancels" the class.  The rigidity theorem
[`h3-full-nine-connecting-class-rigidity.md`](h3-full-nine-connecting-class-rigidity.md)
constrains the third escape for tails that *are* literal chart-labelled
source tails, and its own docstring says exactly what it does not reach:

> It does not exclude an operation whose tail is NOT a literal
> chart-labelled source tail -- in particular it does not exclude the
> Hasse/Spencer totalization or any denominator/cap material that the no-go
> leaves open.

This note closes that remaining space -- and closes it for **any**
adjunction to the committed source, derived or not, at **both**
specializations of the \(p\!-\!r\) block.  The instrument is one structural
fact about the five original columns; the arithmetic that used to look
decisive turns out to be irrelevant.

The conclusion is stronger than "closed for derived material", which is how
an earlier draft of this note stated it.  An independent re-derivation
established that the argument never uses any property of the adjoined
columns, and the checker now verifies that directly against deliberately
illegal adjunctions.

**Krenn's conjecture remains open.**  This closes one mechanism of one
route.  It constructs no replacement comparison and changes nothing on the
certified spine.

Companion checker:
`computations/verify_h3_schur_route_model_independent_closure.py`.

## 1.  Chart-blindness of the five original columns

Write \(A''\) for the lower block of an arbitrary augmented source and
\(T''\) for its leading layer.  The repair covector is chart-odd, and it is
supported on the **five original no-go columns**:

\[
 k_v=r_v^{pq}-r_v^{pr}\in\ker A'' ,
 \qquad
 (\Lambda_vT'')(k_v)=\tfrac12-\bigl(-\tfrac12\bigr)=1 .   \tag{1}
\]

Those five rows are chart pairs of *one* global row -- the committed
no-go's own Fact A, re-derived here by calling its `audit()`.  So every row
of \(A''\) has **equal entries on each of the five \(\{pq,pr\}\) pairs**,
and a covector that is chart-even there annihilates \(k_v\).  Adjoining a
column only *appends* coordinates, on which \(k_v\) is zero.  Hence

> \(k_v\) stays in \(\ker A''\) and \((\Lambda_vT'')(k_v)\) stays \(1\)
> under **any adjunction whatsoever**, so \(\Lambda_vT''\) never lies in
> \(\operatorname{row}A''\) -- not for derived material, not for
> boundary-**mismatched** pairs, not for outright **declared** columns, and
> independently of \(A_{pr}\).

That is the whole argument, and its hypothesis is deliberately weaker than
it first looks.  Both inputs of (1) are unchanged by the tilt, for the
reason in section 3.

**The stronger statement, which the conclusion does not need.**  If every
adjoined column additionally satisfies (D-i) of section 2 -- boundary a
global row or a chart class of one -- then

\[
 \text{every row of }A''\text{ is constant on \emph{every} }\{pq,pr\}
 \text{ pair,}                                                  \tag{2}
\]

so *all* of \(\operatorname{row}A''\) is chart-even.  True, and measured
(chart-odd dimension **0** in all twelve derived augmentations).  But (1)
does not use it.

**What is actually discriminating.**  In the derived augmentations the
three readings -- "\(A''\) is constant on chart pairs", "\(k_v\in\ker
A''\)", "the chart-odd part of \(\operatorname{row}A''\) has dimension
\(0\)" -- are **three views of one construction-forced fact**: the builder
appends the same boundary dictionary twice, so a constant substituted for
either copy leaves all three unchanged.  They discriminate only against a
mutation of the builder, and the note says so rather than presenting them
as three confirmations.

The discriminating test is the **adversarial adjunction probe**, which
breaks the builder on purpose.  Two illegal variants are adjoined, in both
models, on two base derivations:

* **MISMATCHED** -- chart pairs whose two boundaries *disagree* (so they
  are not two charts of one row: (D-i) violated);
* **DECLARED** -- columns whose boundary is a proper sub-sum of a row that
  is not a chart class, carrying an arbitrary chart-odd tail written down
  independently of any row.

In all eight runs, global chart-blindness is **destroyed** -- the chart-odd
part of \(\operatorname{row}A''\) has dimension **10**, and the checker
*requires* it to be nonzero, so the probe cannot pass vacuously -- while
the chart-odd part on the five original columns stays **0**, the five
original squares stay in \(\ker A''\), the connecting sub-block on them
stays \(I_5\), \((\Lambda_vT'')(k_v)\) stays \(1\), no cochain lifts, and
the Rouché–Capelli repair system stays inconsistent with the same witness
equation.  That is the strengthening, machine-checked.

The chart split itself is *not* trivial, and it is exhaustively computed
over all \(3^8=6561\) words in both models:

| model | row | \(pq\) chart | \(pr\) chart |
|---|---|---|---|
| \(A_{pr}=0\) | 90 | \(15+75\) | \(0+90\) |
| \(A_{pr}\) free | 105 | \(15+90\) | \(15+90\) |

so the tilt genuinely switches on a \(pr\)-direct sector.  Zero partition
failures; zero words with a different signature.

## 2.  What "derived" means, and why the tau existence question is decidable

Section 1 does **not** quantify over derived material -- it quantifies over
*any* adjunction, and what legitimises that is the support of \(k_v\), not
any property of the adjoined columns.  The notion below is needed for a
different purpose: it is what makes the *existence* half of the tau story
(section 4) a completed classification rather than an unbounded search, and
it is what yields the stronger fact (2).  Precisely:

> A source datum is **DERIVED** iff
> **(D-i)** its lower boundary is the literal global row \(H_w\) of a
> target-zero colour word \(w\) of the fixed eight-site geometry, or a
> partition class (chart) of that row; and
> **(D-ii)** its leading tail is a literal iterated polar
> \(\partial^{k}H_w/\partial e_1\cdots\partial e_k\) of that **same** row by
> edge variables, tagged by that chart's own sector labels.

Anything written down independently of a row is **declared**, and declared
boundaries are inadmissible under the repo's mapping-cylinder exclusions --
"[a mapping-cylinder cell] supplies (25) by definition rather than deriving
its target component from the source-labelled comparison"
([`n8-chart25-schur-bockstein-dual-lift.md`](n8-chart25-schur-bockstein-dual-lift.md)
§5), and "a mapping-cylinder target cell cannot perform this repair because
it changes the target bookkeeping without cancelling the source-side
identity matrix"
([`h3-literal-full-nine-schur-polar-no-go.md`](h3-literal-full-nine-schur-polar-no-go.md)
§5).  By the strengthening of section 1, declared material is covered
anyway, *as long as it is adjoined* rather than substituted for the
original columns.

(D-ii) is what makes the tau existence question **finitely decidable** at
\(h=3\), in three steps, each verified:

1. **Arity is forced.**  \(H_w\) is edge-degree 4, a \(k\)-fold polar has
   edge-degree \(4-k\), and the prescribed tails are edge-degree 2, so
   \(k=2\) exactly.  Every one-edge polar is checked to have edge-degree 3.
2. **Residual forcing.**  Exhaustively over all
   \(70\times3\times81=17010\) vertex-disjoint two-edge markings (15795 of
   them with nonzero polar), **one deterministic residual colouring per
   marking** -- the residual colour freedom is separately swept in full by
   the candidate-(b) classification below, which forces the word outright --
   a nonzero second polar is supported on
   monomials covering **exactly** the four residual sites, and agrees with
   the closed form \(\operatorname{Haf}(S\setminus\text{cover},w)\) minus
   direct-free terms.  A prescribed 2-edge tail therefore *forces* the
   marked pair to cover exactly the complementary four sites, and the
   search collapses to \(3\) matchings \(\times\,3^4\) colourings per pair.
3. **The CAP family.**  A derived column can meet some \(\Lambda_v\) only
   if \(\operatorname{cover}(\text{marks})=\{x,v,p,q\}\) and
   \(w|_{D\setminus\{v\}}=m\).  That family --
   \(5\times81\times3=1215\) data, 2430 labelled chart columns -- is swept
   **exhaustively**.  The *completeness* direction, that nothing outside it
   can pair, is corroborated **on instances only** (12 words \(\times\) 210
   site-markings \(\times\) 5 sites, 28 nonzero pairings, **0** outside;
   the independent audit reran it at \(33\times\) the scale -- 420,000
   data, 91 hits, 0 outside).  Never exhaustively; it is listed in
   section 8 as a non-closure.  Nothing here rests on it, since section 1
   uses only the five original columns.

So the existence half is a completed classification at this \(h\); the
negative half does not need it.

## 3.  Model independence in \(A_{pr}\)

Split the marked matchings by their use of the site \(p\): \(A\) uses the
\(pq\) edge, \(B\) uses the \(pr\) edge, \(C\) neither.  No matching uses
both.  Then as marked tails

\[
\begin{aligned}
 (pq,\mathrm{direct})&=A, & (pq,\text{two-star})&=B+C,\\
 (pr,\mathrm{direct})&=B, & (pr,\text{two-star})&=A+C,
\end{aligned}                                                   \tag{3}
\]

and the direct-free model is the same formula with \(B\) deleted.  Hence

\[
 \text{TILTED}-\text{DIRECTFREE}=(0,B,B,0) ,                    \tag{4}
\]

the tilt injects its new material into exactly the two sectors the no-go's
ambient \(V\) does not have, and the sensitivity the no-go's own sector
pair measures is

\[
 (pq,\mathrm{direct})-(pr,\text{two-star})=A-(A+C)=-C ,          \tag{5}
\]

which never contains \(B\).  A closed form for \(B\) is proved -- three
cases according to whether the \(pr\) edge is itself marked, is disjoint
from the cover, or meets it -- and (3), (4), (5) and the closed form are
machine-checked on all 210 vertex-disjoint site-markings over a named
58-word sample, **12180 pairs, 0 failures**, with 3480 markings having
\(B\neq0\) (term counts \(1\!:\!2610\), \(3\!:\!870\)), so the closed form
is exercised, not vacuous.

For the no-go's own marking \(B=0\) **identically**, because the cap mark
\(a_{pq}^{00}\) *occupies the site \(p\)*, so no marked matching can also
use the \(pr\) edge.  Machine-checked exhaustively over all
\(6561\times5=32805\) (word, site) data: the four-sector marked profile is
**bit-identical** between the two models in every case, and the tilt-only
sector is empty in every case.  The nonzero support is \(405=5\times81\),
matching the rigidity checker.

Consequently the tilted connecting matrix under the no-go's own
normalization is still exactly \(I_5\).  Over the four-sector leading space
the candidate normalizations behave so:

| normalization | connecting rank | diagonal |
|---|---|---|
| \(pq\)-direct \(-\) \(pr\)-two-star (the no-go's own) | 5 | \(1,1,1,1,1\) |
| \(pq\)-direct \(-\) \(pr\)-direct | 5 | \(\tfrac12\) each |
| \(pq\)-two-star \(-\) \(pr\)-two-star | 5 | \(\tfrac12\) each |
| \(pq\)-total \(-\) \(pr\)-total | 5 | \(1,1,1,1,1\) |
| \(pq\)-direct \(+\) \(pr\)-two-star (chart-**even**) | 0 | \(0,0,0,0,0\) |

Every chart-odd normalization gives an invertible diagonal; only the
chart-even one degenerates.  And the chart-even one is excluded, because
the lower layer of the forced chain map gives \((a+b)G_v=0\) with \(G_v\)
the row's own boundary, still 105 terms and nonzero.  All five candidates
annihilate the pure denominator block \(B'\) -- by disjoint support, so
that condition selects nothing, exactly as
[`h3-denominator-face-decoration-fork.md`](h3-denominator-face-decoration-fork.md)
§4 says.

## 4.  The \(\tau\) columns exist, are derived, and are inert

An **unaudited scratch derivation** (`scratchpad/o3map/`, spec S10,
**uncommitted**, cited as motivation only) prescribes, for the FULL
two-term block \(d_c\), ten extra source columns \(\tau_{uv}\) -- one per
unordered pair of odd sites -- whose leading tails are the \(Q\)-block
entries of \(d_c\) at the single word row \(m=12112\).  Verified
independently here: those tails are the four-site face hafnians

\[
 T_{uv}=\operatorname{Haf}\bigl(\{x\}\cup D\setminus\{u,v\}\bigr),
 \qquad\text{versus}\qquad
 h_v=\operatorname{Haf}\bigl(D\setminus\{v\}\bigr).             \tag{6}
\]

(Nothing here imports that scratch work.  The checker rebuilds \(d_c\) from
the committed base checker, reads the ten tails off its \(Q\)-block at the
row \(m\), and identifies them independently with (6).  "S10" and "o3map"
name files that exist only in scratch and resolve to nothing committed; the
negative result of §1 does not depend on them at all.)

Ten tails, 3 monomials each, 30 distinct, pairwise disjoint supports,
\(\dim W=10\), all coefficients \(+1\).  Every \(T_{uv}\) monomial is
**x-bearing**; every \(h_v\) monomial is **x-free**.  That separation is
what makes the whole story split.

**Existence, derived.**  Three candidates for the lower layer:

* **(a) the no-go's own marking at other words** -- closed with a
  certificate.  Differentiating by \(a_{xv}^{00}\) removes the unique
  x-edge of every surviving monomial, so all 405 nonzero swept tails are
  x-free and **0** of them meet a \(\tau\) monomial.
* **(b) other markings** -- **succeeds**, and the solution set is
  classified completely.  2430 residual-forced candidates, **2106
  solutions**, splitting **CAP 810 / CROSS 1296**.  Per pair the counts are
  \(\{162,243\}\): the four pairs containing \(r=3\) lose one whole CROSS
  pairing to \(A_{pr}=0\), i.e. \(1620-4\times81=1296\).  Exactly the CAP
  family is \(V\)-admissible (810 of 810; CROSS 0 of 1296), because
  differentiating by \(a_{pq}\) forces the \(pq\) edge, so all \(pq\)-chart
  marked material is \(pq\)-direct, and \(A_{pr}=0\) empties the
  \(pr\)-direct piece -- Fact B of the rigidity checker, re-derived for the
  new marking.  After cap normalization there are **9** colour choices per
  pair; three are named:
  * **D1** \((0,0)\): ten fresh double-deletion rows, ten new boundaries;
  * **D2** \((m_u,m_v)\): the single fully-mixed parent
    \(w^{*}=01211200\), of which each of the five committed no-go rows is a
    one-site reset;
  * **D3** \((0,m_v)\) and its mirror **D3\('\)**: a row the no-go already
    has.
  All are literal target-zero rows; none is declared.
* **(c) products and the denominator presentation** -- closed.  No
  \(\tau\) tail has a common edge factor, and the denominator \(l\)-block
  is entirely x-free (1215 monomials, none x-bearing) while all 810
  \(Q\)-block monomials carry exactly one x-edge.

**The repair spec is met.**  With the bare no-go source,
\(\operatorname{Hom}(d_c,\text{source})\) on the full two-term block is
\(0\) per sector.  With the derived \(\tau\) columns adjoined it is \(1\)
per sector, i.e. **dimension 2** (1818 unknowns, rank 1817), generated by
\(\psi_0\) supported on the single word row \(m=12112\), with the ten
\(Q\)-columns \((Q,u,v,m_u,m_v)\) landing on the \(\tau\) groups and the
five \(l\)-columns \((l,v,m_v)\) on the \(h\) groups, all with coefficient
1, and nothing else.  The lower layer then forces \(a+b=0\) again, with a
\(Q\)-block certificate: 27 of the 90 monomials of \(H_w\) are divisible by
no \(Q\)-block cell, and the coefficient equation at any of them reads
\((a+b)=0\).  So the augmented chain map is still chart-**odd**.

**And it is inert.**  Twelve named augmentations -- four derivations
\(\times\) two models, plus the tilted CAP variants -- all nine uniform
colour choices, and the alternative single-column convention, give the same
verdict.  Extract:

| augmentation | model | cols | rank \(A''\) | \(\dim\ker\) | conn rank | lifts | chart-odd \(\operatorname{row}A''\) | repair |
|---|---|---|---|---|---|---|---|---|
| D1 \((0,0)\) | \(A_{pr}=0\) | 30 | 15 | 15 | 5 | 0 | 0 | none |
| D2 \((m,m)\) | \(A_{pr}=0\) | 30 | 6 | 24 | 5 | 0 | 0 | none |
| D3 \((0,m)\) | \(A_{pr}=0\) | 30 | 5 | 25 | 5 | 0 | 0 | none |
| D1 \((0,0)\) | tilted | 30 | 15 | 15 | 5 | 0 | 0 | none |
| D1 \((0,0)\)+CAP | tilted | 50 | 15 | 35 | 5 | 0 | 0 | none |
| D2 \((m,m)\)+CAP | tilted | 50 | 6 | 44 | 5 | 0 | 0 | none |
| D3\('\) \((m,0)\)+CAP | tilted | 50 | 5 | 45 | 5 | 0 | 0 | none |

The nine uniform choices give lower ranks \(15,10,10,8,9,11,12,13,12\) --
genuinely different complexes -- and connecting rank 5 with no lift in all
nine.  The connecting sub-block is

\[
 \bigl[\,I_5\ \big|\ 0\,\bigr]
 \qquad\text{on (five OLD chart squares | ten }\tau\text{ squares)} . \tag{7}
\]

The Rouché–Capelli repair system -- an unknown correction \(c\) supported
on the **new** ambient coordinates (60 of them, 78 with CAP), equations
indexed by \(\ker A''\) -- is inconsistent for every \(v\) in every
augmentation.  The witness equation is indexed by the **old** kernel vector
\(k_v\), involves only the two \(h_v\) columns, contains **no new unknown at
all**, and reads \(0=\pm1\).  Adjoining material cannot change an equation
it does not occur in.  On the tail side, \(\Lambda_v\) is identically zero
on all 60 new coordinates, because \(\Lambda_v\) lives on x-free monomials
and every \(\tau\) monomial is x-bearing.

The test is not passing vacuously: in the tilted CAP augmentations the new
chart squares *are* seen by \(\Lambda_v\) (nonzero entries, required to be
nonzero somewhere), so the inertness verdict is measured against genuinely
chart-sensitive material.  Each such column is still a chart **pair**
sharing one boundary, so its chart difference is again a kernel vector --
precisely the case §1 covers -- and, by the adversarial probe, so is a
column whose chart copies do *not* share a boundary.

## 5.  A derived chart-odd tail forces boundary zero

The forced chain map wants the \(Q\)-column \(\kappa_{uv}\) to go to a
source element with the chart-odd tail \((e_{pq}-e_{pr})\otimes T_{uv}\).
One may declare a **single** column with that odd tail instead of two chart
copies.  **By construction** its lower boundary is then \(H_w-H_w=0\): a
difference of two identical dictionaries, which can never come out nonzero.
That record is labelled `CONVENTION` in the ledger, and the "0 columns with
a nonzero boundary" reading below is a restatement of the construction, not
a verification of it.

What *is* measured is the consequence.  The column is then literally a
rescaled kernel vector, and the connecting verdict is unchanged: in both
models on all four named derivations, 10 chart-odd columns each, all 10 in
the kernel, rank \(A''=5\), \(\dim\ker=15\), connecting rank 5, no lift.

> A chart-odd placement is consistent with a **derived** boundary -- but
> only with the boundary **zero**.  There is no tension, and no freedom.

This is what the chart-parity question resolves to on the derived side.

## 6.  Reconciliations

**With the rigidity theorem.**  Its Facts A–D sweep the marking
\((a_{xv}^{00},a_{pq}^{00})\) over all 6561 words.  The 405 nonzero tails
in that family span 1215 distinct monomials, **all x-free**; the 30 \(\tau\)
monomials are **all x-bearing**; the supports are disjoint (checked).  So
the \(\tau\) adjunction lies **outside** the swept family -- exactly the
case its docstring leaves open.  No contradiction.  But the \(\tau\)
columns satisfy the **analogue of its Fact C**: their two chart copies
share one boundary, so every chart-odd \(\tau\) combination is again
\(T''(\kappa)\) for \(\kappa\in\ker A''\) -- verified on 24 exact rational
trials (2 models \(\times\) 4 derivations \(\times\) 3).  Its
\(\Lambda\cdot B''=0\) condition also survives the augmentation: the
augmented pure denominator block has 15 columns and \(\Lambda_v\)
annihilates all of them, by disjoint support (the block is chart-even,
\(\Lambda_v\) chart-odd).

**With the decoration fork.**
[`h3-denominator-face-decoration-fork.md`](h3-denominator-face-decoration-fork.md)
reduces the denominator escape to one undetermined datum -- chart-neutral,
single-sector, or chart-odd decoration -- and records that "the available
evidence points toward chart-odd, i.e. toward the escape being open".  The
forced chain map does resolve it chart-odd \((a+b=0)\), and §5 shows that a
chart-odd *derived source column* has boundary zero.  The conclusion is
therefore **conditional**:

> **IF** the fork's chart-odd decoration of the attaching cell's
> denominator face is realized by a derived source column of this
> comparison, **THEN** the fork's chart-odd branch closes negatively.

That identification is an **unverified hand step** -- the fork's attaching
map is unconstructed everywhere in the repo, so there is nothing to compare
the decoration against -- and it is listed as such in the checker's
`proof_status.hand_proved_over_machine_verified_inputs`.  Without it, §5
says only what it literally verifies: a chart-odd column *of this
comparison* has boundary zero.

**With the chart-parity reduction.**
[`h3-chart-parity-schur-repair-reduction.md`](h3-chart-parity-schur-repair-reduction.md)
requires a repair tail to carry \(pq\)-direct mass \(-3\) at its own face
and \(0\) at the others.  The \(\tau\) tails carry mass \(0\) at every face,
since their supports are disjoint from every \(h_v\).  No conflict; the
\(\tau\) columns are simply not repair tails.

**Naming collision, resolved.**  The committed ledger's
`polar_audit()["required_additional_row"] = "tau_<deleted_site>"` is a
**five**-name object indexed by the deleted site -- the missing Rees row
that would make \(h_v\) a strict full-nine combination.  S10's
\(\tau_{uv}\) is a **ten**-name object indexed by an unordered pair of odd
sites -- the missing source column carrying the \(Q\)-block entry of
\(d_c\).  These are different objects; the shared letter is a collision.
The checker reads the five-name family off the committed ledger rather than
asserting it, and nothing anywhere assumes the two coincide.

## 7.  What is true by construction, and what is not

Being explicit, because it is the natural place to attack this note.

**Fact A -- "the two chart columns of a row share one lower boundary" -- is
true by construction** once a chart is defined as a partition of one global
row.  It is labelled `CONVENTION` in the checker's ledger and is labelled
here.  Its content is *not* the identity.  Its content is provenance:

* the direct-free branch is computed through the **committed**
  `BASE.chart_partition` of
  `verify_h3_direct_free_literal_four_face_full_nine_no_go.py`, an artifact
  this checker did not author, and its output is additionally agreed
  against an independent flag-based split on all 6561 words;
* the sector tags \((pq,\mathrm{direct})\), \((pr,\text{two-star})\) are
  **imported** from the committed rigidity checker, not re-declared;
* the committed no-go's own \(I_5\) is re-derived here by calling its
  `audit()` and comparing, and its frozen digest is re-checked.

So the convention is the repo's own, and the committed rigidity note treats
the same statement as a checked fact rather than a convention (its Fact A,
"Both are partitions of the *same* \(H_w\)", verified on all 6561 words).
What is **not** true by construction, and is computed: the cardinalities of
the split, which differ between the two models and which a different chart
definition would change.

And the one chart definition under which Fact A genuinely fails is run, as
a flagged probe, and **rejected**.  Under CONV-X5 -- in the \(f\)-chart,
divide every direct monomial by \(a_f\) (the dehomogenized chart) -- the two
chart columns carry different boundaries and Fact A fails on all five rows.
But then the ten columns become independent: rank 10, kernel **0**, and
every cochain lifts **vacuously**.  Identically in the tilted and in the
direct-free model.  So CONV-X5 is not a tilt effect and not an escape: it
is a different definition of a chart column, available and rejected already
at \(A_{pr}=0\), and it is not the definition used by any committed
checker.  Recorded as `CONVENTION`, rejected.

**The derived augmentations do not test chart-blindness.**  As §1 says,
the three readings "\(A''\) constant on chart pairs", "\(k_v\in\ker
A''\)" and "chart-odd part of \(\operatorname{row}A''\) is \(0\)" are one
construction-forced fact seen three ways: substituting a constant for any
one of them leaves the ledger digest unchanged.  They catch a mutation of
the builder and nothing else.  The adversarial adjunction probe of §1 is
what makes the claim discriminating, and it is required to break global
chart-blindness before its verdicts count.  Two further items are
consequences of labelled facts, recomputed anyway:

* \(k_v\in\ker A''\) is forced by Fact A; the checker still applies the
  assembled \(A''\) to each chart square (`CONSEQUENCE`);
* the vanishing of the connecting map on the \(\tau\) squares follows from
  x-edge separation; the checker still measures it (`CONSEQUENCE`).

**On labels.**  Every top-level ledger section carries exactly one label
from `{proved, verified-exhaustively, verified-on-instances, convention,
consequence}`; the per-augmentation and per-probe records are raw
measurements, carrying labels only on the three items above.  The four
universally quantified or unverified steps -- §1's "for any adjunction",
the residual-forcing corollary, the closed form of \(B\), and the fork
identification of §6 -- are flagged in the ledger's `proof_status` as hand
arguments over machine-verified inputs.  Per project discipline this note
is a research reduction until independently audited.

One provenance item is *declared*, not derived: the rigidity checker's
digest is a constant copied from that module rather than recomputed, and
the ledger names it `rigidity_checker_declared_digest` to keep it apart
from the no-go digest, which **is** recomputed by calling that checker's
own `audit()`.

## 8.  Scope

**Closes.**  The \(h=3\) marked-chart Schur comparison mechanism against
**any adjunction** to the committed no-go source -- derived,
boundary-mismatched, or outright declared -- at **both** specializations
\(A_{pr}=0\) and \(A_{pr}\) free.  The connecting matrix stays
\([\,I_5\mid 0\,]\); no \(\Lambda_v\) lifts; no correction drawn from the
new material, on the cochain side or the tail side, changes that.

**Does not close.**

1. **A rebuilt or replaced comparison.**  What is closed is *adjunction*:
   adding columns to the committed source.  An argument that changes the
   five original columns themselves -- a different marking, a different
   normalization of \(\Lambda_v\), a source built from other rows -- is
   outside the hypothesis, because §1 reads \(k_v\) and
   \((\Lambda_vT'')(k_v)\) off exactly those five columns.  Declared
   *cells* are covered; a declared *comparison* is not.
2. **The dehomogenized chart-column convention CONV-X5** (§7).  It
   redefines what a chart column's boundary is, so it changes the original
   columns rather than adding to them.  It does break Fact A, and it does
   trivialize both models identically (rank 10, kernel 0, vacuous lifts).
   Flagged as a convention, rejected, not used.
3. **The completeness direction of the CAP classification** (§2 step 3):
   that nothing outside the CAP family can pair with a \(\Lambda_v\) is
   verified on instances only, never exhaustively.  Nothing here rests on
   it -- §1 uses only the five original columns -- but it is not a theorem.
4. **The \(n=8\) two-chart structure**, which has its own chart geometry
   and is under separate live investigation
   ([`n8-chart25-relative-4d-obstruction.md`](n8-chart25-relative-4d-obstruction.md),
   [`n8-chart25-schur-bockstein-dual-lift.md`](n8-chart25-schur-bockstein-dual-lift.md)).
   Nothing here transfers to it automatically.
5. **Every non-Schur route**: Hamilton descent, chart-26 propagation, the
   diagonal/pencil lane, and membership.  Untouched.
6. **Tails of edge-degree other than two.**  §1 still applies -- it uses no
   property of the adjoined tails beyond their being appended -- but the
   *classification* of §2 is stated for the degree-two tails the scratch
   spec prescribes.

An earlier draft listed "non-derived (declared) material" and "a boundary
rule that is neither the whole row nor a chart class of one" as
non-closures.  Both are now covered, as long as the material is adjoined:
the adversarial probe of §1 verifies exactly those two cases.

This closes one mechanism of one route.  **Krenn's conjecture remains
open.**

## 9.  Exact verification

~~~text
python3 computations/verify_h3_schur_route_model_independent_closure.py
python3 -O computations/verify_h3_schur_route_model_independent_closure.py
python3 -I computations/verify_h3_schur_route_model_independent_closure.py
python3 -S computations/verify_h3_schur_route_model_independent_closure.py
python3 -I -S computations/verify_h3_schur_route_model_independent_closure.py
~~~

Everything is exact (`Fraction` / `int`); `require()` raises `RuntimeError`,
so `-O` does not weaken a single check.  The checker re-derives the
committed no-go's ledger and digest by calling its `audit()`, and imports
its sector tags; sweeps all 6561 words in both models for the chart
cardinalities and the partition agreement with `BASE.chart_partition`;
verifies the four-sector marked profile bit-identical between the models on
all 32805 (word, site) data, with the fused single-pass tails cross-checked
against literal per-sector `sparse_derivative` on all 405 nonzero
instances; checks the ABC identity, the closed form of \(B\) and the
identities (4) and (5) on 12180 (word, marking) pairs; checks the
second-polar closed form and residual forcing on all 17010 vertex-disjoint
markings, **one deterministic residual colouring per marking** (the colour
freedom is swept in full by the candidate-(b) classification, which forces
the word); rebuilds \(d_c\) and the ten \(\tau\) tails and identifies
them independently as face hafnians; runs the complete derivation
classification (405 candidate-(a) tails, 2430 candidate-(b) candidates,
2106 solutions, CAP/CROSS 810/1296, \(V\)-admissibility, the nine
cap-normalized choices, D1/D2/D3/D3\('\)); runs twelve derived
augmentations, **eight adversarial adjunction probes**, nine uniform
choices and eight CONV-T4\('\) runs with exact ranks, kernels, connecting
matrices, Schur-lift tests, chart-odd row-space dimensions and
Rouché–Capelli repair systems; sweeps the 1215-member CAP family plus an
outside-family probe; solves the 1818-unknown augmented
\(\operatorname{Hom}\) system for the chain-map repair spec with its
\(Q\)-block certificate; runs the CONV-X5 probe in both models; and checks
the rigidity reconciliation, the Fact C analogue on 24 trials and
\(\Lambda\cdot B''=0\) on the augmented 15-column block.

Vacuity and discrimination guards require nonzero instance counts at every
stage -- 405 nonzero tails, 3480 nonzero \(B\)'s, 15795 nonzero polars,
810 admissible solutions, 28 probe pairings, at least one new chart square
that a \(\Lambda_v\) actually sees, and, in each adversarial probe, ten
boundary-mismatched pairs and a **strictly positive** chart-odd dimension
of \(\operatorname{row}A''\).  Runtime is fifteen to twenty seconds
depending on the machine.  Its frozen ledger digest is

~~~text
f00ae560ab0df3c7d81ae35856f41d4c02820ab942cb22d4ca12fabd67df0890
~~~

Mutation-tested with twelve source-level injections, each raising under
both `python3` and `python3 -O` with a message naming the broken property:

| # | injection | message names |
|---|---|---|
| M1 | pr-direct \(0\to1\) in the target chart split | `chart cardinality` |
| M2 | pr chart column given a different boundary | `chart-blindness` |
| M3 | delete the \(a_{pr}\times\)two-site-face branch of \(B\) | `closed form of B` |
| M4 | make the no-go cochain chart-even | `connecting map` |
| M5 | perturb a \(\tau\) tail coefficient | `tau spec` |
| M6 | drop the inhomogeneous term of the repair system | `repair test` |
| M7 | drop the direct-free deletion from the polar closed form | `second polar` |
| M8 | feed the bare tail list to the augmented \(\operatorname{Hom}\) | `chain map` |
| M9 | give the chart-odd single column a nonzero boundary | `CONV-T4'` |
| M10 | mis-state the CAP covering site set | `CAP completeness` |
| M11 | make the adversarial probe *not* adversarial (matched boundaries) | `adversarial probe: … (D-i) was not actually violated` |
| M12 | break Fact A on an original column inside the probe | `adversarial probe: an ORIGINAL chart square left ker A''` |

M11 and M12 are the ones that matter for §1: M11 checks that the probe
really does violate (D-i) before its verdicts are counted, and M12 checks
that the conclusion is sensitive to the *only* hypothesis it uses -- Fact A
on the five original columns.  M2, by contrast, mutates the builder, which
is all the derived-augmentation chart-blindness readings can detect; §7
says so.
