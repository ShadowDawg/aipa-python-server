import asyncio
import os
from pprint import pprint
import shutil
import subprocess
import time
from typing import Any

# i like pikachu

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerSse
from agents.model_settings import ModelSettings

async def run(mcp_server: MCPServer, messages: list):
    agent = Agent(
        name="Gmail Assistant",
        instructions="You are a helpful assistant that can handle gmail tasks.",
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="required"),
    )

    # Use the `add` tool to add two numbers
    # message = "send an email to krishsingh2005@gmail.com convincing him that mushroom dosa is goated. also tell him the square root of pi."
    # print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=messages)
    return result


async def main():


    async with MCPServerSse(
            name="SSE GMAIL Server",
            params={
                "url": "https://mcp.composio.dev/gmail/enough-miniature-terabyte-vtIXTm",
            },
        ) as server:
            trace_id = gen_trace_id()
            with trace(workflow_name="SSE Example", trace_id=trace_id):
                print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
                # await run(server)

                messages = []
                while True:
                    user_input = input("User: ")
                    messages.append({"role": "user", "content": user_input, "type": "message"})
                    pprint( messages)
                    result = await run(server, messages)
                    # print(result.to_input_list())
                    pprint(result.final_output)
                    messages = result.to_input_list()
                    
if __name__ == "__main__":
    asyncio.run(main())
