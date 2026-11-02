import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1 < 2", "✅"),
        ("2 < 1", "❌"),
        ("1 <= 1", "✅"),
        ("2 <= 1", "❌"),
        ("2 > 1", "✅"),
        ("1 > 2", "❌"),
        ("1 >= 1", "✅"),
        ("1 >= 2", "❌"),
    ],
)
def test_comparison_operators(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        # Comparison binds tighter than equality: (1 < 2) == ✅, not 1 < (2 == ✅).
        ("1 < 2 == ✅", "✅"),
        ("1 < 2 == ❌", "❌"),
        ("5 < 3 == ❌", "✅"),
        ("1 <= 2 == ✅", "✅"),
        ("2 > 1 == ✅", "✅"),
        ("1 >= 2 == ❌", "✅"),
        # Equality still binds looser than comparison on either side.
        ("1 == 1 < 2", "❌"),
        ("✅ == 1 < 2", "✅"),
        ("1 < 2 != ❌", "✅"),
    ],
)
def test_comparison_binds_tighter_than_equality(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


def test_comparing_a_comparison_does_not_mix_number_and_boolean_operands():
    # Regression: this used to parse as 1 < (2 == ✅) and fail at runtime.
    assert run("hallucinate(1 < 2 == ✅)✨") == "✅\n"
