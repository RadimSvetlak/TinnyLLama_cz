# ------------------------------------------------------------
# Název: Generátor tréninkových dat pro skloňování českých podstatných jmen
# pro množné číslo
# Popis:
#   Tento skript vytváří tréninkové datasety pro model (např. Gemma/LLaMA)
#   určené ke zpracování a pochopení českého skloňování.
#
#   Obsahuje:
#     - Funkci pro vypsání všech vzorů a jejich tvarů podle pádů.
#     - Rodově specifické instrukce a příklady (rod_templates).
#     - Funkce create_gemini_prompts a create_gemini_prompts2, které pro zadaná
#       slova a vzory sestaví prompty s úkolem k vygenerování správných pádových
#       tvarů.
#     - Funkci process_prompts_with_gemma, která odešle tyto prompty do modelu,
#       zpracuje odpověď a uloží ji v několika variantách (přímá otázka,
#       pádová otázka, doplňovací věta) do JSONL souboru.
#     - Funkci create_data, která generuje sadu obecných tréninkových příkladů
#       na základě dostupných vzorů, slov a jejich pádových tvarů.
#
# Vstupy:
#   - Slovníky declension_patterns a vzorova_slova s definicemi vzorů a
#     vzorových slov.
#   - Lokální instance modelu (llm) pro generování tvarů.
#
# Výstupy:
#   - Soubor vystup_trenink.jsonl obsahující prompty a správné odpovědi
#     pro trénink modelu na skloňování.
#   - Soubor train_prompts.jsonl s obecnými tréninkovými páry prompt–completion.
#
# Závislosti:
#   - Python 3.8+
#   - llama-cpp-python
#   - Strukturovaná vstupní data ve slovnících s pádovými vzory a slovy.
#
# ------------------------------------------------------------



import google.generativeai as genai
import time
import re
import json
import random
# Slovník skloňovacích vzorů s příklady tvarů v jednotlivých pádech

from llama_cpp import Llama

# 🧠 Inicializace modelu Gemma
llm = Llama(
    model_path="D:\\AI\\gemma_test\\google_gemma-3-12b-it-qat-Q2_K.gguf",   
    #model_path="D:\\AI\\_models\\gpt-oss-20b-Q4_K_S.gguf",   
    n_ctx=2048,
    n_threads=12,
    n_gpu_layers=-1,
    n_batch=512,
    verbose=True
)



declension_patterns = {
    "ženský": {
        "žena":    ["ženy", "žen", "ženám", "ženy", "ženy", "ženách", "ženami"],
        "růže":    ["růže", "růží", "růžím", "růže", "růže", "růžích", "růžemi"],
        "píseň":   ["písně", "písní", "písním", "písně", "písně", "písních", "písněmi"],
        "kost":    ["kosti", "kostí", "kostem", "kosti", "kosti", "kostech", "kostmi"]
    },
    "střední": {
        "město":   ["města", "měst", "městům", "města", "města", "městech", "městy"],
        "moře":    ["moře", "moří", "mořím", "moře", "moře", "mořích", "mořemi"],
        "stavení": ["stavení", "stavení", "stavením", "stavení", "stavení", "staveních", "staveními"],
        "dítě":    ["děti", "dětí", "dětem", "děti", "děti", "dětech", "dětmi"]
    },
    "mužský_životný": {
        "muž":     ["muži", "mužů", "mužům", "muže", "muži", "mužích", "muži"],
        "pán":     ["páni", "pánů", "pánům", "pány", "páni", "pánech", "pány"],
        "soudce":  ["soudci", "soudců", "soudcům", "soudce", "soudci", "soudcích", "soudci"],
        "učitel":  ["učitelé", "učitelů", "učitelům", "učitele", "učitelé", "učitelích", "učiteli"]
    },
    "mužský_neživotný": {
        "hrad":    ["hrady", "hradů", "hradům", "hrady", "hrady", "hradech", "hrady"],
        "stroj":   ["stroje", "strojů", "strojům", "stroje", "stroje", "strojích", "stroji"]
    }
}


vzorova_slova = {
    "ženský": {
        "žena": ["pěny", "nohy", "matky", "ruce", "dcery", "chudoby", "sestry", "továrny", "knihy"],
        "růže": ["kůže", "učebnice", "práce", "ulice", "nemocnice", "duše", "ulice", "naděje"],
        "píseň": ["plísně", "zbraně", "myši", "věže", "zdi"],
        "kost": ["radosti", "starosti", "noci", "moci", "smrti", "části", "vlhkosti"]
    },
    "střední": {
        "město": ["těsta", "auta", "kola", "okna", "jablka", "divadla", "pouzdra", "razítka"],
        "moře": ["pole", "srdce", "nebe", "slunce", "vejce"],
        "stavení": ["nastavení", "nádraží", "nařízení", "řízení", "podezření"],
        "dítě": ["štěňata", "koťata", "štěňata", "mláďata", "zvířata"]
    },
    "mužský_životný": {
        "muž": ["mlži", "nože", "hráči", "hospodáři", "přátelé"],
        "pán": ["kmáni", "vojáci", "dědečkové", "sousedé", "studenti"],
        "soudce": ["poslanci", "vůdci", "lékaři", "ochránci"],
        "předseda": ["hrdinové", "kolegové", "turisté", "správci", "kupci"]
    },
    "mužský_neživotný": {
        "hrad": ["hrady", "zuby", "sešity", "přístavy", "lesy"],
        "stroj": ["stroje", "pokoje", "vlaky", "stoly", "batohy"]
    }
}


# Výpis všech vzorů a tvarů
def print_declension_patterns():
    for gender, patterns in declension_patterns.items():
        print(f"\nRod: {gender}")
        for pattern, forms in patterns.items():
            print(f"  Vzor: {pattern}")
            print(f"    Pády: {', '.join(forms)}")



# rodově specifická pravidla a příklady
rod_templates = {
    "ženský": """\
- Přechylování: dcery -> dcerám, hole -> holím
- Jemné změny samohlásek: ě po d, t, n (např. ženy -> ženám)
- Změna samohlásky: ě po p, b, v, ale pozor na výjimky jako např. 'matky', kde je správný tvar 'matkám' a ne 'matěm'.
- Měkké souhlásky: k -> c (matky -> matkám), h -> z (nohy -> nohám)
- Vynechání e po měkké souhlásce: písně -> písním
Výjimky: Je důležité, aby model správně pochopil klíčové výjimky, jako jsou 'matky' -> 'matkám' a 'pěny' -> 'pěnám'. 
Tyto výjimky se objevují i v jiných slovech, kde se skloňování může lišit od běžného vzoru.
Příklady: 
tvary slova matky = "matky, matek, matkám, matky, matky, matkách, matkami"
tvary slova chudoby = "chudoby, chudob, chudobám, chudoby, chudoby, chudobách, chudobami"
""",

    "mužský_životný": """\
- 'y' po tvrdých (h, ch, k, r, d, t, n) 
- 'i' po měkkých (ž, š, č, ř, c, j)
- Přechylování kmene: psi -> psům  
- Vynechání e po měkké souhlásce na konci: dědečci -> dědečkům
Příklady: 
tvary slova psi: "psi, psů, psům, psy, psi, psech, psy"
tvary slova muži: "muži, mužů, mužům, muže, muži, mužích, muži"
""",

    "mužský_neživotný": """\
- Změna ů -> o v lokálu/instrumentálu (stoly -> stolům)
- i/y dle tvrdosti souhlásek
Příklady: 
tvary slova stoly = "stoly, stolů, stolům, stoly, stoly, stolech, stoly"
""",

    "střední": """\
Specifika pro rod střední:
- Vokativ často identický s nominativem
Příklady: 
tvary slova těsta = "těsta, těst, těstům, těsta, těsta, těstech, těsty"
tvary slova kuřata = "kuřata, kuřat, kuřatům, kuřata, kuřataa, kuřatech, kuřaty"
tvary slova moře = "moře, moří, mořím, moře, moře, mořích, moři"
"""
}


def create_gemini_prompts():
    gemini_prompts = []
    cases = [
        "nominativ", "genitiv", "dativ",
        "akuzativ", "vokativ", "lokál", "instrumentál"
    ]

    for rod, vzory in vzorova_slova.items():
        for vzor, words in vzory.items():
            if vzor not in declension_patterns.get(rod, {}):
                continue

            # připravíme text paradigmatu 1.–7. pádu
            pattern_forms = declension_patterns[rod][vzor]
            pattern_lines = [
                f"{idx+1}. pád ({cases[idx]}): {form}"
                for idx, form in enumerate(pattern_forms)
            ]
            pattern_text = "\n".join(pattern_lines)

            for word in words:
                # base prompt s úkolem a ukázkou vzoru
                base_prompt = (
                    f"Úkolem je vyskloňovat slovo \"{word}\" podle vzoru \"{vzor}\".\n\n"
                    f"Skloňování vzoru \"{vzor}\" je následující:\n"
                    f"{pattern_text}\n\n"
                    f"Při skloňování pamatujte na možné výjimky:\n"
                )

                # přidáme rodově specifické instrukce
                rod_instr = rod_templates.get(rod, "")

                # spojíme vše dohromady
                prompt = (
                    base_prompt
                    + rod_instr
                    + "\n\n"
                    + f"Vyskloňujte \"{word}\", každý tvar na nový řádek."
                    + "\nPamatujte, nepoužívejte jednotné číslo ani zdrobněliny. "
                    + "\n Odpovídej jedním slovem, které je ve správném tvaru"
                )

                gemini_prompts.append({
                    "prompt": prompt.strip(),
                    "completion": "",
                    "word": word,
                    "muster": vzor
                })

    process_prompts_with_gemma(gemini_prompts)
    return gemini_prompts
    
    
 

def process_prompts_with_gemma(prompts):
    output_file = "vystup_trenink_mn.jsonl"
    total = len(prompts)

    with open(output_file, "w", encoding="utf-8") as f:
        pass;

    for idx, entry in enumerate(prompts, start=1):
        prompt_text = entry["prompt"]
        word = entry.get("word", "???")
        vzor = entry.get("muster", "???")

        print(f"\n🟡 Posílám prompt {idx} / {total}: {word} ({vzor})")

        try:
            # 🔁 Vytvoř prompt pro Gemmu
            full_prompt = (
                "<start_of_turn>user\n"
                "Jsi užitečný chatbot, který rozumí česky. "
                "Když tě požádám o skloňování slova, odpovíš sedmi tvary v pořadí pádů.\n\n"
                f"{prompt_text}\n"
                "<end_of_turn>\n<start_of_turn>model\n"
            )

            # 🔍 Zavolej model
            response = llm(full_prompt, max_tokens=512)
            raw_output = response["choices"][0]["text"].strip()
            print(f"🟢 prompt_text:\n{prompt_text}")
            print(f"🟢 Odpověď:\n{raw_output}")

            # 🧹 Zpracuj výstup – fallback logika
            lines = [line.strip() for line in raw_output.split("\n") if line.strip()]
            forms = []

            for line in lines:
                match = re.search(r"^\d\.?\s*pád:?\s*(.+)", line, re.IGNORECASE) or \
                        re.search(r"^\d\.?\s*:? (.+)", line) or \
                        re.match(r"^[A-Za-zÁ-Žá-ž\-]+$", line)
                if match:
                    cleaned = re.sub(r"^\(?.*?\):\s*", "", line)
                    forms.append(cleaned.strip())



            if len(forms) < 3:
                print(f"⚠️ Výstup je příliš krátký ({len(forms)} tvarů) – přeskočeno")
                continue


            # Pádové otázky a názvy pádů
            padove_otazky = [
                ("Nominativ", "Kdo? Co?"),
                ("Genitiv", "Koho? Čeho?"),
                ("Dativ", "Komu? Čemu?"),
                ("Akuzativ", "Koho? Co?"),
                ("Vokativ", "Oslovení"),
                ("Lokál", "O kom? O čem?"),
                ("Instrumentál", "S kým? S čím?")
            ]
   

            # 💾 Ulož do souboru
            sentence_starters = {
                "1. pád": ["Toto jsou", "Zde stojí", "Tohle jsou", "Za dveřmi jsou", "Hlavní hrdinové jsou"],
                "2. pád": ["Nepůjde to bez", "Vidím to uprostřed", "Bylo to bez", "Bojím se", "Zbavil jsem se"],
                "3. pád": ["Za to děkuji", "Rád pomáhám", "Věřím", "Svěřil jsem se", "Odpovídám"],
                "4. pád": ["Zde vidím", "K tomu potřebuji", "Stále hledám", "Mám rád", "Čekám na"],
                "5. pád": ["Volám vás,", "Vidím vás,", "Slyším vás,", "Kde jste,", "Vážení"],
                "6. pád": ["Mluvili jsme o", "Píšu o", "Zmínil se o", "Přemýšlím o", "Čtu o"],
                "7. pád": ["Jdu s", "Pracuji s", "Setkal jsem se s", "Malujeme s", "Mluvím s"]
            }


            # 💾 Ulož do souboru
            with open(output_file, "a", encoding="utf-8") as f:
                # jednotlivé pády
                for i, form in enumerate(forms[:7]):
                    
                    # 1) -----  konkrétní tvar  ----- 
                    pair = {
                        "prompt": f"napiš slovo '{word}' v {i+1}. pádě:",
                        "completion": form,
                    }
                    f.write(json.dumps(pair, ensure_ascii=False) + "\n")

                    pair = {
                        "prompt": f"vyskloňuj slovo {word} v {i+1}. pádě",
                        "completion": form,
                    }
                    f.write(json.dumps(pair, ensure_ascii=False) + "\n")

                    # 2) pádová otázka
                    nazev_padu, otazka = padove_otazky[i]
                    pad_question = {
                        "prompt": f"Na otázku '{otazka}' odpovídá u slova '{word}' tvar:",
                        "completion": f"{form}"
                    }
                    f.write(json.dumps(pad_question, ensure_ascii=False) + "\n")

                    # 3) doplňovací úloha s náhodným začátkem
                    case_key = f"{i+1}. pád"
                    starter = random.choice(sentence_starters[case_key])
                    fill_prompt = {
                        "prompt": f"Doplň správný tvar: {starter} ({word} v pádě {nazev_padu})",
                        "completion": form
                    }
                    f.write(json.dumps(fill_prompt, ensure_ascii=False) + "\n")

                # obecný zápis všech tvarů
                general = {
                    "prompt": f"jak skloňovat slovo {word} podle vzoru {vzor}",
                    "completion": "\n".join(forms[:7])
                }
                f.write(json.dumps(general, ensure_ascii=False) + "\n")


     

            time.sleep(2)

        except Exception as e:
            print(f"❌ Chyba při volání Gemmy: {e}")
            time.sleep(5)
            continue

    print(f"\n✅ Hotovo: výstup uložen do souboru {output_file}")






def create_data():    

    # 1. Mapování rodů pro vstupy
    gender_labels = {
        "ženský": "ženském roce",
        "střední": "středním rodě",
        "mužský_životný": "mužském životném rodě",
        "mužský_neživotný": "mužském neživotném rodě"
    }

    jsonl_lines = []

    # 1) Seznam vzorů podle rodu
    for gender, patterns in declension_patterns.items():
        label = gender_labels[gender]
        vzory = ", ".join(patterns.keys())
        prompt = f"Jaké jsou vzory podstatných jmen v {label}?"
        jsonl_lines.append({"prompt": prompt, "completion": vzory})

    # 2) Vzorová slova
    for gender, groups in vzorova_slova.items():
        for vzor, words in groups.items():
            prompt = f"Uveď 5 podstatných jmen podle vzoru '{vzor}'."
            completion = ", ".join(words)
            jsonl_lines.append({"prompt": prompt, "completion": completion})

    # 3) Všechny tvary slova
    for gender, patterns in declension_patterns.items():
        for slovo, tvary in patterns.items():
            prompt = f"Jaké jsou tvary slova '{slovo}'?"
            completion = ", ".join(tvary)
            jsonl_lines.append({"prompt": prompt, "completion": completion})

    # 4) Konkrétní pád
    for patterns in declension_patterns.values():
        for slovo, tvary in patterns.items():
            for idx, tvar in enumerate(tvary, start=1):
                prompt = f"{idx}. pád slova '{slovo}'"
                completion = tvar
                jsonl_lines.append({"prompt": prompt, "completion": completion})

    # Uložení do JSONL
    with open("train_prompts.jsonl", "w", encoding="utf-8") as f:
        for entry in jsonl_lines:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")    



# Spuštění výpisu
if __name__ == "__main__":
    create_data()
    create_gemini_prompts()
    print_declension_patterns()