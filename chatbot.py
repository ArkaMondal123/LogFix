#importing internal modules
from intents import intents

#importing external modules
import numpy as np
import spacy
asked = input("Type a message ").strip()
nlp = spacy.load('en_core_web_sm')
spacy_en_stop_words = np.array(nlp.Defaults.stop_words)
match_thr = 0.75

def normalize_message(message):
    import string
    message = u' '.join(message.translate(dict((ord(char), u' ') for char in string.punctuation)).lower().split())
    x = message.split()
    for i in x:
        if i in spacy_en_stop_words:
            x.remove(i)
    return " ".join(x)

resp = {}
asked = normalize_message(asked)
doc = nlp(asked)
for intent in intents:
    for question in intent["qn"]:
        qn = normalize_message(question)
        doc1 = nlp(qn)
        sim = doc.similarity(doc1)
        if sim > match_thr:
            if resp:
                if resp["sim"] < sim:
                    resp["sim"] = sim
                    resp["resp"] = intent["ans"]
            else:
                resp["sim"] = sim
                resp["resp"] = intent["ans"]
if resp:
    print(resp["resp"])
else:
    print("what is you")
