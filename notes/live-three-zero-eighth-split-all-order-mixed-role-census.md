# The eighth split: exact all-order mixed-role census

## 1. Result and scope

Fix \(h=8\), put \(p=8+k\), and let

\[
                  M=k+18,\qquad k\geq1.                 \tag{1}
\]

This note applies the
[all-order mixed-role pair-drop theorem](live-three-zero-eighth-split-all-order-mixed-role-pair-drop-duality.md)
after the uniform higher-collision routes `H/S/C/L/Q/V` in the
[higher-split frontier](live-three-zero-higher-split-collision-frontier.md).
It gives an exact profile criterion at every \(k\), an exhaustive finite
census of the complementary-residue consequences, and the uniform
selected-lift incidence consequences.

The conclusion is sharp for this route set:

* the small-target, simple-root, Wronskian, and double-swap consequences
  occur only at \(1\leq k\leq5\) on the baseline residual ledger;
* selected-lift incidence eliminates every formal selection with
  \(0\leq d\leq4\), uniformly in \(k\);
* consequently there is no formally applicable open tail; every remaining
  profile lies outside the mixed-role selection criterion, with its exact
  count condition stated in Section 5.

Formal-selection applicability itself persists through all orders, but it
now always gives an incidence contradiction.  Profiles without a formal
selection remain, so this census does not prove the global conjecture.

## 2. Exact formal-selection test

Let \(n_i\) be the number of parts of size \(i\) in a profile \(\lambda\),
and let \(C\) be its total number of value classes.  Choose \(d\) repeated
classes at formal role two and \(s=10-2d\) singleton classes at role one.
Write \(q\in\{0,1\}\) for the number of chosen exact triples; the other
\(d-q\) repeated classes are exact doubles.  The exact applicability test is

\[
\boxed{
\begin{gathered}
 0\leq d\leq4,\qquad q\in\{0,1\},\qquad q\leq d,\\
 n_1\geq10-2d,\qquad n_2\geq d-q,\qquad n_3\geq q.
\end{gathered}}                                           \tag{2}
\]

This test includes all possible locations of the unique zero singleton.
Every pair-drop core is legal except possibly the chosen-triple/zero-
singleton pair, which is precisely the one missing edge allowed by the
theorem.

After the full role-ten selection, an exact double disappears, a selected
triple leaves a simple root, and a selected singleton disappears.  Therefore
the complementary polynomial \(A\) has

\[
 \boxed{c=C+d+q-10,\qquad
        j=n_1-10+2d+q,}                                  \tag{3}
\]

where \(c\) is its number of distinct roots and \(j\) is its number of
simple roots.  Its total degree is \(k+8\), as required.

## 3. Exact complementary and incidence closure tests

For every selection satisfying (2), the theorem supplies an injective
two-plane

\[
                         {\cal S}\subseteq
                         \mathbb C[z]_{\leq c-4}.        \tag{4}
\]

The following implications are exact.

1. **Small target (`B`).**  If \(c<5\), the target in (4) has dimension
   less than two, contradicting injectivity.

2. **Linear target with a simple root (`L`).**  If \(c=5\), then
   \({\cal S}=\mathbb C[z]_{\leq1}\).  If \(j>0\), choosing \(S=z-r\)
   at a simple complementary root \(r\) contradicts its exact residue.

3. **Simple-root Wronskian (`W`).**  For \(c\geq6\), all \(j\) simple
   roots divide the nonzero Wronskian of \({\cal S}\), whose degree is at
   most \(2c-10\).  Thus \(j>2c-10\) is impossible.  Equality receives no
   credit.

4. **Complementary-double swaps (`X`).**  Suppose \(c=5\), \(j=0\),
   \(q=0\), \(d\geq1\), and at least two of the original double classes
   remain complementary.  Varying the selected \(d\)-set compares every
   pair of double values outside a fixed anchor \(u\).  The first
   logarithmic jet puts all other double values in a fibre of

   \[
                     \Phi_u(t)={5u+t\over u^2-t^2},      \tag{5}
   \]

   whose cleared fibres have degree at most two.  Four or more original
   double classes are therefore impossible.  With exactly three original
   doubles, necessarily \(d=1\); the second logarithmic jet gives the
   [three-double closure](live-three-zero-eighth-split-k5-three-double-second-jet-closure.md).
   Thus the exact swap criterion is

   \[
   \boxed{q=0,\ d\geq1,\ c=5,\ j=0,\ n_2-d\geq2,
          \quad n_2\geq3.}                              \tag{6}
   \]

   The case \(n_2=2,d=0\) is not included.  In fact, the
   [full-residue boundary model](live-three-zero-eighth-split-k5-two-double-second-jet-boundary.md)
   shows that all ten direct residues for the resulting \(3^3 2^2\)
   complement can vanish on structurally admissible exact data.

5. **Selected-lift incidence (`I`).**  The
   [ten-singleton theorem](live-three-zero-eighth-split-all-order-ten-singleton-incidence-closure.md)
   eliminates \(d=0\), and the
   [low mixed-role theorem](live-three-zero-eighth-split-all-order-low-mixed-role-incidence-closure.md)
   eliminates \(d=1,2,3\).  The
   [four-double two-singleton theorem](live-three-zero-eighth-split-all-order-four-double-two-singleton-incidence-closure.md)
   eliminates \(d=4\).  Thus a profile is closed by incidence exactly
   when it admits any selection (2).  In count form this is

   \[
   \boxed{\begin{aligned}
   &n_1\geq10;\quad\text{or}\\
   &n_1\geq8\ \text{ and }\ (n_2\geq1\ \text{or }n_3\geq1);\quad\text{or}\\
   &n_1\geq6\ \text{ and }\ (n_2\geq2\ \text{or }(n_2\geq1,n_3\geq1));
       \quad\text{or}\\
   &n_1\geq4\ \text{ and }\ (n_2\geq3\ \text{or }(n_2\geq2,n_3\geq1));
       \quad\text{or}\\
   &n_1\geq2\ \text{ and }\ (n_2\geq4\ \text{or }(n_2\geq3,n_3\geq1)).
   \end{aligned}}                                         \tag{7}
   \]

6. **Five-double endpoint (`D5`).**  The
   [endpoint duality and residue theorem](live-three-zero-eighth-split-all-order-five-double-six-class-residue-closure.md)
   extends the kernel to five formal double layers and closes

   \[
                         C=11,\qquad n_2\geq8,\qquad n_1\geq1.         \tag{8}
   \]

Every formal selection is now an actual incidence contradiction.  Endpoint
`D5` remains separate because it can apply to profiles with no selection
(2).

## 4. Exact finite census

Classify profiles sequentially by `B`, `L`, `W`, first-jet swap `X4`,
three-double second-jet swap `X3`, incidence `I`, and endpoint `D5`.  The table applies only to profiles
labelled `R` by the earlier `H/S/C/L/Q/V` frontier, so none of the counts
duplicates those earlier routes.

\[
\begin{array}{c|r|r|rrrrrrr|r|r|r}
k&R&A&B&L&W&X4&X3&I&D5&\text{closed}&A\text{-open}&N\text{-open}\\ \hline
1&35&24&12&7&5&0&0&0&0&24&0&11\\
2&42&32&13&6&4&4&0&5&0&32&0&10\\
3&46&34&5&10&2&3&0&14&1&35&0&11\\
4&46&35&5&5&1&3&0&21&1&36&0&10\\
5&44&38&0&9&0&2&1&26&1&39&0&5\\
6&44&38&0&0&0&0&0&38&0&38&0&6\\
7&40&37&0&0&0&0&0&37&0&37&0&3\\
8&39&37&0&0&0&0&0&37&0&37&0&2\\
9&39&37&0&0&0&0&0&37&0&37&0&2\\
10&39&38&0&0&0&0&0&38&0&38&0&1
\end{array}                                               \tag{9}
\]

Here `A` means that at least one formal selection (2) exists.  `A-open`
means applicable but not closed by any test in Section 3.  `N-open` means
unclosed and without a selection (2); `D5` can close profiles in this class
because it is the separate five-double endpoint.  The former `A-open`
column

\[
                         (0,0,1,1,1,3,2,1,1,1)          \tag{9a}
\]

contained eleven profiles in the first ten rows.  The \(d=4\) theorem makes
every entry zero.

For comparison with the active fifth-order ledger, the nine `L` profiles
at \(k=5\) are

\[
\begin{gathered}
3^5 2^3 1^2,\ 3^5 2^2 1^4,\ 3^5 2 1^6,\ 3^5 1^8,\\
3^4 2^4 1^3,\ 3^4 2^3 1^5,\ 3^4 2^2 1^7,
\ 3^4 2 1^9,\ 3^4 1^{11}.                              \tag{10}
\end{gathered}
\]

The two `X4` profiles are

\[
                       3^3 2^6 1^2,\qquad 3^3 2^4 1^6,  \tag{11}
\]

and the new `X3` profile is

\[
                              3^3 2^3 1^8.              \tag{12}
\]

Several entries in (10)--(11) were already closed by companion arguments;
the table records exact recovery by the all-order mechanism and does not
assign duplicate proof credit.  Incidence now closes the adjacent profile
\(3^3 2^2 1^{10}\), despite the consistency of its direct complementary
residues.

After the first six routes in the table, the six fifth-order baseline survivors
are

\[
 4^2 3^5,\ 3^5 2^4,\ 3^4 2^5 1,\ 3^3 2^7,
 \ 3^2 2^8 1,\ 2^{11}1.                                \tag{13}
\]

Endpoint `D5` closes

\[
                              3^2 2^8 1.                \tag{14}
\]

The other five profiles in (13) already have independently accepted
companion closures.  Sequentially, `I` now closes 26 fifth-order profiles,
including the former \(d=4\) tail member \(2^{10}1^3\), while `D5` closes
the separate endpoint (14).  This is new all-order mechanism credit for
\(2^{10}1^3\), which already had an independent historical closure.  The
current \(k=5\) ledger is empty.

## 5. Why the census is uniform in \(k\)

First consider only the four complementary mechanisms `B/L/W/X`.  Every
applicable profile has at least two singleton classes.
For a baseline residual, failure of the short route `S` then gives

\[
                              \lambda_1+\lambda_2\leq7.  \tag{15}
\]

Let \(\rho=C-n_1\) be the number of repeated classes.  If \(\rho\geq2\),
(11) gives the sharp elementary cap

\[
                 M\leq n_1+3\rho+1.                    \tag{16}
\]

For \(\rho=1\), use \(M\leq n_1+6\).  Substituting (3) and the selection
bound \(n_1\geq10-2d\) gives

\[
\begin{array}{c|c}
\text{closure test}&\text{largest possible }M\\ \hline
c<5&27\\
c=5,\ j>0&28\\
j>2c-10&\leq28\\
\text{double swap}&24.
\end{array}                                               \tag{17}
\]

For example, the Wronskian inequality is exactly

\[
                         n_1+2\rho+q\leq19,              \tag{18}
\]

which combines with (16) and \(n_1\geq2\) to give the displayed cap.
For a double swap, \(n_1=10-2d\), \(\rho=5+d\), and at most three
repeated classes are not doubles; applying (15) to those classes gives
the sharper \(M\leq24\).

Since \(M=k+18\), every `B/L/W/X` closure lies at \(k\leq10\).  The exact
enumeration (9) checks that rows \(6\leq k\leq10\) contain none, so those
four complementary mechanisms give no closure for any \(k\geq6\).  This
is a finite-exception proof, not an extrapolation from a scan.

Endpoint `D5` also has no baseline occurrence beyond \(k=5\).  Under (8),
failure of the short route bounds the total profile size by 24, and the
exact sixth-order census is empty.

Incidence `I`, by contrast, is already the uniform closed-form criterion
(7).  Before the \(d=4\) theorem, the exact formally applicable open tail
was

\[
 \boxed{n_1\in\{2,3\},\qquad
   n_2\geq4\ \text{ or }\ (n_2\geq3,n_3\geq1),}          \tag{19}
\]

and every profile satisfying (19) has a \(d=4\) selection.  Indeed, any
\(d=4\) selection with \(n_1\geq4\) immediately supplies the corresponding
\(d=3\) selection, while fewer than two singleton classes cannot support
\(d=4\).  The new theorem closes (19) uniformly, so the formal open tail is
empty.

The exact no-selection condition, i.e. the negation of (7), is

\[
\boxed{
\begin{array}{c|l}
n_1&\text{no mixed-role selection}\\ \hline
0,1&\text{always}\\
2,3&n_2\leq2\ \text{or}\ (n_2=3,n_3=0)\\
4,5&n_2\leq1\ \text{or}\ (n_2=2,n_3=0)\\
6,7&n_2=0\ \text{or}\ (n_2=1,n_3=0)\\
8,9&n_2=n_3=0\\
\geq10&\text{never}.
\end{array}}                                             \tag{20}
\]

Therefore, for every \(k\geq11\), the consequences of the present theorem
suite have the following exact closed form on the baseline residual ledger:

* profiles satisfying (7), including the former tail (19), are closed by
  incidence;
* every other profile satisfies (20) and has no mixed-role selection (2).

For example, the infinite residual family \((2,1^{k+16})\) admits the
\(d=0\) selection and is now closed by incidence for every \(k\), even
though its simple-root Wronskian inequality fails for \(k\geq2\).

## 6. Exact audit

[verify_live_three_zero_eighth_split_all_order_mixed_role_census.py](../computations/verify_live_three_zero_eighth_split_all_order_mixed_role_census.py)
checks (2)--(3) by literal complement construction, audits every zero
placement and possible missing edge, enumerates every baseline residual in
(9), separates all seven closure labels and the fifth-order lists
(10)--(14), verifies the uniform caps (17), proves the closed-form
equivalences (7), (19), and (20), and checks the infinite family.  No fixed
specialization or finite-field calculation is used.
