# The four-row toy HPL is not source-faithful

This is an exact local no-go and a specification of the minimal missing
relative cell.  It does not exclude a homological-perturbation construction
in a larger label-diagonal or augmented path-forest complex.

## 1. The quotient circuit has a hidden actual row

Remove the common factor

```text
00 0d 11 7e ab dc e0 f3
```

from the chart-25 dual circuit and use

\[
 A=(13)(56),\qquad B=(15)(36),
\]

with states $u=1111,v=2222,s=1212,t=2121$.  The canonical
invariant quotient records three $AB$ representatives and one $B^2$
representative.  The individual-row lift over this fixed common factor has
five rows:

\[
\begin{array}{c|c|c|c}
&\text{factorization}&\text{residual}&\text{actual dual weight}\\ \hline
A_1&A_uB_v&4c62bce5&-1/4\\
A_2&A_sB_t&4d62b8e6&-1/4\\
A_3&A_tB_s&4f5ebce8&-1/4\\
A_4&A_vB_u&505eb8e9&-1/4\\
D&B_uB_v&5e62b8bc&+1/4.
\end{array}                                                   \tag{1}
\]

The fourth $AB$ row is not a new quotient coordinate: it lies in the
eight-element orbit of the first row.  This is why that quotient coordinate
has value $-2$, whereas the other two $AB$ coordinates have value
$-1$.  Consequently the four-entry quotient packet cannot be treated as
a source-labelled local packet.  The literal fibre has four degree-two
$AB$ rows and one degree-four parallel row.

## 2. Exact source incidence

Expand the full dual to its 20 individual rows and enumerate every actual
mixed-hafnian source column incident to them.  There are 56.  Every one hits
exactly two dual rows: one row of weight $-1/4$ and one row of weight
$+1/4$.  The incidence graph is four disjoint stars, with 16 negative
leaves and four positive centres.  Its 16 leaf-centre pairs have source
multiplicity three or four, eight pairs of each kind.

The star over the displayed $D$ has precisely the four leaves in (1),
with source multiplicities

\[
                            (3,4,4,3).                    \tag{2}
\]

It follows without a term order or a rank computation that the restriction
of every rational source boundary satisfies

\[
                  [D]=[A_1]+[A_2]+[A_3]+[A_4].           \tag{3}
\]

Here brackets mean coefficients in the boundary, not equality of monomial
rows.  Equation (3) is also the local statement that the actual dual weights
annihilate every source column.

The naive quotient-level packet

\[
                       q=-A_1-A_2-A_3+D                  \tag{4}
\]

violates (3) by four and pairs with the actual dual by $1$.  Any source
lift with the four displayed coordinates (4) is forced to contain

\[
                            +4A_4.                        \tag{5}
\]

The checker exhibits such a lift using four individually labelled source
columns.  Its local trace is

\[
                 -A_1-A_2-A_3+4A_4+D,                   \tag{6}
\]

its full boundary has 385 rows, and its pairing with the complete dual is
zero.  Thus (5) is not an optional choice of representative.  It is the
unique missing coordinate required by source incidence.

## 3. Literal one-pair contraction gives $-3D$

The five-row quotient of the actual source complex does contain literal
acyclic pairs.  Choose one of the three labelled columns joining $A_4$ to
$D$, put

\[
                         d_0u=A_4,\qquad h(A_4)=u,        \tag{7}
\]

and retain a differently labelled column above the same incidence edge in
the source representative $x$.  To obtain

\[
                         p\delta i(x)=-A_1-A_2-A_3       \tag{8}
\]

with no direct $D$ component, equation (3) forces coefficient $+3$ on
the unmatched $A_4-D$ column.  Therefore $\delta i(x)$ has coefficient
$+3$ on the matched row $A_4$.  With the conventions of the augmented
HPL lemma,

\[
               -p\delta h\delta i(x)=-3D,               \tag{9}
\]

not $+D$.  The transferred packet is

\[
                       -A_1-A_2-A_3-3D,                  \tag{10}
\]

which satisfies (3) and has corrected augmentation zero, as every genuine
transferred boundary must.  The two simultaneous requirements in the toy
model instead demand coefficient $+3$ on $A_4$ to cancel the direct
$D$ term and coefficient $-1$ on $A_4$ to produce the desired second
term.  Their discrepancy is exactly four.

This also reconciles the local calculation with the augmented formula

\[
       a_H=a(1+h\delta)^{-1}i,\qquad a_HD=0.             \tag{11}
\]

Using the naive four displayed coefficients gives augmentation $1$.
The source-forced hidden coordinate (5) contributes $-1$, restoring the
zero in (11).  Calling the naive value the physical readout would therefore
discard the entire corrected-augmentation term.

## 4. Source-label lift choices

There are three individually labelled choices for $u$ in (7), and two
remaining choices for the repeated edge used in $x$.  Including the
choices on the other three star edges gives 288 literal local realizations.
The three possible values of $h(A_4)$ agree on all 20 dual-support rows,
but their full boundary differences have respectively 180, 180, and 204
nonzero rows away from that support.  Thus the local row projection does not
specify a chain-level contraction.

Those differences are honest mixed-source boundaries, so every genuine
augmentation annihilates them.  This is exactly why the corrected
augmentation is the right invariant.  It also shows what a global
construction must retain: a specified labelled lift, or higher cells which
identify these choices before the physical target is read.

## 5. The minimal missing cell

Relative to (8)--(9), the missing projected incidence vector is

\[
                              4D.                         \tag{12}
\]

No linear combination of the known mixed-hafnian source columns can have
(12), since every such combination satisfies (3).  In fact its pairing
with the source-annihilating dual is $1$.  Hence the missing operation
cannot be another ordinary member of the frozen source family, nor can a
fixed-base source syzygy alter the equation: syzygies have zero output
boundary.

There are only two consistent interpretations.

1. Keep the raw source complex.  Then the actual second transfer is (9), and
   the four-row quotient toy must not be used as a curvature obstruction.
2. Enlarge to a relative label-diagonal/target complex containing a new cell
   whose projected boundary contribution is (12), together with an extended
   augmentation which cancels its nonzero dual value.

Thus (12), not an unspecified extra homotopy, is the precise minimal new
datum required for the proposed confluent construction.  It should be sought
in the diagonal Koszul/relative target direction; it is provably absent from
the existing mixed-hafnian source columns on this fibre.

Run

```text
python3 computations/verify_n8_literal_hafnian_hpl_no_go.py
python3 -O computations/verify_n8_literal_hafnian_hpl_no_go.py
python3 -I computations/verify_n8_literal_hafnian_hpl_no_go.py
python3 -S computations/verify_n8_literal_hafnian_hpl_no_go.py
```

The frozen exact ledger digest is
`501f74cb2441c4ce451fc4db2cc8a1d6c13f7a8bc9eec98a14d115d4a406034e`.
