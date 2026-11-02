import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import TokenType, tokenize


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


@pytest.mark.parametrize("name", ["score2", "x1", "a0b9", "_123", "value_2"])
def test_identifiers_may_contain_digits(name: str):
    tokens = tokenize(f"slop {name} = 1✨")
    identifier = tokens[1]
    assert identifier.type is TokenType.IDENTIFIER
    assert identifier.lexeme == name


@pytest.mark.parametrize("source", ["2score", "123abc"])
def test_identifiers_may_not_start_with_digits(source: str):
    tokens = tokenize(source)
    assert tokens[0].type is TokenType.NUMBER
    assert tokens[1].type is TokenType.IDENTIFIER
