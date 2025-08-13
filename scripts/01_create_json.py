"""
# 📜 Parser zákonů do JSON

Tento skript slouží k převodu textových souborů obsahujících znění zákonů (formát `.txt`) do strukturovaného formátu **JSON**.  
Identifikuje paragrafy podle znaku `§` a ukládá jejich obsah do přehledné struktury.

## ✨ Funkce
- **Automatická detekce paragrafů** na základě regulárního výrazu.
- **Čisté oddělení textu** podle struktury zákona.
- **Uložení dat** v UTF-8 kódování.
- **Zachování názvu zákona** v každém záznamu.

"""


import os
import re
import json

# 📁 Nastav cestu ke složce se zákony
INPUT_FOLDER = ".\\zakony"
OUTPUT_FOLDER = ".\\json"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 🔍 Regex pro řádky začínající paragrafem (ignoruje mezery před §)
def is_paragraph_line(line):
    return re.match(r"^\s*§\s*\d+[a-zA-Z]*$", line.strip())

def extract_paragraphs(text):
    lines = text.splitlines()
    paragraphs = []
    current_par = None
    buffer = []

    for line in lines:
        line = line.strip()
        if is_paragraph_line(line):
            if current_par:
                paragraphs.append({
                    "paragraf": current_par,
                    "text": "\n".join(buffer).strip()
                })
                buffer = []
            current_par = line
        elif current_par:
            buffer.append(line)

    # Ulož poslední paragraf
    if current_par and buffer:
        paragraphs.append({
            "paragraf": current_par,
            "text": "\n".join(buffer).strip()
        })

    return paragraphs

for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".txt"):
        zakon_name = os.path.splitext(filename)[0]
        filepath = os.path.join(INPUT_FOLDER, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        # Extrahuj paragrafy
        paragrafy = extract_paragraphs(text)

        # Přidej název zákona ke každému paragrafu
        zakon_json = []
        for p in paragrafy:
            zakon_json.append({
                "zakon": zakon_name,
                "paragraf": p["paragraf"],
                "text": p["text"]
            })

        # Ulož jako JSON
        output_path = os.path.join(OUTPUT_FOLDER, f"{zakon_name}.json")
        with open(output_path, "w", encoding="utf-8") as f_out:
            json.dump(zakon_json, f_out, ensure_ascii=False, indent=2)

        print(f"✅ Hotovo: {filename} → {output_path}")