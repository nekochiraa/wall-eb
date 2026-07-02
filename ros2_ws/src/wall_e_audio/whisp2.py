import whisper
import spacy
from nltk.corpus import wordnet as wn
import nltk
import json

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

lang = 'fra'
nlp = spacy.load("fr_core_news_sm")

# Actions
def big_action():
    action_wake()
    action_bis()
def action_wake():
    print("on est la")

def action_search():
    action_navigate()
    action_scan()
    #print("bip, boup *bruits electroniques*...recherche en cours...")
    # plug navigation de l'atelier + reconnaissance faciale

def action_speak():
    print("que penses tu de la tastycroustification de le societe?")
    # plug llm + tts

def action_shout():
    print("j'ai ete investi d'une grande mission")
    # tts

def action_internet():
    print("fais comme si j'avais google un truc.")
    # llm google un truc, print resultat, tts

def action_bis():
    print("2e action")

def action_none():
    return

def poke_action():
    print("pika")

def action_navigate():
    print("navigating...")

def action_scan():
    print("scanning...")
        
# Dico 
context = {
    "definition":  action_internet,
    "info":        action_internet,
    "information": action_internet,
    "pourquoi":    action_internet,
    "internet":    action_internet,
    "google":      action_search,
    "pokemon":     poke_action,
}

keywords = {
    "parler":   action_speak,
    "parle":    action_speak,
    "chercher": action_search,
    "cherche":  action_search,
    "trouver":  action_search,
    "trouve":   action_search,
    "crier":    action_shout,
    "crie":     action_shout,
}

# Synonymes
def get_synonyms(word: str, lang: str = "fra") -> set[str]:
    synonyms = set()
    for synset in wn.synsets(word, lang=lang):
        for lemma in synset.lemmas(lang=lang):
            synonyms.add(lemma.name().lower().replace("_", " "))
    return synonyms

def build_synonym_map(keywords: dict, lang: str = "fra") -> dict:
    expanded = {}
    for word, action in keywords.items():
        expanded[word] = action
        for synonym in get_synonyms(word, lang):
            expanded[synonym] = action
    return expanded

# Matching 
def match_keyword(line: str, synonym_map: dict, nlp):
    """Retourne (action_name, token_idx) du 1er mot-cle trouve, sinon (None, None)."""
    doc = nlp(line.lower())
    for token in doc:
        for form in (token.text, token.lemma_):
            if form in synonym_map:
                return synonym_map[form].__name__, token.i
    return None, None

def match_context(line: str, synonym_map2: dict, nlp, keyword_idx: int = None):
    """
    Retourne ce qui suit le mot de contexte trouve.
    Fallback: retourne ce qi suit le mot-cle si pas de mot de contexte.
    """
    doc = nlp(line.lower())
    for token in doc:
        for form in (token.text, token.lemma_):
            if form in synonym_map2:
                complement = " ".join(t.text for t in doc[token.i + 1:]).strip()
                return complement if complement else None
    if keyword_idx is not None:
        complement = " ".join(t.text for t in doc[keyword_idx + 1:]).strip()
        return complement if complement else None
    return None

# stuff a faire 
def transcribe(audio_file: str) -> str:
    """Transcrit l'audio en texte et sauvegarde dans transcribed.txt."""
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_file, fp16=False)
    text = result["text"]
    with open("transcribed.txt", "w", encoding="utf-8") as f:
        f.write(text)
    return text

def detect_language(audio_file: str) -> str:
    model = whisper.load_model("tiny")
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    return max(probs, key=probs.get)

def command_tuple(text: str, synonym_map: dict) -> dict:
    for line in text.splitlines():
        action_name, token_idx = match_keyword(line, synonym_map, nlp)
        if action_name is not None:
            complement = match_context(line, context, nlp, keyword_idx=token_idx)
            synonym_map_by_name = {v.__name__: v for v in synonym_map.values()}#prints
            synonym_map_by_name[action_name]()#also prints
            return {"action": action_name, "complement": complement}
        #else:
            #action_search()
    return None

def run(audio_file: str):
    synonym_map = build_synonym_map(keywords, lang=lang)

    text = transcribe(audio_file)

    detected_lang = detect_language(audio_file)
    print(f"Detected language: {detected_lang}")

    result = command_tuple(text, synonym_map)
    print(json.dumps(result, ensure_ascii=False))
    return result


run("audio.wav")

# kachow
# mtn coder les actions, pour le tts, la nav et tout
