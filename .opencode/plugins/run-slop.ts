import { spawn } from "node:child_process";
import { resolve } from "node:path";
import { Plugin } from "@opencode/plugin";

interface SlopResult {
  stdout: string;
  stderr: string;
  exitCode: number | null;
}

function runSloperator(projectRoot: string, file: string): Promise<SlopResult> {
  return new Promise((done) => {
    const child = spawn(
      "uv",
      ["run", "--no-active", "sloperator.py", file],
      {
        cwd: projectRoot,
        stdio: ["ignore", "pipe", "pipe"],
      },
    );

    let stdout = "";
    let stderr = "";

    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk: string) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk: string) => {
      stderr += chunk;
    });

    child.on("error", (error) => {
      done({ stdout, stderr: stderr + error.message, exitCode: null });
    });
    child.on("close", (code) => {
      done({ stdout, stderr, exitCode: code });
    });
  });
}

export default Plugin.define({
  id: "applymaxxing.run-slop",
  setup: async (ctx) => {
    // Run from the canonical project root so `uv` always finds pyproject.toml
    // and `sloperator.py`, regardless of the session's current directory.
    const projectRoot = ctx.location.project.canonical;

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description:
          "Run a SlopLang program with Sloperator. Executes `uv run --no-active sloperator.py <path>` " +
          "from the project root and returns a JSON object with the program's stdout, stderr, and exitCode.",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description:
                "Path to the .slop file. Relative paths resolve from the project root.",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path } = input as { path: string };
          const result = await runSloperator(projectRoot, resolve(projectRoot, path));
          return { content: JSON.stringify(result, null, 2) };
        },
      });
    });
  },
});
