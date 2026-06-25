import rclpy
from rclpy.node import Node
from std_msgs.msg import String

try:
    from cerebras.cloud.sdk import Cerebras
except ImportError:
    Cerebras = None


MODEL_NAME = "gpt-oss-120b"


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
        api_key = os.environ.get("CEREBRAS_API_KEY")
        self.client = Cerebras(api_key=api_key) if Cerebras and api_key else None
        if self.client is None:
            self.get_logger().warn(
                "Cerebras SDK or CEREBRAS_API_KEY missing; echo fallback enabled."
            )

    def handle_prompt(self, msg):
        prompt = msg.data.strip()
        if not prompt:
            return
        response = self.askllm(prompt)
        out = String()
        out.data = response
        self.publisher.publish(out)

    def askllm(self, prompt, context=""):
        if self.client is None:
            return prompt

        completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        prompt
                        + " Tu es wall-eb (prononcer wall-e-bi) un assistant respectueux."
                        " Refuse les contenus haineux, violents, illégaux ou dangereux."
                        " Ne produis jamais de discrimination ou d'incitation à la haine."
                        f" context : {context}"
                    ),
                }
            ],
            model=MODEL_NAME,
            max_tokens=300,
        )
        choice = completion.choices[0]
        content = getattr(choice.message, "content", None)
        if content:
            return content.strip()
        self.get_logger().error("Empty response from Cerebras, echoing prompt.")
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
