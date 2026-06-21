"""
Evaluation utilities for MarathiMWP thesis experiments.
"""
import re
import math
import json
import numpy as np
from collections import Counter

# ─── Answer Extraction ────────────────────────────────────────────────────────

def evaluate_equation(eq_str: str):
    """
    Parse and evaluate an equation string like "X = ( 7.423 + 6.129 )".
    Returns the float answer or None on failure.
    """
    try:
        expr = re.sub(r'X\s*=\s*', '', eq_str).strip()
        result = eval(expr, {"__builtins__": {}}, {})
        return round(float(result), 6)
    except Exception:
        return None


def answers_match(gold_eq: str, pred_eq: str, tol: float = 1e-4) -> bool:
    """True if both equations evaluate to the same answer within tolerance."""
    gold_ans = evaluate_equation(gold_eq)
    pred_ans = evaluate_equation(pred_eq)
    if gold_ans is None or pred_ans is None:
        return False
    if gold_ans == 0 and pred_ans == 0:
        return True
    return abs(gold_ans - pred_ans) <= tol * max(1, abs(gold_ans))


def normalize_equation(eq_str: str) -> str:
    """Normalize whitespace and casing for exact-match comparison."""
    eq = re.sub(r'\s+', ' ', eq_str.strip())
    eq = eq.replace('X =', 'X=').replace('x =', 'X=')
    return eq


def equations_exact_match(gold_eq: str, pred_eq: str) -> bool:
    return normalize_equation(gold_eq) == normalize_equation(pred_eq)


# ─── Sympy Equivalence ────────────────────────────────────────────────────────

def equations_sympy_equivalent(gold_eq: str, pred_eq: str) -> bool:
    """Check mathematical equivalence via SymPy (handles commutativity)."""
    try:
        from sympy import simplify, sympify
        gold_expr = re.sub(r'X\s*=\s*', '', gold_eq).strip()
        pred_expr = re.sub(r'X\s*=\s*', '', pred_eq).strip()
        diff = simplify(sympify(gold_expr) - sympify(pred_expr))
        return diff == 0
    except Exception:
        return answers_match(gold_eq, pred_eq)


# ─── BLEU ─────────────────────────────────────────────────────────────────────

def _ngrams(tokens, n):
    return Counter(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))


def sentence_bleu(reference: str, hypothesis: str, max_n: int = 4) -> float:
    ref_tokens = reference.strip().split()
    hyp_tokens = hypothesis.strip().split()
    if not hyp_tokens:
        return 0.0

    bp = min(1.0, math.exp(1 - len(ref_tokens) / len(hyp_tokens))) if len(hyp_tokens) < len(ref_tokens) else 1.0

    precisions = []
    for n in range(1, max_n + 1):
        ref_ng = _ngrams(ref_tokens, n)
        hyp_ng = _ngrams(hyp_tokens, n)
        clipped = sum(min(cnt, ref_ng[ng]) for ng, cnt in hyp_ng.items())
        total = max(len(hyp_tokens) - n + 1, 0)
        precisions.append(clipped / total if total > 0 else 0.0)

    if any(p == 0 for p in precisions):
        return 0.0
    log_avg = sum(math.log(p) for p in precisions) / max_n
    return bp * math.exp(log_avg)


def corpus_bleu(references: list, hypotheses: list) -> float:
    scores = [sentence_bleu(r, h) for r, h in zip(references, hypotheses)]
    return np.mean(scores) * 100


# ─── Aggregate Metrics ────────────────────────────────────────────────────────

def compute_metrics(gold_equations: list, pred_equations: list,
                    use_sympy: bool = False) -> dict:
    """
    Compute all four metrics for a list of gold/pred equation strings.
    Returns dict with: answer_acc, equation_acc, equation_equiv, bleu
    """
    n = len(gold_equations)
    assert n == len(pred_equations), "Lengths must match"

    aa = sum(answers_match(g, p) for g, p in zip(gold_equations, pred_equations))
    ea = sum(equations_exact_match(g, p) for g, p in zip(gold_equations, pred_equations))

    if use_sympy:
        ee = sum(equations_sympy_equivalent(g, p) for g, p in zip(gold_equations, pred_equations))
    else:
        ee = sum(answers_match(g, p) for g, p in zip(gold_equations, pred_equations))

    bleu = corpus_bleu(gold_equations, pred_equations)

    return {
        "answer_accuracy": aa / n * 100,
        "equation_accuracy": ea / n * 100,
        "equation_equivalence": ee / n * 100,
        "bleu": bleu,
        "n_samples": n,
    }


def print_metrics(name: str, metrics: dict):
    print(f"\n{'='*50}")
    print(f"  {name}")
    print(f"{'='*50}")
    print(f"  Answer Accuracy      : {metrics['answer_accuracy']:.2f}%")
    print(f"  Equation Accuracy    : {metrics['equation_accuracy']:.2f}%")
    print(f"  Equation Equivalence : {metrics['equation_equivalence']:.2f}%")
    print(f"  BLEU Score           : {metrics['bleu']:.2f}")
    print(f"  N Samples            : {metrics['n_samples']}")
