#!/usr/bin/env python3
"""Run the exact higher-epsilon Petersen and bridge audits."""

from explore_higher_epsilon_web import (
    verify_bridged_replacement,
    verify_petersen_web,
)


if __name__ == "__main__":
    verify_petersen_web()
    verify_bridged_replacement()
