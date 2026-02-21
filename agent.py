import json
import anthropic
from composio import Composio
from composio_anthropic import AnthropicProvider
from dotenv import load_dotenv
import pdb

load_dotenv()

composio = Composio(provider=AnthropicProvider())
client = anthropic.Anthropic()

def perform_task(user_task, user_id, tool_name):
    # Create a session for your user
    session = composio.create(user_id=user_id)

    # Get all meta tools
    # List tools within a toolkit (top 20 by default) but we can set a limit to 50
    tools = composio.tools.get(user_id, toolkits=[tool_name.upper()], limit=50)

    pdb.set_trace()

    messages = [
        {"role": "user", "content": user_task}
    ]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        tools=tools,
        messages=messages,
    )

    # Agentic loop — keep executing tool calls until the model responds with text
    while response.stop_reason == "tool_use":
        tool_use_blocks = [block for block in response.content if block.type == "tool_use"]
        print("="*60)
        print(f"Tool : {tool_use_blocks}")
        print("="*60)
        results = composio.provider.handle_tool_calls(user_id="user_123", response=response)
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [
                {"type": "tool_result", "tool_use_id": tool_use_blocks[i].id, "content": json.dumps(result)}
                for i, result in enumerate(results)
            ]
        })
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            tools=tools,
            messages=messages,
        )

    # Print final response
    print("="*60)
    for block in response.content:
        if block.type == "text":
            print(block.text)

    return messages