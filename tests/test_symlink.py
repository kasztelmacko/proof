import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from proof.utils import symlink


def _privilege_error(*args, **kwargs):
    error = OSError(22, "A required privilege is not held by the client")
    error.winerror = 1314
    raise error


class SymlinkPrivilegeTest(unittest.TestCase):
    def test_file_is_linked_when_symlink_privilege_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "CONTEXT.md"
            destination = tmp_path / "analysis" / "CONTEXT.md"
            destination.parent.mkdir()
            source.write_text("project context", encoding="utf-8")

            with patch("proof.utils.os.symlink", side_effect=_privilege_error):
                symlink(source, destination)

            self.assertTrue(destination.is_file())
            self.assertEqual(destination.read_text(encoding="utf-8"), "project context")
            source.write_text("updated context", encoding="utf-8")
            self.assertEqual(destination.read_text(encoding="utf-8"), "updated context")
