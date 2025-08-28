import json
import re
import random
import time
from llama_cpp import Llama

# ==== Model & soubory ====
MODEL_PATH = r"D:\AI\_models\gemma-3n-E2B-it-Q8_0.gguf"
N_CTX = 2048
MAX_TOKENS = 256
TEMPERATURE = 0.2

VSTUP_CSV = "venda.txt"
VYSTUP_JSONL = "train_pairs.jsonl"
MAX_WORDS = 128  ### maximální počet slov pro jeden vstup

# ==== Inicializace modelu ====
llm = Llama(model_path=MODEL_PATH, n_ctx=N_CTX, n_threads=16, n_gpu_layers=-1, verbose=False)

def call_model(prompt: str) -> str:
    context_info = (
        "Textové údaje pro úkoly pocházejí z deníku koně Venouška, jeho kamarádů koní "       
        "Venda píše o sobě, v první osobě s trochu aristokratickým, lehce ironickým tonem. Je to starý klidný koník.\n"
        "Příklady správné češtiny: 'koně chodili', 'Venda byl'.  'Kuba, Kubou', 'Venda, Vendovi', 'Pralinka, Pralinky'"
        "Používej správné tvary sloves na správném místě: 'děti se starají o koně' \n\n"
    
    )
    chat_prompt = (
        "<start_of_turn>user\n"
        f"Toto je kontext pro následující data: '{context_info}'\n"
        "<end_of_turn>\n"
        "<start_of_turn>model\n"
        "beru na vědomí a budu postupovat podle instrukcí. Budu odpovédat stručně a podle instrukcí."
        "<end_of_turn>\n"
        "<start_of_turn>user\n"
        f"Tvůj úkol: {prompt}\n"
        "<end_of_turn>\n"
        "<start_of_turn>model\n"
        
    )
    time.sleep(0.1)
    out = llm(chat_prompt, max_tokens=MAX_TOKENS, temperature=TEMPERATURE, echo=False)
    return out["choices"][0]["text"].strip()

 

# ==== Pomocné funkce ====
def clean_line(text: str) -> str:
    text = text.replace('"', '')
    text = re.sub(r',+', ',', text)
    return text.strip()

def split_long_line(text: str, max_words: int = MAX_WORDS):
    words = text.split()
    if len(words) <= max_words:
        return [text]
    mid = len(words) // 2
    return [" ".join(words[:mid]), " ".join(words[mid:])]

# ==== Úkolové funkce ====

def createQAPairs(src_line: str, count: int = 1):
    pairs = []
    for _ in range(count):
        prompt_q = f"Vytvoř otázku k tomuto textu, zaměř se na místo nebo čas konání: '{src_line}'. Napiš pouze otázku, nic jiného."
        question = call_model(prompt_q)
        pairs.append({"prompt": prompt_q, "completion": question})

        prompt_a = f"vyhledej a napiš odpověď na otázku '{question}'\n Hledej v tomto textu '{src_line}'"
        answer = call_model(prompt_a)
        pairs.append({"prompt": prompt_a, "completion": answer})
    return pairs
    
def createQAPersonPairs(src_line: str, count: int = 1):
    pairs = []
    for _ in range(count):
        prompt_q = f"Vytvoř otázku, kde se zeptáš o kom nebo o čem se píše v textu: '{src_line}'. Napiš pouze otázku, nic jiného."
        question = call_model(prompt_q)
        pairs.append({"prompt": prompt_q, "completion": question})

        prompt_a = f"vyhledej a napiš odpověď na otázku '{question}'\n Hledej v tomto textu '{src_line}'"
        answer = call_model(prompt_a)
        pairs.append({"prompt": prompt_a, "completion": answer})
    return pairs
    

def createSummaryTripleClozePairs(src_line: str, count: int = 1):
    pairs = []
    exclude_names = {"Pralinka", "Venda", "Míša", "Kaly", "Ladoňka", "Radimi", "Kuba"}
    for _ in range(count):
        summary_clean = src_line.strip(" .,")

        words = [w for w in re.findall(r"\b\w+\b", summary_clean)
                 if len(w) > 2 and w not in exclude_names]
        if len(words) < 3:
            continue

        chosen = random.sample(words, 3)
        cloze_sentence = summary_clean
        for w in chosen:
            cloze_sentence = re.sub(rf"\b{re.escape(w)}\b", "(___)", cloze_sentence, count=1)

        pairs.append({
            "prompt": f"Vytvoř větu s chybějícími slovy (___): '{summary_clean}'",
            "completion": cloze_sentence
        })
        pairs.append({
            "prompt": f"Doplň chybějící slova '(___)': '{cloze_sentence}'. "
                      f"Vycházej z tohoto textu: '{src_line}'. ",
            "completion": ", ".join(chosen)
        })
    return pairs

def createYesPairs(src_line: str, count: int = 1):
    pairs = []
    for _ in range(count):
        prompt_q = f"Najdi v textu informaci, která je pravdivá a vytvoř otázku na kterou lze odpovědět 'ano'. Text: {src_line}"
        question = call_model(prompt_q)
        pairs.append({"prompt": prompt_q, "completion": question})

        prompt_a = f"Odpověz 'ano' na otázku '{question}' s ohledem na tento text: '{src_line}'"
        # answer = call_model(prompt_a)
        pairs.append({"prompt": prompt_a, "completion": "ano"})
    return pairs

def createNoPairs(src_line: str, count: int = 1):
    pairs = []
    for _ in range(count):
        prompt_q = f"Vyvoř otázku na informaci, která se v textu nevyskytuje. Zeptej se stylem: 'je v textu toto ...?' odpověď bude 'ne'. Text: {src_line}"
        question = call_model(prompt_q)
        pairs.append({"prompt": prompt_q, "completion": question})

        prompt_a = f"Odpověz 'ne' na otázku '{question}' s ohledem na tento text: {src_line}"
        # answer = call_model(prompt_a)
        pairs.append({"prompt": prompt_a, "completion": "ne"})
    return pairs

# ==== Nové úkolové funkce ====

def createSynonymPairs(src_line: str, count: int = 1):
    pairs = []
    for _ in range(count):
        prompt_s = f"Najdi v tomto textu jedno slovo a napiš jeho synonymum vhodné do tohoto kontextu: '{src_line}'"
        synonym = call_model(prompt_s)
        pairs.append({"prompt": prompt_s, "completion": synonym})
    return pairs

def createAntonymPairs(src_line: str, count: int = 1):
    pairs = []
    for _ in range(count):
        prompt_a = f"Najdi v tomto textu jedno slovo a napiš jeho antonymum (opačný význam) vhodné do tohoto kontextu: '{src_line}'"
        antonym = call_model(prompt_a)
        pairs.append({"prompt": prompt_a, "completion": antonym})
    return pairs

def createCategoryPairs(src_line: str, count: int = 1):
    pairs = []
    for _ in range(count):
        prompt_c = f"Urči, do které kategorie patří tento text (např. ježdění, krmení, úklid stáje, zdraví koní, volný čas): '{src_line}'"
        category = call_model(prompt_c)
        pairs.append({"prompt": prompt_c, "completion": category})
    return pairs

def createEmotionPairs(src_line: str, count: int = 1):
    pairs = []
    for _ in range(count):
        prompt_e = f"Urči hlavní emoci v tomto textu (radost, smutek, hněv, strach, překvapení): '{src_line}'"
        emotion = call_model(prompt_e)
        pairs.append({"prompt": prompt_e, "completion": emotion})
    return pairs

# ==== Hlavní běh ====
with open(VYSTUP_JSONL, "w", encoding="utf-8") as f_out:
    with open(VSTUP_CSV, "r", encoding="utf-8") as l:
        line_count = sum(1 for _ in l)
        l.seek(0)  # vrátit čtecí pozici na začátek

        for i, actline in enumerate(l, start=1):
            actline = clean_line(actline)
            if not actline:
                continue

            print(f"\n[{i}/{line_count}] 📄 Původní řádek: {actline}")

            # 1) podrobné shrnutí
            sum_prompt = f"Vytvoř podrobné shrnutí tohoto textu. Odpovídej *vždy v první osobě*, autor textu píše o sobě: '{actline}'"
            #summary = call_model(sum_prompt).strip()
            summary = actline
            word_count = len(summary.split())
            print(f"    📝 Shrnutí ({word_count} slov): {summary}")

            summaries_to_process = []

            # 2) kontrola délky a případné dělení + nové shrnutí pro každou polovinu
            if word_count > MAX_WORDS:
                print(f"    ✂ Shrnutí > {MAX_WORDS} slov, rozděluji na poloviny a shrnuji znovu…")
                half_words = summary.split()
                mid = len(half_words) // 2
                for part_idx, part in enumerate(
                        [" ".join(half_words[:mid]), " ".join(half_words[mid:])], start=1):
                    sub_sum_prompt = f"Vytvoř podrobné shrnutí tohoto textu v jedné větě: '{part}'"
                    sub_summary = call_model(sub_sum_prompt).strip()
                    print(f"      ➡ Podshrnutí {part_idx} ({len(sub_summary.split())} slov): {sub_summary}")
                    summaries_to_process.append(sub_summary)
            else:
                summaries_to_process.append(summary)

            # 3) spouštění úkolů pro aktuální (pod)shrnutí
            for seg_idx, seg_summary in enumerate(summaries_to_process, start=1):
                print(f"\n=== Segment {seg_idx}/{len(summaries_to_process)} shrnutí řádku {i} ===")
                tasks = [
                    ("QA", createQAPairs, 1),
                    ("QA", createQAPersonPairs, 1),                    
                    ("Summary+TripleCloze", createSummaryTripleClozePairs, 1),
                    ("Yes", createYesPairs, 1),
                    ("No", createNoPairs, 1),
                    ("Synonym", createSynonymPairs, 1),
                    ("Antonym", createAntonymPairs, 1),
                    ("Category", createCategoryPairs, 1),
                    ("Emotion", createEmotionPairs, 1),
                ]
                for j, (task_name, func, count) in enumerate(tasks, start=1):
                    print(f"  → Úkol {j}/{len(tasks)}: {task_name} (opakování {count}×)")
                    pairs = func(seg_summary, count=count)

                    # 4) okamžité uložení výsledků po každém úkolu
                    for pair in pairs:
                        f_out.write(json.dumps(pair, ensure_ascii=False) + "\n")
                    f_out.flush()
                    print(f"    ✓ Uloženo {len(pairs)} párů do {VYSTUP_JSONL}")
                time.sleep(2)
print(f"\n✅ Hotovo – výstup v souboru: {VYSTUP_JSONL}")

if __name__ == "__main__":
    main()