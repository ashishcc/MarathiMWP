# MarathiMWP: Marathi Arithmetic Word Problem Solving

Code and experiments for **MarathiMWP**, the first benchmark dataset and neural
solver study for arithmetic word problems in **Marathi**. This repository
accompanies the MSc thesis *"MarathiMWP: A Benchmark Dataset and Neural Solver
for Grade-School Arithmetic Word Problems in Marathi"* (Liverpool John Moores
University).

The study builds a Marathi arithmetic word-problem dataset (translated from the
Hindi **HAWP** dataset, preserving its gold equations), establishes rule-based,
template-based, and neural baselines, and evaluates pre-trained multilingual
transformers (**mT5-small**, **IndicBART**) and Hindi→Marathi cross-lingual
transfer. Models are additionally tested on a held-out set of **authentic**
Marathi problems transcribed from Balbharati (Maharashtra State Board) Std 4–8
textbooks, to measure how far translated-test accuracy reflects genuine Marathi
understanding.

## Notebooks

| Notebook | Purpose |
|---|---|
| `01_EDA_Dataset_Analysis.ipynb` | Dataset statistics, figures, train/val/test splits |
| `02_Baselines.ipynb` | Rule-based, template-based, and LSTM Seq2Seq baselines |
| `03_Transformer_mT5_IndicBART.ipynb` | Fine-tuning mT5-small and IndicBART (GPU) |
| `04_CrossLingual_Transfer.ipynb` | Zero-shot / few-shot / joint Hindi→Marathi transfer (GPU) |
| `05_Results_Analysis.ipynb` | Master results tables, comparison figures, error analysis |
| `06_Authentic_Marathi_Eval.ipynb` | Evaluation on the authentic Balbharati Std 4–8 set |

## Repository layout

```
.
├── 01..06_*.ipynb        experiment notebooks (run in order)
├── utils/                shared modules: baselines.py, data_utils.py, evaluation.py
├── data/
│   ├── marathi.json                  full MarathiMWP dataset (2,336 problems)
│   └── balbharati_authentic_mwp.json authentic Std 4–8 evaluation set (98 problems)
├── splits/               train/val/test splits + saved model predictions
└── figures/              result charts (PNG) and result tables (CSV)
```

## Requirements

Python 3.10+; see [`requirements.txt`](requirements.txt) (`torch`, `transformers`,
`datasets`, `sentencepiece`, `numpy`, `pandas`, `scipy`, `sympy`, `matplotlib`,
`seaborn`). The transformer notebooks (03, 04, 06) require a GPU; the baseline
notebooks (01, 02) run on CPU.

```bash
pip install -r requirements.txt
```

## Data & setup notes

- **HAWP data is not redistributed here.** The cross-lingual transfer notebook (04)
  needs the Hindi HAWP splits — download them from the
  [HAWP repository](https://github.com/hellomasaya/hawp) and place
  `hawp_train.json` / `hawp_val.json` / `hawp_test.json` in `splits/`.
- Notebook 06 reads the authentic set; set its `AUTH_PATH` to
  `data/balbharati_authentic_mwp.json`.
- Model checkpoints are **not** included (too large); the GPU notebooks regenerate
  them under a local `models/` directory (git-ignored).

## License & attribution

**Source code** in this repository (notebooks, `utils/`, scripts) is released
under the **MIT License** — see [`LICENSE`](LICENSE).

**The datasets are NOT covered by the MIT License** and carry separate terms —
see [`DATA-TERMS.md`](DATA-TERMS.md). In brief:

- **MarathiMWP** (translated problems) is a derivative of **HAWP**
  ([Sharma et al., 2022, LREC](https://aclanthology.org/2022.lrec-1.373/);
  [repo](https://github.com/hellomasaya/hawp)), which carries no explicit
  licence (all rights reserved). The translated set is shared for
  **non-commercial academic research only**, with attribution to HAWP.
- **Authentic Balbharati problems** (Std 4–8) are copyrighted textbook excerpts,
  © Maharashtra State Board, included as a research sample under fair-dealing —
  **not openly licensed**.
- Models used: **mT5** (Apache-2.0), **IndicBART** (MIT) — weights are not
  redistributed here.

If you use this work, please cite the thesis and the HAWP dataset.
