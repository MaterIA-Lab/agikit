# agikit

`agikit` is a command-line toolkit for building `.agi` agent projects. It is installed with `uv`, depends on `uv`, and is designed to generate the base template for agents that later become `.agi` archives.

## Install

```bash
uv tool install .
```

During development you can also run it with:

```bash
uv run agikit --help
```

The CLI uses decorated `rich` output with colored summaries and status blocks, but it stays fully command-driven.

## Quick start

Create a new agent template:

```bash
agikit init my-agent
```

This creates:

```text
my-agent/
├── .agikit/
│   └── project.json
├── agent.yaml
├── mcps/
├── prompt.md
├── skills/
└── tools/
```

Inside the generated project:

- `prompt.md` contains the base instruction template for the agent.
- `skills/` starts empty and contains agent skills.
- `mcps/` starts empty and contains MCP package folders and their JSON definitions.
- `tools/` starts empty and is meant for Python subprojects created with `uv`.
- `agent.yaml` stores the agent metadata and runtime config.
- `.agikit/project.json` marks the directory as a valid agikit template.

## Create a skill

From inside an agikit project:

```bash
agikit skill init my-skill
```

This creates:

```text
skills/
└── my-skill/
    └── SKILL.md
```

## Create an MCP

From inside an agikit project:

```bash
agikit mcp init my-mcp
```

This creates:

```text
mcps/
└── my-mcp/
    └── my-mcp.json
```

## Create a tool package

From inside an agikit project:

```bash
agikit tool init my-tool
```

This uses `uv init --package` inside `tools/` to create a Python package for the tool.

## Build

```bash
agikit build
```

The command exists already, but `.agi` archive generation is still pending implementation.
