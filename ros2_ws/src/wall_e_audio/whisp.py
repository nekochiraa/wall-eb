import whisper


#actions a effectuer par Wall-e B
def action1():
    print("search")

def action2():
    print("speak")

def action3():
    return
#mots a chercher
keywords = {"3":action1, "22":action2}
f = open("output.txt", "w")

#speech to text
model = whisper.load_model("tiny")
result = model.transcribe("audio2.wav", fp16 = False)
with open("output.txt", "w") as f:
    f.write(result["text"])


#test, donc euh pas important
audio = whisper.load_audio("audio2.wav")
audio = whisper.pad_or_trim(audio)
mel = whisper.log_mel_spectrogram(audio).to(model.device)

_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

#search l'output et agir en fonction
with open("output.txt", "r", encoding="utf-8") as f:
    for line in f:
        for search, action in keywords.items():
            if search in line:
                action()

