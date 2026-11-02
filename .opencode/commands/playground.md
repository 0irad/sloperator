---
description: Start the SlopLang playground, reusing any running server
---

Start the SlopLang playground.

Requested port: $ARGUMENTS

If the requested port above is blank, use `8080`.

Current TCP listeners:

!`lsof -nP -iTCP -sTCP:LISTEN`

Steps:

1. Choose the port: the requested port above, or `8080` when blank. If it is not a valid TCP port number, stop and ask.
2. Look for an existing SlopLang playground in the listener list. Confirm candidate Python/`uv` processes with `ps -p <PID> -o command=` and check for `playground/server.py`. If one is running, reuse it: report its URL (`http://localhost:<its port>`) and stop without starting another server.
3. If the chosen port is taken by any other process, do not kill it and do not silently pick a different port. Report the port and the owning process, then stop.
4. Otherwise start the server in the background from the project root:

   `uv run playground/server.py <port>`

5. Confirm it is serving by requesting `http://localhost:<port>/` and checking for a 200 response.
6. Report the URL, the background process ID, and how to stop it.

Do not modify project files, and do not run the server in the foreground.
