# pediatric-gi-survey-figures

Publication-quality figures for:

> **Clinician and Caregiver Perspectives on Diet and Microbiota Interventions
> in Pediatric Gastroenterology: A Cross-Sectional Survey of 1,000 Respondents**

## What this repository contains

A single Python script (`make_figures.py`) that generates all five
manuscript figures at Nature-family specifications:

- **Typography:** Arial 7–8 pt body, 6.5 pt ticks
- **Dimensions:** 183 mm double column (89 mm single column available)
- **Palette:** Okabe-Ito, colorblind-safe
- **Output:** vector PDF for submission, 600 dpi PNG for review
- **Fonts:** TrueType embedded (`pdf.fonttype = 42`), as required by Nature

## Figures

| File | Description |
|------|-------------|
| `fig1_participants.pdf` | Participant characteristics (children and clinicians) |
| `fig2_symptoms_qol.pdf` | Symptom burden and quality-of-life impact |
| `fig3_dietary_practice.pdf` | Dietary practice and adherence barriers |
| `fig4_diagnostic_testing.pdf` | Diagnostic test ordering by clinicians |
| `fig5_computational_analysis.pdf` | Cluster, predictive, and thematic analyses |

## How to run

```bash
pip install -r requirements.txt
python make_figures.py
