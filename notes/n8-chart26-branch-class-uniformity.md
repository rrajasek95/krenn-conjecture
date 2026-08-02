# The two branch signatures split uniformly after source-labelled refinement

The weighted degree-six census isolated coarse classes of sizes 8,412 and
45,776 from one nonsquarefree representative apiece.  A representative does
not control a coarse signature.  The complete exact refinement gives the
sharper statement:

\[
\begin{array}{c|r|r|r}
\text{pair type}&\text{labelled pairs}&\text{squarefree normal form}
 &\text{one-coordinate collision}\\\hline
4\text{--}5&8{,}412&2{,}986&5{,}426\\
5\text{--}5&45{,}776&29{,}212&16{,}564
\end{array}
\]

There are no zero normal forms in either class.  Thus neither coarse class is
"branch-only."  What is uniform is a two-route source-labelled rule: retain
the squarefree normal forms as a separate non-path degree-six frontier, and
apply a geometric vertex split to the 21,990 collision forms.

## 1. Refinement is not chart symmetry

Every member spans the same abstract Hamming square of source words.  For a
4--5 pair, the original word is one intermediate corner of the two-coordinate
move defining the transport.  For a 5--5 pair, the two transports share one
word, have source distances one and two, and occupy three sides of a Hamming
square.  This includes five 4--5 and fifteen 5--5 cases whose fourth corner
is a pure word.

The four-element support stabilizer gives essentially no compression after
the weighted leads have been selected:

\[
\begin{array}{c|r|r|r}
 &\text{selected lead-pair types}&\text{source-label types}
 &\text{labelled pairs}\\\hline
4\text{--}5&8{,}412&4{,}797&8{,}412\\
5\text{--}5&45{,}776&36{,}553&45{,}776.
\end{array}
\]

Every selected lead pair is alone in its stabilizer type.  A proof cannot be
obtained by checking four transforms of the old representative.  It must use
the Hamming-square source formula itself.  Among the 4,797 source-label types
in type 4--5, the selected multiplicities are 2,604 singletons, 1,482 doubles,
and 711 fourfold types.  Among the 36,553 source-label types in type 5--5,
they are 28,786 singletons, 6,311 doubles, and 1,456 triples.

Even a source-label type does not determine the weighted outcome.  Of the
4,797 type-4--5 source types, 1,819 are collision-only, 2,428 are
squarefree-only, and 550 contain both.  Of the 36,553 type-5--5 source types,
the corresponding counts are 8,371, 23,232, and 4,950.  The source-square
identity is uniform; the term-order route must be read after orientation.

## 2. The uniform source formula and the nonuniform normal form

Normalize all degree-four and degree-five lower cells at their certified
weighted pivots.  Each 4--5 critical pair has a source expression

\[
 G=m_HH-m_RR-\sum_j q_jB_j,                         \tag{1}
\]

where the exact lower reduction always has one column (B_1).  Each 5--5
pair has the analogous expression with two input transports and zero, one,
or two lower columns; their exact distribution is

\[
 #\{0,1,2\text{ lower steps}\}=(30{,}239,12{,}627,2{,}910). \tag{2}
\]

For 4--5 all 8,412 reductions have one lower step.  Equations (1)--(2) are
literal identities of normalized chart polynomials.  The weighted leading
term of (G), however, has two possible forms.  It is squarefree in the
counts displayed above, or it contains exactly one decorated coordinate
(x) twice.  No normal form has a larger repeated excess or two different
repeated coordinates.

The collision coordinates are not fixed.  The 4--5 branch stratum has eight
coordinate fibres and the 5--5 branch stratum has twenty-nine.  This is the
precise failure of the representative formula at (x_{02}^{00}) to be a
global formula with one fixed (x).

Squarefree does not mean path-forest here.  The exact lead skeletons are

\[
\begin{array}{c|r|r|r}
 &G_6\text{ branched}+P_2&G_4\text{ branched}+P_2+P_2
 &\text{decorated-squarefree physical parallel}\\\hline
4\text{--}5&2{,}476&510&0\\
5\text{--}5&8{,}663&14{,}259&6{,}290.
\end{array}
\]

Thus all 32,198 squarefree forms still lie outside the simple `P6+P2` and
`P4+P4` complex.  The 6,290 cells in the last column have a squarefree
decorated pivot but a repeated uncoloured physical edge.  They need their own
branched/parallel straightening theorem rather than automatic path-forest
continuation.

## 3. Every closed collision branch contracts in the lower source complex

For each collision form, restrict the complete source expression (1) to
(x=0).  Delete the source columns whose monomial multiplier contains (x),
then restrict the remaining lower polynomials term by term.  The result is
exactly (G|_{x=0}).

The 4--5 branch always leaves two source-labelled lower columns; the 5--5
branch always leaves one.  Hence all 5,426 and 16,564 closed children lie in
the restricted lower boundary image.  This is the uniform version of the
old representative identities

\[
 G_{45}|_{x=0}=b(aH_1-H_{730})|_{x=0},\qquad
 G_{55}|_{x=0}=bR_{730,1459}|_{x=0}.                  \tag{3}
\]

The checker reconstructs both sides of every restricted identity, rather
than inferring (3) only from leading monomials.

## 4. Every open collision branch decreases the Laurent defect

Write the repeated pivot as (x^2u).  Across all 21,990 collision cells,
(u) is squarefree and has uncoloured skeleton

```text
P3+P2+P2+P1.
```

Thus on (x\ne0), the Laurent cell (x^{-2}G) decreases repeated-coordinate
excess from one to zero.  The checker also tests every term of every
collision remainder: no complete degree-four or degree-five pivot divides
any term of (xG).  Because all lower pivots are squarefree, multiplication
by (x^k) has the same lower divisors for every (k\ge1).  There are zero
positive-power lower-normality failures.

This does not say that a Laurent cell has entered the polynomial path-forest
complex.  Its pivot has degree four after removing (x^2), and its skeleton
contains two isolated vertices.  It is a separate localized continuation
whose local defect has strictly decreased.

## 5. Exact scope and proof consequence

The theorem is complete for every labelled degree-six pair in the two frozen
coarse signatures.  It does not classify the other 2,871,617 degree-six
pairs, establish later Buchberger closure, or prove radical membership of the
pure target.

What it removes from the global proof target is the proposed orbit
propagation theorem for these signatures.  They now route exactly as follows:

1. squarefree normal form: enter the newly isolated branched/parallel
   degree-six straightening frontier;
2. collision normal form: the closed child is lower-exact and the open child
   is a Laurent cell with strictly smaller collision excess.

The branch theorem therefore supplies a valid local contraction/split module
for an augmented HPL construction, but it does not close the whole two-class
frontier.  The unresolved work is to straighten the 32,198 non-path
squarefree forms, connect that continuation and the localized cells to the
target augmentation, and control later cells without reintroducing decided
coordinates.

## 6. Verification

Run

```text
python3 computations/verify_n8_chart26_branch_class_uniformity.py
```

The checker rebuilds all 6,558 degree-four and 84,005 degree-five weighted
leads, enumerates the 54,188 selected labelled pairs, replays their exact
integer reductions, reconstructs every closed source identity, and performs
the finite open-colon divisibility tests.  A full run takes about nineteen
minutes on the development machine (969.95 seconds in the frozen run).  Its
ledger digest is

```text
c03003ac8d6261314c2dd5310e97be41ba4651e2c8acf2a2b8ae20f2c95475e9
```
