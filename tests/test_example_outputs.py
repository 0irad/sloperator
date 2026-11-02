"""Exact stdout for every program in examples/.

Add a new entry to EXPECTED_OUTPUTS whenever you add an example. Values are
compared byte-for-byte, including every newline printed by hallucinate.
"""

from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"

# Example file stem -> the exact stdout the program must print.
EXPECTED_OUTPUTS: dict[str, str] = {
    "arithmetic": "7\n",
    "collatz": "27 takes\n111\nsteps\n97 takes\n118\nsteps\n",
    "countdown": "3\n2\n1\nliftoff\n",
    "doubling": "26\n",
    "equality": "✅\n❌\n❌\n",
    "factorial": ("5! =\n120\n20! =\n2432902008176640000\n25! =\n15511210043330985984000000\n"),
    "fib": (
        "fib\n0\n=\n0\n"
        "fib\n1\n=\n1\n"
        "fib\n2\n=\n1\n"
        "fib\n3\n=\n2\n"
        "fib\n4\n=\n3\n"
        "fib\n5\n=\n5\n"
        "fib\n6\n=\n8\n"
        "fib\n7\n=\n13\n"
        "fib\n8\n=\n21\n"
        "fib\n9\n=\n34\n"
        "fib\n10\n=\n55\n"
        "fib_loop(50) =\n12586269025\n"
    ),
    "fizzbuzz": ("1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n"),
    "grouping": "9\n",
    "hello": "hello, slop\n",
    "logic": "7\n9\n3\n5\n✅ ✅\n✅\n✅\n❌\n✅\n✅\n✅\n❌\n",
    "primes": (
        "2\nis prime\n"
        "3\nis prime\n"
        "5\nis prime\n"
        "7\nis prime\n"
        "11\nis prime\n"
        "13\nis prime\n"
        "17\nis prime\n"
        "19\nis prime\n"
        "23\nis prime\n"
        "29\nis prime\n"
        "found\n10\nprimes below 31\n"
    ),
    "scope": ("locked in\ncalm\nbumped\n2\ntimes\nnil\n<clanker bump>\n<clanker hallucinate>\n"),
    "short-circuit": "❌\n✅\n",
    "strings": (
        "hello, Boots!\nquoted: ”slop”\nbackslash: \\\nline one\nline two\n✅\n✅\n❌\n❌\n"
    ),
    "tab": "name\tscore\n",
}


@pytest.mark.parametrize(("name", "expected"), sorted(EXPECTED_OUTPUTS.items()))
def test_example_output(name: str, expected: str):
    source = (EXAMPLES_DIR / f"{name}.slop").read_text(encoding="utf-8")
    result = run_source(source)

    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == expected


def test_every_example_has_expected_output():
    examples = {path.stem for path in EXAMPLES_DIR.glob("*.slop")}
    missing = examples - EXPECTED_OUTPUTS.keys()

    assert not missing, f"examples missing an exact-output entry: {sorted(missing)}"
