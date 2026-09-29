import importlib
import os
from unittest.mock import patch

import pytest

import rich


@pytest.fixture(autouse=True)
def restore_import_cwd():
    """Reload the module afterwards so the real cwd is captured again."""
    yield
    importlib.reload(rich)


@pytest.mark.parametrize(
    "error",
    [
        FileNotFoundError(2, "No such file or directory"),
        PermissionError(1, "Operation not permitted"),
        PermissionError(13, "Permission denied"),
        OSError(5, "Input/output error"),
    ],
)
def test_import_cwd_falls_back_to_empty_string(error):
    """An unresolvable cwd must not break importing rich.

    See https://github.com/Textualize/rich/issues/4201
    """
    with patch.object(os, "getcwd", side_effect=error):
        reloaded_rich = importlib.reload(rich)
    assert reloaded_rich._IMPORT_CWD == ""


def test_import_cwd_is_recorded_when_available():
    reloaded_rich = importlib.reload(rich)
    assert reloaded_rich._IMPORT_CWD == os.path.abspath(os.getcwd())
