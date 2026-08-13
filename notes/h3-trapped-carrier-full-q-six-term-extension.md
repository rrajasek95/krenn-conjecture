# The full-q endpoint extension leaves one exact quotient coefficient

## The physical Jacobian is explicit

Fix the two right endpoint rows `s_1,s_2`, but now allow simultaneous
variation of the two left rows and of every decorated cell of the common
residual `q`.  At `h=3` the domain has

```text
36 left-endpoint coordinates + 15*9 q coordinates = 171 columns.
```

The physical map consists of all `3^6=729` unary rows and all
`4*3^6=2916` response rows.  The endpoint block is the one constructed in
`1fe8dce`.  For a decorated `q` column `(uv;ab)`, its unary entry at output
word `w` is

\[
 \delta_{(w_u,w_v),(a,b)}
 \operatorname {Haf}_q
       (R\setminus\{u,v\};w|_{R\setminus\{u,v\}}).    \tag{1}
\]

There are 10,935 generic nonzero unary entries, each with three two-cell
matching terms.

Its response entry at head `(i,j)` and word `w` is

\[
 \delta_{(w_u,w_v),(a,b)}
 \sum_{\substack{x\ne y\\x,y\notin\{u,v\}}}
 p_i[x,w_x]s_j[y,w_y]
 q_{R\setminus\{u,v,x,y\}}[w].                       \tag{2}
\]

The last factor is the unique decorated cell on the remaining two sites.
There are 43,740 generic response entries, each with twelve terms.  The
checker obtains (1)--(2) independently by differentiating every literal
matching occurrence and verifies all 557,685 resulting monomial terms.

Checker:
[`verify_h3_trapped_carrier_full_q_six_term_extension.py`](../computations/verify_h3_trapped_carrier_full_q_six_term_extension.py).

## Anchor protection also acquires q entries

The marked occurrence used in the fixed-`q` audit was, representatively,

\[
             p_1[0,1]s_1[1,1]q_{23}[0,0]q_{45}[0,0]. \tag{3}
\]

After the nonzero tail is localized and `q` is frozen, its protection row
looks like the coordinate selector `e_(p_1[0,1])`.  Once `q` moves, the
actual protection row is the complete product-rule differential of (3):

\[
\begin{aligned}
 H={}&s_1q_{23}q_{45}\,d p_1
       +p_1s_1q_{45}\,d q_{23}
       +p_1s_1q_{23}\,d q_{45}.                       \tag{4}
\end{aligned}

\]

Thus simply appending (1)--(2) to the old coordinate border would be
incorrect.  Formula (4), and its literal relabelings for every protected
anchor occurrence, is the exhaustive anchor border on the full-q domain.

## Exact structural alternative

Let

* `A` be the evaluated physical map containing (1)--(2) and every other
  already physical protected-zero row in this grade;
* `H` be the full anchor differential (4);
* `e` be the selector isolated by the support-minimal fixed-q branch; and
* `Lambda` be the physical six-term readout

  \[
                 \Lambda=\sum_{r=1}^{6}m_r-operatorname {ainc}     \tag{5}
  \]

  in the same labelled repeated relative grade.

Apply exact Fredholm duality to `J=[A;H]`.

1. If `e` is nonzero on `ker J`, normalize such a vector to obtain an
   anchor-safe full-q kernel exchange.
2. Otherwise `e` belongs to `row J`.  If already `e in row A`, it is a
   physical response/source dual.
3. In the sole protection case,

   \[
                         e=\lambda A+cH,qquad c\ne0.  \tag{6}
   \]

   Apply the pinned exhaustive six-term alternative to `Lambda` on the
   same protected domain.
   If `Lambda` is nonzero on `ker J`, it normalizes to the physical relative
   generator.
4. Otherwise

   \[
                     \Lambda=\nu A+\mu H.             \tag{7}
   \]

   If `mu` is nonzero, eliminate `H` between (6)--(7):

   \[
       e=\left(\lambda-{c\over\mu}\nu\right)A
           +{c\over\mu}\Lambda.                      \tag{8}
   \]

   Hence the protection class transports to the physical six-term row and
   is a separator/dual in the augmented physical map `(A,Lambda)`.

There is no Hall or matching-support branch in this calculation.

## The sole sharp survivor

The only remaining case is

\[
       \boxed{\Lambda\in\operatorname {row}(A),\qquad
              H\notin\operatorname {row}(A).}         \tag{9}
\]

Equivalently, the `H` coefficient `mu` in (7) is zero while the protection
coefficient `c` in (6) is nonzero.  Then the six-term covector has already
factored through the physical response/source rows, but it gives no control
of the independent anchor-protection quotient class.

This is a real linear possibility, not a missing case in the argument.  The
checker freezes a three-column rational guard:

```text
A      = (1,0,0),
H = e  = (0,1,0),
Lambda = (1,0,0).
```

Here `e` kills `ker[A;H]`, is not in `row(A)`, and `Lambda` is already in
`row(A)`.  Therefore arbitrary row-space duality—even after all 135 `q`
columns have been admitted—cannot exclude (9).

The smallest remaining physical theorem is correspondingly precise:

> On a unary-compatible trapped source, either `Lambda` is visible on the
> protected full-q kernel, or every factorization of `Lambda` through
> `[A;H]` has nonzero `H` coefficient.  Equivalently, exclude (9), or
> construct `H` itself as a physical source row.

This is exactly the comparison of the Interface-II occurrence-protection
class with the Interface-I six-term class.  It must preserve the common
word, fine grade, endpoint orientation, anchor incidence and physical
six-term typing; a marked occurrence functional alone is not (5).

## Proof-frontier effect

The q-deformation audit removes two ambiguities.

* The unary block is no longer a silent condition: its 135 q-columns are
  the genuine first-cofactor derivatives (1).
* The selected anchor is no longer an endpoint-only selector: its two q
  product-rule entries are load-bearing.

All branches except (9) now land in already accepted mechanisms:

```text
selector visible on protected kernel -> anchor-safe exchange/deletion
selector physical                  -> response/source dual
six-term visible                   -> normalized relative generator
nonzero H coefficient              -> six-term transport/separator
coefficient zero                   -> exact remaining comparison theorem
```

No finite Hall enumeration is used or needed.  This result does not prove
the final nonzero-coefficient theorem at every unknown trapped source; it
exposes its complete coefficient-level domain and the smallest exact
counterguard.

## Verification

Run:

```text
python3 computations/verify_h3_trapped_carrier_full_q_six_term_extension.py
python3 -O computations/verify_h3_trapped_carrier_full_q_six_term_extension.py
python3 -I -S computations/verify_h3_trapped_carrier_full_q_six_term_extension.py
```

Frozen ledger SHA-256:

```text
e515f5987ce2d716699f76842ea897ef5ddfae4248d0c51791b90323d5113a10
```
