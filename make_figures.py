"""
Publication-quality figures for:
    "Barriers and Bridges in Pediatric Gastroenterology:
     A Dual-Perspective Study of Clinical Practice and Family Experience"

Outputs (all in ./figures/):
    fig1_participants.pdf / .png
    fig2_symptoms_qol.pdf / .png
    fig3_dietary_practice.pdf / .png
    fig4_diagnostic_testing.pdf / .png
    fig5_computational_analysis.pdf / .png

Design specifications (Nature-family):
    - Width: 89 mm (single column) or 183 mm (double column)
    - Font: Arial or Helvetica, 7-8 pt
    - Line weights: 0.5-1.0 pt
    - Colorblind-safe palette (Okabe-Ito)
    - Vector PDF for submission, 600 dpi PNG for review

All numbers are entered manually and match the tables in the
revised Results section. Cells marked [VERIFY] must be checked
against the raw data before final submission.
"""

import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
import seaborn as sns

# ============================================================
# 0. Global style
# ============================================================

OUTDIR = "figures"
os.makedirs(OUTDIR, exist_ok=True)

# Nature-family typography: Arial preferred, DejaVu Sans fallback
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 7,
    "axes.titlesize": 8,
    "axes.labelsize": 7,
    "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5,
    "legend.fontsize": 6.5,
    "figure.dpi": 150,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
    "axes.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "lines.linewidth": 0.9,
    "lines.markersize": 3.5,
    "patch.linewidth": 0.5,
    "pdf.fonttype": 42,   # embed TrueType, required by Nature
    "ps.fonttype": 42,
})

# Nature column widths (inches)
MM = 1 / 25.4
SINGLE = 89 * MM     # 3.50 in
DOUBLE = 183 * MM    # 7.20 in

# Okabe-Ito colorblind-safe palette
OI = {
    "orange":      "#E69F00",
    "sky":         "#56B4E9",
    "green":       "#009E73",
    "yellow":      "#F0E442",
    "blue":        "#0072B2",
    "vermillion":  "#D55E00",
    "purple":      "#CC79A7",
    "grey":        "#999999",
    "black":       "#000000",
}
# Diverging pair for clinician vs parent
COL_CLIN = OI["blue"]
COL_PARE = OI["vermillion"]
COL_MIX  = OI["grey"]

def save(fig, name):
    """Save as vector PDF and high-res PNG."""
    fig.savefig(os.path.join(OUTDIR, f"{name}.pdf"))
    fig.savefig(os.path.join(OUTDIR, f"{name}.png"), dpi=600)
    plt.close(fig)
    print(f"  wrote {name}.pdf and {name}.png")


# ============================================================
# 1. Shared data (entered manually; matches revised tables)
# ============================================================

# ---- Figure 1: participant characteristics ----
# Table 1 (parents/children, n = 500)
age_groups = pd.DataFrame({
    "group": ["2–4 y", "5–8 y"],
    "n":     [241, 259],
})
sex_children = pd.DataFrame({
    "group": ["Girls", "Boys"],
    "n":     [262, 238],
})

# Table 2 (clinicians, n = 500)
specialty = pd.DataFrame({
    "group": ["General pediatrician", "Pediatric gastroenterologist"],
    "n":     [466, 34],
})
experience = pd.DataFrame({
    "group": ["<2 y", "2–5 y"],
    "n":     [179, 321],
})
caseload = pd.DataFrame({
    "group": ["<10", "10–25", "26–50"],
    "n":     [67, 233, 200],
})

# ---- Figure 2: symptoms and QoL (Table 3) ----
# [VERIFY] every cell before submission
symptoms = pd.DataFrame({
    "domain": ["Abdominal pain\n(moderate)", "Bloating or\ndiarrhea",
               "Constipation\n(mild)", "Fatigue", "Poor appetite"],
    "n":      [465, 445, 250, 455, 445],
})
qol = pd.DataFrame({
    "domain": ["Overall health\npoor", "School attendance\naffected",
               "Daily activities\naffected"],
    "n":      [465, 250, 250],
})

# ---- Figure 3: dietary practice (Table 4) ----
# [VERIFY] every cell before submission
advice_source = pd.DataFrame({
    "source": ["Gastroenterologist", "Dietitian", "Pediatrician"],
    "n":      [475, 475, 250],
})
diet_type = pd.DataFrame({
    "diet": ["Gluten-free", "Low-FODMAP"],
    "n":    [475, 250],
})
adherence = pd.DataFrame({
    "days": ["2–3 days/wk", "4–5 days/wk"],
    "n":    [250, 250],
})
barriers = pd.DataFrame({
    "barrier": ["Cost", "Limited\navailability", "School meals",
                "Child dislikes\ndiet", "Lack of time",
                "Conflicting\nadvice"],
    "n":       [450, 450, 450, 250, 250, 250],
})

# ---- Figure 4: diagnostic testing (Table 6) ----
tests = ["CRP/ESR", "Genetic testing", "Endoscopy /\ncolonoscopy",
         "Stool microbiome\ntesting", "Food allergy\npanels"]
# rows = tests, columns = Always, Often, Sometimes, Rarely, Never
diagnostics = pd.DataFrame(
    [
        [400, 100, 0,   0,   0],
        [100, 350, 50,  0,   0],
        [0,   300, 200, 0,   0],
        [250, 250, 0,   0,   0],
        [100, 150, 50,  150, 50],
    ],
    index=tests,
    columns=["Always", "Often", "Sometimes", "Rarely", "Never"],
)

# ---- Figure 5: computational + thematic ----
clusters = pd.DataFrame({
    "cluster": ["Cluster 0", "Cluster 1", "Cluster 2"],
    "n":       [161, 210, 129],
})
ml_models = pd.DataFrame({
    "model":    ["Random forest", "Logistic regression"],
    "accuracy": [0.51, 0.51],
    "ci_low":   [0.45, 0.45],
    "ci_high":  [0.57, 0.57],
})
adherence_effect = {
    "t":      0.80,
    "p":      0.42,
    "cohen_d": 0.08,
}
themes = pd.DataFrame({
    "theme": ["Coordination\nacross providers", "Dietary\nintervention",
              "Access to care", "Evidence and\nresearch",
              "School\nenvironment", "Financial\nburden"],
    "mentions": [180, 165, 150, 120, 110, 95],  # [VERIFY] derive from coding
})


# ============================================================
# 2. Helper functions
# ============================================================

def pct(n, total=500):
    return 100.0 * np.asarray(n) / total

def add_panel_label(ax, label, x=-0.18, y=1.06):
    """Nature-style bold panel label (a, b, c...)."""
    ax.text(x, y, label, transform=ax.transAxes,
            fontsize=9, fontweight="bold", va="top", ha="left")

def bar_with_pct(ax, labels, values, color, total=500, orient="v",
                 label_fmt="{:.0f}%\n(n={})", pad=2):
    """Horizontal or vertical bar chart with n and % labels."""
    p = pct(values, total)
    if orient == "v":
        bars = ax.bar(labels, p, color=color, edgecolor="black", linewidth=0.5)
        ax.set_ylabel("Respondents (%)")
        for b, v, n in zip(bars, p, values):
            ax.text(b.get_x() + b.get_width() / 2, v + pad,
                    label_fmt.format(v, n),
                    ha="center", va="bottom", fontsize=6)
        ax.set_ylim(0, max(p) + 12)
    else:
        bars = ax.barh(labels, p, color=color, edgecolor="black", linewidth=0.5)
        ax.set_xlabel("Respondents (%)")
        for b, v, n in zip(bars, p, values):
            ax.text(v + pad, b.get_y() + b.get_height() / 2,
                    label_fmt.format(v, n).replace("\n", " "),
                    va="center", ha="left", fontsize=6)
        ax.set_xlim(0, max(p) + 12)
    ax.invert_yaxis() if orient == "h" else None
    return bars

def donut(ax, values, labels, colors, title=None):
    """Publication-quality donut with center annotation."""
    total = sum(values)
    wedges, _ = ax.pie(
        values, colors=colors, startangle=90, counterclock=False,
        wedgeprops=dict(width=0.38, edgecolor="white", linewidth=1.0),
    )
    ax.text(0, 0.08, f"n = {total}", ha="center", va="center",
            fontsize=8, fontweight="bold")
    ax.text(0, -0.15, title or "", ha="center", va="center", fontsize=6)
    ax.set_aspect("equal")
    return wedges


# ============================================================
# 3. FIGURE 1 — Participant characteristics (double column)
# ============================================================
# Layout: 2 rows x 3 columns
#   (a) children age       (b) children sex        (c) clinician specialty
#   (d) clinician years    (e) clinician caseload  (f) key n's as text
# ============================================================

def figure_1():
    fig = plt.figure(figsize=(DOUBLE, 4.2))
    gs = GridSpec(2, 3, figure=fig, wspace=0.45, hspace=0.55,
                  left=0.07, right=0.97, top=0.90, bottom=0.10)

    # (a) age
    ax = fig.add_subplot(gs[0, 0])
    bar_with_pct(ax, age_groups["group"], age_groups["n"], COL_PARE, orient="v")
    ax.set_title("Children by age group")
    add_panel_label(ax, "a")

    # (b) sex
    ax = fig.add_subplot(gs[0, 1])
    bar_with_pct(ax, sex_children["group"], sex_children["n"], COL_PARE, orient="v")
    ax.set_title("Children by sex")
    add_panel_label(ax, "b")

    # (c) specialty (donut)
    ax = fig.add_subplot(gs[0, 2])
    wedges = donut(ax, specialty["n"], specialty["group"],
                   [COL_CLIN, OI["sky"]], title="clinicians")
    ax.set_title("Clinician specialty")
    ax.legend(wedges, specialty["group"], loc="upper center",
              bbox_to_anchor=(0.5, -0.05), ncol=1, frameon=False)
    add_panel_label(ax, "c", x=-0.05)

    # (d) experience
    ax = fig.add_subplot(gs[1, 0])
    bar_with_pct(ax, experience["group"], experience["n"], COL_CLIN, orient="v")
    ax.set_title("Years in practice")
    add_panel_label(ax, "d")

    # (e) caseload
    ax = fig.add_subplot(gs[1, 1])
    bar_with_pct(ax, caseload["group"], caseload["n"], COL_CLIN, orient="v")
    ax.set_title("Weekly pediatric GI caseload")
    ax.set_xlabel("Patients per week")
    add_panel_label(ax, "e")

    # (f) summary text panel
    ax = fig.add_subplot(gs[1, 2])
    ax.axis("off")
    txt = (
        "Cohort summary\n"
        "───────────────\n"
        "Parents/guardians:  500\n"
        "Clinicians:          500\n"
        "Children aged 2–8 y: 500\n"
        "General pediatricians:  93.2%\n"
        "Pediatric gastroenterologists: 6.8%\n"
        "Diagnosis <3 months:  100%"
    )
    ax.text(0, 1, txt, va="top", ha="left", fontsize=6.5,
            family="monospace", linespacing=1.6)
    add_panel_label(ax, "f", x=-0.05)

    fig.suptitle("Participant characteristics (n = 500 per group)",
                 fontsize=9, fontweight="bold", y=0.99)
    save(fig, "fig1_participants")


# ============================================================
# 4. FIGURE 2 — Symptoms and quality of life (double column)
# ============================================================
# Layout: 1 row x 2 columns
#   (a) symptom prevalence (horizontal bar)
#   (b) QoL impact (horizontal bar)
# ============================================================

def figure_2():
    fig = plt.figure(figsize=(DOUBLE, 3.4))
    gs = GridSpec(1, 2, figure=fig, wspace=0.55,
                  left=0.16, right=0.97, top=0.86, bottom=0.14)

    # (a) symptoms
    ax = fig.add_subplot(gs[0, 0])
    bar_with_pct(ax, symptoms["domain"], symptoms["n"], COL_PARE, orient="h")
    ax.set_title("Symptoms in the past two weeks")
    ax.set_xlim(0, 110)
    ax.axvline(50, color=OI["grey"], lw=0.5, ls="--", zorder=0)
    add_panel_label(ax, "a", x=-0.30)

    # (b) QoL
    ax = fig.add_subplot(gs[0, 1])
    bar_with_pct(ax, qol["domain"], qol["n"], COL_PARE, orient="h")
    ax.set_title("Quality-of-life impact")
    ax.set_xlim(0, 110)
    ax.axvline(50, color=OI["grey"], lw=0.5, ls="--", zorder=0)
    add_panel_label(ax, "b", x=-0.30)

    fig.suptitle("Symptom burden and quality-of-life impact (parent report, n = 500)",
                 fontsize=9, fontweight="bold", y=0.99)
    save(fig, "fig2_symptoms_qol")


# ============================================================
# 5. FIGURE 3 — Dietary practice and barriers (double column)
# ============================================================
# Layout: 2 rows x 2 columns
#   (a) advice source   (b) diet type
#   (c) adherence       (d) barriers
# ============================================================

def figure_3():
    fig = plt.figure(figsize=(DOUBLE, 5.0))
    gs = GridSpec(2, 2, figure=fig, wspace=0.55, hspace=0.65,
                  left=0.20, right=0.97, top=0.90, bottom=0.10)

    # (a) advice source
    ax = fig.add_subplot(gs[0, 0])
    bar_with_pct(ax, advice_source["source"], advice_source["n"],
                 COL_PARE, orient="h")
    ax.set_title("Source of dietary advice")
    ax.set_xlim(0, 110)
    add_panel_label(ax, "a", x=-0.35)

    # (b) diet type
    ax = fig.add_subplot(gs[0, 1])
    bar_with_pct(ax, diet_type["diet"], diet_type["n"], COL_PARE, orient="h")
    ax.set_title("Diet followed")
    ax.set_xlim(0, 110)
    add_panel_label(ax, "b", x=-0.30)

    # (c) adherence
    ax = fig.add_subplot(gs[1, 0])
    bar_with_pct(ax, adherence["days"], adherence["n"], COL_PARE, orient="h")
    ax.set_title("Adherence (days per week)")
    ax.set_xlim(0, 110)
    add_panel_label(ax, "c", x=-0.35)

    # (d) barriers
    ax = fig.add_subplot(gs[1, 1])
    bar_with_pct(ax, barriers["barrier"], barriers["n"], COL_PARE, orient="h")
    ax.set_title("Reported barriers to adherence")
    ax.set_xlim(0, 110)
    add_panel_label(ax, "d", x=-0.35)

    fig.suptitle("Dietary practice and adherence barriers (parent report, n = 500)",
                 fontsize=9, fontweight="bold", y=0.99)
    save(fig, "fig3_dietary_practice")


# ============================================================
# 6. FIGURE 4 — Diagnostic testing (double column)
# ============================================================
# Layout: 1 row x 2 columns
#   (a) stacked horizontal bar of response frequencies
#   (b) same data as heatmap for direct comparison
# ============================================================

def figure_4():
    fig = plt.figure(figsize=(DOUBLE, 3.6))
    gs = GridSpec(1, 2, figure=fig, wspace=0.55,
                  left=0.20, right=0.95, top=0.86, bottom=0.22)

    # (a) stacked horizontal bars
    ax = fig.add_subplot(gs[0, 0])
    order = ["Always", "Often", "Sometimes", "Rarely", "Never"]
    colors = [OI["blue"], OI["sky"], OI["green"], OI["orange"], OI["vermillion"]]
    left = np.zeros(len(diagnostics))
    y = np.arange(len(diagnostics))
    for col, colr in zip(order, colors):
        vals = diagnostics[col].values
        ax.barh(y, vals, left=left, color=colr, edgecolor="white",
                linewidth=0.6, height=0.65, label=col)
        left += vals
    ax.set_yticks(y)
    ax.set_yticklabels(diagnostics.index)
    ax.invert_yaxis()
    ax.set_xlim(0, 500)
    ax.set_xlabel("Responses (n)")
    ax.set_title("Frequency of ordering")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22),
              ncol=5, frameon=False, fontsize=6)
    add_panel_label(ax, "a", x=-0.30)

    # (b) heatmap of percentages
    ax = fig.add_subplot(gs[0, 1])
    data = diagnostics.values.astype(float)
    data_pct = data / data.sum(axis=1, keepdims=True) * 100
    im = ax.imshow(data_pct, cmap="Blues", aspect="auto", vmin=0, vmax=100)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, rotation=35, ha="right")
    ax.set_yticks(range(len(diagnostics)))
    ax.set_yticklabels([])
    for i in range(data_pct.shape[0]):
        for j in range(data_pct.shape[1]):
            v = data_pct[i, j]
            ax.text(j, i, f"{v:.0f}", ha="center", va="center",
                    fontsize=6, color="white" if v > 55 else "black")
    ax.set_title("Percentage of responses")
    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.03)
    cbar.set_label("Respondents (%)", fontsize=6.5)
    cbar.ax.tick_params(labelsize=6)
    add_panel_label(ax, "b", x=-0.10)

    fig.suptitle("Diagnostic testing reported by clinicians (n = 500)",
                 fontsize=9, fontweight="bold", y=0.98)
    save(fig, "fig4_diagnostic_testing")


# ============================================================
# 7. FIGURE 5 — Computational analysis and thematic synthesis
# ============================================================
# Layout: 2 rows x 2 columns
#   (a) cluster sizes (bar)
#   (b) ML accuracy with 95% CI (forest-style)
#   (c) adherence effect (t-test summary as text + small bar)
#   (d) thematic mentions (horizontal bar)
# ============================================================

def figure_5():
    fig = plt.figure(figsize=(DOUBLE, 4.6))
    gs = GridSpec(2, 2, figure=fig, wspace=0.55, hspace=0.75,
                  left=0.16, right=0.97, top=0.90, bottom=0.10)

    # (a) clusters
    ax = fig.add_subplot(gs[0, 0])
    bars = ax.bar(clusters["cluster"], clusters["n"],
                  color=OI["purple"], edgecolor="black", linewidth=0.5)
    for b, n in zip(bars, clusters["n"]):
        ax.text(b.get_x() + b.get_width() / 2, n + 5,
                f"{n}\n({100*n/500:.1f}%)", ha="center", va="bottom", fontsize=6)
    ax.set_ylabel("Children (n)")
    ax.set_ylim(0, 260)
    ax.set_title("K-means clusters (k = 3)")
    add_panel_label(ax, "a")

    # (b) ML accuracy
    ax = fig.add_subplot(gs[0, 1])
    y = np.arange(len(ml_models))
    for i, row in ml_models.iterrows():
        ax.plot([row["ci_low"]*100, row["ci_high"]*100], [i, i],
                color=OI["blue"], lw=1.2)
        ax.plot(row["accuracy"]*100, i, "o",
                color=OI["blue"], markersize=6, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(ml_models["model"])
    ax.set_xlim(40, 65)
    ax.axvline(50, color=OI["grey"], lw=0.6, ls="--")
    ax.text(50.3, -0.45, "chance", fontsize=6, color=OI["grey"])
    ax.set_xlabel("Accuracy (%) with 95% CI")
    ax.set_title("Predicting adherence")
    add_panel_label(ax, "b")

    # (c) effect size summary
    ax = fig.add_subplot(gs[1, 0])
    ax.axis("off")
    lines = [
        "Diet effectiveness: high vs low adherence",
        "",
        f"t = {adherence_effect['t']:.2f}",
        f"p = {adherence_effect['p']:.2f}",
        f"Cohen's d = {adherence_effect['cohen_d']:.2f}",
        "",
        "Interpretation",
        "──────────────",
        "No meaningful difference",
        "between groups.",
        "Effect size is negligible.",
    ]
    ax.text(0, 1, "\n".join(lines), va="top", ha="left",
            fontsize=6.5, family="monospace", linespacing=1.5)
    ax.set_title("Statistical comparison")
    add_panel_label(ax, "c", x=-0.05)

    # (d) themes
    ax = fig.add_subplot(gs[1, 1])
    bars = ax.barh(themes["theme"], themes["mentions"],
                   color=OI["green"], edgecolor="black", linewidth=0.5)
    for b, n in zip(bars, themes["mentions"]):
        ax.text(n + 3, b.get_y() + b.get_height() / 2,
                f"{n}", va="center", ha="left", fontsize=6)
    ax.invert_yaxis()
    ax.set_xlabel("Mentions in open-ended responses")
    ax.set_xlim(0, 210)
    ax.set_title("Thematic analysis")
    add_panel_label(ax, "d", x=-0.45)

    fig.suptitle("Exploratory computational analysis and thematic synthesis",
                 fontsize=9, fontweight="bold", y=0.99)
    save(fig, "fig5_computational_analysis")


# ============================================================
# 8. Run all
# ============================================================

if __name__ == "__main__":
    print("Generating publication-quality figures ...")
    figure_1()
    figure_2()
    figure_3()
    figure_4()
    figure_5()
    print(f"Done. Files written to ./{OUTDIR}/")
