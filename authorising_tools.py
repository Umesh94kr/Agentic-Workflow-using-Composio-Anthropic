from composio import Composio
from composio_anthropic import AnthropicProvider
from dotenv import load_dotenv
import time

load_dotenv()

def connect_tool(tool_name, user_id: str = "user_123"):
    composio = Composio(provider=AnthropicProvider())
    session = composio.create(user_id=user_id)

    # Check if already connected
    toolkits = session.toolkits()
    for toolkit in toolkits.items:
        if toolkit.name.lower() == tool_name and toolkit.connection.is_active:
            print("Gmail is already connected!")
            return session

    # Trigger OAuth
    connection_request = session.authorize(tool_name)
    print(f"\nOpen this link in your browser to connect Gmail:\n\n  {connection_request.redirect_url}\n")
    input("Press Enter once you've authorized in the browser...")

    # Verify connection
    time.sleep(2)  # give Composio a moment to register
    toolkits = session.toolkits()
    for toolkit in toolkits.items:
        if toolkit.name.lower() == tool_name:
            if toolkit.connection.is_active:
                print(f"{tool_name} connected successfully!")
            else:
                print("Not connected yet — did you complete the OAuth flow in the browser?")
            return session

    print(f"{tool_name} toolkit not found — check your Composio dashboard.")
    return session

if __name__ == "__main__":
    tool_name = "gmail"
    user_id = "user_123"
    connect_tool(tool_name, user_id)