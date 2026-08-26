# D12 v4.1 production through round 1538

Production reached round 1538 exactly from the independently accepted round1527 cap2.75m candidate. Six atomic stages cover rounds1528–1538 with no gaps or overlaps. The endpoint exposes 2,476,308 columns and has dual support 3,910.

All stages used the frozen v4.1 cold/rare hierarchical 16-worker nonincremental kernel, prime 1073741827, cap2.75m, native wall120, wrapper150, and live36GiB RSS guard. Maximum observed RSS was 26,069,568 KiB. Block A consumed259.032220 seconds and Block B240.574562 seconds, both below540. The conservative column guard passed before every launch.

The producer is sealed and held. No later round is claimed until the six cache-descendant edges and final cache are independently replayed.
