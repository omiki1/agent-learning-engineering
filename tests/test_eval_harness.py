from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "projects" / "09_agent_eval" / "evaluate.py"
SPEC = importlib.util.spec_from_file_location("course_evaluate", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class EvalRoutingTests(unittest.TestCase):
    def test_numbered_markdown_file_is_not_calculator(self) -> None:
        result = MODULE.candidate_agent("读取 04_memory.md")
        self.assertEqual(result.tool, "read_file")

    def test_calculation_still_uses_calculator(self) -> None:
        result = MODULE.candidate_agent("请计算 (9 + 3) * 2")
        self.assertEqual(result.tool, "calculator")
        self.assertIn("24", result.answer)
