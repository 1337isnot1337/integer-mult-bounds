#!/usr/bin/env python3
"""Parity rounding of the mixed-negative bound."""


def main():
    def bound(t):
        count = -(-11 * t // 5)
        if count % 2 != t % 2:
            count += 1
        return count

    assert [bound(t) for t in (1, 2, 3, 4)] == [3, 6, 7, 10]
    print("PASS_Q8_BOUND_ATTAINMENT_TEST")


if __name__ == "__main__":
    main()
