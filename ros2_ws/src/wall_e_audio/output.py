from piper import PiperVoice
import wave
import simpleaudio as sa

class TTS(Node):
    def __init__(self):
        self.subscription = self.create_subscription(
            String,
            '/tts_text',
            self.callback,
            10
        )
        self.syn_config = SynthesisConfig(
            volume=0.5,  # half as loud
            length_scale=2.5,  # twice as slow
            noise_scale=1.0,  # more audio variation
            noise_w_scale=1.0,  # more speaking variation
            normalize_audio=False, # use raw audio from voice
        )
        self.voice = PiperVoice.load("fr_FR-gilles-low.onnx")
        self.playobj = None
    def callback(self, msg):
        text = msg.data
        self.get_logger().info(f"Received: {text}")
        self.speak(text)
        
    def speak(self, text):
        
        with wave.open("/tmp/tts.wav", "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file, syn_config=self.syn_config)
        self.play()
    def play(self):
        if playobj:
            if play_obj.is_playing():
                wait_done()
        wave_obj = sa.WaveObject.from_wave_file("/tmp/tts.wav")
        play_obj = wave_obj.play()
