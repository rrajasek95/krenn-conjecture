# Independent audit of the induced-zero-shore hierarchy

## Verdict

**PASS, with no mathematical correction.**  I reconstructed the theorem in
[good-pair-fan-induced-zero-four-cut-reduction.md](good-pair-fan-induced-zero-four-cut-reduction.md)
without using its checker as evidence.  For every integer \(k\geq1\) and
even \(N\geq7k+7\), the stated fan dichotomy, induced-zero shore of size
\(h=k+1\), sparse injective shore frames, and common-power identity are
valid.  In particular, the first four-vertex case really begins at
\(k=3,N=28\), with escape count \(N-27\).

The palette qualification in the primary note is necessary and correctly
stated: zero blocks, supports, Hessians, and selected shores belong to one
fixed functorial ternary projection.  They need not hold termwise among
parallel decorated sources or simultaneously for different palette
triples.  Within that scope, zero blocks, endpoint asymmetry, parallel
aggregates, and arbitrary complex cancellation are all retained.

The independent executable audit is
[audit_good_pair_fan_induced_zero_four_cut_reduction_independent.py](../computations/audit_good_pair_fan_induced_zero_four_cut_reduction_independent.py).
It imports neither primary artifact.

## Frozen primary inputs

The exact primary files audited here had SHA-256 digests

    ba9e7f3d67ecaa13f2cb209932310a7f7789b3e79fc8a6afcd92379545974fb3  notes/good-pair-fan-induced-zero-four-cut-reduction.md
    5edbb2bd60b1f8333c96d2246adc74a8e606b87becc6ea7b417c05c9c2558f20  computations/verify_good_pair_fan_induced_zero_four_cut_reduction.py

The independent checker had SHA-256 digest

    b7f5a99ec36bd21a6bd73c8276277bacd60f3aba1e045b267e393f937ceb99c7  computations/audit_good_pair_fan_induced_zero_four_cut_reduction_independent.py

## 1. The full \(k\)-parameter fan ledger

The target-flattening essential-star theorem gives a vertex \(r\) in at
least \(N-7\) good pairs.  Let \(F\) be the set of neighbours for which the
pair-deleted source Hessian has only vertex-gauge kernel and its rank-three
block graph is connected and nonbipartite.  These are exactly the regular
nonbipartite fan members; the complement consists of the three escape
charts named in the theorem.

For \(x\in F\), the regular-chart sparse-row theorem gives, for each colour
\(c\),

\[
             |S_c(r)\setminus\{x\}|\leq2.               \tag{A1}
\]

If four distinct deletions satisfy (A1), then \(|S_c(r)|\leq2\).  Indeed,
a support of size at least four survives every one-point deletion with
size at least three, while a support of size three can satisfy (A1) only
when the deleted vertex belongs to that three-set; four distinct deleted
vertices make that impossible.  In the nonescape case below,
\(|F|\geq7k\geq7\), so this four-deletion argument always applies.  Hence

\[
 C=S_0(r)\cup S_1(r)\cup S_2(r),\qquad |C|\leq6.        \tag{A2}
\]

Every \(x\in Z:=F\setminus C\) has all three \(r\)-endpoint rows zero, so
the whole aggregate tensor block \(A_{rx}\) is literally zero.

Now split at the exact integer threshold.  If \(|F|\leq7k-1\), the fan has
at least

\[
       (N-7)-(7k-1)=N-7k-6                            \tag{A3}
\]

nonregular pairs.  If \(|F|\geq7k\), then

\[
       |Z|\geq |F|-6\geq7k-6.                          \tag{A4}
\]

Because \(N\geq7k+7\), the escape count in (A3) is nonnegative and in fact
at least one.  No parity rounding is hidden here; if \(7k+7\) is odd, the
smallest admissible even \(N\) is simply the next integer.

## 2. Why the block-support graph has degree at most six

Apply the same regular-chart theorem at the other endpoint of a pair
\(\{r,x\}\), with \(x\in Z\).  It initially bounds each global colour-row
support after deleting \(r\).  Since \(A_{xr}=0\), restoring \(r\) adds no
support, and therefore

\[
                         |S_d(x)|\leq2
                     \qquad(d=0,1,2).                  \tag{A5}
\]

If an aggregate block \(A_{xy}\) is nonzero, at least one of its three
rows in \(x\mid y\) orientation is nonzero.  Thus every neighbour \(y\)
of \(x\) belongs to \(S_0(x)\cup S_1(x)\cup S_2(x)\), a set of size at
most six.  This proves \(\Delta(G_Z)\leq6\); it does not assume that the
three two-site supports coincide.

A greedy algorithm colours a maximum-degree-six graph with seven colours.
Its largest colour class is independent and has size at least

\[
        \left\lceil {|Z|\over7}\right\rceil
        \geq \left\lceil {7k-6\over7}\right\rceil=k.   \tag{A6}
\]

The denominator seven is sharp for this information: disjoint copies of
\(K_7\) have maximum degree six and independence number one per copy.
Selecting \(u_1,\ldots,u_k\) from the class in (A6) makes every
\(A_{u_i u_j}\) zero.  Equation (A2) also makes every \(A_{ru_i}\) zero,
so \(S=\{r,u_1,\ldots,u_k\}\) is an induced aggregate-zero shore.

## 3. Injectivity and coordinate anchors survive removing the shore

At any endpoint \(x\), the mode-\(x\) image of every source matching term
lies in the sum of the mode-\(x\) supports of the incident aggregate
blocks.  The mode-\(x\) flattening of the ternary diagonal target has image
all of \(V_x\cong\mathbb C^3\).  Therefore the complete aggregate star at
every vertex is injective.

For a named \(x_j\in S\), all blocks from \(x_j\) to \(S\setminus\{x_j\}\)
are zero.  Removing every named zero block therefore leaves exactly the
complete star, now written into \(D=B\setminus S\).  Its three endpoint
rows are linearly independent.  The same observation after deleting just
one other named endpoint proves that every pair internal to \(S\) is
doubly aggregate-injective, even though the independent-set construction
did not require the pairs \(u_i u_j\) to be good beforehand.

Every named row has physical support at most two: this is (A2) for \(r\)
and (A5) for each \(u_i\).  For completeness, the coordinate-anchor step
can be reconstructed directly.  If \(p=p_a+p_b\) and a near-top tensor
\(F\) obeys \(pF=X_c\), quotient the \(a\)-factor by
\(\mathbb Cp_a\) and the \(b\)-factor by \(\mathbb Cp_b\).  The left side
vanishes, while the target maps to

\[
 (e_c^{(a)}\bmod p_a)\otimes(e_c^{(b)}\bmod p_b)
       \otimes X_c^{\mathrm{rest}}.                    \tag{A7}
\]

This pure tensor can vanish only if \(p_a\parallel e_c^{(a)}\) or
\(p_b\parallel e_c^{(b)}\).  The one-support case is the same tensor-rank
argument with one factor.  Since every named-to-named block is zero, the
resulting coordinate anchor is a site of \(D\).

## 4. The \(h=k+1\) common-power identity and its exact coefficient

Write \(N=2m\), \(h=k+1\), and let \(q\) be the internal quadratic on
\(D=B\setminus S\).  With the endpoint order kept at each named vertex,
the aggregate quadratic is exactly

\[
 a=q+\sum_{j=0}^{h-1}\sum_{c=0}^2
           e_c^{(x_j)}p_c^{(j)}.                        \tag{A8}
\]

There is no term using two named sites.  Consequently a perfect matching
must send the \(h\) ordered named vertices injectively to \(h\) sites of
\(D\), then match the remaining \(N-2h\) sites internally.  In the divided
power \(a^{[m]}=a^m/m!\), choosing each of the \(h\) square-zero named-star
summands once cancels the multinomial factor exactly.  The coefficient at
named colours \(c_0,\ldots,c_{h-1}\) is therefore

\[
 \left(\prod_{j=0}^{h-1}p_{c_j}^{(j)}\right)q^{[m-h]}. \tag{A9}
\]

The corresponding contraction of the target is zero unless all named
colours agree, and is \(X_{c_0}^D\) when they do.  This proves all \(3^h\)
identities with no missing factorial.

Before colour decoration, there are \((N-h)_h\) injections from the
ordered named vertices into the \(N-h\) complement sites.  Each leaves
\(N-2h\) complement sites, with \((N-2h-1)!!\) perfect matchings.  Hence
the exact support count is

\[
                  (N-h)_h (N-2h-1)!!.                  \tag{A10}
\]

For \(h=4\), this specializes to
\((N-4)(N-5)(N-6)(N-7)(N-9)!!\), exactly as stated.

## 5. The \(6h\)-port cap is literal and cancellation-safe

Let \(P\) be the union of the physical supports of all \(3h\) named rows.
Each row meets at most two sites, so

\[
                             |P|\leq6h.                 \tag{A11}
\]

The same-colour equation in (A9) is nonzero.  Any contributing product
must choose \(h\) distinct row-support sites, and hence \(|P|\geq h\).
This justifies the degree \(|P|-h\) used below, including cases where
different rows or frames share most of their ports.

Put \(Q=q^{[m-h]}\).  It has degree \(|D|-h\) in the site-square-zero
algebra, so it decomposes uniquely into sectors \(Q_{\widehat H}\), one
for every \(h\)-element set \(H\) of missing physical sites.  A product
of the \(h\) named rows can fill \(Q_{\widehat H}\) only by choosing one
distinct local row component at every site of \(H\).  Since all those
components are supported in \(P\), every sector with \(H\nsubseteq P\)
is annihilated by every one of the \(3^h\) row products.  This is a
multigraded statement about the complete aggregate tensor; it does not
separate terms inside a cancelling coefficient of \(Q\).

Discard those universally invisible sectors.  Every remaining sector is
occupied at every site of \(D\setminus P\).  Contract those factors with
the product of the local covectors

\[
              \kappa_x(e_0)=\kappa_x(e_1)=\kappa_x(e_2)=1.
\]

The result is one common degree-\((|P|-h)\) tensor \(\overline Q\) on
\(P\).  Contraction commutes with multiplication by the named rows,
because they are supported in \(P\), while
\(\bigotimes_{x\in D\setminus P}\kappa_x\) sends \(X_c^D\) to \(X_c^P\).
Therefore

\[
 \left(\prod_{j=0}^{h-1}p^{(j)}_{c_j}\right)\overline Q
       =\delta_{c_0=\cdots=c_{h-1}}X_{c_0}^P.          \tag{A12}
\]

This proves the advertised finite interface: \(h=4\) gives all 81
equations on at most 24 ports.  Crucially, \(\overline Q\) is only the
literal cap of the visible sectors of the one common \(q^{[m-h]}\).
Neither the proof nor the statement promotes it to a divided power of a
quadratic on \(P\).

## 6. Endpoint, aggregation, cancellation, and palette audit

The rows \(p_c^{(j)}\) are oriented toward their named endpoint.  If a
physical block is stored in the opposite numerical order, its matrix is
transposed before the row is taken; (A8)--(A9) still attach each colour to
the correct physical tensor factor.  No symmetry between endpoint colours
is used.

Parallel decorated sources on one physical pair may be summed into one
aggregate block because a perfect matching uses that physical pair at
most once.  Distributivity then makes the decorated matching sum exactly
the hafnian coefficient of the aggregate matrices.  Aggregate entries and
whole blocks are allowed to vanish by complex cancellation.  The proof
uses those aggregate zeros only and never selects a nonzero summand from a
cancelling coefficient.

For a larger palette, fix a triple and project every endpoint colour space
functorially onto it.  The matching polynomial commutes with this linear
projection and the full diagonal target maps to \(\Delta_{B,3}\).  The
entire argument then applies to that projected ternary system.  Changing
the triple can change every support, good pair, Hessian chart, and selected
shore; the theorem makes no simultaneous claim.

## 7. Independent executable checks

The standalone clean-room checker:

* checks 2,767,940 full \(k,N,|F|\) threshold cases through \(k=60\) and
  even order \(500\);
* exhausts the four-deletion support implication on eight sites and all
  triples of row supports of size at most two on nine sites;
* constructs and greedily colours sharp disjoint-\(K_7\), circulant, and
  deterministic maximum-degree-six graphs;
* builds an endpoint-asymmetric induced-zero \(K_4\), verifies that its
  complete, shore-deleted, and every pair-deleted star all have rank three,
  and checks its coordinate anchors;
* exhausts 17,298 two-support anchor membership tests over
  \(\mathbb F_5\);
* enumerates all-star matching classes through order fourteen and checks
  signed, zero-entry, endpoint-asymmetric numerical coefficients in 6,406
  common-power cases through \(h=4\);
* expands arbitrary signed \(h\)-hole tensors through \(h=4\), checks that
  precisely the sectors with hole set contained in \(P\) are visible, and
  verifies that product capping commutes with every selected sparse row
  product and sends \(X_c^D\) to \(X_c^P\); and
* expands every decorated parallel-edge choice for all 729 ternary words
  at six sites, verifying aggregation, exact cancellations, and a fixed
  three-colour projection of a five-colour system.

Both the primary and independent checkers return **PASS**.  These finite
checks audit the ledgers and identities; the arguments above establish the
uniform characteristic-zero statements.  This remains a reduction, not a
proof of Krenn's conjecture: excluding the common-power shore identity or
closing one of the three nonregular Hessian charts is still required.
