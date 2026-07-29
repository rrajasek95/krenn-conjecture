# Independent audit: the p=19 five-triple even-span closure

## Verdict

The closure of

\[
4\,3^5 1^{h+2},\qquad 4\,3^5 2\,1^h,
\qquad 13\le h\le18,
\]

is correct.  This audit reconstructed the argument without using the new
closure checker as a premise.

## Profile and dimension checks

For the first profile, give role two to the moving triple and select \(h\)
singleton layers.  For the second, also give role two to the exact double
and select \(h-2\) singleton layers.  In either case two ordinary
singletons remain, while the moving triple leaves one residual simple
class.  The complement is therefore exactly

\[
                         4\,3^4 1^3,
\]

of mass nineteen and with eight value classes.

At \(p=19\), the selected \(q=6\) Wronskian gap is nine for every
\(13\le h\le18\).  Pair drops give kernel dimension at least four, and
the already-audited low-role incidence theorem excludes its
four-dimensional branch.  Thus every moving selection has a
five-dimensional selected-row kernel and a three-dimensional relation
space in \(\mathbb C[z]_{\le4}\).

Multiplication by

\[
                         B_x=(z-x)^2(z+x)^2
\]

transports that relation space into the common degree-eight baseline
kernel with multiplicities \(4,3^5,1^2\).  A hypothetical six-space in
that kernel has forced Wronskian weight

\[
                 (6-4)+5(6-3)+2(6-1)=27,
\]

against cap \(6(9-6)=18\).  The exact-row gcd correction is
nonnegative, so the common kernel has dimension at most five.

## Independent span proof

For distinct, nonopposite triple values, the quartics \(B_x\) are
pairwise coprime.  Two transported three-spaces in an at-most-five-space
intersect, and their degree-eight ambient intersection is precisely the
line spanned by \(B_xB_y\).  Hence every off-diagonal product lies in the
common kernel.

Put \(t=z^2\), \(a_i=x_i^2\), and \(b_i=(t-a_i)^2\).  It suffices to
use any four distinct \(a_i\).  If a functional \(L\) on
\(\mathbb C[t]_{\le4}\) kills all six products \(b_i b_j\), define
\(\beta(f,g)=L(fg)\) on \(\mathbb C[t]_{\le2}\).  Any three \(b_i\)
form a basis.  In the basis \(b_1,b_2,b_3\), the Gram matrix of
\(\beta\) is diagonal.  Every coordinate of \(b_4\) is nonzero, since
no three distinct points of the nondegenerate conic
\([(t-a)^2]\) are collinear.  Orthogonality of \(b_4\) to the first
three basis vectors therefore kills all diagonal entries.  Thus
\(\beta=0\), and because products of two quadratics span
\(\mathbb C[t]_{\le4}\), also \(L=0\).

Consequently the pair products span the five-space
\(\mathbb C[t]_{\le4}|_{t=z^2}\).  Containment and the common-kernel
upper bound force equality with that even five-space.

## Terminal row and zero-value scope

Choose a nonzero triple value \(v\).  Then

\[
                         T=(z^2-v^2)^3
\]

belongs to the common kernel but has
\(T(v)=T'(v)=T''(v)=0\) and \(T'''(v)=48v^3\ne0\).  Hence the exact
baseline row \((U_vT)'''(v)=0\), with \(U_v(v)\ne0\), is violated.

The standard collision hypotheses actually make every repeated value,
including each triple value, nonzero.  The proof is stronger than needed:
if one nevertheless relaxes the setup to permit one zero triple value,
the squared parameters remain distinct, the coprime/span argument still
works, and one of the other four triple values supplies the nonzero
terminal row.  The optional exact double is fully absorbed into the
selection and does not change the complement or common baseline.

## Mechanical audit

[verify_live_three_zero_higher_split_p19_five_triple_even_span_independent_audit.py](../computations/verify_live_three_zero_higher_split_p19_five_triple_even_span_independent_audit.py)
independently checks the two selections for every admissible \(h\), the
kernel arithmetic, the conic coordinates used above, exact ranks including
a zero squared parameter, and the terminal product-rule jet.
