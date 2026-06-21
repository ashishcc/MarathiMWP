# Data terms and attribution

The `LICENSE` file (MIT) applies to the **source code only** — the notebooks,
the `utils/` modules, and the helper scripts. It does **not** grant any rights
over the datasets, which carry separate terms described below. Please read this
before redistributing or reusing any data in this repository.

## 1. MarathiMWP (translated arithmetic word problems)

The MarathiMWP problems are **translations of the HAWP Hindi dataset**, with the
gold equations preserved from HAWP:

> Harshita Sharma, Pruthwik Mishra, and Dipti Sharma. 2022. *HAWP: a Dataset for
> Hindi Arithmetic Word Problem Solving.* In Proceedings of the Thirteenth
> Language Resources and Evaluation Conference (LREC), pages 3479–3490,
> Marseille, France. European Language Resources Association.
> https://aclanthology.org/2022.lrec-1.373/ — https://github.com/hellomasaya/hawp

At the time of release, the HAWP repository carries **no explicit licence**.
Under default copyright this means all rights are reserved by the HAWP authors.
The MarathiMWP set is a derivative work and is therefore **not released under an
open data licence**. It is shared **for non-commercial academic research only**,
with attribution to HAWP. The underlying rights to the problem content remain
with the HAWP authors; anyone wishing to use the data beyond non-commercial
research should contact the HAWP authors directly. If the HAWP authors grant
explicit permission (e.g. CC BY 4.0), this notice will be updated accordingly.

## 2. Authentic Balbharati problems (Standard 4–8)

The authentic evaluation set (`balbharati_authentic_mwp.json`) consists of
arithmetic word problems transcribed from the Maharashtra State Board
(Balbharati) mathematics textbooks for Standards 4–8.

> Mathematics textbook content © Maharashtra State Bureau of Textbook Production
> and Curriculum Research (Balbharati), Pune.

These problems are **copyrighted textbook excerpts**, included here as a small
research sample under fair-dealing for non-commercial academic research and
criticism. They are **not** placed under any open licence. Copyright in the
original problem text remains with the Maharashtra State Board. Do not
redistribute this subset for commercial purposes.

## 3. Pre-trained models used (not redistributed here)

This repository does not redistribute model weights, but the experiments rely on:

- **mT5** (Xue et al., 2021) — Apache License 2.0
- **IndicBART** (Dabre et al., 2022) — MIT License

## Summary

| Component | Terms |
|---|---|
| Source code (notebooks, `utils/`, scripts) | MIT (see `LICENSE`) |
| MarathiMWP translated data | Non-commercial research only; derivative of HAWP (no upstream licence); attribute HAWP |
| Balbharati authentic data | © Maharashtra State Board; research excerpt, non-commercial; not openly licensed |
| Model weights | Not redistributed; mT5 = Apache-2.0, IndicBART = MIT |

If you use this work, please cite the accompanying thesis and the HAWP dataset.
