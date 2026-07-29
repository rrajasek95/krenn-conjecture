# Independent audit: the \(p=28\) all-triple tangent-involution drop

## 1. Verdict and exact scope

This audit independently reconstructs
[the all-triple tangent-involution argument](live-three-zero-higher-split-p28-all-triple-tangent-involution-drop.md).
The argument is sound.

Among the nine residual tuples in the first-six-kernel boundary ledger,
it applies to exactly

\[
                 (e,a,b,u)=(0,10,0,0),\qquad(0,10,1,-2).
                                                               \tag{1}
\]

Its conclusion is only that the ten moving-triple selections cannot all
have selected kernel dimension six.  Thus one explicit selection has
kernel dimension at most five.  This is not a contradiction to either
original collision profile and is not a profile closure.

The reconstruction found one harmless typographical defect in the first
factor of the primary equation (20).  It was corrected from plain text
\(widetilde G\) to \(\widetilde G\) before registry promotion; no
mathematical formula depended on the typo.

## 2. Applicability to the two residual tuples

For \((0,10,0,0)\), select one of the ten triples in role two and select
all \(h\) original singletons in role one.  The complement is

\[
                              3^9 1_i.                         \tag{2}
\]

For \((0,10,1,-2)\), keep the unique double selected in role two, select
one moving triple in role two, and select all \(h-2\) original
singletons.  The double is then absent from the complement, and the
complement is again (2).  Holding the selected double fixed adds the same
selected-row layer to every member of the family and does not alter the
relation-space transport.

In both cases restoring the moving triple produces the common relation
baseline \(3^{10}\).  Conversely, every other tuple in the nine-member
residual ledger has a positive quartic count or fewer than ten triples,
so its restored baseline is not \(3^{10}\).  The theorem therefore
covers exactly the two tuples in (1) within that ledger.

The repeated triple values are structurally nonzero.  Distinct value
classes are pairwise nonopposite.  Hence the twenty signed points
\(\{\pm i\}\) are distinct and every pair of quartics

\[
                         B_i=(z-i)^2(z+i)^2                    \tag{3}
\]

is coprime.

## 3. Saturation of each relation four-space

Assume all ten selected kernels have dimension six.  The relation-space
theorem gives, for every moving value \(i\),

\[
                 {\cal S}_i\subseteq{\mathbb C}[z]_{\le6},
                 \qquad\dim{\cal S}_i=4.                     \tag{4}
\]

At the selected residual simple row the least vanishing sequence is
\((0,2,3,4)\), of Wronskian weight three.  At each of the other nine
triple rows it is \((0,1,2,4)\), of weight one.  Their total weight is

\[
                             3+9=12,                          \tag{5}
\]

equal to the full Wronskian cap \(4(7-4)=12\).

The primary gcd argument is valid.  If a four-space has common order
\(g<m\) at an exact order-\(m\) row, division leaves an exact
order-\((m-g)\) row and the total local cost is

\[
                    4g+\max(0,4-m+g)>4-m.                    \tag{6}
\]

If \(g=m\), all lower jets vanish and the nonzero highest-jet coefficient
forces the divided sections to vanish once more.  Thus \(g=m\) could not
have been the maximal common order.  Orders \(g>m\), and gcd roots away
from the listed values, also add strictly positive weight.  Saturation
therefore makes every \({\cal S}_i\) primitive.

The twelve forced finite zeros make the Wronskian degree at least twelve.
If \(n_0<\cdots<n_3\le6\) are the echelon degrees, its degree is
\(\sum n_r-6\le12\).  Equality forces the unique profile

\[
                              (n_0,n_1,n_2,n_3)=(3,4,5,6).
                                                               \tag{7}
\]

Consequently there is no Wronskian zero or base point at infinity, and
every unlisted finite point is regular.  In particular every \(-j\) is
regular for \({\cal S}_i\), while \(j\ne i\) has sequence
\((0,1,2,4)\).

## 4. The pair intersections really give tangent equality

The exact quartic lift puts

\[
            {\cal T}_i=B_i{\cal S}_i\subseteq{\cal K}
                         \subseteq{\mathbb C}[z]_{\le10}.      \tag{8}
\]

The common baseline has ten exact order-three rows.  A seven-space would
have forced Wronskian weight \(10(7-3)=40\), against cap
\(7(11-7)=28\).  The usual gcd corrections are nonnegative, so
\(\dim{\cal K}\le6\).

For \(i\ne j\), two transported four-spaces meet in dimension at least
two.  Coprimality gives the exact ambient intersection

\[
 B_i{\mathbb C}[z]_{\le6}\cap B_j{\mathbb C}[z]_{\le6}
                 =B_iB_j{\mathbb C}[z]_{\le2}.                \tag{9}
\]

After division by \(B_i\), the intersection is the subspace of
\({\cal S}_i\) divisible by \(B_j\).  It is the kernel of the four
signed first-jet rows at \(j,-j\).  The two rows at \(j\) are independent
by sequence \((0,1,2,4)\); the two at \(-j\) are independent because
that point is regular.  Hence the four-row matrix has rank at least two.
The intersection lower bound says its kernel has dimension at least two,
so its rank is exactly two and

\[
 \langle F_i(j),F_i'(j)\rangle
       =\langle F_i(-j),F_i'(-j)\rangle.                      \tag{10}
\]

This also shows that every pair intersection has dimension exactly two.
If \(\dim{\cal K}<6\), the elementary dimension lower bound would make it
at least three, a contradiction.  Thus \(\dim{\cal K}=6\), although this
equality is not needed after (10).

## 5. The tangent Pluecker map and the root count

For a basis vector \(F_i=(f_0,\ldots,f_3)\), let

\[
                G_{ab}=f_af_b'-f_bf_a'.                      \tag{11}
\]

The echelon degrees (7) give \(\deg G_{ab}\le10\), and the minor of the
degree-five and degree-six basis elements has degree exactly ten.  The
local sequence \((0,2,3,4)\) at \(i\) gives a common zero of order exactly
one in the six minors.  At every other finite point one minor is a unit,
and the leading degree-ten minor excludes a common zero at infinity.
Therefore

\[
                         \widetilde G=G/(z-i)                  \tag{12}
\]

is a primitive, everywhere nonzero degree-nine Pluecker vector.

For any two coordinates \(g_\alpha,g_\beta\) of \(\widetilde G\), set

\[
 H_{\alpha\beta}(z)=
 g_\alpha(z)g_\beta(-z)-g_\beta(z)g_\alpha(-z).               \tag{13}
\]

This polynomial is odd.  Although the crude product bound is eighteen,
the degree-eighteen coefficient cancels, so \(\deg H_{\alpha\beta}\le17\).
Equation (10) supplies the eighteen distinct roots

\[
                          \{\pm j:j\ne i\}.                    \tag{14}
\]

Thus every cross-minor (13) vanishes identically.  Equivalently, the
degree-nine tangent-line morphism satisfies

\[
                              \tau_i(z)=\tau_i(-z).            \tag{15}
\]

Primitivity and the absence of base points in (12) justify passing from
the vanishing cross-minors to an identity of morphisms, including at the
exceptional points.

## 6. Audit of both involution branches

Write \(t=z^2\) and

\[
                       F_i(z)=E(t)+zO(t).                     \tag{16}
\]

If \([F_i(z)]\) and \([F_i(-z)]\) are generically distinct, they span the
common tangent line in (15), namely \(\langle E,O\rangle\).  Since both
first derivatives lie on that line,

\[
 \begin{aligned}
 F_i'(z)-F_i'(-z)&=4zE'(t),\\
 F_i'(z)+F_i'(-z)&=2O(t)+4tO'(t)
 \end{aligned}                                               \tag{17}
\]

imply \(E',O'\in\langle E,O\rangle\) for generic nonzero \(t\).  Hence
the derivative of the Pluecker point \([E\wedge O]\) is zero.  In
characteristic zero that Grassmannian-valued rational map is constant.
All \(F_i(z)\) then lie in one fixed two-plane in \({\mathbb C}^4\),
giving two constant linear relations among the four basis polynomials.
That contradicts \(\dim{\cal S}_i=4\).

It remains to check carefully the projectively proportional branch.
Write

\[
                         F_i(-z)=\rho(z)F_i(z),\qquad
                         \rho=A/B,\quad (A,B)=1.               \tag{18}
\]

The vector \(F_i\) is primitive.  From
\(BF_i(-z)=AF_i(z)\), coprimality of \(A,B\) makes \(B\) divide every
coordinate of \(F_i(z)\).  Thus \(B\) is constant and \(\rho\) is a
polynomial.  Applying the involution to (18) gives

\[
                         \rho(z)\rho(-z)=1,                   \tag{19}
\]

so \(\rho\) is a nonzero constant and then \(\rho=\pm1\).  The sign
\(-1\) would make all four coordinates odd, hence all divisible by
\(z\), contradicting primitivity.  Thus all four basis polynomials are
even.

The even polynomials of degree at most six form the four-space

\[
                       \langle1,z^2,z^4,z^6\rangle.            \tag{20}
\]

Four independent even basis polynomials must fill this complete space.
At the structurally nonzero value \(i\), the map \(z\mapsto t=z^2\) is
etale, and the complete cubic system in \(t\) has sequence
\((0,1,2,3)\).  This contradicts the forced selected sequence
\((0,2,3,4)\).

Both generic branches are impossible.  The claimed dimension drop
follows, with precisely the limited scope stated in Section 1.

## 7. Independent executable audit

[verify_live_three_zero_higher_split_p28_all_triple_tangent_involution_drop_independent_audit.py](../computations/verify_live_three_zero_higher_split_p28_all_triple_tangent_involution_drop_independent_audit.py)
does not import the primary checker.  It reconstructs the two covered
residual profiles for every \(p=28\) split, all local Wronskian and gcd
arithmetic, the unique echelon profile, the common-kernel and coprime
intersection dimensions, the degree-seventeen odd cross-minor bound, the
even/odd derivative identities, the constant-plane Pluecker identity,
and the nonzero-point jets of the complete even cubic system.
