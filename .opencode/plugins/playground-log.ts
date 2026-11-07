import { appendFile, mkdir } from "node:fs/promises";
import { join } from "node:path";
import { Plugin } from "@opencode/plugin";

function commandFrom(input: unknown): string | undefined {
  if (typeof input !== "object" || input === null) return undefined;
  const command = (input as { command?: unknown }).command;
  return typeof command === "string" ? command : undefined;
}

export default Plugin.define({
  id: "applymaxxing.playground-log",
  setup: async (ctx) => {
    const logsDirectory = join(ctx.location.project.canonical, "logs");
    const logPath = join(logsDirectory, "plugin-playground.log");

    const registration = await ctx.tool.hook("execute.before", async (event) => {
      if (event.tool !== "shell") return;

      const command = commandFrom(event.input);
      if (command === undefined || !command.includes("playground/server.py")) {
        return;
      }

      await mkdir(logsDirectory, { recursive: true });
      await appendFile(
        logPath,
        `playground shell request: ${command}\n`,
        "utf8",
      );
    });

    return () => registration.dispose();
  },
});