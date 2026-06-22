import rclpy
import os
from std_msgs.msg import String
import asyncio
from cerebras.cloud.sdk import Cerebras
from rclpy.node import Node
client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)


class Content(Node):
    def __init__(self):
        super().__init__('Content')
        self.publisher = self.create_publisher(
            String,
            '/tts_text',
            10
        )
        self.askllm = self.create_service(
            askllm,
            'askllm',
            self.askllm
        )

async def llmstreamaudio(input, context=""):
    chat_completion = await client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": input+" Tu es wall-eb (prononcer wall-e-bi) un assistant respectueux.
Refuse les contenus haineux, violents, illégaux ou dangereux.
Ne produis jamais de discrimination ou d'incitation à la haine. context : " +context ,
        }
    ],
    model="gpt-oss-120b",
    max_tokens=300,
    stream = true,
    )
    Str = ""
    async for chunk in chat_completion:
        Str += (chunk.choices[0].delta.content or "")
        if "!" in Str or "." in Str or "?" in Str or "/n" in Str:
            
            Str = ""
    
def askllm(input, context=""):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": input+" Tu es wall-eb (prononcer wall-e-bi) un assistant respectueux.
Refuse les contenus haineux, violents, illégaux ou dangereux.
Ne produis jamais de discrimination ou d'incitation à la haine. context : " +context ,
        }
    ],
    model="gpt-oss-120b",
    max_tokens=300,
    )
    return chat_completion
    
