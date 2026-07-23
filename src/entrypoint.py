"""zipsearcher — search filenames inside zip archives via the central directory.

The tool answers "which entries in these archives have a name matching PATTERN?"
by reading only the zip central directory. It never inflates any member, so it
stays cheap even on huge archives.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import sys
import zipfile
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Match:
    """One matching entry: which archive, its internal path, its uncompressed size."""

    archive: str
    name: str
    size: int


def build_parser() -> argparse.ArgumentParser:
    """Construct the argparse parser for the zipsearcher CLI."""
    parser = argparse.ArgumentParser(
        prog="zipsearcher",
        description="Search for files by name inside zip archives via the central directory (no decompression).",
    )
    parser.add_argument("pattern", metavar="PATTERN", help="pattern matched against each entry inside the zip")
    parser.add_argument("archives", metavar="ARCHIVE", nargs="+", help="one or more .zip archives (or dirs with -R)")
    parser.add_argument(
        "--path",
        action="store_true",
        dest="use_path",
        help="match against the full internal path instead of the basename",
    )
    parser.add_argument("-i", "--ignore-case", action="store_true", help="case-insensitive match")
    parser.add_argument("--regex", action="store_true", help="treat PATTERN as a Python regex instead of a glob")
    parser.add_argument("-R", "--recursive", action="store_true", help="walk any ARCHIVE that is a directory for *.zip")
    parser.add_argument(
        "-l",
        "--files-with-matches",
        action="store_true",
        help="print only the archive paths that contain at least one match",
    )
    parser.add_argument("-c", "--count", action="store_true", help="print archive:N match counts")
    parser.add_argument("--size", action="store_true", help="append the entry's uncompressed size to each match line")
    parser.add_argument("-0", "--null", action="store_true", help="NUL-separate output records (for xargs -0)")
    return parser


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse argv (or sys.argv when None) into a Namespace."""
    return build_parser().parse_args(argv)


def _basename(name: str) -> str:
    """Return the basename of a zip entry name (zip entries always use '/' separators)."""
    return name.rsplit("/", 1)[-1]


def make_matcher(
    pattern: str,
    *,
    regex: bool,
    ignore_case: bool,
    use_path: bool,
) -> Callable[[str], bool]:
    """Build a predicate that reports whether a zip entry name matches PATTERN.

    Raises re.error if regex is requested and PATTERN is not a valid regex.
    """
    if regex:
        compiled = re.compile(pattern, re.IGNORECASE if ignore_case else 0)

        def regex_match(name: str) -> bool:
            target = name if use_path else _basename(name)
            return compiled.search(target) is not None

        return regex_match

    # fnmatchcase is deterministic across platforms (plain fnmatch case-folds via
    # os.path.normcase, which differs on Windows); we normalise case ourselves.
    glob_pattern = pattern.lower() if ignore_case else pattern

    def glob_match(name: str) -> bool:
        target = name if use_path else _basename(name)
        if ignore_case:
            target = target.lower()
        return fnmatch.fnmatchcase(target, glob_pattern)

    return glob_match


def iter_archives(paths: Sequence[str], recursive: bool) -> Iterator[str]:
    """Yield archive paths, expanding directories to their *.zip files when recursive."""
    for path in paths:
        if recursive and os.path.isdir(path):
            for root, _dirs, files in os.walk(path):
                for filename in sorted(files):
                    if filename.endswith(".zip"):
                        yield os.path.join(root, filename)
        else:
            yield path


def search_archive(archive: str, matcher: Callable[[str], bool]) -> list[Match] | None:
    """Return the matches in one archive, or None if the archive could not be read."""
    try:
        # infolist() parses ONLY the central directory record at the end of the
        # archive; it never reads or inflates any member payload. We deliberately
        # never call .read()/.open()/.extract*(), so nothing is decompressed —
        # that is what makes searching a huge archive cheap.
        with zipfile.ZipFile(archive) as archive_file:
            infos = archive_file.infolist()
    except (OSError, zipfile.BadZipFile) as error:
        print(f"zipsearcher: {archive}: {error}", file=sys.stderr)
        return None
    return [Match(archive, info.filename, info.file_size) for info in infos if matcher(info.filename)]


def _emit(record: str, separator: str) -> None:
    """Write one output record followed by the configured separator."""
    sys.stdout.write(record + separator)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI. Exit codes (grep-like): 0 matches, 1 no matches, 2 error and no matches."""
    args = parse_arguments(argv)

    try:
        matcher = make_matcher(
            args.pattern,
            regex=args.regex,
            ignore_case=args.ignore_case,
            use_path=args.use_path,
        )
    except re.error as error:
        # A malformed regex is a deterministic usage error — fail fast.
        print(f"zipsearcher: invalid regex {args.pattern!r}: {error}", file=sys.stderr)
        return 2

    separator = "\0" if args.null else "\n"
    total_matches = 0
    had_error = False

    for archive in iter_archives(args.archives, args.recursive):
        result = search_archive(archive, matcher)
        if result is None:
            had_error = True
            continue

        total_matches += len(result)

        if args.count:
            _emit(f"{archive}:{len(result)}", separator)
        elif args.files_with_matches:
            if result:
                _emit(archive, separator)
        else:
            for match in result:
                line = f"{match.archive}:{match.name}"
                if args.size:
                    line = f"{line}:{match.size}"
                _emit(line, separator)

    if total_matches > 0:
        return 0
    if had_error:
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
