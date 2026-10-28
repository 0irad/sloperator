import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize


@pytest.mark.parametrize(
    ("source", "line", "character"),
    [
        ("$", 1, "$"),
        ("x = @", 1, "@"),
        ("x = 1\nx = #", 2, "#"),
        ("x = %", 1, "%"),
    ],
)
def test_unexpected_character_fallback(source: str, line: int, character: str):
    message = f"unexpected character '{character}'"
    with pytest.raises(LexicalError) as info:
        tokenize(source)
    assert info.value.line == line
    assert info.value.message == message
    assert str(info.value) == f"SlopLang lexical error at line {line}: {message}"
