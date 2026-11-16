import hashlib
import subprocess
import sys

import pytest
from PIL import Image


@pytest.mark.parametrize(
    ("mode_options", "expected_hash"),
    [
        ([], hashlib.md5(b"Hashpic rocks!").hexdigest()),
        (["--sha512"], hashlib.sha512(b"Hashpic rocks!").hexdigest()),
        (["--sha3"], hashlib.sha3_512(b"Hashpic rocks!").hexdigest()),
        (["--blake2b"], hashlib.blake2b(b"Hashpic rocks!").hexdigest()),
        (
            ["--shake256", "--length", "4"],
            hashlib.shake_256(b"Hashpic rocks!").hexdigest(4),
        ),
    ],
)
def test_hash_modes_use_selected_algorithm(tmp_path, mode_options, expected_hash):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hashpic",
            *mode_options,
            "-d",
            "--svg",
            "Hashpic rocks!",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert f"will be following hash: {expected_hash}" in result.stdout


@pytest.mark.parametrize(
    ("mode_options", "expected_size"),
    [
        ([], 1024),
        (["--sha512"], 1024),
        (["--sha3"], 1024),
        (["--blake2b"], 1024),
        (["--shake256", "--length", "4"], 1200),
    ],
)
def test_hash_modes_create_valid_png(tmp_path, mode_options, expected_size):
    output = tmp_path / "mode-output.png"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hashpic",
            *mode_options,
            "Hashpic rocks!",
            "-o",
            "mode-output",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    with Image.open(output) as image:
        assert image.format == "PNG"
        assert image.size == (expected_size, expected_size)


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
    with Image.open(tmp_path / "md6-output.png") as image:
        assert image.format == "PNG"
        assert image.size == (1024, 1024)


def test_file_hash_matches_hash_of_same_text(tmp_path):
    source = tmp_path / "input.txt"
    source.write_text("Hashpic rocks!")

    file_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hashpic",
            "--file",
            str(source),
            "-o",
            "file-output",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    text_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hashpic",
            "Hashpic rocks!",
            "-o",
            "text-output",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert file_result.returncode == 0, file_result.stderr
    assert text_result.returncode == 0, text_result.stderr
    assert (tmp_path / "file-output.png").read_bytes() == (
        tmp_path / "text-output.png"
    ).read_bytes()


def test_stdin_hash_matches_hash_of_same_text(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hashpic",
            "-o",
            "stdin-output",
        ],
        cwd=tmp_path,
        input="Hashpic rocks!",
        capture_output=True,
        text=True,
    )
    expected = subprocess.run(
        [
            sys.executable,
            "-m",
            "hashpic",
            "Hashpic rocks!",
            "-o",
            "text-output",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert expected.returncode == 0, expected.stderr
    assert (tmp_path / "stdin-output.png").read_bytes() == (
        tmp_path / "text-output.png"
    ).read_bytes()


def test_bypass_accepts_uppercase_valid_hash(tmp_path):
    bypass_hash = "5C1F05A8" * 4
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hashpic",
            "--bypass",
            bypass_hash,
            "ignored-extra-argument",
            "-o",
            "bypass-output",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    with Image.open(tmp_path / "bypass-output.png") as image:
        assert image.size == (1024, 1024)


def test_invalid_bypass_hash_reports_error(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hashpic",
            "--bypass",
            "not-a-hash",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "is not a valid MD5 hash" in result.stderr


def test_shake256_requires_a_supported_length(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hashpic",
            "--shake256",
            "--length",
            "2",
            "Hashpic rocks!",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "only a length" in result.stderr


def test_shake256_requires_a_length(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hashpic",
            "--shake256",
            "Hashpic rocks!",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Please specify a --length" in result.stderr


def test_maximum_shake256_svg_contains_all_tiles(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hashpic",
            "--shake256",
            "--length",
            "255",
            "--svg",
            "-o",
            "shake-output",
            "Hashpic rocks!",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    svg = (tmp_path / "shake-output.svg").read_text()
    assert svg.count("<rect ") == 256
