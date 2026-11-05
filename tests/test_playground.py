import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "playground" / "index.html"

RENDER_HARNESS = """
const output = {
  textContent: "",
  children: [],
  appendChild(child) { this.children.push(child); },
};
const document = { createElement: () => ({ className: "", textContent: "" }) };

__RENDER_RESULT__

function snapshot() {
  const errors = output.children.map((child) => [child.textContent, child.className]);
  return [output.textContent, errors];
}

function reset() {
  output.textContent = "";
  output.children = [];
}

const cases = [];
renderResult({
  stdout: "before the crash\\n",
  stderr: "SlopLang runtime error at line 2: division by zero\\n",
  exit_code: 1,
});
cases.push(snapshot());
reset();

renderResult({ stdout: "only stdout\\n", stderr: "", exit_code: 0 });
cases.push(snapshot());
reset();

renderResult({ stdout: "", stderr: "", exit_code: 0 });
cases.push(snapshot());

console.log(JSON.stringify(cases));
"""


def render_result_source() -> str:
    html = INDEX.read_text(encoding="utf-8")
    match = re.search(r"function renderResult\(result\) \{.*?\n      \}", html, re.S)
    assert match, "playground/index.html must define renderResult(result)"
    return match.group(0)


def test_render_result_is_defined_in_the_page():
    assert "renderResult(result)" in INDEX.read_text(encoding="utf-8")


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_render_result_shows_output_written_before_a_runtime_error(tmp_path: Path):
    script = tmp_path / "render.js"
    harness = RENDER_HARNESS.replace("__RENDER_RESULT__", render_result_source())
    script.write_text(harness, encoding="utf-8")
    completed = subprocess.run(["node", str(script)], capture_output=True, encoding="utf-8")
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout) == [
        [
            "before the crash\n",
            [["SlopLang runtime error at line 2: division by zero\n", "err"]],
        ],
        ["only stdout\n", []],
        ["(no output)", []],
    ]
