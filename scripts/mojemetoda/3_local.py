#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fast_dataset_generator.py
- Optimalizováno pro slabší PC
- Anglické instrukce pro model, české prompty do trénovacích dat
- Průběžné ukládání, minimální overhead
"""

import os, sys, json, time, random, re
from pathlib import Path
from typing import List, Optional, Dict

try:
    from llama_cpp import Llama
except Exception as e:
    print("❌ Chybí llama-cpp-python", file=sys.stderr)
    sys.exit(1)

# ======= KONFIGURACE PRO SLABŠÍ PC =======
MODEL_PATH = r"D:\AI\gpt-oss\gemma-3n-E4B-it-Q8_0.gguf"
MODEL_PATH = r"D:\AI\gemma3\google_gemma-3-4b-it-qat-Q6_K_L.gguf"
INPUT_FILE = "moje_metoda.txt"
OUTPUT_FILE = None

# OPTIMALIZACE PRO SLABŠÍ HW
CHUNK_SIZE = 50           # malé chunky pro rychlost
OVERLAP = 10               # minimální overlap
TASKS_PER_CHUNK = 6       # více úkolů na chunk
MAX_TOKENS = 80           # krátké odpovědi
TEMPERATURE = 0.5         # nižší pro stabilitu
BATCH_SIZE = 128           # malý batch pro slabší PC
N_CTX = 1024              # menší kontext
DELAY = 0.0               # žádný delay

# ======= MAPOVÁNÍ ÚKOLŮ =======
# Instrukce pro model (anglicky) → České prompty pro trénovací data
TASK_MAP = {
    'paraphrase': {
        'model_instruction': 'Rewrite the following text using different words but keep the same meaning. Answer only in Czech, without English translations unless explicitly asked:',
        'training_prompt': 'Parafrázuj tento text:'
    },
    'summarize': {
        'model_instruction': 'Summarize this text in 1-2 sentences. Answer only in Czech, without English translations unless explicitly asked:',
        'training_prompt': 'Shrň tento text:'
    },
    'expand': {
        'model_instruction': 'Expand this text into 2-3 sentences with more details. Answer only in Czech, without English translations unless explicitly asked:',
        'training_prompt': 'Rozveď tento text:'
    },
    'simplify': {
        'model_instruction': 'Explain this text in simple words for children. Answer only in Czech, without English translations unless explicitly asked:',
        'training_prompt': 'Vysvětli jednoduše:'
    },
    'keywords': {
        'model_instruction': 'Extract 3-5 key words from this text. Answer only in Czech, without English translations unless explicitly asked:',
        'training_prompt': 'Vypiš klíčová slova z textu:'
    },
    'title': {
        'model_instruction': 'Create a short title for this text (max 6 words). Answer only in Czech, without English translations unless explicitly asked:',
        'training_prompt': 'Vytvoř titulek pro text:'
    },
    'question': {
        'model_instruction': 'Create a question that can be answered from this text. Answer only in Czech, without English translations unless explicitly asked:',
        'training_prompt': 'Vytvoř otázku k textu:'
    },
    'continue': {
        'model_instruction': 'Write the next logical sentence that would follow this text. Answer only in Czech, without English translations unless explicitly asked:',
        'training_prompt': 'Pokračuj v textu další větou:'
    }
}

TASK_LIST = list(TASK_MAP.keys())

def read_file(path: Path) -> str:
    """Rychlé čtení souboru."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp1250")

def make_chunks(text: str) -> List[str]:
    """Rychlé rozdělení na chunky."""
    # Jednoduchá tokenizace
    words = re.sub(r'\s+', ' ', text.replace('\n', ' ')).split()
    
    chunks = []
    step = CHUNK_SIZE - OVERLAP
    
    for i in range(0, len(words), step):
        chunk = words[i:i + CHUNK_SIZE]
        if len(chunk) >= 15:  # min délka
            chunks.append(' '.join(chunk))
        if i + CHUNK_SIZE >= len(words):
            break
    
    return chunks

def clean_response(text: str) -> str:
    text = text.strip()
    # případně jen lehké očištění bez ořezu:
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

class FastDataGen:
    def __init__(self):
        self.llm = None
        self.total_items = 0
        self.start_time = None
    
    def init_model(self):
        """Rychlé načtení modelu."""
        print("🔄 Načítám model...")
        start = time.time()
        
        self.llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=N_CTX,
            n_threads=min(4, os.cpu_count() or 2),  # max 4 vlákna
            n_gpu_layers=-1,  # -1 = auto
            verbose=False,
            n_batch=BATCH_SIZE,
            f16_kv=True,
            use_mlock=False,
        )
        
        # Warm-up
        self.llm("Hi", max_tokens=1, temperature=0)
        print(f"✅ Ready ({time.time() - start:.1f}s)")
    
    def generate(self, task: str, chunk: str) -> Optional[Dict[str, str]]:
        """Jedna rychlá generace."""
        task_info = TASK_MAP[task]
        
        # Prompt pro model (anglicky)
        model_prompt = f"{task_info['model_instruction']}\n\n{chunk}\n\nAnswer:"
        # print("PROMT = " + str(model_prompt) + "\n")
        try:
            response = self.llm(
                model_prompt,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                top_p=0.9,
                echo=False,
            )
            
            completion = clean_response(response["choices"][0]["text"])
            
            if len(completion.strip()) < 5:
                return None
            
            # Trénovací prompt (česky)
            training_prompt = f"{task_info['training_prompt']} {chunk}"
            
            return {
                'prompt': training_prompt,
                'completion': completion
            }
            
        except Exception:
            return None
    
    def save_item(self, item: Dict[str, str], file_path: Path):
        """Uloží pouze prompt a completion (bez context)."""
        clean_item = {
            'prompt': item['prompt'],
            'completion': item['completion']
        }
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(clean_item, ensure_ascii=False) + "\n")
    
    def process(self, input_file: Path, output_file: Path):
        """Hlavní zpracování."""
        text = read_file(input_file)
        chunks = make_chunks(text)
        
        if not chunks:
            print("❌ Žádné chunky")
            return
        
        # Připrav výstup
        output_file.parent.mkdir(exist_ok=True)
        if output_file.exists():
            output_file.unlink()
        
        print(f"📄 {len(chunks)} chunků")
        print(f"💾 {output_file.name}")
        print(f"⚡ {TASKS_PER_CHUNK} úkolů/chunk\n")
        
        self.total_items = 0
        self.start_time = time.time()
        
        try:
            for i, chunk in enumerate(chunks, 1):
                # Random úkoly pro tento chunk
                tasks = random.sample(TASK_LIST, min(TASKS_PER_CHUNK, len(TASK_LIST)))
                chunk_count = 0
                
                for task in tasks:
                    item = self.generate(task, chunk)
                    if item:
                        self.save_item(item, output_file)
                        chunk_count += 1
                        self.total_items += 1
                    
                    if DELAY > 0:
                        time.sleep(DELAY)
                
                # Progress každých 10 chunků
                if i % 10 == 0 or i == len(chunks):
                    elapsed = time.time() - self.start_time
                    rate = self.total_items / elapsed if elapsed > 0 else 0
                    progress = (i / len(chunks)) * 100
                    
                    print(f"{i:3d}/{len(chunks)} ({progress:4.1f}%) | "
                          f"{self.total_items:4d} items | "
                          f"{rate:5.1f}/s")
            
            # Finální stats
            elapsed = time.time() - self.start_time
            print(f"\n🎉 {self.total_items} položek za {elapsed:.1f}s")
            print(f"⚡ {self.total_items/elapsed:.1f} položek/s")
            
        except KeyboardInterrupt:
            print(f"\n⚠️ Přerušeno - uloženo {self.total_items} položek")

def main():
    input_path = Path(INPUT_FILE)
    if not input_path.exists():
        print(f"❌ {input_path} neexistuje")
        sys.exit(1)
    
    output_path = Path(OUTPUT_FILE or f"{input_path.stem}_dataset.jsonl")
    
    print("🚀 RYCHLÝ GENERÁTOR DATASETU")
    print(f"🎯 {input_path.name} → {output_path.name}")
    print(f"💻 Optimalizováno pro slabší PC\n")
    
    generator = FastDataGen()
    
    try:
        generator.init_model()
        generator.process(input_path, output_path)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()