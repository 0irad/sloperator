import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        # * and / bind tighter than + and -.
        ("1 + 2 * 3", "7"),
        ("1 * 2 + 3", "5"),
        ("2 + 8 / 4", "4"),
        ("2 * 3 - 4", "2"),
        ("2 - 3 * 4", "-10"),
        # Same precedence is left associative.
        ("10 - 2 - 3", "5"),
        ("20 / 2 / 5", "2"),
        # +, - bind tighter than comparison.
        ("1 + 1 < 3", "✅"),
        ("2 * 2 > 3", "✅"),
        # Comparison binds tighter than equality.
        ("1 < 2 == ✅", "✅"),
        ("1 == 1 < 2", "❌"),  # parses as 1 == (1 < 2)
        ("5 < 3 == ❌", "✅"),
        # Equality binds tighter than &&, which binds tighter than ||.
        ("❌ && 1 == 1", "❌"),
        ("✅ && 1 == 1", "✅"),
        ("❌ || 1 == 1", "✅"),
        ("❌ || ❌ && ✅", "❌"),  # parses as ❌ || (❌ && ✅)
        ("✅ || ❌ && ❌", "✅"),
        # Grouping overrides precedence.
        ("(1 + 2) * 3", "9"),
        ("(2 - 3) * 4", "-4"),
        ("(1 < 2) == ✅", "✅"),
        ("1 + 2 == 2 + 1", "✅"),
        # Unary minus binds tighter than *.
        ("-2 * 3", "-6"),
        ("--5", "5"),
    ],
)
def test_operator_precedence(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"
