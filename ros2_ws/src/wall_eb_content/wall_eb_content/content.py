from dotenv import load_dotenv
from ollamafreeapi import OllamaFreeAPI
import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Content(Node):
    def __init__(self):
        super().__init__("content_node")
        self.publisher = self.create_publisher(String, "/tts_text", 10)
        self.subscription = self.create_subscription(
            String,
            "/prompt",
            self.handle_prompt,
            10,
        )
        self.client = OllamaFreeAPI()

    def handle_prompt(self, msg):
        prompt = msg.data.strip()
        if not prompt:
            return
        response = self.askllm(prompt)
        print(response)
        out = String()
        out.data = response
        self.publisher.publish(out)

    def askllm(self, prompt, context=""):
        if self.client is None:
            return prompt
        model="llama3.2:latest"
        message = prompt + " Tu es wall-eb (prononcer wall-e-bi) un assistant respectueux. Refuse les contenus haineux, violents, illégaux ou dangereux. Ne produis jamais de discrimination ou d'incitation à la haine." + f" context : {context}"
        
        content = self.client.chat(prompt = message, model=model)
        print(content)
        if content:
            print(content)
            return content
        self.get_logger().error("Empty response.")
        return ""


def main():
    rclpy.init()
    node = Content()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
