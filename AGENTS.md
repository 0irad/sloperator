# AGENTS.md

Sloperator is a Python 3.13 tree-walking interpreter for SlopLang. Runtime dependencies are empty; keep the interpreter stdlib-only unless there is a strong reason not to.

## Project layout

- `sloperator.py` — CLI entry point.
- `sloperator/` — pipeline stages: `lexer/` → `parser/` → `evaluator/`, wired together by `runner.py`; shared diagnostics live in `errors.py`.
- `docs/spec.md` — source of truth for the language.
- `tests/` — pytest suite. `test_examples.py` auto-discovers `examples/*.slop`.
- `examples/` — runnable `.slop` programs.
- `playground/server.py` — web playground that shells out to the CLI.
- `.opencode/` — agent tooling, including the `run_slop` tool and the `validate` skill.

## Validation

After any code change, run `uv run ruff format` to format the code.

Run from the repo root with `uv`, in this order:

1. Tests: `uv run pytest`
2. Format: `uv run ruff format --check`
3. Lint: `uv run ruff check`
4. Types: `uv run ty check`

There is no CI or pre-commit, so run these locally. The `validate` skill runs the first three. For a single test: `uv run pytest tests/test_parser.py::test_name`. For comparison and operator-precedence tests: `uv run pytest tests/test_comparisons.py`.

## Regression tests

Add a regression test whenever you:

- fix a bug — assert the previously broken behaviour;
- change syntax, semantics, or diagnostics — update the existing assertions;
- add or change a CLI error path;
- touch lexer edge cases — those belong in `tests/test_lexer_regression.py`.

Tests assert exact messages, line numbers, and exit codes, so update them alongside any diagnostic change. Every `examples/*.slop` must exit cleanly and print non-empty stdout.

## Language behaviour

See [docs/spec.md](docs/spec.md). It is the source of truth for syntax, semantics, values, operators, and diagnostics; `README.md` is only a quick start. Update the spec whenever language behaviour changes.
