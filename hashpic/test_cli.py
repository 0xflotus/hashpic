import subprocess
import sys


def test_md6_cli_creates_png(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hashpic",
            "--md6",
            "Hashpic rocks!",
            "-o",
            "md6-output",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "md6-output.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
