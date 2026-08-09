# The Lemma-E shared packet passes support but its first sparse tori are empty

Bounded exact advance on the sole selected-witness dependency packet.  The
literal support shadow is **SAT** in both inequivalent shared-head cases.
Thus the diagonal essential packet is not killed by a singleton-matching
argument alone.  Deterministic deletion produces source-faithful 39- and
46-cell packets, each irredundant under every one-cell deletion.  Both full
support tori are nevertheless coefficient-empty: three literal two-term
source rows form an odd Laurent circuit and give an exact `2 * unit`
certificate.

This does not close the normalized packet.  The frozen supports are the
first canonical sparse packets, not an exhaustive support-poset census or a
proof of globally minimum cardinality.  Their value is diagnostic: the next
theorem must propagate the three-row character obstruction, or find a
different coefficient identity, across arbitrary support.  A larger generic
P5/Hasse or face-by-face search is not implicated.

## 1. Exact normalized packet

Let the deficient reciprocal arm be `pq`, normalize sites

```text
p=0, q=1, r=2, residual sites=2,3,4,5,6,7,
```

and normalize its essential colour and coefficient to

\[
                         A_{01}=E_{00}.                    \tag{1}
\]

Lemma E gives the two load-bearing identities

\[
 (A_{0x})_{0,*}=0\quad(x\ne1),
 \qquad H_{\{2,\ldots,7\}}(A)=e_0^{\otimes6}.             \tag{2}
\]

Write `Q` for the aggregate matrix on the six residual sites, and `p_i,s_j`
for the two endpoint stars.  Expanding the eight-site hafnian by the
partners of `p,q` gives all nine pair-response tensors

\[
 \delta_{i0}\delta_{j0}Q^{[3]}+p_i s_jQ^{[2]}
                         =\delta_{ij}X_i.                  \tag{3}
\]

Here `X_i=e_i^{tensor6}`.  By (2), `p_0=0` and `Q^[3]=X_0`, so the nontrivial
rows are

\[
       p_b s_jQ^{[2]}=\delta_{bj}X_b,qquad b=1,2,quad
       j=0,1,2.                                            \tag{4}
\]

The second reciprocal arm has outgoing colour one, distinct from the
essential colour zero.  Its shared-site head has two inequivalent values
under the remaining colour stabilizer:

\[
                         A_{02}=E_{11}quad\text{or}\quad E_{21}. \tag{5}
\]

The checker retains literal endpoint-labelled cells and ordinary
site-square-zero perfect matchings throughout; it does not replace (3) by
abstract tensor rows.

## 2. The exact support-shadow test

For a proposed cell support, a necessary condition for (2)--(3) over an
integral domain is:

1. every nonzero target fibre has at least one supported matching monomial;
2. every zero target fibre has either zero or at least two supported
   matching monomials—exactly one cannot cancel.

The audit checks all 729 residual words against the 15 six-site perfect
matchings and all 6,561 pair words against the 105 eight-site perfect
matchings.  Both cases in (5) have literal support-shadow witnesses.

The smaller, diagonal-head packet has 39 total cells (the two fixed units
plus 37 optional cells).  Its complete matching histogram is

```text
residual target: 1 word with 2 monomials
residual zero:   699 with 0, 29 with 2
full targets:    3 words with 2 monomials
full zero:       6337 with 0, 209 with 2, 12 with 4
```

The off-diagonal-head packet has 46 total cells (two fixed plus 44 optional):

```text
residual target: 1 word with 2 monomials
residual zero:   668 with 0, 60 with 2
full targets:    3 words with 2 monomials
full zero:       6328 with 0, 218 with 2, 12 with 4
```

Every optional cell in either frozen support has a machine-recorded witness
fibre which violates the shadow after that cell alone is deleted.  This is
the precise `deletion-irredundant` claim.  Because the shadow property is not
monotone under deleting several cells—a singleton can later become empty—the
note does **not** turn this into an unsupported global-minimality claim.

## 3. Diagonal-head coefficient unit

For `A_02=E_11`, take the following three zero target words.  The first is a
residual word (the leading `00` only pads sites `p,q`); the other two are full
eight-site words:

```text
00020200   residual
22020000   full
22221220   full
```

Each row has exactly two supported monomials.  Write its equation as
`E_i=m_i0+m_i1=0`.  Their exponent differences satisfy

\[
  \exp(m_{10}/m_{11})+\exp(m_{20}/m_{21})
                       =\exp(m_{30}/m_{31}).               \tag{6}
\]

The exact monomials are frozen in the checker.  For example, after cancelling
common factors, (6) reads

```text
(+23_02 +57_20 -27_00 -35_22)
+(+13_22 +27_00 -17_20 -23_02)
= +13_22 +57_20 -17_20 -35_22.
```

Consequently the literal polynomial combination

\[
 m_{20}m_{31}E_1-m_{11}m_{31}E_2+m_{11}m_{21}E_3
                              =2M                         \tag{7}
\]

has `M=m10*m20*m31=m11*m21*m30`.  Every cell of `M` belongs to the frozen
support and is nonzero on its torus, so `M` is a Laurent unit.  Equation (7)
is a contradiction in characteristic zero (indeed in every characteristic
other than two).

## 4. Off-diagonal-head coefficient unit

For `A_02=E_21`, the same circuit already occurs entirely inside the
residual unary-top equation.  The three words are

```text
00001001   residual
00020001   residual
00021201   residual
```

Their two matching monomials again obey (6), and the identical polynomial
combination (7) reduces to twice a support-torus unit.  Thus both canonical
sparse packets are coefficient-empty without using the later endpoint rows
for the second circuit.

The result is stronger than a numerical or finite-field failure: it is an
exact source-row identity with literal matching provenance.  It is weaker
than global infeasibility because a different support can have a different
binomial character lattice or higher-term fibres.

## 5. Proof consequence and next target

The earliest decisive facts are now:

\[
 \boxed{\text{the nine-row support shadow is SAT}}
 \qquad\text{and}\qquad
 \boxed{\text{its first irredundant sparse tori are coefficient-empty}.}
\]

Therefore a pure support-only proof of the shared Lemma-E packet is false in
its naive singleton form.  The three-row circuit suggests the smallest
theorem-directed continuation: derive a support-independent signed-character
or matching-exchange identity from `Q^[3]=X_0`, then couple it to the two
nonzero diagonal responses in (4).  Alternatively, an exact rational point
of (2)--(4) would be a decisive counterexample packet and must pass these
character constraints.

## 6. Reproduction and scope

Run

```text
.venv/bin/python computations/verify_n8_lemma_e_shared_unary_top_support_packets.py
.venv/bin/python -O computations/verify_n8_lemma_e_shared_unary_top_support_packets.py
```

The checker is solver-free on the frozen packets.  It enumerates every
residual and pair-response fibre, verifies each deletion witness, expands the
three source rows, checks their exponent identity, and multiplies out the
Laurent certificate (7).  Frozen digest:

```text
125fa4d16c3e4e25dc7fda24706e398b27540acdb5416aa3a4973e5b18df6410
```

The theorem covers only the two displayed support tori and their one-cell
deletion audit.  It does not prove the full normalized packet inconsistent,
provide an exact packet point, complete the shared-goodness lemma, or prove
the N=8 conjecture.
