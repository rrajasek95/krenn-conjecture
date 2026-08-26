# Aligned-boundary and one-defect audit (current terminal)

The simultaneous B4 census of the three cofactor-orientation masks and the
permanent-term charts has exactly 50 aligned zero-cell representatives.  Exact
mod-1009/mod-1013 screening followed by rational Singular lifts gives 43 unit
ideals and seven nonunit representatives:

```text
(0,12), (0,30), (0,63), (1,12), (1,38), (1,63), (11,21).
```

All 43 units are frozen with their literal source-row ledgers and exact
coefficient identities.  The source-row support histogram is
`{2:13,3:4,4:7,5:8,6:1,7:1,10:1,12:1,13:2,14:3,16:2}`.  This is a census
of the aligned boundary charts only; it is not a classification of the
surrounding open 24-variable charts.  The checker/result SHA256 values are
`ab9a8c53...` and `06cd981b...`; the three-mode logical digest is
`27a36e24f009503149e6162060588f883ee8df7d7f3dcbf7c00ce5556a9ec3f9`.

The assigned survivor `(branch0,term30)` closes more strongly than expected.
Its corrected zero cells are `2,7,11,15,19,22`.  On this chart the pure
Hafnian itself is an exact combination of nine of the sixteen nonzero literal
rows (three triangle and six diagonal-cofactor rows), with 26 terms total.
No localization is used.  Consequently this chart has no H-live Q/X/C
stratum and no partner problem.  The checker/result SHA256 values are
`2606f802...` and `ee876f95...`; logical digest `70041a8c...` is stable under
standard Python, `-O`, and `-I -S`.

The branch1 uniform `d=0`, offdiagonal-all chart has exactly two dimension-one
components, over `z^2-14z-1` and `z^2+2z-1`.  On both, `H=4`; the Q support is
generically size 11 and specializes only at `T=0` to the known size-six set
`{3,5,6,9,10,12}`.  The generic size-11 point cannot be selected as the
smaller member of a Q-compatible pair, but that counting observation alone
does not rule out an unknown support-at-most-five mate.  The two fixed-left
mate ideals are nevertheless exact unit ideals: the generic Q support forces
the eleven barred mate Q equations, the generic cofactor support forces the
five mate entry zeros, and the generic entry support forces all position
0/1/2 mate cofactor equations.  Both raw identities use 14 nonzero
coefficients and no H inverse.  Independent classifier logical digest is
`fe7e4604...`; its checker/result SHA256 values are `c42b20cd...` and
`d6c93112...`.  Independent mate-unit logical digest is `016ab93b...`; its
checker/result SHA256 values are `9a3845a1...` and `7d63c696...`.

The final aligned survivor `(branch11,term21)` is also completely classified.
With gauge `b0=b4=a3=1`, the 16 nonzero raw specialized rows (15 distinct)
have Gröbner basis size 30 and dimension one.  Exact `minAssGTZ` returns two
and only two dimension-one primes, each with Gröbner basis size 14.  They are
the two displayed affine lines over `Q(r), r^2-2r-1=0`; raw substitution
replays all 22 source rows and gives `H=4`.  At `T=0` both have Q support six
`{1,4,7,8,11,14}`; for `T!=0` both have Q support eleven
`{0,1,2,3,4,6,7,8,10,11,14}` and the same 17-cell entry support.  Their
generic cofactor supports are respectively `{3,9,10,12,15,21}` and
`{3,4,7,17,18,21}`.

Those three support ledgers force the companion mate equations literally:
barred Q zeros, cofactors at the 17 left-entry positions, and cells at the six
left-cofactor positions.  The two resulting 38-row ideals have exact unit
certificates using 22 and 14 nonzero source coefficients.  The independent
referee additionally lifts each quotient identity back to the full
24-variable ring with all six forced cell equations (six and five nonzero
correction coefficients); deletion mutations fire.  The producer
classification/certificate logical digests are `bcb36aae...` and
`666b8ba0...`.  Independent three-mode logical digest is `479886e8...`, with
checker/result SHA256 values `c56a8cba...` and `cd15d6f7...`.  This closes
the aligned `(11,21)` boundary and its B4 transforms, not off-boundary
releases.

Finally, the branch0/offdiagonal-all aligned boundary is rigid against a
single lower-right-entry defect.  For a released `d=d_01` and
`c_01=-(1+a_01*d)/b_01`, two literal cofactor rows give

```text
(b0*b1*b2*b4*z/2)*(cofactor_1_0+cofactor_2_0)
  - d*(z*b0*b1*b2*b3*b4*b5-1) = d.
```

Thus only the product of the six live `b` entries is localized; the producer's
H localizer has zero coefficient.  Direct raw replays on all six edges,
including the denominator changes caused by endpoint transposition, verify
that the S4 edge action transports the result to every single defect.
Simultaneous defects on two or more edges remain out of scope.  Logical digest
is `80484ccc...`; checker/result SHA256 values are `58cc103c...` and
`97766d3c...`, stable in all three modes.

# Diagonal-packet component audit (current terminal)

The only support-level mates of the branch-51 one-coordinate axis are now
excluded by a compact universal unit identity.  Normalize the left live Q
support to `{0,1,3,5,6,9,10,12}`.  Then the mate support is forced to
`{0,1,2,4,7,8,11,13}`, its branch mask is one of 7, 25, 42, and the left
cofactor signature forces mate entries
`x3=x7=x9=x10=x13=x14=x19=x23=0`.  Raw 4+4 rows force `Q3=Q5=0`.  Modulo
those entry zeros, the exact identity is

```text
2 = x15*x16*x21*e01 + x15*x17*x20*e02
    + e12 + e13 + e23 - t123
    - x6*x15*x20*Q3 - x2*x15*x16*Q5.
```

The checker stores the six explicit entry-zero correction multipliers, so
this is a literal polynomial certificate rather than quotient arithmetic.
It reconstructs the left generic-axis signature over
`Q(r), r^2+2r-1=0`, and replays the source core labels from all 105 raw
perfect matchings.  No selected cofactor equation and no Hafnian inverse is
used; consequently the same certificate kills all three forced branches.

The attempted one-colour support lower bound is false.  The exact checker
`audit_weight0_char0_family_and_packet.py` verifies two H-live
characteristic-zero components from raw matching definitions:

- a support-eight family over `Q(sqrt(2),sqrt(65))`, whose full 384-element
  B4 action produces 96 distinct joint supports; all 9,216 ordered pairs fail
  the necessary 4+4 packet, with at least two offending coordinates;
- a support-six point over `Q(sqrt(2))` with `H=4`, Q support
  `{3,5,6,9,10,12}`, all twelve antidiagonal X cells live, and cofactor support
  `{9,10,13,14}`.  Its enriched B4 orbit has 24 elements.  Of 576 ordered
  pairs, 288 pass the Q-support test, but every one of those fails both
  `X_left*C_right` and `X_right*C_left`; hence zero pass the full support test.

The exact-Q NONUNIT ideals obtained by allowing seven Q coordinates do not
establish exact support-seven components: both contain this support-six point.
The exact d=0 normal form makes the remaining support-eight handoff finite.
The four one-coordinate strata `F union {Q0,Qi}` are one joint B4 orbit of
size 192.  After normalizing the left branch to mask 51 with live support
`{0,1,3,5,6,9,10,12}`, compatibility forces the right live support to be
`{0,1,2,4,7,8,11,13}` and leaves only branch masks 7, 25, and 42 (two orbits
under the normalized left stabilizer: `{7}` and `{25,42}`).  The two-coordinate
`Q0=0` strata form orbits of sizes 192 and 96 and have no support-compatible
mate, including across the one-coordinate orbit.

Independent replay of the root-integration normal-form checker (logical digest
`49b276074d8a6bd311b63a3ff593b923a59053623742d3e3ad85bbfe2d4d4ef7`)
also retains the literal entry/cofactor masks on the punctured one-coordinate
lines.  Across the support-six and one-coordinate enriched orbits it finds
2,016 Q-compatible ordered pairs, but zero satisfy either directional
entry/cofactor condition.  This closes the full diagonal packet on the
localized branch-51 `d=0`, support-at-most-eight chart.

The decisive remaining gate is a component classification (or a different
source-level argument) excluding compatible cross-pairs involving other
H-live components of the three cofactor-orientation branch ideals.  No such
global classification is claimed here.

Endpoint/orientation controls use raw 105-perfect-matching evaluation and the
full B4 group; the global clone flip is retained because it is not redundant
for Q supports.  The checker is replayed under standard Python, `-O`, and
`-I -S`, with a coefficient mutation required to fire.

# Orbit0 T-square leading test (superseded route history)

Status: setup.  This lane tests only whether the certified cutoff-8 leading
class `R8` has a **positive direct** representation in the degree-24,
K-degree-16 associated-graded image.

The frozen input is the 301-row invariant quotient residual with logical
digest `25d4acd094eb27e78e3941b738611522f112f57f4ef6f78f3657d50e18762d03`.
Its coefficients are integral multiples of 48 and its labelled support has
453,600 degree-12 monomials.

For residual orbit `i`, quotient mass `m_i`, and orbit size `s_i`, the labelled
coefficient is `m_i/s_i`.  For `i<j`, fixing the first representative and
enumerating `y` in the second orbit contributes

`2 m_i m_j / s_j * #{ y : can(r_i y)=k }`

to product orbit `k`; the diagonal has no factor two.  The implementation must
retain repeated variables in the 24-cell product monomial.

Methodology guard: the direct min-K16 matrix omits hidden initial forms from
lower-K cancellations.  A positive representation is valid.  A negative
result is **not** a global obstruction without the complete cutoff-below-17
kernel/whole truncated component.
