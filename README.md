# Sloperator

A tree-walking interpreter for SlopLang, written in Python. The full language reference lives in [docs/spec.md](docs/spec.md).

## Quick Start

```bash
uv run sloperator.py path/to/program.slop          # run
uv run sloperator.py --check path/to/program.slop  # syntax check only
```

`--check` reports lexical and syntax errors only; runtime errors are not evaluated.

## Validation

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

## Example

```slop
clanker describe(count) {
    vibe count > 1 { ship “big slop”✨ } nah { ship “small slop”✨ }
}

slop count = 0✨
ralph count < 3 {
    hallucinate(describe(count))✨
    count = count + 1✨
}
```

Prints `small slop` twice, then `big slop`.

## Layout

| Path | What it is |
| --- | --- |
| `sloperator.py` | Command-line entrypoint |
| `sloperator/` | Lexer, parser, evaluator, and runner |
| `examples/` | Example programs |
| `tests/` | Pytest suite |
| `playground/` | Web server and editor page |

For the browser editor, run `uv run playground/server.py`, then open <http://localhost:8080>.
