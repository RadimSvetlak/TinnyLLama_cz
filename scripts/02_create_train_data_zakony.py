# ------------------------------------------------------------
# Název: Generátor tréninkových dat z paragrafů zákonů
# Popis:
#   Tento skript načítá JSON soubory se strukturou:
#       { "zakon": "...", "paragraf": "§ X", "text": "..." }
#   a pro každý záznam vytvoří několik tréninkových prompt–completion párů.
#   Používá lokálně běžící model přes knihovnu llama_cpp pro:
#       1) Základní uložení textu paragrafu.
#       2) Generování jedné otázky a odpovědi k paragrafu (pokud je dost dlouhý).
#       3) Vytvoření shrnutí do jedné věty (u delších textů).
#   Výsledky ukládá ve formátu JSONL do souboru OUTPUT_FILE.
#
# Vstup:
#   - Soubory .json ve složce DATA_FOLDER (každý obsahuje list paragrafů).
#
# Výstup:
#   - Soubor JSONL s prompt–completion dvojicemi (pro trénink modelu).
#
# Závislosti:
#   - Python 3.8+
#   - llama-cpp-python
#
# ------------------------------------------------------------


import os
import json
import re
from llama_cpp import Llama

# 🔧 Cesta k modelu GGUF
MODEL_PATH = "D:\\AI\\gemma_test\\google_gemma-3-4b-it-qat-Q8_0.gguf"

# 📁 Složka s JSON soubory
DATA_FOLDER = "data"

# 📤 Výstupní soubor
OUTPUT_FILE = "training_data.jsonl"

# 🧠 Inicializační prompt pro Gemma-chat
initial_prompt = "<start_of_turn>user\n"
initial_prompt += (
    "Jsi užitečný chatbot, který rozumí česky a má informace o České republice. "
    "Odpovídej pouze česky, se správnou gramatikou, skloňováním a časováním. "
    "Když tě požádám o vytvoření otázky a odpovědi, vždy odpovídej ve formátu:\n\n"
    "Otázka: ...\nOdpověď: ...\n\n"
    "Nepoužívej hvězdičky ani jiné formátování. Odpovědi piš stručně, jasně a věcně."
)
initial_prompt += "<end_of_turn>\n<start_of_turn>model\n"

# 🚀 Inicializace modelu s GPU
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=-1,
    #verbose=False
)

def format_prompt(user_input):
    return initial_prompt + f"<start_of_turn>user\n{user_input}<end_of_turn>\n<start_of_turn>model\n"

def clean_text(text):
    return re.sub(r"\*+", "", text).strip()

def extract_qa(text):
    match = re.search(r"Otázka[:\-]?\s*(.*?)\s*Odpověď[:\-]?\s*(.*)", text, re.DOTALL | re.IGNORECASE)
    if match:
        question = clean_text(match.group(1))
        answer = clean_text(match.group(2))
        return question, answer
    elif ":" in text:
        parts = text.split(":", 1)
        return clean_text(parts[0]), clean_text(parts[1])
    else:
        return None, None

def generate(user_input, max_tokens=256):
    prompt = format_prompt(user_input)
    output = llm(prompt, max_tokens=max_tokens, stop=["<end_of_turn>"])
    return output["choices"][0]["text"].strip()

def process_paragraph(zakon, paragraf, text):
    entries = []

    entries.append({
        "prompt": f"{zakon} {paragraf}",
        "completion": text.strip().replace("\n", " ")
    })

    if len(text) > 100:
        q_prompt = (
            "Vytvoř jednu otázku a odpověď k následujícímu paragrafu. "
            "Použij formát:\nOtázka: ...\nOdpověď: ...\n\n"
            f"{text.strip()}"
        )
        qa_raw = generate(q_prompt)
        question, answer = extract_qa(qa_raw)
        if question and answer:
            entries.append({
                "prompt": question,
                "completion": answer
            })

    if len(text) > 300:
        s_prompt = f"Shrň následující paragraf do jedné věty:\n\n{text.strip()}"
        summary = generate(s_prompt)
        entries.append({
            "prompt": f"Shrň paragraf {paragraf} zákona {zakon}.",
            "completion": clean_text(summary)
        })

    return entries

# 🧠 Zpracování všech souborů
all_items = []
for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".json"):
        filepath = os.path.join(DATA_FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_items.extend(data)

total = len(all_items)

# 📤 Průběžné ukládání do souboru
with open(OUTPUT_FILE, "a", encoding="utf-8") as out_file:
    for idx, item in enumerate(all_items, start=1):
        zakon = item.get("zakon")
        paragraf = item.get("paragraf")
        text = item.get("text")
        if zakon and paragraf and text:
            print(f"🔄 Pracuji na paragrafu {idx} / z celkových {total}")
            entries = process_paragraph(zakon, paragraf, text)
            for entry in entries:
                out_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"\n✅ Hotovo! Výstupní data jsou v souboru: {OUTPUT_FILE}")