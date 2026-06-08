from pathlib import Path


DEFAULT_PROMPT = """# Agent Instructions

Describe the purpose of this agent in clear English.

Include:
- what the agent is responsible for
- how it should use its tools, MCPs, and skills
- what boundaries or constraints it must respect
- the expected tone, workflow, and output style

Recommended structure:
1. Purpose
2. Responsibilities
3. Tools and MCP usage
4. Skills and context
5. Constraints
6. Output expectations
"""


def build_prompt_file(root: Path) -> Path:
    prompt_path = root / "prompt.md"
    prompt_path.write_text(DEFAULT_PROMPT, encoding="utf-8")
    return prompt_path
