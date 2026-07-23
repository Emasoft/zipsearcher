import argparse
import logging
import sys
from collections.abc import Iterator

import pytest

from src.entrypoint import main, parse_arguments, setup_logging


@pytest.fixture
def isolated_root_logger() -> Iterator[logging.Logger]:
    root = logging.getLogger()
    saved_handlers, saved_level = root.handlers[:], root.level
    yield root
    root.handlers[:] = saved_handlers
    root.setLevel(saved_level)


def test_parse_arguments_without_flags_defaults_to_not_verbose(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["prog"])

    arguments = parse_arguments()

    assert arguments.verbose is False


def test_parse_arguments_with_verbose_flag_sets_verbose(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["prog", "--verbose"])

    arguments = parse_arguments()

    assert arguments.verbose is True


def test_setup_logging_when_verbose_sets_info_level(isolated_root_logger: logging.Logger) -> None:
    isolated_root_logger.handlers.clear()
    isolated_root_logger.setLevel(logging.DEBUG)

    setup_logging(argparse.Namespace(verbose=True))

    assert isolated_root_logger.level == logging.INFO


def test_setup_logging_by_default_sets_warning_level(isolated_root_logger: logging.Logger) -> None:
    isolated_root_logger.handlers.clear()
    isolated_root_logger.setLevel(logging.DEBUG)

    setup_logging(argparse.Namespace(verbose=False))

    assert isolated_root_logger.level == logging.WARNING


def test_main_when_verbose_logs_parsed_arguments(monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    monkeypatch.setattr(sys, "argv", ["prog", "--verbose"])

    with caplog.at_level(logging.INFO):
        main()

    assert "verbose=True" in caplog.text
