# Claude Code Clone

A minimal implementation of Claude Code - an AI coding assistant that uses Large Language Models (LLMs) with tool calling capabilities to interact with files and execute commands.

## Features

This implementation supports three core tools:

- **Read**: Read and return the contents of files
- **Write**: Write content to files (creates or overwrites)
- **Bash**: Execute shell commands and capture output

## Prerequisites

- Python 3.7+
- `uv` package manager (or `pip`)
- OpenRouter API key

## Setup

1. Install dependencies:
```sh
uv pip install openai
```

2. Set environment variables:
```sh
export OPENROUTER_API_KEY="your-api-key-here"
export OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"  # Optional, defaults to this
```

## Usage

Run the program with a prompt:

```sh
python app/main.py -p "Read the README.md file"
```

Or use the provided script:

```sh
./your_program.sh -p "Create a new file called hello.txt with the content 'Hello World'"
```

## Examples

**Read a file:**
```sh
python app/main.py -p "What's in the main.py file?"
```

**Write to a file:**
```sh
python app/main.py -p "Create a file called test.txt with 'Hello, World!'"
```

**Execute commands:**
```sh
python app/main.py -p "List all Python files in the current directory"
```

**Combine operations:**
```sh
python app/main.py -p "Read app/main.py, create a backup called main_backup.py, then verify the backup exists"
```

## How It Works

1. **User Input**: You provide a natural language prompt
2. **LLM Processing**: The prompt is sent to Claude (via OpenRouter) with available tools
3. **Tool Calling**: If needed, Claude requests tool calls (Read/Write/Bash)
4. **Execution**: Your program executes the requested tools
5. **Response Loop**: Results are sent back to Claude, which may request more tools
6. **Final Output**: Claude provides a natural language response

## Architecture

```
┌─────────────┐
│ User Prompt │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  call_llm()         │
│  - Send to Claude   │
│  - Tools available  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────────┐
│  Tool Calls Loop        │
│  - While tool_calls:    │
│    - execute_tool_call()│
│    - Send results back  │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────┐
│  Final Response     │
│  - Natural language │
└─────────────────────┘
```

## Tool Implementations

### Read Tool
```python
with open(file=arguments["file_path"], mode="r", encoding="utf-8") as f:
    return f.read()
```

### Write Tool
```python
with open(file=file_path, mode="w", encoding="utf-8") as f:
    f.write(content)
```

### Bash Tool
```python
result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
return result.stdout + result.stderr
```

## Model

Currently using: `anthropic/claude-haiku-4.5` via OpenRouter

## Safety Notes

- The Bash tool executes commands with shell access - use with caution
- Commands timeout after 30 seconds
- File operations use UTF-8 encoding
- Write operations will overwrite existing files without warning

## Credits

Based on the ["Build Your own Claude Code" Challenge](https://codecrafters.io/challenges/claude-code) from CodeCrafters.

## License

MIT
