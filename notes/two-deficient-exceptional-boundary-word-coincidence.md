# Exceptional two-defect boxes force the same coincidence at both bad sites

## 1. Result

Use the setup of
[the balanced-word coupling theorem](two-deficient-balanced-word-coupling.md):
\(U=G\sqcup\{o,t\}\), \(|G|=4\), the three field vectors are independent
at every good site, and

\[
 F=\sum_{r=0}^2\sum_{P\in\binom U2}\lambda_{rP}
       \bigotimes_{u\notin P}a_r^{(u)}
\]

satisfies the nine exact responses \(p_i s_jF=\delta_{ij}X_i\).
No independence is assumed at \(o,t\), and no common-power equation is
used here.

The preceding theorem classifies the nonaxial good-site target boxes which
contain no balanced \(2+2\) word into ten orbits.

**Theorem 1.1 (double-bad-site coincidence).**  If the good-site support
box of a target \(X_i\) belongs to one of those ten exceptional orbits,
then there are distinct fields \(r,s\) such that

\[
 \begin{aligned}
 e_i^{(o)}\otimes e_i^{(t)}
   &\in\mathbb C^*
      \bigl(a_r^{(o)}\otimes a_r^{(t)}\bigr),\\
 e_i^{(o)}\otimes e_i^{(t)}
   &\in\mathbb C^*
      \bigl(a_s^{(o)}\otimes a_s^{(t)}\bigr).
 \end{aligned}                                                   \tag{1}
\]

Consequently the same two field lines coincide at both deficient sites:

\[
                   L_r^{(o)}=L_s^{(o)},\qquad
                   L_r^{(t)}=L_s^{(t)}.                          \tag{2}
\]

In orbit 4 below, (1)--(2) hold for every pair of the three fields.

This retains arbitrary aggregate coefficients, both endpoint orders,
multi-site response rows, and complex cancellation.

## 2. Unique boundary words

Call a good-site word **uniquely \(r\)-centred** if it contains exactly
two occurrences of \(r\) and no other field occurs twice.  It is then at
distance exactly two from \(r^4\) and outside both other radius-two field
balls.  A transverse symbol, when present, is written \(T\).

The ten support representatives have the following literal witnesses:

\[
\begin{array}{c|c|c}
 &\text{supports}&\text{unique centres and witness words}\\ \hline
1&0,1,01,2&0:0102,\quad1:0112\\
2&0,1,01,T&0:010T,\quad1:011T\\
3&0,1,01,2T&0:0102,\quad1:0112\\
4&0,1,2,012&0:0120,\quad1:0121,\quad2:0122\\
5&0,1,02,02&0:0102,\quad2:0122\\
6&0,01,01,T&0:001T,\quad1:011T\\
7&0,01,01,2T&0:0012,\quad1:0112\\
8&0,12,12,12&1:0112,\quad2:0122\\
9&01,01,01,T&0:001T,\quad1:011T\\
10&01,01,01,2T&0:0012,\quad1:0112.
\end{array}                                                    \tag{3}
\]

Every displayed word chooses one symbol from each displayed support.

## 3. Coefficient extraction

Fix a uniquely \(r\)-centred word \(w\), and let \(P_w\subset G\) be its
two non-\(r\) positions.  Extract the coefficient of \(w\) on the four
good sites from the diagonal response \(p_i s_iF=X_i\).

A field-\(r\) lift contributes only if its missing pair contains both
deviations of \(w\), hence only when that pair is exactly \(P_w\).  A lift
from either other field differs from \(w\) at at least three good sites
and cannot contribute.  Both response rows therefore occupy the two sites
of \(P_w\), in the two possible endpoint orders, while the factors at
\(o,t\) remain untouched.  The extracted coefficient is

\[
 \kappa_w e_i^{(o)}\otimes e_i^{(t)}
  =c_w a_r^{(o)}\otimes a_r^{(t)},\qquad \kappa_w\ne0.             \tag{4}
\]

The target coefficient \(\kappa_w\) is nonzero because \(w\) belongs to
the support box.  Thus (4) also forces \(c_w\ne0\), and it gives the first
line of (1).  Apply the same extraction to the witness of the second
centre in (3).  Proportional nonzero decomposable tensors have
proportional factors at every named site, which proves (2).  The three
witnesses in orbit 4 make all three field lines coincide at both sites.

No zero matching fibre has been split into summands: the good-coordinate
word isolates one complete field module and one aggregate missing-pair
coefficient before (4) is read.

## 4. Exact audit and scope

The standalone checker
[verify_two_deficient_exceptional_boundary_word_coincidence.py](../computations/verify_two_deficient_exceptional_boundary_word_coincidence.py)
reconstructs all ten boxes from their support masks, verifies every word in
(3), and independently enumerates all fields, all fifteen missing pairs,
and both row endpoint orders.  For each witness it finds exactly four
ordered formal terms in a two-centre comparison, namely two
endpoint orders for each centre.  Equivalently, each individual witness
has exactly two terms: one field, one all-good missing pair, and the two
endpoint orders.

This theorem does not eliminate the double-coincidence strata in (2).
It reduces every nonaxial balanced-free target to them.  The remaining
two-defect response classification therefore splits into:

1. balanced-word targets, governed by the two-point Segre constraint;
2. the exceptional boxes, now confined to a field coincidence at both bad
   sites; and
3. axial boxes, whose exact-distance-two boundary words or higher axial
   multiplicities still have to be coupled across the three targets.
