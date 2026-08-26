# Independent canonical rank-two branch referee

Status: **PASS for the canonical support, all ranks.** The producer manifest replays, and each of the five characteristic-zero chart results independently has 6,589 input generators, a one-element Gröbner basis, zero unit remainder, and `STATUS=UNIT_IDEAL`. Their source hashes match the five exact generated chart programs.

The rank-two orientation is `A57=UV^T`, `A56=-U(A26V)^T`; the guard reduces to `A06V=0` and `(I-A17A26)V=0`. The five equality-pattern charts exhaust all 27 triples of failed color and chosen nonzero `U,V` minors. The sealed rank-at-most-one theorem supplies the lower-rank branch, while `A06 A57^T=0` with nonzero `A06` excludes rank three.

This proves the active-triangle-or-star dichotomy only for the canonical representative and its named guard mate. An independent 40,320-permutation replay gives transport counts `[1,0,0,0,0,0]`; therefore the other five full-family representatives, all 64 coefficient loci, and any uniform induction remain unproved.
