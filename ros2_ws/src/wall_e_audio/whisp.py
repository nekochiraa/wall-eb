import whisper
import spacy
from nltk.corpus import wordnet as wn
import nltk
import json
 
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
 
lang='fra'
 
nlp = spacy.load("fr_core_news_sm")
#actions a effectuer par Wall-eB
def action_wake():#wake up word de Wall-eB
    print("on est la")
def action_search():
    print("bip, boup *bruits electroniques*...recherche en cours...")
    #la on plug in la navigation de l'atelier + reconnaissance faciale
 
def action_speak():
    print("que penses tu de la tastycroustification de le societe?")
    #plug le llm + le tts
 
def action_shout():
    print("j'ai ete investi d'une grande mission")
    #tts encore hein, on change pas une equipe qui gagne
 
def action_internet():
    print("fais comme si j'avais google un truc.")
    #llm google un truc, puis print le resultat puis tts ou qqchose comme ca
 
def action_bis():
    print("2e action")
def action_none():
    return
def poke_action():
    print("pika")
#mots qui contextualisent
context = {
    "definition": action_internet,
    "info":       action_internet,
    "information": action_internet,
    "pourquoi":   action_internet,
    "internet":   action_internet,
    "google": action_search,
    "pokemon": poke_action,
}
keywords = {
    "parler": action_speak,
    "parle": action_speak,
    "chercher": action_search,
    "cherche": action_search,
    "trouver": action_search,
    "trouve": action_search,
    "crier": action_shout,
    "crie": action_shout,
    #"internet": action_internet,
 
 
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
 
def match_keyword(line: str, synonym_map: dict, nlp):
    doc = nlp(line.lower())
    for token in doc:
        for form in (token.text, token.lemma_):
            if form in synonym_map:
                action = synonym_map[form]
                return action.__name__, token.i
    return None, None
 
def match_context(line: str, synonym_map2: dict, nlp, keyword_idx: int = None):
    doc = nlp(line.lower())
    for token in doc:
        for form in (token.text, token.lemma_):
            if form in synonym_map2:
                # tout ce qui vient apres ce token de contexte is le complement
                complement_tokens = doc[token.i + 1:]
                complement = " ".join(t.text for t in complement_tokens).strip()
                return complement if complement else None
 
    # fallback: pas de mot de contexte -> on prend ce qui suit le mot-cle lui-meme
    if keyword_idx is not None:
        complement_tokens = doc[keyword_idx + 1:]
        complement = " ".join(t.text for t in complement_tokens).strip()
        return complement if complement else None
 
    return None
 
#speech to text
model = whisper.load_model("tiny")
result = model.transcribe("audio.wav", fp16 = False)
with open("transcribed.txt", "w") as f:
    f.write(result["text"])
 
#veritable audio feed a uttiliser
audio = whisper.load_audio("audio.wav")
audio = whisper.pad_or_trim(audio)
mel = whisper.log_mel_spectrogram(audio).to(model.device)
 
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")
 
#comnstruire la synonym map
synonym_map = build_synonym_map(keywords, lang=lang)
#print(f"Watching for {len(synonym_map)} words/synonyms: {sorted(synonym_map)}\n")
 
#search l'output et construire le json {action, complement}
result_json = None
 
with open("transcribed.txt", "r") as f:
    for line in f:
        action_name, token_idx = match_keyword(line, synonym_map, nlp)
        if action_name is not None:
            complement = match_context(line, context, nlp, keyword_idx=token_idx)
            result_json = {
                "action": action_name,
                "complement": complement
            }
            break
        #essayer de faire des actions en particuler avec certains mots, pour pas avoir a se casser la tete avec un contexte
 
print(json.dumps(result_json, ensure_ascii=False))
 
#kachow
#pour l'instant, des que wall-eB match une action, il l'execute
#mtn coder les actions, pour le tts, la nav et tout - on a des tuples maintenant

