# Parser conventions

- **One method per grammar rule.** Mirror the grammar in `docs/spec.md`: each rule gets a method named after it (`logic_or`, `logic_and`, `equality`, `comparison`, `term`, `factor`, `unary`, `call`, `primary`, etc.). Keep the call structure matching the grammar instead of inlining sub-rules.
- **Syntax errors must describe the token that was found.** For unexpected-token errors, raise through `Parser.error()` so the message ends with `, found '<lexeme>'` (or `, but reached end of file` at EOF). Raise `SlopSyntaxError` directly only for context errors with no single offending token, such as duplicate parameter names or `ship` outside a `clanker`.
