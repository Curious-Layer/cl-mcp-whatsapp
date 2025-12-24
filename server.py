from tools.tool_registry import TOOLS

def list_tools():
    return [
        {
            "name": name,
            "description": tool["description"],
            "input_schema": tool["schema"].schema()
        }
        for name, tool in TOOLS.items()
    ]


def call_tool(tool_name: str, payload: dict):
    if tool_name not in TOOLS:
        raise ValueError(f"Tool '{tool_name}' not found")

    tool = TOOLS[tool_name]
    validated_input = tool["schema"](**payload)
    return tool["handler"](validated_input)


if __name__ == "__main__":
    print("CL-WhatsApp MCP Server Ready")
