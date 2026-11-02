import pytest

from sloperator.runner import run_source


@pytest.mark.parametrize(
    "operand",
    ["✅", "❌"],
    ids=["true", "false"],
)
def test_unary_minus_rejects_boolean_literals(operand: str):
    result = run_source(f"hallucinate(-{operand})✨")
    assert result.stdout == ""
    assert result.stderr == (
        "SlopLang runtime error at line 1: operand of unary '-' must be a number, got boolean\n"
    )
    assert result.exit_code == 1


def test_unary_minus_rejects_boolean_variable():
    result = run_source("slop b = ✅✨\nhallucinate(-b)✨")
    assert result.stdout == ""
    assert result.stderr == (
        "SlopLang runtime error at line 2: operand of unary '-' must be a number, got boolean\n"
    )
    assert result.exit_code == 1
