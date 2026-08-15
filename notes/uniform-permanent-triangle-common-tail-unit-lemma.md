# A permanent triangle is a six-site, tail-stable unit obstruction

## The structural lemma

Let (k) be a field with (2\ne0), and localize the diagonal coefficient
ring at every cell declared nonzero by the support.  Choose two row sites
(r,s), three column sites (x,y,z), and six same-colour support units

\[
Q=\begin{pmatrix}a&b&c\\ d&e&f\end{pmatrix}
 =\begin{pmatrix}
 q^\alpha_{rx}&q^\alpha_{ry}&q^\alpha_{rz}\\
 q^\alpha_{sx}&q^\alpha_{sy}&q^\alpha_{sz}
 \end{pmatrix}.
\]

Suppose three mixed source words have literal coefficients

\[
\begin{aligned}
F_{xy}&=U_{xy}(ae+bd),\\
F_{xz}&=U_{xz}(af+cd),\\
F_{yz}&=U_{yz}(bf+ce),
\end{aligned}                                                \tag{1}
\]

where the (U_{ij}) are supported tail monomials, hence units.  They need
not be equal and may use different decorations of the same physical tail.
Then

\[
\begin{aligned}
&cU_{xz}U_{yz}F_{xy}
 +bU_{xy}U_{yz}F_{xz}
 -aU_{xy}U_{xz}F_{yz}\\
&\hspace{35mm}=2bcd\,U_{xy}U_{xz}U_{yz}.                    \tag{2}
\end{aligned}
\]

The right side is a unit.  Therefore the three mixed coefficient rows
generate the unit ideal after support localization.  No pure normalization,
resultant, or additional Plücker equation is used.

This is just the source-labelled lift of

\[
c(ae+bd)+b(af+cd)-a(bf+ce)=2bcd.                            \tag{3}
\]

The checker
`computations/verify_uniform_permanent_triangle_common_tail_unit_lemma.py`
verifies (2) as a sparse polynomial identity and reconstructs literal clean
hafnian packets at orders (6,8,10,12,14).

## Why the minimum packet has six sites

The three permanents use the five-site (K_{2,3}) core

\[
\{r,s\}\mathbin{|}\{x,y,z\}.
\]

In the (xy) row, the unused column (z) must still be covered by a full
perfect matching; similarly (y) and (x) must be covered in the other two
rows.  One completion hub (h), with supported spokes
(p_x=q_{hx},p_y=q_{hy},p_z=q_{hz}), is the smallest simultaneous
completion.  Thus the minimal source packet has six active sites and nine
active cells.  With a forced decorated matching (T) on another (2q)
sites and monomial (\tau=q_T), the rows are

\[
\begin{aligned}
F_{xy}&=\tau p_z(ae+bd),\\
F_{xz}&=\tau p_y(af+cd),\\
F_{yz}&=\tau p_x(bf+ce).
\end{aligned}                                                \tag{4}
\]

Hence the obstruction is stable for every even order

\[
N=6+2q,\qquad q\ge0.                                        \tag{5}
\]

Multiplying by a common tail changes neither the three-row identity nor its
unit conclusion; it merely multiplies the right side of (2) by (\tau^3).

## Exact source-isolation criterion

The factorization (1) is guaranteed by the following word-filtered support
condition.  For each pair (ij\in\{xy,xz,yz\}), let (k) be the omitted
column and choose a mixed word (w_{ij}).  In the graph retaining only cells
compatible with (w_{ij}), require:

1. every spectator-tail vertex has degree one to its mate in (T);
2. (h) and (k) form a forced component through the supported spoke
   (p_k);
3. the remaining four vertices (r,s,i,j) have exactly the two perfect
   matchings of the displayed (K_{2,2}); and
4. all matrix, spoke, and tail cells in these matchings are nonzero.

Every compatible full matching then splits uniquely as (T\sqcup hk)
times one of the two (K_{2,2}) matchings, proving (1) term by term.  This is
an equality in the original coefficient row, not a projection onto selected
occurrences.

The degree-one formulation is sufficient, not necessary.  The exact
necessary-and-sufficient hypothesis consumed by the algebra is simply the
three literal factorizations (1), with unit (U_{ij}) and mixed rows.

## The doubled-(K_4) support is an instance

For the canonical support-28 design, take

```text
row sites       r,s = 0,3
column sites    x,y,z = 1,2,5
completion hub  h = 4
physical tail   67
core colour     alpha = 1
```

Then

\[
(a,b,c,d,e,f)=
(x_{01}^1,x_{02}^1,x_{05}^1,x_{13}^1,x_{23}^1,x_{35}^1),
\]

and the three tail units are

\[
U_{xy}=x_{45}^0x_{67}^2,\quad
U_{xz}=x_{24}^2x_{67}^0,\quad
U_{yz}=x_{14}^0x_{67}^2.
\]

The words are respectively `11110022`, `11212100`, and `10110122`.
Thus the earlier three-binomial sign obstruction is precisely (2) in a
doubled-(K_4) chart.  Notice that edge (67) is a common physical tail but
its decoration changes in the middle word; equality of the three
(U_{ij}) is not part of the lemma.

## What a terminal ear/core must supply

A graph-theoretic theta or (K_{2,3}) minor is not enough.  To force the
unit obstruction from a terminal ear/core, one needs exactly these four
source statements:

1. **Bright theta:** after contracting already forced unit paths, two poles
   and three exposed ports give the six nonzero cells of one same-colour
   (K_{2,3}).
2. **Completion:** omitting any one port leaves a supported hub/spoke and a
   perfect matching on the remaining tail sites.
3. **Mixedness:** the three completions live in mixed output words, so their
   coefficients vanish rather than being pure target normalizations.
4. **Private cofactor isolation:** in each of those words, terminality makes
   the completion forced and excludes every matching beyond the two local
   (K_{2,2}) choices.

Under these hypotheses the terminal core contains a permanent triangle and
is impossible by (2).  If the completion in item 2 is absent, the core is in
the existing Tutte/Hall tail-debt branch.  If item 4 fails, the row is a
genuine multiterm-contamination branch and cannot be silently treated as a
binomial.  If item 3 fails, one has a pure normalization row, not a zero row.

Consequently, the exact remaining forcing theorem is:

> Every terminal theta/ear surviving support lowering and the Tutte/Hall
> exit admits three mixed, private word-filtered cofactors as above, or its
> first nonprivate cofactor is landed by the multiterm/Fitting alternative.

This private-cofactor statement is strictly stronger than ordinary ear
terminality and is not proved here.

## Sharp counterguard to graph-only forcing

Keep the six bright (K_{2,3}) cells and the three completion spokes, but
add the colour-(\alpha) cells (g=q^\alpha_{rs}) and
(k=q^\alpha_{xy}).  Literal enumeration of the six-site output words
`000011`, `000101`, and `001001` then adds a third compatible matching only
to the first row:

\[
ae+bd+gk=0,\qquad af+cd=0,\qquad bf+ce=0.                   \tag{6}
\]

The all-unit assignment

\[
a=b=c=d=e=g=1,\qquad f=-1,\qquad k=-2
\]

solves all three equations over characteristic zero.  Thus even the literal
(K_{2,3}) support core does not force a unit when a word has an extra
matching.  This proves that private word isolation is load-bearing, rather
than editorial bookkeeping.

## Scope

The lemma is uniform in even (N), arbitrary tail length, and arbitrary
row-specific unit completions.  It applies to diagonal, occurrence-labelled
hafnian coefficient rows over characteristic different from (2).  It does
not force a permanent triangle from an uncoloured matching minor, handle an
extra compatible matching, or extend directly to off-diagonal endpoint
weights without a corresponding source-row factorization.

Run all modes:

```text
python3 computations/verify_uniform_permanent_triangle_common_tail_unit_lemma.py --mode structural
python3 -O computations/verify_uniform_permanent_triangle_common_tail_unit_lemma.py --mode full
python3 -I -S computations/verify_uniform_permanent_triangle_common_tail_unit_lemma.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
fc6821a5ff6140cc76e2769916c17c7115445fa1419a9bd708c6e7abd70f6176
```
