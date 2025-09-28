

#!/usr/bin/env python3
"""
Calculate approximations of π (pi) from first principles, several ways.

Usage examples:
  python 4-calculate-pi.py                 # defaults to Nilakantha with n=1_000_000
  python 4-calculate-pi.py --method leibniz --n 2_000_000
  python 4-calculate-pi.py --method wallis --n 1_000_000
  python 4-calculate-pi.py --method montecarlo --n 2_000_000 --seed 42

Methods implemented:
- leibniz:    π = 4 * Σ (-1)^k / (2k+1)                     (Gregory–Leibniz series)
- nilakantha: π = 3 + Σ 4 * (-1)^{k+1} / (2k·(2k+1)·(2k+2)) (Nilakantha series)
- wallis:     π/2 = Π [(2n)/(2n-1)] * [(2n)/(2n+1)]          (Wallis product)
- montecarlo: Area of quarter circle inside unit square      (geometric probability)

No external packages required.
"""
from __future__ import annotations
import argparse
import math
import random
import time
from typing import Callable


def leibniz(n: int) -> float:
    """Gregory–Leibniz series; painfully slow convergence but very "first principles"."""
    s = 0.0
    sign = 1.0
    for k in range(n):
        s += sign / (2 * k + 1)
        sign = -sign
    return 4.0 * s


def nilakantha(n: int) -> float:
    """Nilakantha series (faster than Leibniz). n is number of terms after the initial 3."""
    pi = 3.0
    sign = 1.0
    for k in range(1, n + 1):
        a, b, c = 2 * k, 2 * k + 1, 2 * k + 2
        pi += sign * 4.0 / (a * b * c)
        sign = -sign
    return pi


def wallis(n: int) -> float:
    """Wallis product. n is the number of product factors."""
    prod = 1.0
    for k in range(1, n + 1):
        prod *= (4.0 * k * k) / (4.0 * k * k - 1.0)
    return 2.0 * prod


def montecarlo(n: int, seed: int | None = None) -> float:
    """Monte Carlo quarter-circle in unit square. Deterministic if seed is provided."""
    if seed is not None:
        random.seed(seed)
    inside = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return 4.0 * inside / n


METHODS: dict[str, Callable[..., float]] = {
    "leibniz": leibniz,
    "nilakantha": nilakantha,
    "wallis": wallis,
    "montecarlo": montecarlo,
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Approximate π using different first-principles methods.")
    parser.add_argument(
        "--method",
        choices=sorted(METHODS.keys()),
        default="nilakantha",
        help="Which method to use (default: nilakantha)",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1_000_000,
        help="Number of terms/samples/factors (method-dependent).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed (only used by montecarlo).",
    )

    args = parser.parse_args()

    start = time.perf_counter()
    if args.method == "montecarlo":
        estimate = METHODS[args.method](args.n, args.seed)  # type: ignore[arg-type]
    else:
        estimate = METHODS[args.method](args.n)
    elapsed = time.perf_counter() - start

    err = abs(estimate - math.pi)
    rel = err / math.pi

    print(f"Method       : {args.method}")
    print(f"n            : {args.n}")
    if args.method == "montecarlo":
        print(f"seed         : {args.seed}")
    print(f"π estimate   : {estimate:.15f}")
    print(f"math.pi      : {math.pi:.15f}")
    print(f"abs error    : {err:.3e}")
    print(f"rel error    : {rel:.3e}")
    print(f"elapsed time : {elapsed*1000:.1f} ms")


if __name__ == "__main__":
    main()