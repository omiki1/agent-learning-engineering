from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


DEMO_DIR = Path(__file__).resolve().parents[1] / "examples" / "00_simple_agent"
sys.path.insert(0, str(DEMO_DIR))

from main import (  # noqa: E402
    Agent,
    ScriptedModel,
    ToolCall,
    build_registry,
    safe_calculate,
)


class CalculatorTests(unittest.TestCase):
    def test_calculates_supported_expression(self) -> None:
        self.assertEqual(safe_calculate("(23 + 19) * 2"), 84)

    def test_rejects_power_operator(self) -> None:
        with self.assertRaisesRegex(ValueError, "不支持"):
            safe_calculate("2 ** 100")


class RegistryTests(unittest.TestCase):
    def test_unknown_tool_becomes_observation(self) -> None:
        output = build_registry().execute(
            ToolCall(call_id="1", name="missing", arguments="{}")
        )
        self.assertEqual(json.loads(output)["error"], "unknown_tool")

    def test_invalid_json_becomes_observation(self) -> None:
        output = build_registry().execute(
            ToolCall(call_id="1", name="calculator", arguments="not-json")
        )
        self.assertEqual(json.loads(output)["error"], "invalid_arguments")


class AgentLoopTests(unittest.TestCase):
    def test_offline_agent_calls_tool_then_finishes(self) -> None:
        traces: list[str] = []
        agent = Agent(
            ScriptedModel(),
            build_registry(),
            max_steps=4,
            trace_sink=traces.append,
        )

        answer = agent.run("请计算 (23 + 19) * 2")

        self.assertEqual(answer, "计算结果是 84。")
        self.assertEqual(len(traces), 3)
        self.assertIn("tool_calls=calculator", traces[0])
        self.assertIn('"value": 84', traces[1])
        self.assertIn("final", traces[2])

    def test_max_steps_stops_loop(self) -> None:
        agent = Agent(
            ScriptedModel(),
            build_registry(),
            max_steps=1,
            trace_sink=lambda _: None,
        )

        with self.assertRaisesRegex(RuntimeError, "达到最大步数"):
            agent.run("请计算 1 + 1")


if __name__ == "__main__":
    unittest.main()

