import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


def calculator(a: float, b: float, operator: str) -> str:
    """Perform basic arithmetic operations."""
    try:
        if operator == '+':
            return str(a + b)
        elif operator == '-':
            return str(a - b)
        elif operator == '*':
            return str(a * b)
        elif operator == '/':
            if b == 0:
                return 'Error: Division by zero'
            return str(a / b)
        else:
            return 'Error: Invalid operator. Please use +, -, *, or /'
    except Exception as e:
        return f'Error: {str(e)}'


async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4o-2024-11-20")
    termination = MaxMessageTermination(
    max_messages=10) | TextMentionTermination("TERMINATE")

    assistant = AssistantAgent(
    "assistant",
    model_client=model_client,
    system_message="You are a helpful assistant."
    )

    critic_agent = AssistantAgent(
    "critic",
    model_client=model_client,
    system_message=(
    "Criticize the assistant's answer and suggest improvements. "
    "If there are issues to be address, respond with the list of issues. "
    "However, if all issues are addressed, respond with TERMINATE."
    )
    )

    team = RoundRobinGroupChat(
    [assistant, critic_agent],
    termination_condition=termination
    )

    await Console(team.run_stream(task="Write a 5 line haiku about the ocean."))

asyncio.run(main())
