# A genuine full-nine midpoint row retains its response companion

## Outcome

The proposed normalization

\[
                         \sum_{|S|=3}D_S=0              \tag{1}
\]

from
[`h3-grade3-middle-attaching-target-obstruction.md`](h3-grade3-middle-attaching-target-obstruction.md)
is not the literal attaching statement in a common full-nine packet.  It is
the correct defect for an **internal diagonal source** considered separately
from the selected endpoint response.  Once both pieces belong to one source,
every mixed word also contains the response companion.

Fix an off-diagonal selected row `(p,a;q,b)`, `a != b`, let
`alpha=A_pq(a,b)`, and use the notation of
[`h3-three-set-source-relative-terminal-class.md`](h3-three-set-source-relative-terminal-class.md).
For `w_S=e^S c^{S^c}`, put

\[
 \Theta_S^{\rm src}=\operatorname {haf}(q^{w_S}),\qquad
 \Theta_S^{\rm can}=\Theta_S(2\alpha R,R,Q),           \tag{2}
\]

\[
 D_S=\Theta_S^{\rm src}-\Theta_S^{\rm can},\qquad
 M_S=[R^{w_S}(q^{w_S})^{[2]}].                         \tag{3}
\]

Write

\[
 C=\sum_S\Theta_S^{\rm can}=8\chi,\qquad
 D=\sum_SD_S,\qquad M=\sum_SM_S.                       \tag{4}
\]

The twenty literal target-zero source rows give exactly

\[
 \boxed{\alpha(C+D)+M=0.}                              \tag{5}
\]

They do **not** give `Theta_S^src=0`.  Even a diagonal mixed row has the
form

\[
 d_{ii}\Theta_S^{\rm src}+M_{ii,S}=0,                 \tag{6}
\]

because its mixed GHZ target is zero.  The response term in (6) cannot be
dropped.  The pure diagonal anchor is instead

\[
 d_{ii}\operatorname {haf}(q^{i^6})+M_{ii,i^6}-1=0,   \tag{7}
\]

so complete target bookkeeping retains an explicit `-1`; it supplies no
coefficientwise identification between (6) and the internal hafnian.

Consequently (1) is neither a literal consequence of the displayed source
rows nor sufficient for the terminal conclusion.  If `D=0`, (5) merely
sets

\[
                              M=-\alpha C,              \tag{8}
\]

and permits `C != 0`.  The exact missing source-relative row is

\[
 \boxed{\mathcal K:=\alpha D+M=0.}                     \tag{9}
\]

Subtracting (9) from (5) gives `alpha C=0`.  On the localized selected
chart `alpha != 0`, this gives `C=8chi=0`; combined with the Hamming-two
relation it also gives `Q_3=0`.

Thus the genuine normalization target is the companion-corrected class
from commit `cd52b2b`, not the internal defect `D` alone.

## 1. Exact H2 normalization

The Hamming-two relation is

\[
                         \alpha Q_2+3Q_3=0.             \tag{10}
\]

Since `C=8(alpha Q_2+Q_3)`, it gives

\[
                              C+16Q_3=0.                \tag{11}
\]

Equations (5) and (11) are the entire honest three-coordinate attaching
presentation before a new adjacent-chart comparison is supplied.  In
coordinates `(C,D,M,Q_3)` their rows are

\[
                 (\alpha,\alpha,1,0),\qquad(1,0,0,16). \tag{12}
\]

Adjoining `D=0` leaves the exact separator

\[
                         (C,D,M,Q_3)=(1,0,-\alpha,-1/16), \tag{13}
\]

so both the clean and terminal coordinates remain nonzero.  In contrast,
adjoining `K=0`, whose row is `(0,alpha,1,0)`, makes the clean row
`(1,0,0,0)` and terminal row `(0,0,0,1)` consequences of (12).

This is a formal source-relative counterguard, not a claimed common
full-nine coefficient point.  It proves exactly that the literal rows and
targets under discussion do not contain (1) or (9) in their linear source
span.  The full nonlinear full-nine system could still force (9); that is
the open positive Bianchi problem.

## 2. The absent physical provenance

Every term of (5) has a literal source label:

* `alpha Theta_S^src + M_S` is row `(p,a;q,b)` at the word
  `e^S c^{S^c}`;
* `C` is the canonical response two-jet marking of the same selected row;
* (11) is the same selected row tagged twice by response `(a,b)`.

All these targets are zero.  The three pure anchors (7) live at different
endpoint fine grades and carry target one.  The committed endpoint-degree
audit shows that no nonnegative literal tag route moves a diagonal anchor
into the selected terminal grade.  Therefore the absent provenance is not
another raw target value.  It is an adjacent-chart comparison which cancels
the physical response companions at the same time as it compares actual and
canonical internal cells—precisely the row `K=0` in (9).

Equivalently, any proposed Bianchi identity must have source expansion

\[
       \sum_{|S|=3}\bigl(M_S+\alpha D_S\bigr)=0,       \tag{14}
\]

with any pure-anchor uses written as normalized rows of the form (7).  An
identity proving only `sum D_S=0` leaves the response companion channel and
does not close the terminal class.

## 3. Verification and scope

The dependency-free checker
[`verify_h3_full_nine_middle_companion_normalization_guard.py`](../computations/verify_h3_full_nine_middle_companion_normalization_guard.py)
audits all twenty mixed targets and all three pure-anchor targets; computes
the exact ranks and separators in (12)--(13) at three nonzero rational
values of `alpha`; and direct-sums the dynamic presentation with the
committed rank-four static two-chart block and three explicitly augmented
anchor rows.  It verifies that `D=0` leaves cleanliness independent, whereas
`K=0` contains both the clean and terminal rows.

No physical counterexample is claimed, and Krenn's conjecture remains open.
