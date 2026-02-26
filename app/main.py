import argparse
import os
import sys
import json

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")

def call_llm(msg):

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    chat = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=msg,
            tools=[
            {
                "type": "function",
                "function": {
                    "name": "Read",
                    "description": "Read and return the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "The path to the file to read",
                            }
                        },
                        "required": ["file_path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Write",
                    "description": "Write content to a file",
                    "parameters": {
                        "type": "object",
                        "required": ["file_path", "content"],
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "The path of the file to write to"
                                },
                            "content": {
                                "type": "string",
                                "description": "The content to write to the file"
                                }
                            }
                        }
                    }
                }
            ]
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    return chat.choices[0].message


def execute_tool_call(tool_call: dict):
    tool_call_id = tool_call.id
    name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    if name == "Read":
        with open(
            file=arguments["file_path"], mode="r", encoding="utf-8"
        ) as file_contents:
            return {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": file_contents.read(),
            }
    elif name == "Write":
        file_path = arguments["file_path"]
        content = arguments["content"]
        with open(file=file_path, mode="w", encoding="utf-8") as f:
            f.write(content)
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": f"Successfully wrote to {file_path}",
        } 


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    messages = [{ "role": "user", "content": args.p}]

    response = call_llm(messages)

    while response.tool_calls:
        messages.append(response)
        for tool_call in response.tool_calls:
            messages.append(execute_tool_call(tool_call))
        response = call_llm(messages) 

    print("Logs from your program will appear here!", file=sys.stderr)

    print(response.content)


if __name__ == "__main__":
    main()
