# Characteristic-zero lift of the profile71 crossing packet

## Verdict

The `maxabs=16001` balanced vector at `p=32003` is a poor lift of a
half-integral rational dual, not evidence of prime-dependent rank.
Multiplying the modular vector by two and balancing produces a primitive
integer separator of support 138 and maximum absolute coefficient 8.

Exact replay at primes 31991, 32003, 32009, and 32749 gives the same:

- 177,996 independent initial rows;
- the complete 33-round rank/crossing/pivot-size signature;
- terminal rank 185,635 and remainder size 13,636;
- the same 138 dual columns.

At every prime, doubling the 138 coefficients gives exactly the same integer
vector, with histogram

```
-8:2, -6:6, -4:19, -2:30, -1:8,
 1:11, 2:36, 4:18, 6:7, 8:1.
```

Over the integers this vector annihilates every nonnegative semigroup
translation of every admitted source row and pairs with the 13,974-term
target by exactly 2.  It is therefore a characteristic-zero nonmembership
certificate in the abstract joint edge/colour semigroup for the fixed word
packet.

The explanation for `16001` is elementary: the elimination normalized one
dual coordinate to 1, while nineteen other entries are half-integral.  The
residues of `+/-1/2` balance to numbers of size approximately `p/2`.

## Critical scope correction

The file called `results_closure22_plus_profile71_joint_cegar_rust.json`
does not contain the full `7+1` orbit.  It contains 29 words: closure22 plus
the seven words that crossed the earlier 100-term separator.  Only 15 of the
48 literal `7+1` words are present; 33 remain missing.  A true union of
closure22 with the full orbit has 62 words.

The artifact's own scan confirms the distinction: its terminal modular dual
is crossed by omitted `7+1` words `00000001` and `00100000`, two translations
each.  Consequently the exact integer certificate above is theorem-grade
for the 29-word crossing packet, but says nothing yet about the actual full
orbit.  No additional words were introduced in this audit.

Replay:

```
python3 computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/audit_profile71_crossing_packet_char0_lift.py --check-results
python3 -O computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/audit_profile71_crossing_packet_char0_lift.py --check-results
python3 -I -S computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/audit_profile71_crossing_packet_char0_lift.py --check-results
```
