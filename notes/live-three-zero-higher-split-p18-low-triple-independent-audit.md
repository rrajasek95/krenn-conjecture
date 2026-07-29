# Independent audit of the complete \(p=18\) low-triple closure

## 1. Verdict

The proof in
[the low-triple common-lift closure](live-three-zero-higher-split-p18-low-triple-singleton-common-lift-closure.md)
passes an independent reconstruction.  In particular:

1. the fixed complementary triple really supplies one common exact
   third-order row for every moving-singleton lift;
2. the strengthened Wronskian inequality forces the common kernel to have
   dimension three;
3. \(b=9\) is the first equality case of the cubic-divisor count and its
   seven double rows exclude that equality space; and
4. the \(a=0,b=11\) selected-pair endpoint has a genuinely common baseline
   row \(J_{v,i}\), and its nine-index rational-fibre contradiction is
   valid with all required index exclusions.

No division by a possibly zero singleton or by an unproved unit is used.
Repeated values are nonzero; distinct value classes are nonopposite; and
common-pole separation makes every baseline unit nonzero at the row where
it is evaluated.

The independent checker is
[verify_live_three_zero_higher_split_p18_final_low_triple_independent_audit.py](../computations/verify_live_three_zero_higher_split_p18_final_low_triple_independent_audit.py).

## 2. The complementary-triple row

For one triple and \(b\) doubles, fix all but the moving selected singleton
\(q\).  The selected relation space is a three-space
\({\cal S}_q\), and multiplication by

\[
                         f_q=(z-q)^2(z+q)                         \tag{1}
\]

places it in the common degree-\(N\) kernel.  Let \(x\) be the fixed
complementary triple.  If \(U_x\) is the baseline regular unit, then the
unit for the selection using \(q\) is \(f_qU_x\), up to an irrelevant
nonzero normalization scalar.  Since \(x\ne\pm q\),

\[
 (U_xf_qS)'''(x)=0\qquad(S\in{\cal S}_q)                         \tag{2}
\]

is one common normalized third-order row.  Its highest-jet coefficient is
\(U_x(x)\ne0\).  The same transport supplies the simple pool rows and the
complementary-double second-order rows; at the selected point \(q\), the
double zero of \(f_q\) kills the simple baseline row automatically.

Writing \(P=|P|\) and \(R\) for the numbers of pool singletons and
complementary doubles, a \(D\)-dimensional common kernel therefore obeys

\[
             P(D-1)+R(D-2)+(D-3)\le D(N+1-D).                   \tag{3}
\]

For both \(b=0,1\), where \((P,R,N)=(16,0,15)\), and for
\(2\le b\le9\), where

\[
                    (P,R,N)=(20-2b,b-2,17-b),                  \tag{4}
\]

equation (3) is exactly

\[
                              D^2+D\le19.                        \tag{5}
\]

The transported three-space gives \(D\ge3\), while (5) excludes \(D=4\)
and every larger value.  Thus \(D=3\), every transported space equals the
common kernel, and every member is divisible by
\(\prod_{q\in P}f_q\).

The degree-\(N\) multiple space has dimension

\[
                       \max\{N-3P+1,0\}.                         \tag{6}
\]

It is smaller than three through \(b=8\).  At \(b=9\),
\((P,R,N)=(2,7,8)\) and (6) equals three exactly.  Hence the only possible
kernel is

\[
                       f_{q_1}f_{q_2}\mathbb C[z]_{\le2}.        \tag{7}
\]

For any complementary double \(v\), the member
\(f_{q_1}f_{q_2}(z-v)^2\) belongs to (7), but its exact second-order row is

\[
        (U_vf_{q_1}f_{q_2}(z-v)^2)''\big|_{z=v}
             =2U_v(v)f_{q_1}(v)f_{q_2}(v)\ne0.                  \tag{8}
\]

This closes the sharp equality case.  Nonopposition supplies both nonzero
factors in (8); no reciprocal of \(q_i\) is taken, so a zero singleton is
also covered.

## 3. The eleven-double endpoint

For the profile \(2^{11}1^{h-2}\), selecting doubles \(i,j\) and all
singletons leaves \(2^9\).  Hence

\[
             {\cal S}_{i,j}\subseteq\mathbb C[z]_{\le5},
             \qquad \dim{\cal S}_{i,j}=3.                       \tag{9}
\]

Fix \(i\), put \(g_j=(z-j)^3(z+j)^2\), and use the baseline unit

\[
 U_{v,i}=
 { (z+\mu)^k(z+i)^2\prod_{y\in Y}(z+y)
  \over
   \prod_{w\in{\mathscr D}\setminus\{i,v\}}(z-w)^3}.            \tag{10}
\]

For \(v\ne i,j\), the unit belonging to the formal pair selection
\(\{i,j\}\) is exactly \(g_jU_{v,i}\).  At \(v=j\), the triple zero of
\(g_j\) kills the full two-jet.  Thus

\[
        {\cal T}_{i,j}=g_j{\cal S}_{i,j}\subseteq{\cal K}_i
             \subseteq\mathbb C[z]_{\le10}.                     \tag{11}
\]

Crucially, \(U_{v,i}\) depends only on \(i,v\), not on either moving
partner.  Its value at \(v\) is nonzero: \(v\) is a nonzero repeated value,
all other exceptional values are distinct and nonopposite to it, and
\(v+\mu\ne0\).

The ten normalized second-order rows give, for
\(D_i=\dim{\cal K}_i\),

\[
                         10(D_i-2)\le D_i(11-D_i),               \tag{12}
\]

so \(D_i\le5\).  For distinct \(j,k\ne i\), the coprime quintics have

\[
 g_j\mathbb C[z]_{\le5}\cap g_k\mathbb C[z]_{\le5}
                            =\mathbb Cg_jg_k                    \tag{13}
\]

inside degree ten.  Two three-spaces in a space of dimension at most four
would intersect in dimension at least two, contrary to (13).  Therefore
\(D_i=5\); dimension counting now makes every pairwise intersection the
line in (13), and

\[
                              g_jg_k\in{\cal K}_i.                \tag{14}
\]

Fix \(v\ne i\).  There are exactly nine indices in
\(\Omega={\mathscr D}\setminus\{i,v\}\).  For distinct \(j,k\in\Omega\),
the one common row \(J_{v,i}\) applied to (14) gives

\[
                         C+B_j+B_k+2A_jA_k=0,                    \tag{15}
\]

where

\[
                         A_j={g_j'(v)\over g_j(v)}
                            ={5v+j\over v^2-j^2}.                \tag{16}
\]

All divisions in (16) are valid because \(j\ne\pm v\).  If two values
\(A_k,A_\ell\) differ, subtracting the \((j,k)\) and \((j,\ell)\)
instances of (15) forces the other seven \(A_j\)'s to be equal.  If no two
differ, all nine are equal.  But a fibre \(A_x=c\) is cut out by

\[
                       c(v^2-x^2)-(5v+x)=0,                     \tag{17}
\]

a nonzero polynomial of degree at most two whose coefficient of \(x\) is
\(-1\).  Every fibre therefore has size at most two, contradicting either
seven or nine equal values.

## 4. Reproducibility

Both exact checkers pass when run from the project root:

    python computations/verify_live_three_zero_higher_split_p18_low_triple_singleton_common_lift_closure.py
    python computations/verify_live_three_zero_higher_split_p18_final_low_triple_independent_audit.py

The first reconstructs the full fifty-family ledger.  The second imports
none of its low-triple calculations and separately verifies every count,
Wronskian cap, sharp divisor dimension, product-rule identity, logarithmic
jet, fibre polynomial, and index cardinality used above.
