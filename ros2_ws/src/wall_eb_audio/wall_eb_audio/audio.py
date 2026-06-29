from pathlib import Path
import wave
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
        self.subscription = self.create_subscription(
            String,
            "/tts_text",
            self.ttscallback,
            10,
        )
        self.voice = PiperVoice.load("/workspace/ros2_ws/tom1.onnx")
        self._play_obj = None
    def ttscallback(self, msg):
        text = msg.data.strip()
        if not text:
            return
        self.get_logger().info(f"Received: {text}")
        print(text)
        self.speak(text) #ici on convertie le texte en phonetique pour eviter que le tts galere (premier commentaire qui n'est pas ecris par gpt)

    def speak(self, text):
        path = "/tmp/tts.wav"
        self.get_logger().info(f"Received: {text}")
        with wave.open(path, "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file)
        self.play(path)
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
