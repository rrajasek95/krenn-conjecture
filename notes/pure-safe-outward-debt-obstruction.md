# Outward debt cannot close without changing a pure fibre

## 1. Outcome

The six- and eight-site Hamiltonian cycle-cover modules cannot be completed
by adding arbitrary bichromatic coordinate cells while keeping their three
pure fibres as the original singletons.

More precisely, start with either seed in
[hamiltonian-cubic-cycle-cover-countermodels.md](hamiltonian-cubic-cycle-cover-countermodels.md).
On every vertex pair, allow any additional coordinate cell \(ab\) with
\(a\ne b\), with an arbitrary nonzero weight.  Multiple new cells may lie
on the same underlying pair; no rank condition is imposed on their
aggregate.  Do not add a new monochromatic cell \(ii\).  Then every support
between the seed and this full bichromatic universe has a mixed singleton
fibre.

Thus the outward debt exposed by the cycle covers cannot be paid by any
number of pure-safe coordinate-cell additions, nor by any collection of
bichromatically decorated extra matching factors.  Any continuation of
these seeds must activate a new monochromatic cell and make at least one
pure fibre multiterm.  Merely preserving the *value* of the pure
coefficient by cancellation is not excluded here.

At six sites there is a five-word hand proof.  At eight sites exact unit
propagation produces a deletion-minimal unit-resolution core with

\[
  106\text{ variables},\qquad 107\text{ clauses},\qquad
  23\text{ mixed words}.                                 \tag{1}
\]

The dependency-free audit is
[verify_pure_safe_outward_debt.py](../computations/verify_pure_safe_outward_debt.py).
The bounded exploratory search above the eight-site seed is
[search_hamiltonian_cycle_cover_closure.py](../computations/search_hamiltonian_cycle_cover_closure.py).

## 2. Why the pure coefficients stay fixed

Write a coordinate cell on the sorted pair \(u<v\) as \(uv;ab\), where
\(a\) is the colour at \(u\) and \(b\) the colour at \(v\).  In either
seed, the only \(ii\)-cells are the edges of \(P_i\).  A term in the
constant-\(i\) word can use only \(ii\)-cells.  If all added cells satisfy
\(a\ne b\), its compatible support therefore remains exactly \(P_i\).
Consequently

\[
                         F(i^n)=\{P_i\}                  \tag{2}
\]

and assigning the seeded pure cells weight one keeps all three pure
coefficients equal to one.  The obstruction below is purely support-level:
a mixed singleton has a nonzero monomial for every choice of nonzero cell
weights.

## 3. Five-word propagation at six sites

Use the factors and endpoint words in equations (15)--(17) of the
cycle-cover note.  Six relevant seeded cells are

\[
 01;00,\quad 23;00,\quad 45;00,\qquad
 04;01,\quad 13;20,\quad 25;10.                          \tag{3}
\]

“Feasible” below means that a term uses only the seeded monochromatic cells
and arbitrary bichromatic cells.  Exact matching enumeration gives one
feasible term in each of the first three fibres:

\[
\begin{array}{c|l|c}
\text{word}&\text{unique feasible term}&\text{cell forced absent}\\ \hline
000010&01;00\;23;00\;45;10&45;10\\
001000&01;00\;23;10\;45;00&23;10\\
020000&01;02\;23;00\;45;00&01;02.
\end{array}                                               \tag{4}
\]

In each row the other two cells are seeded.  If the last cell were present,
the displayed term would be a mixed singleton.  Hence every singleton-free
extension must omit all three cells in the last column.

The word \(021000\) has exactly two feasible terms,

\[
\begin{aligned}
 A&=01;02\;23;10\;45;00,\\
 B&=02;01\;13;20\;45;00.                                 \tag{5}
\end{aligned}
\]

Term \(A\) is already disabled twice by (4).  The last two cells of \(B\)
are seeded, so presence of \(02;01\) would make \(B\) a singleton.
Therefore

\[
                         02;01\text{ is absent}.          \tag{6}
\]

Finally consider the seeded word \(021010\).  Its complete feasible fibre
has the following six terms:

\[
\begin{array}{c|l|c}
&\text{term}&\text{already absent cell}\\ \hline
0&01;02\;23;10\;45;10&01;02\\
2&01;02\;25;10\;34;01&01;02\\
3&02;01\;13;20\;45;10&02;01\\
5&02;01\;15;20\;34;01&02;01\\
10&04;01\;13;20\;25;10&\text{none: seeded}\\
11&04;01\;15;20\;23;10&23;10.
\end{array}                                               \tag{7}
\]

The seeded term in row 10 is present, while (4) and (6) disable every
possible mate.  It is an unavoidable mixed singleton.  This proves the
six-site result for the entire \(99\)-cell pure-safe universe, not merely
through a bounded number of additions.

## 4. Canonical no-singleton CNF

The same argument is larger but still entirely finite at eight sites.  It
is useful to state the exact encoding because the extracted certificate
then has a transparent meaning.

For every allowed cell \(q\), introduce a support variable \(x_q\).  For
every feasible decorated matching term \(M\) in a mixed word \(c\),
introduce \(y_{c,M}\).  Make it exactly the conjunction of its four cell
variables:

\[
\begin{aligned}
 &\neg y_{c,M}\vee x_q &&(q\in M),\\
 &y_{c,M}\vee\bigvee_{q\in M}\neg x_q.                   \tag{8}
\end{aligned}
\]

Set the twenty seed variables true.  Finally, forbid any feasible term from
being alone in its fibre:

\[
 \neg y_{c,M}\ \vee\
 \bigvee_{\substack{N\ne M\\N\text{ feasible at }c}}y_{c,N}.          \tag{9}
\]

This encoding is exact.  Given a cell support, (8) fixes precisely its
supported matching terms, and (9) says exactly that no mixed fibre has
cardinality one.  Conversely any satisfying assignment projects to such a
support.

For the eight-site seed, the pure-safe universe contains \(180\) cells.
There are \(179{,}750\) feasible mixed terms in \(6{,}558\) nonempty word
fibres.  The checker performs unit resolution on (8)--(9) without storing
the large redundant CNF.  It uses only the following equivalent rules:

1. a term is false if one of its cells is false, and true if all are true;
2. a true term forces all of its cells true;
3. a false term with three true cells forces its fourth cell false;
4. if a fibre has only one still-possible term, that term is false;
5. if a true term has only one still-possible mate, that mate is true.

After five propagation rounds the word

\[
                              12000100                   \tag{10}
\]

has one true term and every other feasible term false.

## 5. The 107-clause unit core

Tracing the reasons for (10) backward uses only 41 cell variables and 65
term variables.  Replacing each propagation step by its literal clause
from (8) or (9) gives:

\[
\begin{array}{c|r}
\text{clause kind}&\text{count}\\ \hline
\text{seed unit}&19\\
y_{c,M}\Longrightarrow x_q&42\\
\bigwedge_{q\in M}x_q\Longrightarrow y_{c,M}&23\\
\text{no-singleton propagation}&22\\
\text{final no-singleton conflict}&1\\ \hline
\text{total}&107.
\end{array}                                               \tag{11}
\]

The term variables in this core belong to only 23 mixed words.  Ordinary
unit propagation on these 107 clauses derives the empty clause.  As an
additional audit, deleting any one of the 107 clauses makes this particular
unit-resolution derivation stop without conflict.  Thus (11) is
deletion-minimal as a *unit-propagation core*; no claim of minimum general
resolution size is needed.

This is the requested outward-debt invariant.  A unique feasible term
forces one prospective repair cell absent; those absences remove terms in
nearby fibres, and the process eventually returns to a seed-supported term
with no mate.  The eight-site Hamiltonian cycle cover escapes every
pure-core counting test, but it cannot survive this full word-level
propagation unless a new monochromatic cell is introduced.

## 6. Remaining boundary

The theorem deliberately keeps the pure fibres literally unchanged.
Allowing new \(ii\)-cells may create additional constant-word matchings
whose weighted sum is still one.  That larger chart requires simultaneous
mixed cancellation and nonzero pure normalization; support propagation
alone cannot reject it, because the full 252-cell universe has many terms
in every word.  The next useful search must therefore allow diagonal cells
and retain the pure coefficient equations, rather than silently treating
pure-fibre cardinality as fixed.
