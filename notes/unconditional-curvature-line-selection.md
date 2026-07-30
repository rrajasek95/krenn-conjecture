# Every hypothetical realization admits a physical curvature-line representative

## 1. Outcome

Let \(B\) have even size \(N\geq8\), let \(V_u\cong\mathbb C^3\), and
suppose endpoint-ordered aggregate blocks satisfy

\[
                         H_B(A)=\Delta_{B,3}.                    \tag{1}
\]

Among all aggregate solutions of (1), choose one with the fewest nonzero
matrix entries.  Then some centre \(p\), two good neighbours \(q,r\), and
colours \(a,b,c\) have a nonzero canonical transition

\[
 D_{qr}^a(b,c)
 =A_{pq}(a,b)S_{r,c}-A_{pr}(a,c)S_{q,b}\ne0.                    \tag{2}
\]

Consequently there are a fourth site \(s\) and colour \(d\) for which the
literal source-block minor

\[
 \boxed{
 A_{pq}(a,b)A_{rs}(c,d)
 -A_{pr}(a,c)A_{qs}(b,d)\ne0.}                                \tag{3}
\]

After interchanging \(q,r\) if necessary, \(A_{pq}(a,b)\ne0\), and the
physical pair \(pq\) has the canonical cap line

\[
 K_z=E_{ab}+zI.                                                \tag{4}
\]

All but finitely many points of (4) are active: its direct scalar and all
three target coefficients are nonzero.  Thus the complete uniform source
selection problem is no longer

\[
        \text{curved line}\quad\text{or}\quad\text{flat cubic core};
\]

the flat alternative is empty among minimum-support representatives.  Every
hypothetical counterexample can therefore be placed unconditionally on a
generically active, source-provenant curvature line.

This is not yet the clean-cap theorem.  The remaining equation is the
tensor-valued common-root condition

\[
                         {\cal E}_{p,q}(K_z)=0.                 \tag{5}
\]

An active zero of (5) gives the exact \(N\mapsto N-2\) descent.  The result
here proves that the line exists; it does not assert that (5) has a zero.

## 2. The globally flat alternative is impossible

Call a pair good when both deleted endpoint-star maps are injective.  The
[target-flattening theorem](target-flattening-essential-star-pair-bound.md)
proves that the bad-pair graph is \(4\)-degenerate.  In particular it has
a site with at least three good neighbours at every \(N\geq8\), so the
canonical good-fan transitions are available.

Assume for a contradiction that every such physical transition vanishes.
This is precisely the globally flat branch used in the following audited
reductions.

First,
[exact pure-port merging](flat-degree-four-essential-purity-nullity-export.md)
shows that every site with at least three good neighbours is already a
diagonal cubic site in an entry-minimal source.  Put

\[
 C=\{u:\deg_{\rm good}(u)\geq3\},\qquad X=B\setminus C.        \tag{6}
\]

The
[flat boundary-core theorem](flat-cubic-boundary-core-order-eight-reduction.md)
then proves, with a separate independent audit, that global flatness is
impossible at every even order \(N\geq10\).  Its proof retains all
cancellation and uses only exact coefficient factorization on an
exceptional set of at most seven sites.  At \(N=8\) it leaves exactly

\[
                         1\leq|C|\leq4.                        \tag{7}
\]

The four values in (7) are now all excluded.

* The
  [small-core essential-complement obstruction](flat-n8-small-c-essential-complement-obstruction.md)
  excludes \(|C|=1,2\).  Its essential-incidence budget kills one cubic
  site directly.  Equality with two cubic sites forces six distinct
  anchors; purity of one internal essential edge then produces a
  complementary block on a colour line different from the line forced at
  its nonessential endpoint.
* The
  [large-core matching-cut obstruction](flat-n8-large-c-matching-cut-obstruction.md)
  excludes \(|C|=3,4\).  With three cubic sites, one all-cross constant
  fibre forces reciprocal impossible degree inequalities.  With four,
  a fourth occurrence matching fixes the two internal cubic edges and a
  mixed forced selection leaves an active two-site residual which exact
  factorization says must be zero.

These contradictions exhaust (7).  Hence the assumption that every
canonical good-fan transition vanishes is false, proving (2).

## 3. From a transition to an active line

The coefficient of (2) at a fourth site \(s\) in colour \(d\) is exactly
the determinant (3), by the
[canonical transition-pencil theorem](canonical-transition-pencil-fan-dichotomy.md).
Since (3) is nonzero, one of its first-row entries is nonzero; exchange
\(q,r\) if needed so that

\[
                              A_{pq}(a,b)\ne0.                  \tag{8}
\]

For the line (4), let \(s(K)\) be its direct-edge scalar and let
\(\kappa_i(K)\) be its three diagonal target coordinates.  Directly,

\[
 \begin{aligned}
 \kappa_i(K_z)&=\delta_{a,i}\delta_{b,i}+z,\\
 s(K_z)&=A_{pq}(a,b)+z\sum_iA_{pq}(i,i).
 \end{aligned}                                                \tag{9}
\]

Neither polynomial product

\[
                         s(K_z)\prod_{i=0}^2\kappa_i(K_z)       \tag{10}
\]

is identically zero, by (8).  Its complement is therefore a nonempty
Zariski-open subset of the affine line.  Every point in that subset is an
active cap with the exact contracted target rows inherited from (1).

The aggregate minimization used above is legitimate for the decorated
problem.  There are finitely many aggregate coordinates at fixed \(N\),
so a minimum support solution exists whenever any solution exists; every
nonzero aggregate entry lifts to one finite decorated degree-two source.
Endpoint colours, complex weights, and parallel original sources are all
retained by aggregation.

## 4. Exact remaining gate

The clean error on (4) is a degree-\(h\) tensor polynomial, where
\(2h=N-2\).  The currently audited curved reductions isolate its genuine
boundaries:

1. a clean inactive root exports an exact lower-colour source or a nonzero
   nilpotent response packet;
2. two clean roots leave the explicit polarization residual, and at the
   first \(8\to6\) boundary it is \(uv(uR_0+vR_1)\);
3. coordinate roots on the two pair charts in (3) share one literal
   four-cut \((L,M)\) packet and the curvature square \(AU-BF\ne0\).

These are recorded in
[the inactive-root ledger](curved-cap-inactive-root-export-and-osculating-ledger.md)
and the
[two-root curvature-square theorem](curved-two-root-polarization-and-four-cut-square.md).
The shortest remaining main-line theorem is therefore one of the
following equivalent forms of progress:

* prove that the coordinates of \({\cal E}_{p,q}(K_z)\) have a common
  active root using the full transverse target rows and good-star
  injectivity;
* exclude the no-root and all-inactive-root packets simultaneously on the
  two overlapping pair charts selected by (3); or
* turn the inverse two-flag selector behind (3) into a direct one-sided
  order descent.

The first two are bounded resultant/catalecticant problems with literal
source provenance.  None requires reopening the globally flat graph or
enumerating its former low-degree cases.
