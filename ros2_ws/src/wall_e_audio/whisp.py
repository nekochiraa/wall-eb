import whisper
import spacy
from nltk.corpus import wordnet as wn
import nltk

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

lang='fra'


nlp = spacy.load("fr_core_news_sm")
#actions a effectuer par Wall-e B
def action_search():
    print("search")

def action_speak():
    print("speak")

def action_none():
    return
#mots a chercher -> action
keywords = {
    "chercher": action_search,   
    "parler":   action_speak,    
}
 
#synonymes depuios wordnet
def get_synonyms(word: str, lang: str = "fra") -> set[str]:
    synonyms = set()
    for synset in wn.synsets(word, lang=lang):
        for lemma in synset.lemmas(lang=lang):
            synonyms.add(lemma.name().lower().replace("_", " "))
    return synonyms

def build_synonym_map(keywords: dict, lang: str = "fra") -> dict[str, callable]:

    expanded = {}
    for word, action in keywords.items():
        expanded[word] = action                        
        for synonym in get_synonyms(word, lang):
            expanded[synonym] = action               
    return expanded

def match_line(line: str, synonym_map: dict, nlp) -> None:
    doc = nlp(line.lower())
    for token in doc:
        for form in (token.text, token.lemma_):
            if form in synonym_map:
                print(f"  → matched '{form}' in: {line.strip()!r}")
                synonym_map[form]()
                break 
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

#comnstruire la synonym map
synonym_map = build_synonym_map(keywords, lang=lang)
print(f"Watching for {len(synonym_map)} words/synonyms: {sorted(synonym_map)}\n")

#search l'output et agir en fonction
with open("output.txt", "r", encoding="utf-8") as f:
    for line in f:
        match_line(line, synonym_map, nlp)

#maybe get the word, write all of its synonyms in a file, read that file, match with a keyword, execute action