"""
This module provides the ability to estimate PI using Leibniz's method and
determine how far off the estimate is from the "accepted" value in math.pi.
"""

import math

DEFAULT_NUM_TERMS: int = 4


def _handle_user_input() -> int:
    """
    Handle all use input... including parsing.

    If a non-integer value is supplied... return the default value
    """

    input_str = input("How many terms should be used? ")

    try:
        num_terms = int(input_str)

    except ValueError as _err:
        num_terms = DEFAULT_NUM_TERMS

    return num_terms


def abs_error_from_known(estimate: float, known: float = math.pi) -> float:
    """
    Use the absolute error formula.

    Args:
        estimate - computed value
        known - accepted (correct value)

    Returns:
        |estimate - known|
    """

    return abs(estimate - known)


def pi_leibniz(num_terms: int) -> float:
    """
    Use Leibniz's Method to compute an estimate for PI

    Args:
        num_terms - number of terms to compute for the estimate

    Returns:
        approximate value for pi.
    """

    if num_terms <= 0:
        return 0.0
    
    pi_estimate = 0.0
    for i in range(num_terms):
        term = 4.0 / (2 * i + 1)
        if i % 2 == 1:
            pi_estimate -= term
        else:
            pi_estimate += term

    return pi_estimate


def main():
    num_terms = _handle_user_input()

    pi_estimate = pi_leibniz(num_terms)
    error = abs_error_from_known(pi_estimate)

    print()
    print("-" * 72)
    print(f"Estimated: {pi_estimate:.16f}")
    print(f"Known    : {math.pi:.16f}")
    print(f"Abs Error: {error:.16f}")


if __name__ == "__main__":
    main()
