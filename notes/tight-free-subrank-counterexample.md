# Tight and free does not turn subrank three into monomial subrank three

This note tests a possible exact-versus-degeneration bridge for the
perfect-matching incidence tensor.  The proposed general statement

> a tight free tensor of subrank three has monomial subrank three

is false, even for an order-four tensor over (mathbb C).  The example is
small enough to audit without computer algebra.  Its failure mechanism is
an exact two-term cancellation between local symbols which an ordinary
linear restriction identifies, but a monomial restriction cannot identify.

The example is not itself a perfect-matching incidence support.  Thus a
strictly incidence-specific theorem could still hold, but it would have to
use the rectangle-completion property of independent choices of parallel
sources, not tightness and freeness alone.

## 1. Definitions used here

For a tensor in fixed product bases, call its support (S) **free** if any
two support tuples differ in at least two coordinates.  Equivalently,
deleting any one coordinate is injective on (S).

Call (S) **tight** if there are injective integer-valued functions
(alpha_v) on the local alphabets such that

\[
                         \sum_v\alpha_v(s_v)=0\qquad(s\in S).
\tag{1}
\]

The subrank is the largest diagonal tensor obtainable by arbitrary local
linear maps.  The monomial subrank is the same quantity with generalized
monomial maps.  In a fixed support it is the maximum size of an induced
matching: a set (D\subseteq S) whose coordinate projections are injective
and for which

\[
 S\cap\prod_v\pi_v(D)=D.                                  \tag{2}
\]

The second condition prevents an unwanted mixed support tuple from
surviving the coordinate restriction.

## 2. The five-term tensor

Use local alphabets

\[
 X_0=X_2=\{0,1,2,p\},\qquad X_1=X_3=\{0,1,2\},
\tag{3}
\]

and define

\[
\begin{split}
 T={}&e_0e_0e_0e_0+e_1e_1e_1e_1+e_2e_2e_2e_2\\
    &+e_0e_1e_0e_1-e_pe_1e_pe_1.
\end{split}                                                 \tag{4}
\]

Tensor signs in (4) are coefficients, while the four juxtaposed vectors
belong to the four different local spaces.

Map (0,1,2) to the corresponding standard vectors of (mathbb C^3) at
every site, and map (p\mapsto e_0) at sites zero and two.  The last two
terms of (4) have identical images and opposite coefficients.  Therefore

\[
                         (A_0\otimes A_1\otimes A_2\otimes A_3)T
                         =\Delta_{4,3}.                     \tag{5}
\]

All four maps have rank three.  Since two local dimensions in (3) are
three, (5) proves that the ordinary subrank is exactly three.

## 3. Exact tightness and freeness

In the symbol orders (0,1,2,p) where applicable, take

\[
\begin{array}{c|rrrr}
v=0&0&1&3&2\\
v=1&0&1&2&\\
v=2&0&-1&3&-2\\
v=3&0&-1&-8&
\end{array}                                                  \tag{6}
\]

as the local (alpha_v)-values.  Every row is injective.  The five support
tuples in (4) have respective total weights

\[
                 0,\quad 1+1-1-1,\quad3+2+3-8,
                 \quad0+1+0-1,\quad2+1-2-1,
\tag{7}
\]

all zero.  Hence the tensor is tight.

The only pairs at Hamming distance two are the evident pairs involving
(0101) or (p1p1); no pair differs in only one coordinate.  Thus the
support is free.

## 4. Its monomial subrank is only two

The three diagonal tuples (0000,1111,2222) are a matching, but not an
induced one: (0101) lies in the product of their coordinate projections.

The tuple (0101) cannot occur in a matching with (0000) (they agree at
sites zero and two) or with (1111) (they agree at sites one and three).
Thus it belongs to no matching triple.  The tuple (p1p1) cannot coexist
with (1111); its only possible matching triple is

\[
                         \{p1p1,0000,2222\},                \tag{8}
\]

but (8) is not induced because (0101) again lies in the product of its
coordinate projections.  These cases exhaust the five support tuples, so
there is no induced matching of size three.  On the other hand
({0000,2222}) is an induced matching.  Therefore

\[
                         Q(T)=3,\qquad Q_{\rm mon}(T)=2.    \tag{9}
\]

## 5. Why this does not yet settle the incidence-specific question

A local symbol of a perfect-matching incidence tensor denotes one fixed
source edge, hence fixes the symbol at its other endpoint.  In (4), the
tuples (0000) and (0101) force the symbols (0) at sites zero and two
to denote the same (02)-source, while the tuples (1111) and (0101)
force the symbols (1) at sites one and three to denote the same
(13)-source.  The (p1p1) tuple then represents a parallel (02)-source
combined with that (13)-source.  Independent selection of the two
parallel-source families would also create all the missing rectangle
corners.  They are absent from (4).

Consequently, tightness plus freeness is too weak, while the additional
rectangle-completion law of matching-incidence supports remains available.
Any valid bridge for Krenn's problem must use that law (and, for (n\ge6),
must also handle extra perfect matchings created by alternating-cycle
switches inside three selected one-factors).

The dependency-free exact enumeration and the tightness audit are included
in `computations/verify_minimal_norm_gauge.py`.
