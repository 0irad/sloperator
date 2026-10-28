import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTERPRETER = ROOT / "sloperator.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INTERPRETER), *args], capture_output=True, encoding="utf-8"
    )


def test_runs_a_file():
    completed = run_cli(str(ROOT / "examples/hello.slop"))
    assert completed.returncode == 0
    assert completed.stdout == "hello, slop\n"
    assert completed.stderr == ""


def test_error_goes_to_stderr_after_earlier_output(tmp_path: Path):
    program = tmp_path / "boom.slop"
    program.write_text("hallucinate(“before”)✨\nhallucinate(missing)✨\n", encoding="utf-8")
    completed = run_cli(str(program))
    assert completed.returncode == 1
    assert completed.stdout == "before\n"
    assert completed.stderr == "SlopLang runtime error at line 2: undefined variable 'missing'\n"
    assert "Traceback" not in completed.stderr


def test_division_by_zero_is_a_slop_runtime_error_without_a_traceback(tmp_path: Path):
    program = tmp_path / "division_by_zero.slop"
    program.write_text("hallucinate(1 / 0)✨\n", encoding="utf-8")
    completed = run_cli(str(program))
    assert completed.returncode == 1
    assert completed.stdout == ""
    assert completed.stderr == "SlopLang runtime error at line 1: division by zero\n"
    assert "Traceback" not in completed.stderr


def test_missing_file_and_usage():
    assert run_cli().returncode == 2
    assert run_cli("--check").returncode == 2
    missing = run_cli(str(ROOT / "nope.slop"))
    assert missing.returncode == 2
    assert "could not read" in missing.stderr
    missing_check = run_cli("--check", str(ROOT / "nope.slop"))
    assert missing_check.returncode == 2
    assert "could not read" in missing_check.stderr


def test_check_accepts_valid_syntax_without_running():
    completed = run_cli("--check", str(ROOT / "examples/hello.slop"))
    assert completed.returncode == 0
    assert completed.stdout == ""
    assert completed.stderr == ""


def test_check_accepts_programs_that_would_fail_at_runtime(tmp_path: Path):
    program = tmp_path / "runtime_error.slop"
    program.write_text("hallucinate(missing)✨\n", encoding="utf-8")
    completed = run_cli("--check", str(program))
    assert completed.returncode == 0
    assert completed.stdout == ""
    assert completed.stderr == ""


def test_check_reports_lexical_and_syntax_errors(tmp_path: Path):
    lexical = tmp_path / "lexical.slop"
    lexical.write_text('hallucinate("hi")✨\n', encoding="utf-8")
    completed = run_cli("--check", str(lexical))
    assert completed.returncode == 1
    assert completed.stderr == (
        "SlopLang lexical error at line 1: straight quotes are not supported, "
        "use “ and ” for strings\n"
    )

    syntax = tmp_path / "syntax.slop"
    syntax.write_text("slop x = 1\n", encoding="utf-8")
    completed = run_cli("--check", str(syntax))
    assert completed.returncode == 1
    assert "SlopLang syntax error at line 2" in completed.stderr
