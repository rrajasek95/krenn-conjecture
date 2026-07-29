# A primitive GHZ jet that survives modulo eight

This note records an exact warning against any specialization argument that
expects the first failed lift to occur modulo eight.  On vertices
`0,1,2,3,4,5`, take the following nine same-color aggregate entries, with all
unlisted entries zero:

\[
\begin{array}{c|ccc}
\text{color}&\multicolumn{3}{c}{\text{edge and weight}}\\ \hline
0&01:1&25:2&34:1\\
1&02:1&13:2&45:1\\
2&04:2&12:1&35:1.
\end{array}
\]

The source is primitive because it has odd entries.  Exact enumeration of the
15 perfect matchings and all (3^6) colorings gives the integer identity

\[
 H_6(A)=2\Delta_{6,3}
 +8e_2\otimes e_1\otimes e_0\otimes e_1\otimes e_2\otimes e_0.
\]

Indeed, the three displayed rows give the three monochromatic coefficients,
each equal to (2).  The only additional supported perfect matching is

\[
 04\mid13\mid25,
\]

whose three weights are (2,2,2), giving the displayed mixed coefficient
(8).  Thus

\[
 H_6(A)\equiv2\Delta_{6,3}\pmod 8.
\]

This particular residue class cannot lift one step farther.  Put
(q=(2,1,0,1,2,0)).  For every perfect matching, the three entries selected
by (q) contain no pair of odd entries.  If (A'=A+8C), the change of a
matching monomial modulo (16) is a sum of terms

\[
 8C_e\prod_{f\ne e}A_f,
\]

and every displayed product is even.  Hence

\[
 H_6(A')_q\equiv H_6(A)_q\equiv8\pmod {16},
\]

whereas the target (2\Delta_{6,3}) has coefficient zero at (q).

The verifier
[`verify_base_locus_ghz_second_jet.py`](../computations/verify_base_locus_ghz_second_jet.py)
checks the exact integer identity, all 729 coefficients, primitivity, and the
vanishing derivative at (q).  The result says only that obstruction order is
not uniformly bounded by the first jet: an obstruction appears at modulus
four for some fibers and at modulus sixteen for this fiber.  It does **not**
show that finite-order lifting can be delayed arbitrarily, nor that every
primitive modulo-eight solution is obstructed modulo sixteen.
