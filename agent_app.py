"""
A minimal Chainlit app that showcases the new OpenAI function-calling (tool) capability
inside a Chainlit chat interface. The agent exposes one simple tool – it returns the
current date & time.

Run with:
    chainlit run agent_app.py -w

Requirements (see requirements.txt):
    pip install openai chainlit python-dotenv
"""

from __future__ import annotations

import datetime
import os
from typing import Dict, List

import chainlit as cl
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------------------------------
# Environment / client setup
# ---------------------------------------------------------------------------
# Load variables from a .env file if present (handy for OPENAI_API_KEY)
load_dotenv()

client = OpenAI()  # expects OPENAI_API_KEY in the environment

# ---------------------------------------------------------------------------
# Tool (function) definition sent to the model
# ---------------------------------------------------------------------------
FUNCTIONS: List[Dict] = [
    {
        "name": "get_current_datetime",
        "description": "Return the current date and time in ISO-8601 format.",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    }
]

def get_current_datetime() -> str:
    """Implementation of our single tool."""
    return datetime.datetime.now().isoformat()


# ---------------------------------------------------------------------------
# Chainlit event handlers
# ---------------------------------------------------------------------------
@cl.on_chat_start
async def on_chat_start():
    # Store (role, content) chat history in the session so every request has context
    cl.user_session.set("history", [])


@cl.on_message
async def on_message(message: cl.Message):
    # Retrieve conversation so far and append the new user message
    history: List[Dict] = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    # First request – let the model decide if it wants to call a tool
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-1106"),
        messages=history,
        functions=FUNCTIONS,
        function_call="auto",
    )

    msg = response.choices[0].message

    # Did the model request a function/tool?
    if msg.function_call:
        if msg.function_call.name == "get_current_datetime":
            # Execute the tool locally
            tool_result = get_current_datetime()

            # Add the assistant message that contained the function_call
            history.append(
                {
                    "role": "assistant",
                    "content": None,
                    "function_call": msg.function_call.model_dump(),
                }
            )
            # Add the function result message
            history.append(
                {
                    "role": "function",
                    "name": "get_current_datetime",
                    "content": tool_result,
                }
            )

            # Second request – with the tool result – so the model can respond
            follow_up = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-1106"),
                messages=history,
            )
            assistant_content = follow_up.choices[0].message.content
        else:
            assistant_content = "I don't know how to run the requested function."
    else:
        assistant_content = msg.content

    # Persist assistant response in history and send it back to the UI
    history.append({"role": "assistant", "content": assistant_content})
    cl.user_session.set("history", history)

    await cl.Message(content=assistant_content).send() 