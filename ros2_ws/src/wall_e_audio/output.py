from pathlib import Path
import wave

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from ament_index_python.packages import get_package_share_directory
from piper import PiperVoice
import simpleaudio as sa


def resolve_model_path():
    local_path = Path(__file__).resolve().with_name("fr_FR-gilles-low.onnx")
    if local_path.exists():
        return local_path
    share_path = Path(get_package_share_directory("wall_e_audio"))
    model_path = share_path / "fr_FR-gilles-low.onnx"
    if model_path.exists():
        return model_path
    raise FileNotFoundError(f"Missing Piper model: {model_path}")


class TTS(Node):
    def __init__(self):
        super().__init__("tts_node")
        self.subscription = self.create_subscription(
            String,
            "/tts_text",
            self.callback,
            10,
        )
        self.voice = PiperVoice.load(str(resolve_model_path()))
        self._play_obj = None

    def callback(self, msg):
        text = msg.data.strip()
        if not text:
            return
        self.get_logger().info(f"Received: {text}")
        self.speak(text)

    def speak(self, text):
        with wave.open("/tmp/tts.wav", "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file)
        self.play()

    def play(self):
        if self._play_obj and self._play_obj.is_playing():
            self._play_obj.wait_done()
        wave_obj = sa.WaveObject.from_wave_file("/tmp/tts.wav")
        self._play_obj = wave_obj.play()


def main():
    rclpy.init()
    node = TTS()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
