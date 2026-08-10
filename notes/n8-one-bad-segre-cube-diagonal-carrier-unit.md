# The Segre--K4 carrier cannot be repaired by arbitrary diagonal cells

## Exact theorem

Let \(H\) be the fixed fourteen-cell common quadratic of the Segre--K4
counterguard.  Add arbitrary decorated cells on all fifteen physical edges,

\[
 q=H+\sum d_{ij}x_i^0x_j^0
     +\sum a_{ij}x_i^1x_j^1
     +\sum b_{ij}x_i^2x_j^2.
\]

Then \(q^{[3]}\ne X_0\) over every characteristic-zero field.  In
particular, adding the two disjoint `11` carriers and two disjoint `22`
carriers forced by the diagonal one-bad responses cannot repair the unary
top while the mixed Segre--K4 part remains fixed.  The statement allows all
thirty such carrier cells at once with arbitrary coefficients; it is not a
support-cardinality search.

## Six-row integral certificate

Order the pure variables by physical edge,

```text
d0=01, d1=02, d2=03, d3=04, d4=05,
d5=12, d6=13, d7=14, d8=15,
d9=23, d10=24, d11=25, d12=34, d13=35, d14=45.
```

For \(g_w=[q^{[3]}]_w\), direct matching expansion gives

\[
\begin{aligned}
[q^{[3]}]_{000000}={}&
 d_{11}g_{000001}-d_{10}g_{000020}+d_9g_{000100}\\
&-(d_1d_6+d_1d_7+d_2d_5+d_3d_5)g_{100020}\\
&+(d_1d_6+d_2d_5)g_{102000}\\
&+(d_1d_6+d_1d_8+d_2d_5+d_4d_5)g_{200001}.
\end{aligned}
\]

The six right-hand coefficients are mixed and therefore vanish in an exact
GHZ source.  The pure coefficient on the left is the fifteen-term hafnian
of \(d\), because no `11` or `22` cell can contribute to the all-zero word.
The identity forces that hafnian to be zero, contradicting the normalized
unary row \([q^{[3]}]_{000000}=1\).

The checker
`computations/verify_n8_one_bad_segre_cube_diagonal_carrier_unit.py`
reconstructs the fifteen physical matchings and the full 45-variable sparse
polynomial identity over the integers.

## Consequence and remaining gate

The preceding response audit showed that a full one-bad packet must leave
the one-zero-endpoint chart by adding diagonal carriers.  The present
identity shows that diagonal carriers alone still cannot restore the unary
top.  Therefore every surviving deformation of this Segre chart must also
change the original one-zero-endpoint mixed carrier: it must add `12/21`
cells, add new `01/10/02/20` cells, or alter/cancel the pinned fourteen
coefficients.  The next useful object is the first variation of the six-row
certificate in those directions, coupled to the four response rows.

This theorem is local to the fixed Segre--K4 initial form.  It does not
normalize every one-bad packet to that form and does not by itself prove the
conjecture.
