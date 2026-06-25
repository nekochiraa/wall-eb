from pathlib import Path
import wave

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from phonemizer import phonemize
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
        self.voice = PiperVoice.load("/workspace/ros2_ws/fr_FR-gilles-low.onnx")
        self._play_obj = None
        self.syn_config = SynthesisConfig(
    volume=2.0,              # Entre 0.5 et 2.0 (0.5 = plus silencieux)
    length_scale=1.0,        # > 1.0 = plus lent, < 1.0 = plus rapide
    noise_scale=1.0,         # Contrôle la variation audio
    noise_w_scale=1.0,       # Contrôle la variation des phonèmes
    normalize_audio=False,   # True = normaliser le volume
    speaker_id=0             # Pour les modèles multi-locuteurs
)
    def ttscallback(self, msg):
        text = msg.data.strip()
        if not text:
            return
        self.get_logger().info(f"Received: {text}")
        self.speak(phonemize(text,language="fr-fr", backend="espeak")) #ici on convertie le texte en phonetique pour eviter que le tts galere (premier commentaire qui n'est pas ecris par gpt)

    def speak(self, text):
        with wave.open("/tmp/tts.wav", "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file, syn_config=self.syn_config)
        self.play()

    def play(self):
        if self._play_obj and self._play_obj.is_playing():
            self._play_obj.wait_done()
            self._play_obj = None
        wave_obj = sa.WaveObject.from_wave_file("/tmp/tts.wav")
        self._play_obj = wave_obj.play()


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
