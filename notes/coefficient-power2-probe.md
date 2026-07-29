# Coefficient-aware `P^2` filtration probe

`computations/coefficient_power2_filtration.py` follows one concrete
coefficient-aware continuation of the diagonal square certificate over
`GF(1009)`.  At each positive off-diagonal degree it solves the actual
nonzero residual, using a goal-directed triangular right inverse, and
propagates the coefficients of every nonleading output through degree six.

The audited run has the following sizes:

\[
\begin{array}{c|r|r}
K\text{-degree}&\text{nonzero residual rows}&\text{nonzero corrections}\\ \hline
2&7{,}575&7{,}941\\
3&88&174\\
4&46{,}795&63{,}147\\
5&62{,}458&90{,}946.
\end{array}
\]

The resulting degree-six residual has 366,992 nonzero row orbits.  Most
importantly, the particular cone row singled out by
`computations/verify_reachable_k9_obstruction.py` has coefficient

\[
 0\pmod {1009}.                                          \tag{1}
\]

Therefore the previously observed path

\[
 \text{degree-six cone row}
 \longrightarrow
 \text{unique cone correction}
 \longrightarrow
 \text{dead degree-nine row}
\]

is an artifact of the coefficient-independent support overapproximation for
this lift: its first arrow is never activated because (1) requires no cone
correction.  The structural reachability certificate remains correct as a
statement about possible supports, but it is not a nonmembership obstruction
for the actual modular coefficients followed here.

This computation proves neither `P^2` membership nor nonmembership in the
full source ideal.  It follows one choice of diagonal solution and triangular
right inverses over one finite field, stops before correcting degree six, and
does not provide a characteristic-zero lift.  Its rigorous conclusion is
only the exact modular zero (1) and the resulting failure of that specific
support-only obstruction.

