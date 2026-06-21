"""
Data loading and splitting utilities for MarathiMWP experiments.
"""
import json
import re
import random
from pathlib import Path
from collections import Counter

#ROOT = Path(__file__).resolve().parents[2]  # Thesis/
ROOT = Path(".")
MARATHI_PATH = ROOT / "datasets/marathi.json"
HAWP_PATH = ROOT / "datasets/hawp.json"
SPLITS_DIR = ROOT / "splits"


# ─── Loaders ──────────────────────────────────────────────────────────────────

def load_marathi() -> list:
    with open(MARATHI_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_hawp() -> list:
    with open(HAWP_PATH, encoding="utf-8") as f:
        return json.load(f)


# ─── Number Extraction ────────────────────────────────────────────────────────

DEVANAGARI_DIGIT_MAP = {
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9',
}


def devanagari_to_arabic(text: str) -> str:
    for dev, arab in DEVANAGARI_DIGIT_MAP.items():
        text = text.replace(dev, arab)
    return text


def extract_numbers(text: str) -> list:
    text = devanagari_to_arabic(text)
    return [float(m) for m in re.findall(r'\d+\.?\d*', text)]


def extract_equation_answer(eq_str: str):
    try:
        expr = re.sub(r'X\s*=\s*', '', eq_str).strip()
        return round(eval(expr, {"__builtins__": {}}, {}), 6)
    except Exception:
        return None


# ─── Splits ───────────────────────────────────────────────────────────────────

def stratified_split(data: list, train_ratio=0.70, val_ratio=0.15, seed=42) -> tuple:
    """
    Stratify by Number of Operators to preserve distribution across splits.
    Returns (train, val, test) lists.
    """
    random.seed(seed)
    buckets = {}
    for item in data:
        key = item.get("Number of Operators", 1)
        buckets.setdefault(key, []).append(item)

    train, val, test = [], [], []
    for key in sorted(buckets):
        items = buckets[key][:]
        random.shuffle(items)
        n = len(items)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)
        train.extend(items[:n_train])
        val.extend(items[n_train:n_train + n_val])
        test.extend(items[n_train + n_val:])

    return train, val, test


def save_splits(train, val, test, lang="marathi"):
    SPLITS_DIR.mkdir(parents=True, exist_ok=True)
    for name, split in [("train", train), ("val", val), ("test", test)]:
        path = SPLITS_DIR / f"{lang}_{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(split, f, ensure_ascii=False, indent=2)
        print(f"Saved {path.name}: {len(split)} problems")


def load_splits(lang="marathi") -> tuple:
    splits = []
    for name in ["train", "val", "test"]:
        path = SPLITS_DIR / f"{lang}_{name}.json"
        with open(path, encoding="utf-8") as f:
            splits.append(json.load(f))
    return tuple(splits)


# ─── Operator Analysis ────────────────────────────────────────────────────────

def get_operators_in_equation(eq_str: str) -> list:
    return re.findall(r'[+\-*/]', eq_str.replace('X =', ''))


def classify_operation(eq_str: str) -> str:
    ops = get_operators_in_equation(eq_str)
    op_set = set(ops)
    if len(ops) == 1:
        return {'+': 'addition', '-': 'subtraction',
                '*': 'multiplication', '/': 'division'}.get(ops[0], 'unknown')
    return 'mixed'
