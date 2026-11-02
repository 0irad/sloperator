---
description: Review changes, commit with a message, then rebase on main
---

Review the current project changes, commit them, then sync with `main`.

Commit message: $ARGUMENTS

Steps:

1. Inspect the working tree with `git status --short`, `git diff`, and `git diff --cached`. Read the diff and look for anything unintended, such as debug code, secrets, or unrelated files.
2. If there is nothing to commit, stop and say so.
3. If the commit message above is empty, stop and ask for one. Never invent a message.
4. Stage the project changes with `git add -A` (ignored files stay ignored).
5. Commit using the message above verbatim as a single `-m` argument. Do not amend, and do not add attribution or trailers.
6. Run `git pull --rebase origin main`.
7. If the rebase stops on conflicts, leave the working tree as it is, list the conflicted files, and stop. Do not abort or resolve conflicts without asking.
8. Do not push.

Report the commit hash, the message used, and the result of the pull.
