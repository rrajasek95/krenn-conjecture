#!/usr/bin/env python3
"""Clean complete replay for the minimal two-extra response."""

from __future__ import annotations

import verify_live_three_zero_minimal_two_extra_boundary_cells as boundary
import verify_live_three_zero_minimal_two_extra_central_uniform as central
import verify_live_three_zero_minimal_two_extra_frontier as frontier


def main():
    frontier.main()
    central.main()
    boundary.main()
    print("minimal two-extra (r,t)=(2,0): COMPLETE PASS")
    print("all nine ordered cells uniformly rank 20 over QQ")


if __name__ == "__main__":
    main()
