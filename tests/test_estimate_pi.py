import math
from typing import Generator, Iterable

import pytest
from hamcrest import assert_that, close_to, greater_than, is_

import estimate_pi


def reciprocals(terms: Iterable[float | int]) -> Generator[float, None, None]:
    """
    Compute the reciprocals of a sequence of terms.
    """

    for term in terms:
        yield 1.0 / term


def alternate_term_signs(terms: Iterable[float | int]) -> Generator[float | int, None, None]:
    """
    This is a utility function that will flip the sign
    (alternate between + and -) from one term to the next.
    """

    sign = -1.0

    for term in terms:
        sign = -sign
        yield sign * term


def odd_range(num_terms: int) -> Generator[int, None, None]:
    """
    Generate the sequence 1, 3, 5, 7, 11, ... for the specified number of terms
    """

    current = -1
    for _ in range(0, num_terms):
        current += 2
        yield current


@pytest.fixture
def estimates_for_10_100_10000():
    yield (
        estimate_pi.pi_leibniz(10),
        estimate_pi.pi_leibniz(100),
        estimate_pi.pi_leibniz(10_000),
    )


@pytest.mark.parametrize(
    "computed, known",
    [(0.0, 0.0), (1.0, 1.0), (2.0, 4.61), (3.14, math.pi), (100.0, 100.001)],
)
def test_abs_error_from_known(computed, known):
    expected_error = math.fabs(computed - known)

    assert_that(
        estimate_pi.abs_error_from_known(computed, known),
        is_(close_to(expected_error, 1e-6)),
    )


@pytest.mark.parametrize("number_of_terms", range(1, 10))
def test_pi_leibniz_1_to_9_terms(number_of_terms):
    expected_pi = 4.0 * sum(alternate_term_signs(reciprocals(odd_range(number_of_terms))))
    assert_that(estimate_pi.pi_leibniz(number_of_terms), is_(close_to(expected_pi, 1e-16)))

def test_pi_leibniz_up_to_10_terms(estimates_for_10_100_10000):
    terms_10, terms_100, terms_10_000 = estimates_for_10_100_10000

    assert_that(math.fabs(terms_10 - terms_100), is_(greater_than(1e-4)))
    assert_that(math.fabs(terms_10 - terms_10_000), is_(greater_than(1e-4)))

    expected_pi = 4.0 * sum(alternate_term_signs(reciprocals(odd_range(10))))
    assert_that(estimate_pi.pi_leibniz(10), is_(close_to(expected_pi, 1e-16)))


def test_pi_leibniz_up_to_100_terms(estimates_for_10_100_10000):
    terms_10, terms_100, terms_10_000 = estimates_for_10_100_10000

    assert_that(math.fabs(terms_100 - terms_10_000), is_(greater_than(1e-8)))

    expected_pi = 4.0 * sum(alternate_term_signs(reciprocals(odd_range(100))))
    assert_that(estimate_pi.pi_leibniz(100), is_(close_to(expected_pi, 1e-16)))


def test_pi_leibniz_up_to_10_000_terms(estimates_for_10_100_10000):
    _, _, terms_10_000 = estimates_for_10_100_10000

    expected_pi = 4.0 * sum(alternate_term_signs(reciprocals(odd_range(10_000))))
    assert_that(estimate_pi.pi_leibniz(10_000), is_(close_to(expected_pi, 1e-16)))
