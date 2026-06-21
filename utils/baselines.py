"""
Rule-based and template-based baselines for MarathiMWP.

This module mirrors the baseline logic defined inline in Notebook 02
(`02_Baselines.ipynb`) so that the same baselines can be reused for the
authentic-Marathi evaluation in Notebook 06 without duplicating code.

Both baselines are deterministic and require no GPU.
"""
import math
import re
from collections import Counter

from utils.data_utils import extract_numbers

# ─── Rule-Based Baseline ────────────────────────────────────────────────────

ADDITION_KW = ['बेरीज', 'जोड', 'एकत्र', 'मिळून', 'एकूण', 'आणखी', 'मिळाले', 'जास्त', 'वाढ']
SUBTRACTION_KW = ['वजा', 'कमी', 'शिल्लक', 'उरले', 'काढले', 'फरक', 'गेले', 'खर्च', 'दिले']
MULTIPLY_KW = ['गुणा', 'पट', 'प्रत्येक', 'गुणिले']
DIVISION_KW = ['भाग', 'भागा', 'वाटा', 'समान', 'प्रत्येकाला']


def detect_operation(text: str) -> str:
    """Return guessed operation from Marathi keyword presence."""
    scores = {'addition': 0, 'subtraction': 0, 'multiplication': 0, 'division': 0}
    for kw in ADDITION_KW:
        if kw in text:
            scores['addition'] += 1
    for kw in SUBTRACTION_KW:
        if kw in text:
            scores['subtraction'] += 1
    for kw in MULTIPLY_KW:
        if kw in text:
            scores['multiplication'] += 1
    for kw in DIVISION_KW:
        if kw in text:
            scores['division'] += 1

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 'addition'  # default fallback


def rule_based_solve(problem: dict) -> str:
    """Keyword-driven single-operation equation guess."""
    text = problem['Problem']
    numbers = extract_numbers(text)

    # Use relevant indices to pick numbers when available
    rel_idx = problem.get('Relevant Indices', [])
    relevant_nums = []
    for idx in rel_idx:
        if idx != 'implicit' and isinstance(idx, int) and idx < len(numbers):
            relevant_nums.append(numbers[idx])
    if not relevant_nums:
        relevant_nums = numbers[:2] if len(numbers) >= 2 else numbers

    if len(relevant_nums) == 0:
        return 'X = 0'

    if len(relevant_nums) == 1:
        return f'X = {relevant_nums[0]}'

    a, b = relevant_nums[0], relevant_nums[1]
    op = detect_operation(text)

    if op == 'addition':
        return f'X = ( {a} + {b} )'
    elif op == 'subtraction':
        big, small = (a, b) if a >= b else (b, a)  # heuristic: larger - smaller
        return f'X = ( {big} - {small} )'
    elif op == 'multiplication':
        return f'X = ( {a} * {b} )'
    elif op == 'division':
        return f'X = ( {a} / {b} )'

    return f'X = ( {a} + {b} )'


# ─── Template-Based Baseline ────────────────────────────────────────────────

def equation_to_template(eq: str) -> str:
    """Replace numbers with NUM placeholder to get structural template."""
    return re.sub(r'\d+\.?\d*', 'NUM', eq)


def _get_tfidf_keywords(problem_text: str, vocab_idf: dict) -> set:
    """Return set of high-IDF words from problem text."""
    words = set(problem_text.split())
    return {w for w in words if vocab_idf.get(w, 0) > 2.0}


class TemplateBaseline:
    """Nearest-keyword template retrieval, fit on the training split."""

    def __init__(self, train: list):
        self.template_counts = Counter(
            equation_to_template(x['Equation']) for x in train)

        doc_freq = Counter()
        for item in train:
            doc_freq.update(set(item['Problem'].split()))
        n = len(train)
        idf = {w: math.log(n / (1 + cnt)) for w, cnt in doc_freq.items()}

        self.train_records = []
        for item in train:
            self.train_records.append({
                'template': equation_to_template(item['Equation']),
                'keywords': _get_tfidf_keywords(item['Problem'], idf),
            })

    def solve(self, problem: dict) -> str:
        text = problem['Problem']
        test_words = set(text.split())
        test_nums = extract_numbers(text)

        best_score, best_template = -1, None
        for rec in self.train_records:
            score = len(test_words & rec['keywords'])
            if score > best_score:
                best_score = score
                best_template = rec['template']

        if best_template is None:  # fallback: majority template
            best_template = self.template_counts.most_common(1)[0][0]

        slots = best_template.count('NUM')
        padded = (test_nums + [0] * slots)[:slots]
        result = best_template
        for num in padded:
            result = result.replace('NUM', str(num), 1)
        return result
