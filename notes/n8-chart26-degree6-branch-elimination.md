# The two branch-only degree-six cells admit an exact vertex split

The weighted degree-six census found two representatives whose normal forms
contain no simple `P6+P2` or `P4+P4` term.  This note gives their exact
source-labelled geometric split.  It is bounded to the frozen representatives;
it does not yet propagate the formulas over all 8,412 and 45,776 members of
their coarse census classes.

## 1. The cells and the split coordinate

Write

\[
 x=x_{02}^{00}=\mathtt{09},\qquad
 a=x_{01}^{01}=\mathtt{01},\qquad
 b=x_{02}^{10}=\mathtt{0c}.
\]

The first cell is the weighted remainder of (H_1) against the degree-five
transport (R_{730,2188}).  Exact reduction uses one original generator and
gives

\[
 G_{45}=abH_1-xR_{730,2188}-bH_{730}.                 \tag{1}
\]

It has 330 terms and degree histogram

\[
 \#_{\deg_y=3,4,5,6}=(2,26,122,180).
\]

Its weighted lead is

```text
0309094bc6f4,
```

with (x) repeated twice.  Its degree-six terms consist of 132 branched
`G6...+P2`, 36 branched `G4...+P2+P2`, and 12 parallel-edge
`P4+P2+P2` monomials.  There is no `P6+P2` or `P4+P4` term.

The second cell is the weighted remainder of (R_{730,1459}) against
(R_{730,3646}).  The one lower reduction has source
(R_{1459,2917}), with orientation

\[
 G_{55}=bR_{730,1459}-xR_{730,3646}+xR_{1459,2917}.   \tag{2}
\]

It has 480 terms, with degree histogram

\[
 \#_{\deg_y=4,5,6}=(12,108,360),
\]

and repeated weighted lead

```text
0409094ec6f4.
```

Its degree-six skeleton counts are exactly twice those of (G_{45}), and it
also contains no simple even path forest.

These are literal polynomial identities in the normalized chart, not inferred
relations between leading monomials.

## 2. The closed branch dies in the lower source complex

Setting (x=0) in (1) gives

\[
 G_{45}|_{x=0}=b(aH_1-H_{730})|_{x=0}.                \tag{3}
\]

The restriction has 150 terms, degree histogram

\[
 (\#_3,\#_4,\#_5,\#_6)=(2,19,73,56),
\]

and temporary weighted lead `010c123fc6f4`.  Exact division first uses the
changed restricted lead `123fc6f4` of (H_1), with multiplier `010c`, and
then the restricted lead `0175c6f4` of (H_{730}), with multiplier `0c`.
The remainder is zero.

Similarly, (2) restricts to

\[
 G_{55}|_{x=0}=bR_{730,1459}|_{x=0}.                  \tag{4}
\]

Its 150 terms have degree histogram ((\#_4,\#_5,\#_6)=(4,34,112)).
The changed restricted lead `012d7375c6` of (R_{730,1459}), multiplied by
`0c`, removes it in one exact division.  Again the remainder is zero.

Thus neither closed cell needs to be transported into the path-forest
complex: both are already null in the restricted source-labelled lower
complex.  This is stronger than merely exposing another squarefree lead.

## 3. The open branch has a squarefree Laurent pivot

All 6,558 degree-four and 84,005 degree-five weighted leads are squarefree.
For each (G\in\{G_{45},G_{55}\}), no lower lead divides any term of (xG).
Because another copy of (x) does not change the squarefree support, the same
finite check proves that (x^kG) is lower-basis normal for every (k\geq1).
This is a statement about division by the completed lower leading set; the
lower set is not being claimed to be a Gröbner basis in degree six.

On the Laurent branch, put (widehat G=x^{-2}G).  The two selected pivots
become

```text
G45: 034bc6f4
G55: 044ec6f4
```

They are squarefree and both have uncoloured skeleton
`P3+P2+P2+P1`.  The Laurent exponent histograms are

\[
\begin{array}{c|rrr}
 &\nu_x=-2&\nu_x=-1&\nu_x=0\\ \hline
\widehat G_{45}&150&165&15\\
\widehat G_{55}&150&300&30.
\end{array}
\]

The exact denominator-clearing identities are (x^2\widehat G_{45}=G_{45})
and (x^2\widehat G_{55}=G_{55}).  Localization therefore removes the
repeated-pivot defect, but it does not move either cell into the degree-six
`P6+P2`/`P4+P4` forest complex.

## 4. Exact local descent statistic

For a branch history, mark each physical coordinate once it has been declared
zero or invertible, and ignore powers of an already invertible coordinate when
measuring pivot multiplicity.  On these two cells use the lexicographic pair

\[
 \Delta=(\#\text{ undecided decorated coordinates},
          \text{ repeated-coordinate excess of the localized pivot}). \tag{5}
\]

Both children of the split strictly decrease the first entry by deciding
(x).  More concretely, the closed child deletes the cell altogether, while
the open child also decreases the second entry from one to zero: its pivot is
squarefree after (x^{-2})-division.  Because a decided coordinate is never
split again, (5) is well-founded for every fixed finite chart.

This certifies the local termination clause for the two representatives.  A
global geometric-vertex argument still has to prove that every member of the
two coarse classes has the same source-labelled split, and that future cells
respect the rule that decided coordinates are never reintroduced into the
defect count.

## 5. Verification

Run

```text
python3 computations/verify_n8_chart26_degree6_branch_elimination.py
```

The checker rebuilds the complete lower weighted lead dictionaries, constructs
only the two named S-pairs, replays their exact reductions and closed-branch
certificates, proves all-positive-(x)-power lower normality from squarefree
divisibility, audits both Laurent supports, and freezes the ledger by SHA-256.
