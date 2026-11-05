---
description: Split changes into atomic commits on a topic branch, with descriptive messages
---

Create responsible, review-ready commits for the current project changes.

Additional context: $ARGUMENTS

Apply GitLab's version control best practices: keep changes small and incremental, make each commit atomic, develop on branches instead of `main`, write descriptive imperative commit messages, and leave the work ready for code review.

Steps:

1. Inspect the working tree with `git status --short`, `git diff`, `git diff --cached`, and `git branch --show-current`. Read every hunk and identify secrets or credentials, debug code, generated files, unrelated edits, and changes with different purposes.
2. If there is nothing to commit, stop and say so. If you find a secret or credential, do not commit it: stop and report the file and line.
3. If the additional context above is empty, infer the intent from the diff. Do not invent facts, and never mention tools, files, or issue numbers that are not in the diff.
4. If the current branch is `main` or detached, create and switch to a descriptive topic branch before committing, named `<type>/<short-slug>` with `feat`, `fix`, `refactor`, `docs`, `test`, or `chore`. Derive the slug from the change, not from a generic word. If you are already on another branch, keep it. Never commit directly to `main`.
5. If the diff touches Python, validate before committing: run `uv run ruff format`, then `uv run pytest`, `uv run ruff check`, and `uv run ty check` (see `AGENTS.md`). If a check fails, stop and report it; do not commit broken code. If the diff is docs-only, skip validation and say so.
6. Group the changes into atomic commits: one purpose per commit, such as one feature, fix, refactor, test, or docs update. Do not bundle unrelated purposes. Stage explicit paths only; never use `git add -A` or `git add .`. If one file mixes unrelated purposes and cannot be split cleanly, stop and list the file instead of making a non-atomic commit.
7. Commit one group at a time. Write the subject in the imperative present tense (for example `Add branch check to commit command`, not `Added` or `Adds`), keep it concise, then leave a blank line and explain what changed and why in the body, wrapped near 72 characters. Reference an issue or URL only after summarizing the relevant point. Add no attribution or trailers, and do not amend.
8. After committing, show `git log --oneline` for the new commits and `git status --short`.
9. Do not push, open a merge request, rebase, or rewrite history. Report the branch name, each commit hash and subject, any skipped validation steps, and tell the user to push the branch and open a merge request so the changes can be reviewed.
