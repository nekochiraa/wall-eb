import pyaudio
import wave


import pyaudio
#'''
p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)

    if info["maxInputChannels"] > 0:
        print(
            i,
            info["name"],
            "inputs:",
            info["maxInputChannels"]
        )
#'''
#'''Test pour peripheriques audio
p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(i, info["name"])
#'''
#'''
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

audi = pyaudio.PyAudio()


stream = audi.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    #input_device_index = 13,
    frames_per_buffer=CHUNK
)

frames = []

for _ in range(int(RATE/ CHUNK * 5)):
    data = stream.read(CHUNK)
    frames.append(data)

stream.stop_stream()
stream.close()
audi.terminate()

wf = wave.open("audio.wav", "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(audi.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b"".join(frames))
wf.close()
#'''





