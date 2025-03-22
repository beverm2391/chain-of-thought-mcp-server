import os
from groq import AsyncGroq
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set")

class GroqClient:
    def __init__(self, model: str):
        self.model = model
        self.temperature = 0
        # pass in api key to the client
        self.client = AsyncGroq(
            api_key=GROQ_API_KEY,
        )

    async def reasoning_completion(
        self,
        messages: List[Dict[str, Any]],
        thoughts_only: bool = False,
    ):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            stream=True,
        )
        try:
            async def response_generator():
                in_think_block = False
                has_processed_think_block = False
                async for chunk in response:
                    content = chunk.choices[0].delta.content  # type: ignore
                    if content is None:
                        continue

                    # Check for think tags
                    if "<think>" in content:
                        in_think_block = True
                        content = content.replace("<think>", "")
                    if "</think>" in content:
                        in_think_block = False
                        has_processed_think_block = True
                        if thoughts_only:
                            break
                        content = content.replace("</think>", "")

                    # If thoughts_only and we're not in a think block, skip
                    if thoughts_only and has_processed_think_block:
                        continue

                    yield {
                        "choices": [
                            {
                                "delta": {
                                    "content": content if not in_think_block else "",
                                    "reasoning_content": (
                                        content if in_think_block else ""
                                    ),
                                }
                            }
                        ],
                    }

            return response_generator()

        except ValueError as e:
            raise e  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")
