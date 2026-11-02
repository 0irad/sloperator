from sloperator.runner import run_source


def test_loop_with_false_condition_never_runs_its_body():
    source = """ralph ❌ {
    hallucinate(“never”)✨
}"""

    result = run_source(source)

    assert result.stdout == ""
    assert result.stderr == ""
    assert result.exit_code == 0
