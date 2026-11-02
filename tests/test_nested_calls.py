from sloperator.lexer import tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Call, ExprStmt, FunctionDecl, Literal, Variable


def parse_source(source: str):
    return parse(tokenize(source))


def test_call_as_direct_argument_to_another_call():
    source = """clanker add(left, right) {
    ship left + right✨
}
hallucinate(add(1, 2))✨"""
    declarations = parse_source(source)
    assert len(declarations) == 2
    assert isinstance(declarations[0], FunctionDecl)

    statement = declarations[1]
    assert isinstance(statement, ExprStmt)

    outer = statement.expression
    assert isinstance(outer, Call)
    assert isinstance(outer.callee, Variable) and outer.callee.name.lexeme == "hallucinate"
    assert len(outer.arguments) == 1

    inner = outer.arguments[0]
    assert isinstance(inner, Call)
    assert isinstance(inner.callee, Variable) and inner.callee.name.lexeme == "add"
    assert len(inner.arguments) == 2
    assert all(isinstance(argument, Literal) for argument in inner.arguments)
    assert [argument.value for argument in inner.arguments] == [1, 2]
