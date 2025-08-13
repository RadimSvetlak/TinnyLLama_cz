# ------------------------------------------------------------
# Název: Generátor tréninkových otázek k větám s kontextem shrnutí odstavce
# Popis:
#   Tento skript zpracovává textové soubory (.txt) a pro každý odstavec:
#     1) Vygeneruje stručné shrnutí odstavce pomocí lokálního jazykového modelu.
#     2) Rozdělí odstavec na jednotlivé věty.
#     3) Pro každou větu vygeneruje s využitím modelu sadu jednoduchých otázek 
#        (kdo, co, kdy, kde, proč, jak, s kým, čím, kolik) s ohledem na shrnutí
#        odstavce, aby měly lepší kontext.
#   Výsledkem jsou páry prompt–completion, kde prompt je otázka a completion
#   je původní věta, vhodné pro trénink menších jazykových modelů.
#
# Vstupy:
#   - Textové soubory ve složce INPUT_DIR.
#   - Parametry pro model (MODEL_PATH, N_QUESTIONS, MAX_TOKENS).
#
# Výstupy:
#   - Soubor OUTPUT_PATH s řádky ve formátu:
#       prompt: <otázka>, completion: <původní věta>
#
# Klíčové funkce:
#   - safe_read_text: Načítání textu s fallback kódováním.
#   - split_into_paragraphs: Rozdělení textu na odstavce.
#   - split_into_sentences: Rozdělení odstavce na jednotlivé věty.
#   - make_summary_prompt: Vytvoření promptu pro shrnutí odstavce.
#   - make_sentence_prompt_with_context: Vytvoření promptu pro otázky 
#        k větě s kontextem shrnutí.
#   - summarize_paragraph: Volání modelu pro získání shrnutí odstavce.
#   - try_parse_questions: Bezpečné parsování JSON výstupu otázek z modelu.
#   - sanitize_for_line: Očištění řetězce pro zápis na jeden řádek.
#
# Závislosti:
#   - Python 3.8+
#   - llama-cpp-python
#   - Standardní knihovny: os, re, json
#
# ------------------------------------------------------------


import os
import re
from typing import List, Optional
from llama_cpp import Llama
import json

# ====== Nastavení ======
MODEL_PATH = r"D:\AI\gemma_test\google_gemma-3-4b-it-qat-Q8_0.gguf"
INPUT_DIR = "./"
OUTPUT_PATH = "train_prompts.txt"
N_QUESTIONS = 3                   # přesně 3 otázky na větu
MAX_TOKENS = 512                  # krátké výstupy (shrnutí / otázky)
MIN_SENT_LEN = 12                 # minimální délka věty (znaky), jinak skip
VERBOSE = True

# ====== Inicializace modelu ======
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=8192,
    n_threads=8,
    n_gpu_layers=-1,
    verbose=False,
    temperature=0.7,
    top_k=50,
    top_p=0.9,
    repeat_penalty=1.05,
)

# ====== Načítání s fallback kódováním ======
def safe_read_text(path: str) -> str:
    for enc in ("utf-8", "windows-1250", "iso-8859-2"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    print(f"⚠ Nelze načíst soubor kvůli kódování: {path}")
    return ""

# ====== Dělení na odstavce ======
def split_into_paragraphs(text: str) -> List[str]:
    # Primárně děl na prázdné řádky; odstraň extrémně krátké/whitespace bloky
    parts = re.split(r"(?:\r?\n){2,}", text.strip())
    paras = ["\n".join(p.strip().splitlines()) for p in parts if p and p.strip()]
    # Pokud není žádný nebo jen jeden odstavec, nechej text tak jak je
    return paras if paras else [text.strip()]

# ====== Heuristické dělení na věty (bez NLTK/SciPy) ======
ABBREV = {
    "např", "atd", "apod", "tj", "tzn", "tzv", "mj", "aj", "ap",
    "ing", "mgr", "phdr", "phd", "bc", "bcaa", "bca", "bcs", "dr",
    "p", "str", "sv", "č", "ul", "tř", "nám", "r", "čj", "čís", "př",
}

def split_into_sentences(text: str) -> List[str]:
    t = re.sub(r"[ \t]+", " ", text.replace("\r", " "))
    t = re.sub(r"\n+", " ", t).strip()

    sentences = []
    buf = []
    i = 0
    L = len(t)

    while i < L:
        ch = t[i]
        buf.append(ch)

        if ch in ".!?":
            prev_chunk = "".join(buf).rstrip()
            m = re.search(r"([\wÁČĎÉĚÍŇÓŘŠŤÚŮÝŽáčďéěíňóřšťúůýž]+)\.$", prev_chunk)
            prev_word = m.group(1).lower() if m else ""

            j = i + 1
            while j < L and t[j] in ['"', "”", "“", "»", "«", "’", "'", " "]:
                j += 1

            is_abbrev = prev_word in ABBREV
            next_cap = j < L and (t[j].isupper() or t[j].isdigit())

            if not is_abbrev and next_cap:
                sentence = "".join(buf).strip()
                if len(sentence) >= MIN_SENT_LEN:
                    sentences.append(sentence)
                buf = []
        i += 1

    tail = "".join(buf).strip()
    if len(tail) >= MIN_SENT_LEN:
        sentences.append(tail)

    sentences = [" ".join(s.split()) for s in sentences]
    return sentences

# ====== Prompty ======
def make_summary_prompt(paragraph: str) -> str:
    compact = " ".join(paragraph.split())
    return (
        "<bos><start_of_turn>user\n"
        "Shrň následující odstavec do 1–2 velmi krátkých vět v češtině.\n"
        "- Použij jen klíčové události a subjekty.\n"
        "- Bez odrážek, bez formátování, bez závorek.\n"
        "<end_of_turn>\n"
        "<start_of_turn>user\n"
        f"Odstavec:\n{compact}\n"
        "<end_of_turn>\n"
        "<start_of_turn>model\n"
    )

def make_sentence_prompt_with_context(sentence: str, summary: str, n_questions: int = 3) -> str:
    return (
        "<bos><start_of_turn>user\n"
        "Vygeneruj jednoduché otázky v češtině k jedné větě, s ohledem na shrnutí odstavce.\n"
        "Cíl: pomoci malému modelu učit se českou větnou stavbu.\n"
        f"- Vytvoř přesně {n_questions} krátkých otázek (A1–A2) typu kdo, co, kdy, kde, proč, jak, s kým, čím, kolik.\n"
        "- Nepoužívej externí znalosti, vyhni se otázkám ano/ne.\n"
        "Výstup: JSON pole objektů {{\"question\":\"...\"}} bez dalších textů.\n"
        "<end_of_turn>\n"
        "<start_of_turn>user\n"
        f"Shrnutí odstavce:\n{summary}\n\n"
        f"Věta:\n{sentence}\n"
        "<end_of_turn>\n"
        "<start_of_turn>model\n"
    )

# ====== Parsování JSON výstupu (jen otázky) ======
def try_parse_questions(s: str) -> Optional[list]:
    s = s.strip()
    start = s.find("[")
    end = s.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            data = json.loads(s[start:end+1])
            if isinstance(data, list):
                qs = []
                for i in data:
                    if isinstance(i, dict) and "question" in i:
                        q = str(i["question"]).strip()
                        if q:
                            qs.append(q)
                return qs if qs else None
        except Exception:
            return None
    return None

# ====== Util: sanitizace pro formát řádku (zachovej diakritiku, odstraň čárky) ======
def sanitize_for_line(s: str) -> str:
    s = s.replace(",", " ")
    s = " ".join(s.split())
    return s

def summarize_paragraph(paragraph: str) -> Optional[str]:
    prompt = make_summary_prompt(paragraph)
    try:
        resp = llm(prompt, max_tokens=128)
        summary = resp["choices"][0]["text"].strip()
        # lehká očista
        summary = " ".join(summary.split())
        return summary if summary else None
    except Exception as e:
        print(f"⚠ Chyba při shrnutí odstavce: {e}")
        return None

# ====== Hlavní běh ======
def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".txt")]
    total_files = len(files)
    total_pairs = 0

    with open(OUTPUT_PATH, "a", encoding="utf-8") as out_f:
        for file_index, filename in enumerate(files, start=1):
            if VERBOSE:
                print(f"📂 soubor {file_index}/{total_files}: {filename}")
            try:
                raw_text = safe_read_text(os.path.join(INPUT_DIR, filename))
            except Exception as e:
                print(f"⚠ Nelze číst {filename}: {e}")
                continue

            if not raw_text.strip():
                continue

            paragraphs = split_into_paragraphs(raw_text)
            if VERBOSE:
                print(f"   ➜ nalezeno odstavců: {len(paragraphs)}")

            for pi, para in enumerate(paragraphs, start=1):
                if len(para.strip()) < MIN_SENT_LEN:
                    continue

                # 1) Shrnutí odstavce
                summary = summarize_paragraph(para)
                if not summary:
                    # Fallback: vezmi prvních ~200 znaků odstavce jako "pseudo-shrnuti"
                    summary = " ".join(para.split())[:200]

                # 2) Rozdělit odstavec na věty
                sentences = split_into_sentences(para)
                if VERBOSE:
                    print(f"      - odstavec {pi}: věty = {len(sentences)}")

                # 3) Pro každou větu generovat otázky s kontextem shrnutí
                for si, sentence in enumerate(sentences, start=1):
                    if len(sentence) < MIN_SENT_LEN:
                        continue

                    prompt = make_sentence_prompt_with_context(sentence, summary, N_QUESTIONS)
                    try:
                        resp = llm(prompt, max_tokens=MAX_TOKENS)
                        raw = resp["choices"][0]["text"]
                    except Exception as e:
                        print(f"⚠ Chyba volání modelu u věty {si} (odstavec {pi}): {e}")
                        continue

                    questions = try_parse_questions(raw)
                    if not questions:
                        # Fallback: zkuste snížit teplotu
                        try:
                            resp2 = llm(prompt, max_tokens=MAX_TOKENS, temperature=0.3)
                            raw2 = resp2["choices"][0]["text"]
                            questions = try_parse_questions(raw2)
                        except Exception:
                            questions = None

                    if not questions:
                        continue

                    sent_clean = sanitize_for_line(sentence)
                    for q in questions:
                        q_clean = sanitize_for_line(q)
                        out_f.write(f"prompt: {q_clean}, completion: {sent_clean}\n")
                        out_f.flush()
                        total_pairs += 1

    print(f"✔ Hotovo, uloženo {total_pairs} párů do {OUTPUT_PATH}")

if __name__ == "__main__":
    main()