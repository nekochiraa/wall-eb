import sounddevice as sd
from scipy.io.wavfile import write

sample_rate = 16000
time = 6 #on changera plus tard

audio = sd.rec(
    int(sample_rate * time),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

write("audio.wav", sample_rate, audio)
