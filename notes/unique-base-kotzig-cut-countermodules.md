# Unique-base Kotzig cuts do not support a crossing descent

## 1. Outcome

Let \(A_{uv}(i,j)\) denote the aggregate decorated cell on the ordered
endpoints \(u<v\), and let \(G_{00}\) be the graph of pairs for which
\(A_{uv}(0,0)\neq0\).  If the all-zero coefficient is represented by one
nonzero perfect-matching term, then \(G_{00}\) has a unique perfect
matching.  Kotzig's theorem supplies a matching bridge and hence an odd
shore with only one nonzero \(00\) cell across it.

The hoped-for next step is false: the complete mixed equations do not, even
on one exact binary face, force that shore to be tight.  There is an exact
six-site binary source for \(\Delta_{6,2}\) with a unique all-zero matching
and a three-cross cancellation term across the Kotzig shore.

The genuinely ternary boundary is equally sharp.  A nine-cell prism source
has all three constant fibers unique and normalized and has every binary
face exactly equal to \(\Delta_{6,2}\).  Its only error is one ternary
three-cross term.  All fourteen possible underlying cancellation mates of
that term preserve the unique all-zero matching and create new mixed
singleton fibers whose sole matchings cross the shore once.

This first \(3\to1\) step is not a well-founded descent.  A rational
thirteen-cell repair web cancels the ternary error and then cancels one of
the crossing-one singleton errors.  It preserves the unique all-zero
matching but creates two new crossing-one singleton errors.  Thus the
proposed alternative

> every mate either creates a second all-zero perfect matching or creates a
> mixed singleton of strictly smaller shore-crossing complexity

already fails on the second four-cycle repair.  Exact enumeration also
shows that four new cells are minimal for such a two-stage repair.

These countermodules are not three-color Krenn counterexamples: the final
thirteen-cell source still has three explicitly listed mixed singleton
errors.  They prove that uniqueness of one constant term, the two other
constant equations, and even all pairwise binary mixed equations do not
make the Kotzig cut collapsible.  A proof must couple several genuinely
ternary crossing-one fibers at once.

## 2. An exact binary non-tight Kotzig shore

On vertices \(0,\ldots,5\), put the following \(2\times2\) aggregate
matrices, with every omitted matrix zero:

\[
\begin{array}{c|c@{\qquad}c|c}
01&E_{00}&23&E_{00}+E_{11}\\
02&-E_{01}&13&E_{01}\\
45&E_{00}&05&E_{11}\\
12&E_{11}&34&E_{11}.
\end{array}                                                \tag{1}
\]

The underlying eight-edge support has exactly three perfect matchings,

\[
\begin{aligned}
 M_0&=01\mid23\mid45,\\
 M_*&=02\mid13\mid45,\\
 M_1&=05\mid12\mid34.                                   \tag{2}
\end{aligned}
\]

The \(E_{00}\) choice on edge \(23\) makes \(M_0\) contribute
\(e_0^{\otimes6}\), while its \(E_{11}\) choice contributes the word
\(001100\).  The matching \(M_*\) contributes the same word with coefficient
\(-1\), and \(M_1\) contributes \(e_1^{\otimes6}\).  Hence, coefficient by
coefficient,

\[
                         H_6(A)=\Delta_{6,2}.              \tag{3}
\]

The graph \(G_{00}\) consists of the three edges of \(M_0\), so \(M_0\) is
its unique perfect matching.  Take

\[
                              S=\{0,1,5\}.                 \tag{4}
\]

The only nonzero \(00\) cell across \(\delta(S)\) is \(45_{00}\).  However,

\[
 \bigl(|M_0\cap\delta(S)|,
       |M_*\cap\delta(S)|,
       |M_1\cap\delta(S)|\bigr)=(1,3,1).                 \tag{5}
\]

Thus the cut is not tight even though the full binary target identity,
including every mixed zero coefficient, holds exactly.  Any argument that
tries to tighten the Kotzig shore separately on the \(0,1\) and \(0,2\)
faces is therefore invalid.

## 3. The pairwise-exact ternary prism

Use the three one-factors

\[
\begin{aligned}
 P_0&=01\mid23\mid45,\\
 P_1&=05\mid12\mid34,\\
 P_2&=03\mid15\mid24,                                   \tag{6}
\end{aligned}
\]

and put the unit cell \(E_{rr}\) on every edge of \(P_r\), with no other
cells.  Each pairwise union \(P_r\cup P_s\) is a Hamilton six-cycle, so
each principal two-color restriction is exactly

\[
                         e_r^{\otimes6}+e_s^{\otimes6}.    \tag{7}
\]

The union in (6) has exactly one further perfect matching,

\[
                   R=03\mid12\mid45,                      \tag{8}
\]

whose coloring is

\[
                   c=(2,1,1,2,0,0).                       \tag{9}
\]

Consequently the complete tensor is

\[
                  H_6(A)=\Delta_{6,3}+e_c.                \tag{10}
\]

In particular the three constant fibers are singleton fibers of coefficient
one, every binary mixed coefficient is zero, and (9) is the only failed
coefficient among all \(3^6\) words.

For the same shore (4), the unique \(00\) crossing cell is again \(45_{00}\),
and

\[
 \bigl(|P_0\cap\delta(S)|,|P_1\cap\delta(S)|,
       |P_2\cap\delta(S)|,|R\cap\delta(S)|\bigr)
                         =(1,1,1,3).                      \tag{11}
\]

Thus the first genuinely ternary error is exactly the three-cross sector
which a cut descent would have to remove.

## 4. Classification of every first mate

Fix the nine cells (6), and let \(N\ne R\) be any of the other fourteen
underlying perfect matchings.  Add the \(c\)-decorated occurrences of \(N\)
which are not already present.  These are the only cells needed to make
\(N\) a cancellation mate for (9).

No new occurrence is diagonal.  Indeed, the three same-color pairs of the
word \(c\) are precisely \(03,12,45\), and their \(22,11,00\) cells are
already present in (6).  Therefore all three constant fibers, in particular
the unique all-zero fiber, remain unchanged.

There are four exact cases:

\[
\begin{array}{c|c|c|c}
|N\cap\delta(S)|&\text{new cells}&
 \text{new mixed singleton fibers}&\text{matchings }N\\ \hline
1&2&2&P_0,P_1,P_2\\
3&2&2&02|13|45,\ 03|14|25,\ 04|12|35\\
3&3&3&02|14|35,\ 04|13|25\\
1&3&5&01|24|35,\ 01|25|34,\ 02|15|34,\\
 &&&04|15|23,\ 05|13|24,\ 05|14|23.
\end{array}                                                \tag{12}
\]

**Lemma 4.1 (first-mate classification).**  In every row of (12), the
\(c\)-fiber after the addition consists exactly of \(R,N\).  Every new
mixed singleton displayed in the third column has a sole underlying
matching \(L\) with

\[
                         |L\cap\delta(S)|=1.              \tag{13}
\]

Moreover the new cells can be assigned nonzero weights so that \(R\) has
weight \(+1\) and \(N\) has weight \(-1\), while all three constant
coefficients remain one.

**Proof.**  The fifteen perfect matchings on six vertices are obtained by
choosing the mate of vertex \(0\) and then one of the three matchings of the
remaining four vertices.  Removing \(R\) and sorting the remaining fourteen
by crossing count and by whether they share an edge with \(R\) gives the
four rows of (12).  Direct compatibility with the nine cells (6) gives the
third column and (13).  This is a finite proof with respectively
\(3,3,2,6\) matchings in the four rows.

Every occurrence shared by \(R\) and \(N\) already has weight one.  Give all
new occurrences weight one except for one, which is assigned weight
\(-1\).  Then the two terms in the \(c\)-fiber cancel.  Since all new cells
are off-diagonal, none enters a constant fiber. \(\square\)

Thus Lemma 4.1 validates the first apparent descent step: the three-cross
error always pays for at least two crossing-one singleton errors.  The next
section shows why this is not inductive.

## 5. A smallest stalled two-square repair

Start from (6), retain unit weight on its nine cells, and add

\[
\begin{array}{c|rrrr}
\text{cell}&01_{21}&23_{12}&02_{01}&13_{02}\\ \hline
\text{weight}&-1&1&-1&1.
\end{array}                                                \tag{14}
\]

There are only eight nonempty coloring fibers.  Their complete exact list is

\[
\begin{array}{c|c|c}
\text{word}&\text{underlying matching terms}&\text{coefficient}\\ \hline
000000&P_0&1\\
111111&P_1&1\\
222222&P_2&1\\
211200&R,\ P_0&1-1=0\\
001200&P_0,\ 02|13|45&1-1=0\\
210000&P_0&-1\\
021112&02|15|34&-1\\
102221&05|13|24&1.
\end{array}                                                \tag{15}
\]

The first binomial in (15) is the repair of the original three-cross
residual.  It uses the alternating four-cycle

\[
            (03|12)\longleftrightarrow(01|23).             \tag{16}
\]

After that repair, \(001200\) is a singleton carried by the crossing-one
matching \(P_0\).  The second binomial repairs it through the other
alternating four-cycle

\[
            (01|23)\longleftrightarrow(02|13).             \tag{17}
\]

The mate \(02|13|45\) crosses \(S\) three times.  Nevertheless the two new
singleton errors created by (17), \(021112\) and \(102221\), and the
unrepaired companion \(210000\), are all carried by matchings crossing
\(S\) exactly once.  The all-zero graph is unchanged and still has only
\(P_0\).

This directly refutes strict descent at its minimum positive value.  When
the singleton \(001200\) of complexity one is repaired, no second all-zero
matching appears and the new singleton complexities are again one, not
strictly less than one.

There is also a sharp support-minimality statement.  Any first mate for
\(211200\) requires at least two new cells.  Exhausting its new
crossing-one singleton fibers and all their possible mates shows that a
second repair which preserves the unique all-zero matching and creates a
further singleton requires at least four new cells in total.  Construction
(14) attains four.  This is support minimality within the natural
cell-additive repair chart; it does not assert minimality under operations
which first cancel an existing aggregate coordinate to zero.

## 6. Exact audit and consequence

[verify_unique_base_kotzig_cut_countermodules.py](../computations/verify_unique_base_kotzig_cut_countermodules.py)
uses only integer and rational arithmetic.  It:

1. checks all \(2^6\) coefficients of (1)--(3);
2. checks all \(3^6\) coefficients and all three binary faces of (6)--(10);
3. enumerates all fourteen first mates and verifies exactly the four rows of
   (12), including every new singleton and its cut count;
4. checks all \(3^6\) coefficients in (15); and
5. exhausts every two-stage cell-additive repair to certify the four-new-cell
   minimum.

The surviving route is consequently narrower than "unique constant term
implies a tight Kotzig cut."  Even full binary cancellation can move through
the three-cross sector, and the ternary prism reaches crossing complexity
one without contradiction.  Any continuation must find an algebraic
incompatibility among several crossing-one fibers, rather than assign a
strictly decreasing crossing number to one chosen cancellation mate.
