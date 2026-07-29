# Independent audit of the two-deficient balanced-word coupling

## 1. Verdict

This is a clean-room audit of
[two-deficient-balanced-word-coupling.md](two-deficient-balanced-word-coupling.md).
Both mathematical claims are sound over \(\mathbb C\):

1. a supported \(2+2\) word on the four good sites forces the target tensor
   at the two deficient sites into the span of the two corresponding
   coherent field tensors; and
2. the nonaxial, balanced-free support boxes form exactly the ten stated
   \(S_4\times S_3\)-orbits, with \(492\) labelled boxes and orbit sizes
   \(72,72,72,24,72,72,72,12,12,12\).

The audit found no omitted endpoint order, multi-site-row term, aggregate
cancellation, transverse coordinate, or deficient-field degeneration.
The result retains its stated limited scope: it is a response-level
constraint and does not close the two-deficient branch.

The independent checker is
[audit_two_deficient_balanced_word_coupling_independent.py](../computations/audit_two_deficient_balanced_word_coupling_independent.py).
It imports no primary code and uses a different orbit canonicalization.

## 2. Reconstruction of the balanced coefficient

Fix distinct fields \(r,s\), a partition

\[
                         G=R\sqcup S,\qquad |R|=|S|=2, \tag{A1}
\]

and the good-site coordinate word \(w\) which equals \(r\) on \(R\) and
\(s\) on \(S\).  Expand the arbitrary degree-one rows by site,

\[
                         p_i=\sum_{u\in U}p_{i,u},\qquad
                         s_i=\sum_{u\in U}s_{i,u}.      \tag{A2}
\]

Consider one aggregate lift \(\lambda_{hP}A_h(P)\).  A product

\[
                         p_{i,x}s_{i,y}A_h(P)           \tag{A3}
\]

can contribute to a full six-site coefficient only if \(x,y\) are the two
distinct sites of \(P\).  A row component on a site outside \(P\) repeats
the existing \(a_h\)-factor and vanishes in the local square-zero algebra;
two row components on one site also vanish and leave the other missing
site unfilled.  Thus both endpoint orders

\[
                 (x,y)=(P_1,P_2)\quad\hbox{and}\quad(P_2,P_1) \tag{A4}
\]

are the complete list.

At each good site outside \(P\), the coordinate in (A3) is forced to be
\(h\).  Therefore the deviation set

\[
                         D_h(w)=\{v\in G:w_v\ne h\}     \tag{A5}
\]

must be contained in \(P\).  For the balanced word,

\[
                         D_r(w)=S,\qquad D_s(w)=R,      \tag{A6}
\]

and both sets have size two.  Hence the \(r\)-lift has \(P=S\), the
\(s\)-lift has \(P=R\), and neither missing pair contains a deficient
site.  For the third field \(h\notin\{r,s\}\), \(D_h(w)=G\), so it cannot
contribute.

There are consequently exactly four formal terms: the two endpoint orders
of \((r,S)\) and the two endpoint orders of \((s,R)\).  Before any
cancellation, their two aggregate scalar coefficients have the form

\[
\begin{aligned}
c_r&=\lambda_{rS}\bigl(
  [p_{i,S_1}]_s[s_{i,S_2}]_s+
  [p_{i,S_2}]_s[s_{i,S_1}]_s\bigr),\\
c_s&=\lambda_{sR}\bigl(
  [p_{i,R_1}]_r[s_{i,R_2}]_r+
  [p_{i,R_2}]_r[s_{i,R_1}]_r\bigr).
                                                               \tag{A7}
\end{aligned}
\]

Here brackets mean the selected coordinate of the arbitrary row vector.
Formula (A7) displays explicitly that parallel-source aggregation,
arbitrary row support, both endpoint orders, and cancellation are all
absorbed into \(c_r,c_s\).

Because \(P=R\) or \(S\) lies entirely in \(G\), both deficient factors of
each lift remain untouched.  Put

\[
 \kappa=
 \prod_{v\in R}\alpha_{i,v,r}
 \prod_{v\in S}\alpha_{i,v,s}\ne0.                    \tag{A8}
\]

The selected coefficient of the diagonal response is exactly

\[
 \kappa\,e_i^{(o)}\otimes e_i^{(t)}
 =
 c_r\,a_r^{(o)}\otimes a_r^{(t)}
 +c_s\,a_s^{(o)}\otimes a_s^{(t)}.                    \tag{A9}
\]

This proves the claimed span containment without requiring either
\(c_r\) or \(c_s\) to be individually nonzero.

## 3. Deficient-site degeneracies

All field vectors involved at \(o,t\) are nonzero, but their lines may
coincide.  There are only the following possibilities for the two selected
fields.

* Both pairs of local lines are distinct.  In bases adapted to them, a
  combination of the two coherent tensors has matrix
  \(\operatorname {diag}(c_r,c_s)\).  A nonzero decomposable target has
  rank one, so \(c_rc_s=0\), and it aligns with one coherent tensor.
* The two lines coincide at \(o\).  The entire span is the common
  \(o\)-line tensored with the span of the two \(t\)-vectors.  Thus the
  target's \(o\)-factor lies on that common line; no assertion of alignment
  at \(t\) is needed.
* The two lines coincide at \(t\), symmetrically.
* If they coincide at both sites, both preceding descriptions apply and
  the coherent-tensor span is itself one-dimensional.

This exhausts the dependence types of two pairs of nonzero vectors.  The
determinant is the monomial \(c_rc_s\), so there is no exceptional complex
value or field-degeneracy case hidden in the rank-one argument.

## 4. Transverse coordinates

For a fixed target \(i\) and good site \(v\), let

\[
 L_v=\operatorname {span}\{a_0^{(v)},a_1^{(v)},a_2^{(v)}\}.
                                                               \tag{A10}
\]

Choose any complement \(C_v\).  The projection of \(e_i^{(v)}\) to
\(C_v\) is either zero or one nonzero vector \(t_{i,v}\).  In the latter
case, take \(t_{i,v}\) itself as the first vector of a basis of \(C_v\).
Thus the coordinate support of this one target factor is exactly a
nonempty subset of

\[
                              \{0,1,2,T_v\}.            \tag{A11}
\]

No higher-dimensional transverse component is lost: a single vector has
only one direction after its field-span projection is fixed.  This basis
may depend on \(i\); the box census is applied separately to each target,
so no simultaneous transverse-basis claim is required.

The symbol \(T_v\) is private to its site.  In the finite checker all four
private symbols use the same integer code, but neither validity nor the
balanced-word test ever counts that code as a repeated field.  Under a
site permutation it moves with its support.  Hence the coding does not
identify transverse directions across sites.

## 5. Independent box enumeration

The checker represents each support literally as a nonempty subset of
\(\{0,1,2,T\}\), and visits all

\[
                              15^4=50{,}625             \tag{A12}
\]

labelled boxes.  It tests validity by expanding every word and requiring
some field to occur at least twice.  It detects a balanced word separately,
by choosing a field pair and a two-site placement; this does not reuse the
primary word-count predicate.

For orbit reduction, site permutations are absorbed by numerically sorting
the four relabelled support masks.  The checker then minimizes only over
the six field permutations.  This gives a clean-room canonicalization
different from the primary checker's explicit \(24\cdot6\) ordered-image
minimum.  A second literal orbit construction verifies every orbit size
and shows that the ten disjoint listed orbits exhaust all exceptional
labelled boxes.

The reconstructed counts are

\[
\begin{array}{c|r}
\text{class}&\text{labelled boxes}\\ \hline
\text{valid}&6625\\
\text{valid axial}&3681\\
\text{valid nonaxial}&2944\\
\text{valid nonaxial balanced-free}&492,
\end{array}                                             \tag{A13}
\]

and the exceptional representatives are exactly

\[
\begin{gathered}
(0,1,01,2),\ (0,1,01,T),\ (0,1,01,2T),\ (0,1,2,012),\\
(0,1,02,02),\ (0,01,01,T),\ (0,01,01,2T),\
(0,12,12,12),\\
(01,01,01,T),\ (01,01,01,2T).
\end{gathered}                                          \tag{A14}
\]

Their independently generated literal orbit sizes are

\[
                         72,72,72,24,72,72,72,12,12,12. \tag{A15}
\]

Every orbit member is valid, nonaxial, and balanced-free, their union has
size \(492\), and it equals the complete exceptional set found before
canonicalization.

## 6. A uniquely centered strengthening

This section independently audits the separate primary theorem
[two-deficient-exceptional-boundary-word-coincidence.md](two-deficient-exceptional-boundary-word-coincidence.md).

Call a word uniquely centered at field \(r\) if it has exactly two
\(r\)-positions and every other field occurs at most once.  Equivalently,
its Hamming distance from \(r^4\) is exactly two and its distance from
every other coherent field word is at least three.

If \(w\) is uniquely centered at \(r\), the same deviation-set argument as
in Section 2 leaves only the \(r\)-lift, with missing pair
\(D_r(w)\).  Both endpoint orders remain, but no second field tensor can
occur.  Since a word chosen from the target support box has a nonzero
target coefficient, its extracted equation is

\[
 \kappa_w e_i^{(o)}\otimes e_i^{(t)}
     =c_{r,w}a_r^{(o)}\otimes a_r^{(t)},\qquad
 \kappa_w\ne0.                                         \tag{A16}
\]

The left side and the field tensor are nonzero, so \(c_{r,w}\ne0\), and
the target deficient-site tensor is proportional to the coherent
field-\(r\) tensor.

The independent checker finds uniquely centered fields in the ten
representatives (A14) as follows:

\[
                         01,\ 01,\ 01,\ 012,\ 02,\
                         01,\ 01,\ 12,\ 01,\ 01.       \tag{A17}
\]

It verifies these sets from the literal words and, more strongly, checks
all \(492\) labelled exceptional boxes directly: every one has at least
two distinct uniquely centered fields.  For every representative witness,
it also reruns the formal contributor enumeration and finds exactly the two
endpoint orders of its unique field, with both deficient factors untouched.

Choose two distinct centers \(r,s\).  Equation (A16) for their respective
words makes the two nonzero decomposable tensors

\[
                a_r^{(o)}\otimes a_r^{(t)}
        \quad\hbox{and}\quad
                a_s^{(o)}\otimes a_s^{(t)}              \tag{A18}
\]

proportional to the same target tensor.  Uniqueness of the local factor
lines of a nonzero decomposable tensor therefore gives

\[
 \mathbb C a_r^{(o)}=\mathbb C a_s^{(o)},\qquad
 \mathbb C a_r^{(t)}=\mathbb C a_s^{(t)}.               \tag{A19}
\]

Thus every one of the ten nonaxial exceptional orbits forces an actual
coincidence of two field lines at both deficient sites.  This conclusion
is stronger than the two-field span containment alone and remains valid
with arbitrary aggregate cancellation.

## 7. Scope

The coefficient argument uses only a diagonal response equation and the
three coherent line fields.  It does not use \(F=q^{[2]}\), \(q^{[3]}=0\),
or the off-diagonal responses, and it does not prove that a target support
box contains a balanced word.  Axial boxes and the resulting
double-coincidence strata remain genuine downstream cases.
