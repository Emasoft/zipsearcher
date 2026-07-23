import zipfile
from pathlib import Path

import pytest

from src.entrypoint import main


def _make_zip(path: Path, names: list[str]) -> Path:
    """Build a real zip whose central directory lists the given entry names."""
    with zipfile.ZipFile(path, "w") as archive:
        for name in names:
            archive.writestr(name, b"payload for " + name.encode())
    return path


def test_basename_glob_matches_entry_basename(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """A default glob PATTERN matches against each entry's basename."""
    archive = _make_zip(tmp_path / "a.zip", ["docs/readme.txt", "src/main.py"])

    code = main(["*.txt", str(archive)])
    out = capsys.readouterr().out

    assert code == 0
    assert out == f"{archive}:docs/readme.txt\n"


def test_path_flag_matches_full_internal_path(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """--path matches PATTERN against the full internal path instead of the basename."""
    archive = _make_zip(tmp_path / "a.zip", ["docs/readme.txt", "notes/readme.txt"])

    code = main(["--path", "docs/*", str(archive)])
    out = capsys.readouterr().out

    assert code == 0
    assert out == f"{archive}:docs/readme.txt\n"


def test_ignore_case_matches_regardless_of_case(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """-i makes the match case-insensitive."""
    archive = _make_zip(tmp_path / "a.zip", ["READ.ME"])

    code = main(["-i", "read.me", str(archive)])
    out = capsys.readouterr().out

    assert code == 0
    assert out == f"{archive}:READ.ME\n"


def test_regex_pattern_matches_as_python_regex(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """--regex treats PATTERN as a Python regex searched against the basename."""
    archive = _make_zip(tmp_path / "a.zip", ["log01.txt", "log02.dat", "readme.md"])

    code = main(["--regex", r"^log\d+\.txt$", str(archive)])
    out = capsys.readouterr().out

    assert code == 0
    assert out == f"{archive}:log01.txt\n"


def test_no_match_exits_one(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """With no matching entry the tool prints nothing and exits 1."""
    archive = _make_zip(tmp_path / "a.zip", ["a.txt"])

    code = main(["*.png", str(archive)])
    out = capsys.readouterr().out

    assert code == 1
    assert out == ""


def test_corrupt_archive_warns_and_exits_two(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """A corrupt archive is warned about on stderr and yields exit code 2 with no matches."""
    bad = tmp_path / "bad.zip"
    bad.write_bytes(b"this is not a zip file")

    code = main(["*", str(bad)])
    captured = capsys.readouterr()

    assert code == 2
    assert captured.out == ""
    assert str(bad) in captured.err


def test_invalid_regex_warns_and_exits_two(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """A malformed --regex PATTERN is reported on stderr and exits 2 without searching."""
    archive = _make_zip(tmp_path / "a.zip", ["a.txt"])

    code = main(["--regex", "(unclosed", str(archive)])
    captured = capsys.readouterr()

    assert code == 2
    assert captured.out == ""
    assert "invalid regex" in captured.err


def test_count_flag_prints_per_archive_counts(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """-c prints archive:N with the number of matching entries."""
    archive = _make_zip(tmp_path / "a.zip", ["a.txt", "b.txt", "c.md"])

    code = main(["-c", "*.txt", str(archive)])
    out = capsys.readouterr().out

    assert code == 0
    assert out == f"{archive}:2\n"


def test_files_with_matches_prints_only_archive_paths(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """-l prints only the archive paths that contain at least one match."""
    hit = _make_zip(tmp_path / "hit.zip", ["found.txt"])
    miss = _make_zip(tmp_path / "miss.zip", ["other.md"])

    code = main(["-l", "*.txt", str(hit), str(miss)])
    out = capsys.readouterr().out

    assert code == 0
    assert out == f"{hit}\n"


def test_size_flag_appends_uncompressed_size(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """--size appends the entry's uncompressed size to each match line."""
    archive = tmp_path / "a.zip"
    with zipfile.ZipFile(archive, "w") as writer:
        writer.writestr("data.bin", b"0123456789")

    code = main(["--size", "*.bin", str(archive)])
    out = capsys.readouterr().out

    assert code == 0
    assert out == f"{archive}:data.bin:10\n"


def test_multiple_archives_are_all_searched(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Every archive on the command line is searched and matches are reported per archive."""
    first = _make_zip(tmp_path / "first.zip", ["hello.txt"])
    second = _make_zip(tmp_path / "second.zip", ["world.txt", "skip.md"])

    code = main(["*.txt", str(first), str(second)])
    out = capsys.readouterr().out

    assert code == 0
    assert out == f"{first}:hello.txt\n{second}:world.txt\n"


def test_recursive_flag_walks_directory_for_zips(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """-R walks a directory argument for *.zip archives and searches each one."""
    nested = tmp_path / "sub"
    nested.mkdir()
    _make_zip(tmp_path / "top.zip", ["top.txt"])
    _make_zip(nested / "deep.zip", ["deep.txt"])

    code = main(["-R", "*.txt", str(tmp_path)])
    out = capsys.readouterr().out

    assert code == 0
    assert f"{tmp_path / 'top.zip'}:top.txt\n" in out
    assert f"{nested / 'deep.zip'}:deep.txt\n" in out


def test_null_flag_nul_separates_records(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """-0 separates output records with NUL bytes instead of newlines."""
    archive = _make_zip(tmp_path / "a.zip", ["a.txt", "b.txt"])

    code = main(["-0", "*.txt", str(archive)])
    out = capsys.readouterr().out

    assert code == 0
    assert out == f"{archive}:a.txt\0{archive}:b.txt\0"
