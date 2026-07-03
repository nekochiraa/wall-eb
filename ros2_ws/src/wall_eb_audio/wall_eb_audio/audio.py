from pathlib import Path
import wave
from wall_eb_interfaces.srv import GenerateMessage
import subprocess
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ament_index_python.packages import get_package_share_directory
from piper import PiperVoice, SynthesisConfig
import simpleaudio as sa

class audio(Node):
    def __init__(self):
        Node.__init__(self, "audio_node")
        self.action_generateTTs(
            self,
            GenerateTTs,
            "GenerateTTs",
            self.ttscallback,
        )
        self.GenerateMessage = self.create_client(
            GenerateMessage,
            "generate_message"
        )
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("En attente du service...")
        self.action_play(
            self,
            Play,
            "Play",
            self.play,
        )
        self.voice = PiperVoice.load("/workspace/ros2_ws/tom1.onnx")
        self._play_obj = None

    async def ttscallback(self, goal_handle):
        text = goal_handle.request.text
        self.get_logger().info(f"Génération : {text}")

        request = GenerateMessage.Request()
        request.prompt = text
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        
        path = self.speak(response)

        goal_handle.succeed()
        result = GenerateTTS.Result()
        result.success = True
        result.audio_id = audio_id
        return result
    
    def speak(self, text):
        path = "/tmp/tts.wav"
        self.get_logger().info(f"Received: {text}")
        with wave.open(path, "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file)
        return path
    def is_playing(self):
        return getattr(self, '_proc', None) is not None and self._proc.poll() is None
    def play(self, path):
        while (self.is_playing()):
            pass
        subprocess.run(['aplay',path])
        

def main():
    rclpy.init()
    node = audio()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
