"""Tests for app quiz label discovery."""

import importlib
import sys
import tempfile
import types
import unittest
from pathlib import Path


sys.modules.setdefault("streamlit", types.SimpleNamespace(session_state={}))
app = importlib.import_module("app")


class ScanQuizFilesTests(unittest.TestCase):
    def test_strips_quiz_prefix_from_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            quiz_dir = Path(tmp) / "quizzes"
            quiz_dir.mkdir()
            quiz_file = quiz_dir / "quiz-sample-exam.json"
            quiz_file.write_text("[]", encoding="utf-8")

            original_dirs = app.QUIZ_DIRS
            app.QUIZ_DIRS = [quiz_dir]
            try:
                quiz_files = app.scan_quiz_files()
            finally:
                app.QUIZ_DIRS = original_dirs

        self.assertIn("sample-exam", quiz_files)
        self.assertEqual(quiz_files["sample-exam"], quiz_file)
        self.assertNotIn("quizzes/quiz-sample-exam", quiz_files)

    def test_preserves_filename_without_quiz_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            quiz_dir = Path(tmp) / "quizzes"
            quiz_dir.mkdir()
            quiz_file = quiz_dir / "networking-basics.json"
            quiz_file.write_text("[]", encoding="utf-8")

            original_dirs = app.QUIZ_DIRS
            app.QUIZ_DIRS = [quiz_dir]
            try:
                quiz_files = app.scan_quiz_files()
            finally:
                app.QUIZ_DIRS = original_dirs

        self.assertIn("networking-basics", quiz_files)
        self.assertEqual(quiz_files["networking-basics"], quiz_file)

    def test_appends_numeric_suffix_for_duplicate_labels(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            quiz_dir = Path(tmp) / "quizzes"
            quiz_dir.mkdir()
            first = quiz_dir / "quiz-same-topic.json"
            second = quiz_dir / "same-topic.json"
            first.write_text("[]", encoding="utf-8")
            second.write_text("[]", encoding="utf-8")

            original_dirs = app.QUIZ_DIRS
            app.QUIZ_DIRS = [quiz_dir]
            try:
                quiz_files = app.scan_quiz_files()
            finally:
                app.QUIZ_DIRS = original_dirs

        self.assertEqual(quiz_files["same-topic"], first)
        self.assertEqual(quiz_files["same-topic (2)"], second)


if __name__ == "__main__":
    unittest.main()
