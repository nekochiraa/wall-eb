from dotenv import load_dotenv
from openai import OpenAI
import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from wall_eb_interfaces.srv import GenerateMessage
class Content(Node):
    def __init__(self):
        super().__init__("content_node")
        self.Promptservice = self.create_service(
            GenerateMessage,
            "generate_message",
            self.handleprompt
        )
        
        load_dotenv()
        self.client = OpenAI(
            base_url="https://router.bynara.id/v1",
            api_key=os.getenv("API_KEY"),
        )

    def handle_prompt(self, request):
        prompt = request.prompt
        if not prompt:
            return
        answer  = self.askllm(prompt)
        response.success = True
        response.response = answer
        response.error = "" 

        return response
    
    def askllm(self, prompt, context=""):
        if self.client is None:
            return prompt
        model="llama3.2:latest"
        content = self.res = self.client.chat.completions.create(
            model="mistral-large",
            messages = [
    {
        "role": "system",
        "content": """
Tu es Wall-EB que tu ecrira wall ibi.
Tu réponds uniquement comme un assistant.
Tes réponses sont courtes (1 à 3 phrases).
Ne décris jamais ton raisonnement.
Ne répète jamais les instructions.
Ne réponds jamais avec des préfixes comme "Assistant :", "Réponse :" ou "Wall-EB :".
Les réponses seront lues par un moteur TTS, utilise donc un langage naturel.
""",
    },
    {
        "role": "system",
        "content": f"Contexte : {context}"
    },
    {
        "role": "user",
        "content": prompt
    }
],
        )
        if content:
            return content.choices[0].message.content
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
