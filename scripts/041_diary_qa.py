# -*- coding: utf-8 -*-
# ------------------------------------------------------------
import os
import re
import json
from typing import List, Tuple, Optional
from llama_cpp import Llama

# ====== Nastavení ======
INPUT_FILE = "denik_pralinky_20_23.txt"
OUTPUT_FILE = "train_pairs.txt"

# Cesty k modelu – zadej větší model (Gemma3/OSS 20B) v GGUF
# MODEL_PATH = r"D:\AI\_models\gpt-oss-20b-mxfp4.gguf"  # uprav dle sebe
# MODEL_PATH = r"D:\AI\_models\gemma-3n\gemma-4.5B-3n-F16.gguf"  # uprav dle sebe
MODEL_PATH = r"D:\AI\gemma_3_12B\gemma-3-12b-it-q4_0.gguf"
N_THREADS = 24
N_GPU_LAYERS = 48
CTX_LEN = 8192

# Generování
MAX_TOKENS = 512
TEMPERATURE = 0.7
TOP_K = 50
TOP_P = 0.9
REPEAT_PENALTY = 1.05

# Parsing / chunking
MAX_CHARS_PER_BLOCK = 2500   # požadavek: pokud odstavec > 2500 znaků → dělit
OVERLAP_CHARS = 500          # požadavek: překryv 500 znaků
MIN_SENT_LEN_CHARS = 12
SANITIZE_COMMAS = True       # nahradí "," za " " ve výstupech (jednoduchá CSV-like linka)
VERBOSE = True

# Debug výpisy
DEBUG = True                 # přepni na False pro vypnutí detailních výpisů
DEBUG_MAX_CHARS = None       # např. 2000 pro zkrácení dlouhých výpisů; None = celé

# Kolik generovat
N_QA_QUESTIONS = 5           # požadavek: přesně 5 otázek
N_COMP_QA = 4                # porozuměcí otázky s odpovědí
N_YESNO_POS = 3              # kolik ANO výroků
N_YESNO_NEG = 3              # kolik NE výroků
INCLUDE_SUMMARY = True
INCLUDE_CLOZE = False        # volitelné (aktuálně nepoužito)

# ====== Kontext deníku (stálý rámec) ======
BASE_CONTEXT = (
    "Toto je osobní deník psaný z pohledu majitele koně Radima. "
    "Deník popisuje kobylku jménem Pralinka, ustájenou v Dobroníně poblíž Jihlavy. "
    "Vystupují také koně Kaly, Ladoňka a Amálka a osoby panička a Kuba."
)

# ====== Inicializace modelu ======
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=CTX_LEN,
    n_threads=N_THREADS,
    n_gpu_layers=-1,
    verbose=True,
    temperature=TEMPERATURE,
    top_k=TOP_K,
    top_p=TOP_P,
    repeat_penalty=REPEAT_PENALTY,
    
)

# ====== Utility ======
def safe_read_text(path: str) -> str:
    for enc in ("utf-8", "windows-1250", "iso-8859-2"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    print(f"⚠ Nelze načíst soubor kvůli kódování: {path}")
    return ""

def sanitize(s: str) -> str:
    s = s.replace("\r", " ").replace("\n", " ")
    s = " ".join(s.split())
    if SANITIZE_COMMAS:
        s = s.replace(",", " ")
    return s

def ensure_parent_dir(path: str) -> None:
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def write_pair(out_path: str, prompt_text: str, completion_text: str) -> None:
    """Okamžitý, odolný zápis (append + flush + fsync) a krátký debug log."""
    ensure_parent_dir(out_path)
    p = sanitize(prompt_text)
    c = sanitize(completion_text)
    line = f"\"prompt\": \"{p}\", \"completion\": \"{c}\"\n"
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(line)
        f.flush()
        os.fsync(f.fileno())
    if DEBUG:
        print(f"📝 WRITE → prompt[{len(p)}], completion[{len(c)}]")

def debug_print(title: str, text: str, max_chars: Optional[int] = DEBUG_MAX_CHARS) -> None:
    if not DEBUG:
        return
    try:
        if max_chars is not None and len(text) > max_chars:
            shown = text[:max_chars] + f"\n... [truncated {len(text)-max_chars} chars]"
        else:
            shown = text
    except Exception:
        shown = str(text)
    print(f"\n===== {title} (len={len(text) if isinstance(text, str) else 'n/a'}) =====")
    print(shown)
    print(f"===== END {title} =====\n")

# ====== Parsování a chunkování ======
def split_paragraphs_by_dated_header(text: str) -> List[str]:
    """
    Rozparsuje text do bloků. Nový blok začíná na řádku:
      ^\s*\d{1,2}\.\s+
    (např. '3. ...'). Zachová první řádek v bloku.
    Ignoruje systémové hlavičky začínající na ---.
    """
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("---")]
    joined = "\n".join(lines).strip()
    if not joined:
        return []
    parts = re.split(r"(?m)^(?=\s*\d{1,2}\.\s+)", joined)
    paras = [p.strip() for p in parts if p.strip()]
    return paras

def chunk_by_chars_with_overlap(paragraph: str, max_chars: int, overlap: int) -> List[str]:
    """Dělí odstavec po znacích s překryvem 'overlap' (požadavky 2500/500)."""
    text = paragraph.strip()
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == n:
            break
        start = end - overlap if end - overlap > start else end
    return chunks

# ====== Volání LLM (Gemma‑3 turn formát) ======
def call_llm(prompt: str,
             max_tokens: int = MAX_TOKENS,
             temperature: Optional[float] = None,
             label: Optional[str] = None) -> str:
    """
    Zabalení promptu do formátu pro Gemma‑3 Instruct modely.
    """
    wrapped_prompt = (
        f"<start_of_turn>user\n{prompt.strip()}\n<end_of_turn>\n"
        f"<start_of_turn>model\n"
    )

    if label:
        debug_print(f"LLM PROMPT [{label}]", wrapped_prompt)
    else:
        debug_print("LLM PROMPT", wrapped_prompt)

    kwargs = {}
    if temperature is not None:
        kwargs["temperature"] = temperature

    resp = llm(
        wrapped_prompt,
        max_tokens=max_tokens,
        **kwargs
    )
    text = resp["choices"][0]["text"].strip()

    if label:
        debug_print(f"LLM RESPONSE [{label}]", text)
    else:
        debug_print("LLM RESPONSE", text)

    return text

# ====== Prompty a parsování ======
def prompt_summary(block: str) -> str:
    compact = " ".join(block.split())
    return (
        f"{BASE_CONTEXT}\n"
        "Odpovídej česky.\n"
        "Úkol: Shrň následující český text do 1–2 velmi krátkých vět.\n"
        "- Použij jen klíčové události a subjekty.\n"
        "- Bez odrážek, bez formátování, stručně.\n\n"
        f"Text:\n{compact}\n\n"
        "Odpověď:"
    )

def prompt_questions_with_summary(block: str, summary: str, n: int) -> str:
    txt = " ".join(block.split())
    sm = " ".join(summary.split())
    return (
        f"{BASE_CONTEXT}\n"
        "Odpovídej česky.\n"
        f"Úkol: Na základě původního českého textu a jeho shrnutí vytvoř přesně {n} jednoduchých, srozumitelných otázek.\n"
        "- Každá otázka musí být jednoznačně zodpověditelná pouze z textu.\n"
        "- Nepoužívej otázky ano/ne.\n"
        "- Jedna krátká věta, bez číslování a bez dodatečných vysvětlivek.\n"
        "- Vyhýbej se zájmenům typu 'to', 'tamto'; ptej se konkrétně (kdo, co, kdy, kde, proč, jak, kolik...).\n"
        "- Vrať pouze čisté JSON pole řetězců (bez jakéhokoli dalšího textu).\n\n"
        f"Text:\n{txt}\n\n"
        f"Shrnutí:\n{sm}\n\n"
        "JSON:"
    )

def prompt_comp_qa(block: str, n: int) -> str:
    txt = " ".join(block.split())
    return (
        f"{BASE_CONTEXT}\n"
        "Odpovídej česky.\n"
        f"Úkol: Vytvoř {n} krátkých porozuměcích otázek k českému textu a zároveň uveď správnou krátkou odpověď.\n"
        "- Zaměř se na: o čem se píše, kdo/co/kde/kdy/proč/jak, a 'kolik' apod.\n"
        "- Odpovědi musí být explicitně v textu. Nepřidávej informace z vnějších zdrojů.\n"
        "- Otázka i odpověď musí být stručné a přesné (max. ~10 slov).\n"
        "- Formát: JSON pole objektů {\"question\": \"...\", \"answer\": \"...\"}.\n"
        "- Vrať pouze validní JSON, nic navíc.\n\n"
        f"Text:\n{txt}\n\n"
        "JSON:"
    )

def prompt_yesno(block: str, n_pos: int, n_neg: int) -> str:
    txt = " ".join(block.split())
    return (
        f"{BASE_CONTEXT}\n"
        "Odpovídej česky.\n"
        f"Úkol: Na základě textu vytvoř {n_pos} výroků, které text výslovně POTVRZUJE (label = \"ano\"), "
        f"a {n_neg} výroků, které text NEUVÁDÍ (label = \"ne\").\n"
        "- Výroky musí být krátké a konkrétní.\n"
        "- Pro 'ano' vybírej tvrzení, která jsou v textu explicitně uvedena (ne domněnky).\n"
        "- Pro 'ne' vytvoř tvrzení, která se v textu nevyskytují a nejsou z něj odvoditelná.\n"
        "- Formát: JSON pole objektů {\"claim\": \"...\", \"label\": \"ano\"|\"ne\"}.\n"
        "- Vrať pouze validní JSON, nic navíc.\n\n"
        f"Text:\n{txt}\n\n"
        "JSON:"
    )

def prompt_answer_question(question: str, block: str) -> str:
    """Instruktivní QA prompt pro získání stručné odpovědi k jedné otázce."""
    q = question.strip()
    txt = " ".join(block.split())
    return (
        f"{BASE_CONTEXT}\n"
        "Odpovídej česky.\n"
        "Úkol: Odpověz co nejstručněji a přesně na otázku pouze na základě textu.\n"
        "- Odpověď jednej krátkou frází (ideálně do 5–10 slov), bez dovysvětlování.\n\n"
        f"Otázka: {q}\n"
        f"Text:\n{txt}\n\n"
        "Odpověď:"
    )

def try_parse_json_list_of_strings(s: str) -> Optional[List[str]]:
    s = s.strip()
    start = s.find("["); end = s.rfind("]")
    if start == -1 or end == -1 or end <= start:
        if DEBUG: print("🧩 PARSE questions: nenalezeno pole []")
        return None
    try:
        data = json.loads(s[start:end+1])
        if isinstance(data, list) and all(isinstance(i, str) and i.strip() for i in data):
            if DEBUG: print(f"🧩 PARSE questions: OK (n={len(data)})")
            return [i.strip() for i in data]
    except Exception as e:
        if DEBUG: print(f"🧩 PARSE questions: ERROR {e}")
        return None
    if DEBUG: print("🧩 PARSE questions: nevalidní obsah")
    return None

def try_parse_json_qa_objects(s: str) -> Optional[List[Tuple[str, str]]]:
    s = s.strip()
    start = s.find("["); end = s.rfind("]")
    if start == -1 or end == -1 or end <= start:
        if DEBUG: print("🧩 PARSE comp_qa: nenalezeno pole []")
        return None
    try:
        data = json.loads(s[start:end+1])
        out = []
        if isinstance(data, list):
            for obj in data:
                if isinstance(obj, dict) and "question" in obj and "answer" in obj:
                    q = str(obj["question"]).strip()
                    a = str(obj["answer"]).strip()
                    if q and a:
                        out.append((q, a))
        if out:
            if DEBUG: print(f"🧩 PARSE comp_qa: OK (n={len(out)})")
            return out
        if DEBUG: print("🧩 PARSE comp_qa: prázdné nebo nevalidní")
        return None
    except Exception as e:
        if DEBUG: print(f"🧩 PARSE comp_qa: ERROR {e}")
        return None

def try_parse_yesno_objects(s: str) -> Optional[List[Tuple[str, str]]]:
    s = s.strip()
    start = s.find("["); end = s.rfind("]")
    if start == -1 or end == -1 or end <= start:
        if DEBUG: print("🧩 PARSE yesno: nenalezeno pole []")
        return None
    try:
        data = json.loads(s[start:end+1])
        out = []
        if isinstance(data, list):
            for obj in data:
                if isinstance(obj, dict) and "claim" in obj and "label" in obj:
                    claim = str(obj["claim"]).strip()
                    label = str(obj["label"]).strip().lower()
                    if claim and label in {"ano", "ne"}:
                        out.append((claim, label))
        if out:
            if DEBUG: print(f"🧩 PARSE yesno: OK (n={len(out)})")
            return out
        if DEBUG: print("🧩 PARSE yesno: prázdné nebo nevalidní")
        return None
    except Exception as e:
        if DEBUG: print(f"🧩 PARSE yesno: ERROR {e}")
        return None

# ====== Pomocné formátování promptů pro dataset ======
def to_qa_prompt(question: str, text: str) -> str:
    """
    Datasetový prompt: otázka + text + jasná instrukce "odpověz co nejstručněji".
    """
    q = question.strip()
    if q.endswith("?"):
        q = q[:-1].strip()
    return f"Odpověz co nejstručněji na otázku. Otázka: {q}. Text: {text}"

def yesno_dataset_prompt(claim: str, text: str) -> str:
    """
    Datasetový prompt pro binární ověření výroku.
    """
    claim_s = claim.replace('"', "'").strip()
    return f'Odpověz pouze "ano" nebo "ne". Psalo se v textu: "{claim_s}"? Text: {text}'

# ====== QA odpověď (interní inference) ======
def answer_question_with_llm(block: str, question: str) -> str:
    a_prompt = prompt_answer_question(question, block)
    ans = call_llm(a_prompt, max_tokens=64, temperature=0.2, label="ANSWER_QA")
    if not ans.strip():
        ans = call_llm(a_prompt, max_tokens=64, temperature=0.0, label="ANSWER_QA retry")
    return ans.strip()

# ====== Deduplikace párů ======
def dedup_pairs(pairs: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    seen = set()
    out: List[Tuple[str, str]] = []
    for p, c in pairs:
        key = (p, c)
        if key in seen:
            continue
        seen.add(key)
        out.append((p, c))
    return out

# ====== Hlavní generace pro 1 blok ======
def generate_pairs_for_block(block: str) -> List[Tuple[str, str]]:
    pairs: List[Tuple[str, str]] = []

    # 1) Shrnutí
    summary = ""
    if INCLUDE_SUMMARY:
        s_prompt = prompt_summary(block)
        summary = call_llm(s_prompt, max_tokens=128, temperature=0.6, label="SUMMARY")
        if not summary.strip():
            summary = call_llm(s_prompt, max_tokens=128, temperature=0.2, label="SUMMARY retry")

    # 2) Otázky → pro každou vyžádej stručnou odpověď a vytvoř QA pár
    q_prompt = prompt_questions_with_summary(block, summary, N_QA_QUESTIONS)
    raw_q = call_llm(q_prompt, max_tokens=256, temperature=0.7, label="QUESTIONS")
    questions = try_parse_json_list_of_strings(raw_q)
    if not questions:
        raw_q = call_llm(q_prompt, max_tokens=256, temperature=0.2, label="QUESTIONS retry")
        questions = try_parse_json_list_of_strings(raw_q)
    if questions:
        for q in questions:
            answer = answer_question_with_llm(block, q)
            if answer:
                pairs.append((to_qa_prompt(q, block), answer))

    # 3) Shrnutí jako pár
    if INCLUDE_SUMMARY and summary.strip():
        pairs.append((f"shrn tento text: {block}", summary))

    # 4) Porozuměcí otázky s odpověďmi (další QA páry)
    comp_prompt = prompt_comp_qa(block, N_COMP_QA)
    raw_comp = call_llm(comp_prompt, max_tokens=256, temperature=0.6, label="COMP_QA")
    comp_qa = try_parse_json_qa_objects(raw_comp)
    if not comp_qa:
        raw_comp = call_llm(comp_prompt, max_tokens=256, temperature=0.2, label="COMP_QA retry")
        comp_qa = try_parse_json_qa_objects(raw_comp)
    if comp_qa:
        for q, a in comp_qa:
            pairs.append((to_qa_prompt(q, block), a))

    # 5) Ano/Ne výroky → dataset prompt + čisté "ano"/"ne"
    yn_prompt = prompt_yesno(block, N_YESNO_POS, N_YESNO_NEG)
    raw_yn = call_llm(yn_prompt, max_tokens=256, temperature=0.6, label="YESNO")
    yesno = try_parse_yesno_objects(raw_yn)
    if not yesno:
        raw_yn = call_llm(yn_prompt, max_tokens=256, temperature=0.2, label="YESNO retry")
        yesno = try_parse_yesno_objects(raw_yn)
    if yesno:
        for claim, label in yesno:
            p = yesno_dataset_prompt(claim, block)
            c = "ano" if label == "ano" else "ne"
            pairs.append((p, c))

    pairs = dedup_pairs(pairs)

    if DEBUG:
        print(f"✅ BLOCK pairs generated: {len(pairs)}")
    return pairs

# ====== Běh skriptu ======
def main():
    if VERBOSE:
        print(f"📂 Čtu: {INPUT_FILE}")
    text = safe_read_text(INPUT_FILE)
    if not text.strip():
        print("⚠ Soubor prázdný nebo nečitelný.")
        return

    paragraphs = split_paragraphs_by_dated_header(text)
    if VERBOSE:
        print(f"   ➜ nalezeno odstavců: {len(paragraphs)}")

    # Příprava výstupního souboru (přepíšeme a budeme appendovat okamžitě)
    ensure_parent_dir(OUTPUT_FILE)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("")

    total_pairs = 0
    for i, para in enumerate(paragraphs, start=1):
        head = sanitize(para.split("\n", 1)[0])[:80]
        if VERBOSE:
            print(f"\n------ odstavec {i}: {head} ------")

        # Chunkování po znacích s překryvem
        blocks = chunk_by_chars_with_overlap(para, MAX_CHARS_PER_BLOCK, OVERLAP_CHARS)
        if VERBOSE:
            print(f"   · bloků po chunkování: {len(blocks)}")

        for bi, block in enumerate(blocks, start=1):
            if VERBOSE:
                print(f"\n   ▶ blok {bi}: len={len(block)}")

            pairs: List[Tuple[str, str]] = []
            try:
                pairs = generate_pairs_for_block(block)
            except Exception as e:
                print(f"⚠ Chyba při generování pro odstavec {i}, blok {bi}: {e}")

            for prompt_text, completion_text in pairs:
                write_pair(OUTPUT_FILE, prompt_text, completion_text)
                total_pairs += 1

            if VERBOSE:
                print(f"   ▷ vygenerováno párů = {len(pairs)}")

    print(f"\n✔ Hotovo, uloženo {total_pairs} párů do {OUTPUT_FILE}")

if __name__ == "__main__":
    main()