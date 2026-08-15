# The first two-crossing tail closes to a contaminated anti-diagonal packet

## Result

The first all-order nonlift from the conditioned transverse-seed theorem is
already the literal common-factor `C4` row

\[
 a_{01}^{00}a_{23}^{00}
 \left(a_{45}^{01}a_{67}^{22}+a_{46}^{02}a_{57}^{12}\right)=0. \tag{1}
\]

Retaining the endpoint colours present in its canonical parent does **not**
turn (1) into the three-binomial permanent triangle.  The two additional
decorations \(a_{45}^{00}\) and \(a_{45}^{21}\) first expose two literal
mixed singleton rows.  After adjoining the missing third matching and
closing those singletons minimally, there are exactly two labelled
singleton-free completions.  Each has two `C4` binomials bracketing one
three-term row and admits an all-unit solution.

Every support-minimum completion of either packet by one pure occurrence in
each colour has a mixed singleton.  Thus the minimum full-GHZ stratum gives a
unit; an arbitrary larger source can escape only by adding a further
operation-labelled mate.  The result is intrinsic to coefficient rows and
does not use a protected `B/Eq` presentation.

The exact checker is
`computations/verify_n8_two_crossing_c4_three_colour_completion_guard.py`.

## 1. The complete ordered-colour `C4` fibre

Write

```text
P0 = 45|67,       P1 = 46|57,       P2 = 47|56,
T  = a01^00 a23^00.
```

Endpoint colours are ordered by their sites: for example, `a45^21` means
colour two at site 4 and colour one at site 5.  The inherited six-cell
packet is

```text
a45^00  a45^01  a45^21  a67^22  a46^02  a57^12.
```

Enumeration of all \(3^4\) local words and all three `C4` matchings gives
exactly

```text
local word   live operations
0022         P0
0122         P0,P1
2122         P0.
```

After multiplication by \(T\), the full eight-site words are respectively
`00000022`, `00000122`, and `00002122`.  All are mixed source equations.
Hence the two endpoint-colour companions are units unless they acquire
matching mates.

Adding the missing matching in the central word means adding

```text
a47^02 a56^12.
```

It changes only `0122`, from a binomial to a trinomial.  The other two rows
remain singletons.  Exhaustion over all 54 ordered-colour cells on the six
physical `C4` edges proves that no one-cell enlargement kills both
singletons.  There are exactly two minimum two-cell enlargements:

```text
section A: a46^22, a56^02,
section B: a47^22, a57^02.
```

The crossed choice is forced.  Choosing both repairs through `P1`, or both
through `P2`, creates a fourth singleton at local word `2022`.

## 2. It reproduces the parent anti-diagonal, not the permanent triangle

For section A put

\[
\begin{array}{c|cccccccccc}
 &A&B&C&D&E&F&G&H&I&J\\ \hline
 &a_{45}^{00}&a_{45}^{01}&a_{45}^{21}&a_{67}^{22}&
 a_{46}^{02}&a_{57}^{12}&a_{47}^{02}&a_{56}^{12}&
 a_{46}^{22}&a_{56}^{02}.
\end{array}
\]

The **complete** nonempty eight-site source inventory of the twelve-cell
packet \(\{a_{01}^{00},a_{23}^{00}\}\cup\{A,\ldots,J\}\) is

\[
\begin{aligned}
F_{00000022}&=T(AD+GJ),\\
F_{00000122}&=T(BD+EF+GH),\\
F_{00002122}&=T(CD+IF).                                  \tag{2}
\end{aligned}
\]

There are no other supported output words.  Thus factoring the unit tail is
an exact contraction of this named mixed packet, with word, fine, and
`P0/P1/P2` operation labels retained.

The assignment

\[
 A=C=-1,\qquad B=-2,\qquad D=E=F=G=H=I=J=1             \tag{3}
\]

kills all three rows and keeps every cell nonzero.  Consequently these rows
do not generate the Laurent unit ideal.

They are not the permanent triangle of `90e5faf`.  In that triangle all
three rows are binomials with four variables and the triple intersection of
their variable supports is empty.  In (2) the support sizes are
\((4,6,4)\), and \(D\) occurs in all three.  The third perfect matching
merely contaminates the middle member of a parallel parent-antidiagonal
packet.  The all-unit point (3) is also a direct countercertificate to any
claimed permanent-triangle unit identity.

Section B is the site-reflected version and has the same complete census.

## 3. Pure normalization forces a unit on the minimum stratum

The mixed packet by itself is not a full GHZ source: it has no occurrence in
the pure-one word, for example.  To avoid promoting a partial guard, the
checker exhausts the support-minimum pure completions at order eight.

For each section, the minimum numbers of new diagonal cells needed for one
pure occurrence in colours zero, one, and two are

```text
1, 4, 3.
```

There are respectively `1`, `105`, and `30` choices of the supporting pure
matching, hence

\[
                         1\cdot105\cdot30=3150             \tag{4}
\]

minimum completions.  In every completion each pure word has exactly one
occurrence.  Complete enumeration of all supported mixed words shows that
every completion also has a mixed singleton.  The number of mixed
singletons ranges from 9 to 105; the minimum 9 is attained 32 times in each
section.  Therefore every support-minimum full-target completion generates a
unit after support localization.

This is a source-row obstruction, not merely lack of a pure matching.  It
uses all three pure normalizations and every output word supported by the
completion.

## 4. Exact remaining escape

The conclusion is a finite alternative.

1. Before repair, `00000022` or `00002122` is a literal singleton/unit.
2. Adding the third matching and closing the endpoint-colour packet minimally
   yields (2), a solvable contaminated anti-diagonal guard rather than a
   permanent triangle or active cap.
3. Completing pure targets minimally again yields a mixed singleton/unit.
4. A surviving nonminimum full source must add a labelled `P1` or `P2`
   cancellation mate to that new singleton.  This is the first unclassified
   repair branch.

For instance, at the canonical minimum-pure witness `00000100`, the existing
fine is `01|23|45|67`.  A mate requires either the two `P1` cells
`a46^00,a57^10` or the two `P2` cells `a47^00,a56^10` (or an occurrence that
leaves the named window).  No one-cell local repair is available.

The packet-relative factorization by \(T\) is exact, but it is not a global
tail contraction theorem for an arbitrary larger source: extra
window-crossing matchings may contaminate the same words.  Nor does a
monochromatic/local coefficient restriction provide the three nonzero
endpoint covectors of an active cap or transport every output row of a
smaller GHZ tensor.

Run all modes:

```text
python3 computations/verify_n8_two_crossing_c4_three_colour_completion_guard.py --mode structural
python3 -O computations/verify_n8_two_crossing_c4_three_colour_completion_guard.py --mode full
python3 -I -S computations/verify_n8_two_crossing_c4_three_colour_completion_guard.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
a8802aee3f284196caf7708c95730744ce5e4916a6e0d8bec3d80ce9db74a50a
```
