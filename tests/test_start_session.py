import os
import tempfile
import unittest
from pathlib import Path

from proof.commands import resume_session, start_session
from proof.config import CLAUDE_SESSIONS_FILE_PATH, PROOF_FILE_PATH, PROOF_PROJECT_CONTEXT_FILE_NAME
from proof.exceptions import AnalysisNotFoundException, NotebookNotFoundException, SessionNotFoundException


class StartWithoutCreateTest(unittest.TestCase):
    def test_start_raises_when_analysis_was_not_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            proof_dir = tmp_path / PROOF_FILE_PATH
            proof_dir.mkdir()
            (proof_dir / PROOF_PROJECT_CONTEXT_FILE_NAME).write_text("", encoding="utf-8")

            previous_cwd = Path.cwd()
            os.chdir(tmp_path)
            try:
                with self.assertRaises(AnalysisNotFoundException):
                    start_session(
                        analysis_name="test1",
                        notebook_name="notebook.py",
                        session_name="planing",
                    )
                self.assertFalse((proof_dir / "test1").exists())
            finally:
                os.chdir(previous_cwd)

    def test_start_raises_when_notebook_does_not_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            proof_dir = tmp_path / PROOF_FILE_PATH
            analysis_root = proof_dir / "test1"
            proof_dir.mkdir()
            (proof_dir / PROOF_PROJECT_CONTEXT_FILE_NAME).write_text("", encoding="utf-8")
            analysis_root.mkdir()

            previous_cwd = Path.cwd()
            os.chdir(tmp_path)
            try:
                with self.assertRaises(NotebookNotFoundException):
                    start_session(
                        analysis_name="test1",
                        notebook_name="notebook.py",
                        session_name="planing",
                    )
                self.assertFalse((analysis_root / CLAUDE_SESSIONS_FILE_PATH).exists())
            finally:
                os.chdir(previous_cwd)

    def test_resume_raises_when_notebook_does_not_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            proof_dir = tmp_path / PROOF_FILE_PATH
            analysis_root = proof_dir / "test1"
            proof_dir.mkdir()
            (proof_dir / PROOF_PROJECT_CONTEXT_FILE_NAME).write_text("", encoding="utf-8")
            analysis_root.mkdir()
            sessions_path = analysis_root / CLAUDE_SESSIONS_FILE_PATH
            sessions_path.parent.mkdir(parents=True)
            sessions_path.write_text('["planing"]\n', encoding="utf-8")

            previous_cwd = Path.cwd()
            os.chdir(tmp_path)
            try:
                with self.assertRaises(NotebookNotFoundException):
                    resume_session(
                        analysis_name="test1",
                        notebook_name="notebook.py",
                        session_name="planing",
                    )
            finally:
                os.chdir(previous_cwd)

    def test_resume_raises_when_session_does_not_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            proof_dir = tmp_path / PROOF_FILE_PATH
            analysis_root = proof_dir / "test1"
            proof_dir.mkdir()
            (proof_dir / PROOF_PROJECT_CONTEXT_FILE_NAME).write_text("", encoding="utf-8")
            analysis_root.mkdir()
            (analysis_root / "notebook.py").write_text("", encoding="utf-8")

            previous_cwd = Path.cwd()
            os.chdir(tmp_path)
            try:
                with self.assertRaises(SessionNotFoundException):
                    resume_session(
                        analysis_name="test1",
                        notebook_name="notebook.py",
                        session_name="planing",
                    )
            finally:
                os.chdir(previous_cwd)
