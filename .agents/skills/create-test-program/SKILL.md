---
name: create-test-program
description: Add a runnable SlopLang example and an exact-output test for a language feature
---

# Create Test Program

Given a language feature, add a runnable example to `examples/` and pin its exact
stdout in `tests/test_example_outputs.py`.

## 1. Read the spec first

`docs/spec.md` is the source of truth for SlopLang. Find the feature's section and
note:

- syntax — keywords, punctuation, and where `✨` is required;
- semantics and value types;
- output formatting, including separators and newlines;
- error behaviour, if the goal is to exercise a diagnostic.

Do not rely on the README or on memory when the spec disagrees.

## 2. Write the example

Create `examples/<feature>.slop`, named after the feature in lowercase (for
example `recursion.slop`). Follow the conventions of the existing examples:

- Start with a short `—` line comment describing the feature.
- Keep the program small and deterministic so its output is stable.
- Use the real language characters: `“ ”`, `—`, `✨`, `✅`, `❌`.
- End declarations, assignments, `ship`, and expression statements with `✨`;
  never put `✨` after a block's closing `}`.
- Print observable results with `hallucinate(...)`.
- Stay inside the language: numbers, strings, booleans, functions, `vibe`/`nah`,
  and `ralph` only. There are no floats, arrays, maps, classes, `%`, `for`,
  `break`, or `else if`.

Run it from the project root and capture the real output:

```bash
uv run sloperator.py examples/<feature>.slop
```

## 3. Add the exact output test

Open `tests/test_example_outputs.py` and add one entry to `EXPECTED_OUTPUTS`,
keyed by the example's file stem (the file name without `.slop`). The value is
the program's exact stdout, including the trailing newline from every
`hallucinate` call:

```python
EXPECTED_OUTPUTS: dict[str, str] = {
    "hello": "hello, slop\n",
    "my_feature": "first line\nsecond line\n",
}
```

Use `\n` escapes, or implicit string concatenation for long outputs. Never
approximate: do not trim whitespace, compare substrings, or normalize symbols.
Register the exact output you observed in step 2.

The test module runs every registered example through `run_source` and asserts
`stdout` is byte-for-byte equal. Its coverage test also fails when an example
exists without an entry.

## 4. Validate

Format the new Python test, run the focused test, then run the full checks (see
the `validate` skill):

```bash
uv run ruff format
uv run pytest tests/test_example_outputs.py
```

All checks must pass before reporting completion. If the output changed, update
the expected string — never weaken the assertion.
