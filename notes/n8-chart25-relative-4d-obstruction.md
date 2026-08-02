# The missing \(4D\) is a relative target class, not a diagonal boundary

This is an exact classification on the frozen chart-25 five-row fibre. It
does not construct the global source-provenant jet comparison needed for the
curvature branch, and it does not prove Krenn's conjecture.

## 1. Outcome

Write the actual rows over the frozen common factor as

\[
 A_1,A_2,A_3,A_4,D,
 \qquad
 \lambda(A_i)=-\frac14,\qquad \lambda(D)=\frac14 .       \tag{1}
\]

The 14 individually labelled mixed-source columns over this \(D\)-centre
occur with multiplicities \((3,4,4,3)\). After projection to the five rows,
every column on the \(i\)-th edge has

\[
                         \partial e_{i,j}=A_i+D.         \tag{2}
\]

Thus the local source image has rank four and is exactly

\[
                         \ker\lambda\subset C_0.         \tag{3}
\]

The literal transferred packet and invariant-quotient packet differ by

\[
 \begin{aligned}
 b&=-A_1-A_2-A_3-3D,\\
 q&=-A_1-A_2-A_3+D,\\
 q-b&=4D.                                                \tag{4}
 \end{aligned}
\]

Here \(\lambda(b)=0\), while

\[
                         \lambda(q)=\lambda(4D)=1.       \tag{5}
\]

Consequently \(4D\) is the generator of the one-dimensional source
cokernel on this fibre. The three candidate mechanisms have sharply
different outcomes.

1. An ordinary label-diagonal Koszul tensor product does **not** produce
   \(4D\).
2. Reynolds/orbit transfer sends \(4D\) to the same nonzero invariant
   obstruction; it does **not** turn it into a boundary.
3. The target mapping cylinder contains the formal relative cell

   \[
                            d(4sD)=4D-\tau,              \tag{6}
   \]

   with an extended augmentation and \(d^2=0\). Formula (6) says that the
   packet represents the target generator \(\tau\); it is not a new hafnian
   source identity.

Therefore the honest interpretation of the missing operation is presently
the **curvature obstruction branch**. Calling (6) a correction inside the
source complex would be circular.

## 2. Why ordinary label-diagonal Koszul cells cannot supply it

Let

\[
 P=\mathbb Q[\ell_1,\ldots,\ell_r],\qquad
 K=K_P(\ell_1,\ldots,\ell_r),                           \tag{7}
\]

where the \(\ell_i\) are source-label differences, and extend the frozen
source complex by the ordinary tensor product

\[
                         C_P\otimes_P K.                 \tag{8}
\]

Let \(\epsilon:P\to\mathbb Q\) be physical diagonal specialization,
\(\epsilon(\ell_i)=0\). A total degree-one chain has the form

\[
                    z=c+\sum_i v_i\varepsilon_i,
       \qquad c\in C_1\otimes P,\qquad v_i\in C_0\otimes P. \tag{9}
\]

The tensor differential gives

\[
       (1\otimes\epsilon)d_{\rm tot}z
             =\partial_C c(0)+\sum_i\epsilon(\ell_i)v_i(0)
             =\partial_C c(0).                          \tag{10}
\]

Hence the physical degree-zero boundary image after specialization is still
\(\operatorname{im}\partial_C\). Every positive-exterior Koszul boundary
carries at least one label difference and disappears under \(\epsilon\).
Higher exterior cells enforce the usual syzygies but cannot enlarge the
degree-zero image.

Equivalently, \(\lambda\otimes\epsilon\) kills every total boundary in (8),
whereas it takes \(4D\) to one. This proves the no-go for any number of
ordinary diagonal labels, not only the four labels used by the checker.
The checker verifies the full Koszul signs and

\[
                         d_{\rm tot}^{\,2}=0             \tag{11}
\]

on all \(16\) exterior subsets for four labels. After specialization the
boundary rank is four, and adjoining \(4D\) raises it to five.

This argument is deliberately scoped. It does not rule out a module whose
source differential itself couples to the label ideal, a non-flat
specialization which creates a new source kernel, or a higher comparison map
with nonzero Taylor component. Those are precisely the possible genuine
enlargements; they are not the ordinary complex (8).

## 3. Orbit transfer preserves the obstruction

The exact chart-25 support stabilizer \(G\) has order eight. The actual row
\(D\) has orbit size four and stabilizer size two. Therefore Reynolds
averaging gives

\[
 {1\over |G|}\sum_{g\in G}g(4D)
                    =\sum_{D'\in G D}D'.                \tag{12}
\]

Every row on the right has actual dual weight \(1/4\), so (12) still pairs
to one. In the invariant quotient it is the canonical \(D\)-coordinate,
whose exact quotient functional value is \(+1\).

The checker retains group multiplicities and verifies, on all 14 actual
source labels over the frozen centre,

\[
                         R\partial=\partial R,
       \qquad \lambda(R\partial e)=0.                   \tag{13}
\]

This is also forced abstractly: in characteristic zero, invariants and
coinvariants for a finite group are exact, and Reynolds is a chain map.
Orbit transfer can expose the quotient multiplicity which hid \(A_4\), but
it cannot manufacture a boundary with nonzero \(\lambda\)-value.

## 4. The exact target mapping cylinder

Let \(T=\mathbb Q\tau\) be concentrated in degree zero and regard

\[
                         a=\lambda:C\longrightarrow T   \tag{14}
\]

as the target augmentation. The relevant relative object is the graph cone,
equivalently the algebraic mapping cylinder of \(a\). In the degrees used
here it is

\[
\begin{array}{c|c}
0&C_0\oplus T\\
1&C_1\oplus sC_0\\
2&sC_1,
\end{array}                                             \tag{15}
\]

with differential

\[
 \begin{aligned}
 d(e)&=\partial e,\\
 d(sv)&=v-a(v)\tau,\\
 d(se)&=e-s(\partial e).                                \tag{16}
 \end{aligned}
\]

The last line retains the exact source label on \(e\). It gives

\[
 d^2(se)=\partial e-\bigl(\partial e-a(\partial e)\tau\bigr)=0, \tag{17}
\]

because \(a\partial=0\). Define the extended augmentation by

\[
             \widehat a(v+c\tau)=a(v)+c.                \tag{18}
\]

Then \(\widehat a d=0\), and (1), (16) give exactly

\[
                         d(4sD)=4D-\tau.                 \tag{19}
\]

Likewise

\[
                         d(sq)=q-\tau.                   \tag{20}
\]

Thus \(q\) and \(\tau\) represent the same absolute information. The
mapping cylinder has not proved \(q=0\); it has made the nonzero target value
of \(q\) into a literal relative boundary. This construction exists for
every augmented complex and is therefore formal. In particular, the
coefficient four in (19) is chosen because \(a(D)=1/4\). It cannot be cited
as independent evidence for a source relation.

The plain cone of \(a\), after the \(C_0\) copy is collapsed, has shifted
rows mapping only to \(T\); it does not even have a retained \(C_0\)
projection equal to \(4D\). The projected vector in (19) belongs to the
graph/mapping-cylinder presentation.

The exact audit constructs (15)--(18) over the complete boundaries of all
14 actual source columns. Their union has 1,145 individual monomial rows.
It checks every degree-two identity (17), so the result is not obtained by
identifying the three possible lifts over one incidence edge.

## 5. Minimality and the next genuine datum

The five-row dimensions make the minimality transparent. The old boundary
rank is four in a five-dimensional row space, and \(\lambda\) spans its
cokernel. If one merely adjoins a degree-one generator \(r\) with

\[
                              dr=4D,                    \tag{21}
\]

then no extension of the physical augmentation can kill boundaries, since
\(a(dr)=1\). Preserving the target therefore requires at least one new
degree-zero direction. One target row and one graph cell suffice:

\[
                    dr=4D-\tau,\qquad \widehat a(\tau)=1. \tag{22}
\]

The resulting local degree-zero space has dimension six, boundary rank five,
and one-dimensional homology detected by \(\widehat a\). So (22) does not
kill the obstruction; it names it.

A legitimate source derivation of the relative operation must now provide
more than (22). It must construct a source-provenant label/jet complex \(J\)
and a coherent comparison into (15) whose first nonzero mixed component
lands on \(4sD\) (up to old source boundaries), while inducing the target
component \(-\tau\) rather than inserting it by definition. Its source-label
changes must lift through degree two as in the third line of (16).

Equivalently, the required enlargement must have a nonzero mixed
source--diagonal transgression to the one-dimensional cokernel (3).
Ordinary diagonal Koszul tensoring has zero transgression by (10), and orbit
transfer has zero transgression by (13). A non-flat coupled module,
principal-parts/\(A_\infty\) comparison, or an independently derived target
augmentation component is the minimal remaining kind of mathematics.

Until such a comparison is constructed, (19) belongs on the obstruction
side of the curvature--Bockstein dichotomy: the exact ternary source kills
ordinary source boundaries, while the \(4D\) class has target value one.

## 6. Exact verification

Run

~~~text
python3 computations/verify_n8_chart25_relative_4d_obstruction.py
python3 -O computations/verify_n8_chart25_relative_4d_obstruction.py
python3 -I computations/verify_n8_chart25_relative_4d_obstruction.py
python3 -S computations/verify_n8_chart25_relative_4d_obstruction.py
~~~

The frozen exact ledger digest is
edc1b143d174ea6ddd0d449080aadc8084b785dce85f9a96c3b0827ec1ffcac4.
