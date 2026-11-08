---
name: survey-instrument-analysis
description: Use when testing survey validity and reliability data.
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [survey, statistics, validity, reliability, cronbach-alpha, likert, jupyter, questionnaire]
    category: productivity
---

# Survey Instrument Analysis

Perform statistical instrument testing (validity, reliability, Likert scale normalization, Cronbach's Alpha) on questionnaire datasets and generate high-resolution visual evidence reports.

## Always-On Rules

- Never rely on static positional index slicing (e.g. `df.columns[9:24]`) to group indicator columns. Survey spreadsheets frequently contain interleaved `Total_X` sum columns, metadata, or variable item counts that differ from draft templates. Always filter item columns dynamically by prefix or regex pattern (e.g. `[c for c in df.columns if str(c).startswith('X1.')]`) and explicitly exclude summary or total columns.
- Normalize Likert scale responses robustly before numerical analysis: parse leading digits first (e.g. `'5 - Sangat Setuju'` -> `5`), map standard textual scales (`'Sangat Setuju'` -> `5`, `'Setuju'` -> `4`, `'Netral'` -> `3`, `'Tidak Setuju'` -> `2`, `'Sangat Tidak Setuju'` -> `1`), and drop rows with incomplete responses across indicator sets (`dropna(subset=all_item_cols)`).
- Calculate critical correlation thresholds ($r_{\text{tabel}}$) dynamically using the Student's $t$-distribution quantile with degrees of freedom $df = n - 2$ at $\alpha = 0.05$ two-tailed:
  ```python
  df_res = n - 2
  t_val = stats.t.ppf(1 - alpha / 2, df_res)
  r_table = round(t_val / np.sqrt(t_val**2 + df_res), 4)
  ```
  Never hardcode static table values, ensuring threshold accuracy across varying sample sizes $n$.
- Distinguish between Corrected Item-Total Correlation (korelasi butir dengan total skor tanpa butir itu sendiri, $r_{i(t-i)}$) and Standard Pearson Product Moment ($r_{ix}$). In survey instrument testing, corrected item-total correlation prevents self-correlation inflation:
  ```python
  korelasi_corrected = [
      data[item].corr(data[[c for c in cols if c != item]].sum(axis=1))
      for item in cols
  ]
  ```
- Compute Cronbach's Alpha reliability using item variances and total composite score variance:
  $$\alpha = \frac{k}{k - 1} \left(1 - \frac{\sum s_i^2}{s_t^2}\right)$$
  Classify thresholds: $\alpha \ge 0.9$ (Sangat Tinggi), $0.8 \le \alpha < 0.9$ (Tinggi), $0.6 \le \alpha < 0.8$ (Cukup / Reliabel), $\alpha < 0.6$ (Tidak Reliabel).
- Execute Jupyter notebooks headlessly using `uv run --with jupyter --with nbconvert --with pandas --with scipy` and `ExecutePreprocessor` to ensure outputs and Styler tables persist into the `.ipynb` file.
- Generate high-resolution visual evidence screenshots of styled DataFrame outputs: convert notebook to HTML via `nbconvert --to html` and screenshot individual table elements using Playwright with local Chrome (`device_scale_factor=2`) rather than capturing raw console logs or distorted matplotlib dumps. Deliver images natively with `MEDIA:/absolute/path/to/image.png`.

## Procedure

1. **Dataset & Question Inventory:**
   - Inspect spreadsheet structure with pandas / openpyxl: inspect sheet names, column names, respondent count, and data types.
   - Identify demographic columns, indicator columns per variable ($X_1, X_2, \dots, Y$), and any pre-existing total/score columns.
2. **Column Extraction & Preprocessing:**
   - Filter indicator columns per variable group using string prefix filtering (`startswith('X1.')`, `startswith('X2.')`, `startswith('Y.')`).
   - Apply Likert conversion to numeric integers 1–5. Drop rows containing nulls across evaluated indicators to obtain clean sample size $n$.
3. **Validity Testing:**
   - Calculate degrees of freedom $df = n - 2$ and exact $r_{\text{tabel}}$ via `scipy.stats.t.ppf`.
   - Calculate item correlations. Mark each item `Valid` if $r_{\text{hitung}} > r_{\text{tabel}}$, otherwise `Tidak Valid`.
   - Format results into a styled DataFrame with indicator code, question prompt snippet, $r_{\text{hitung}}$, $r_{\text{tabel}}$, and color-coded status badges.
4. **Reliability Testing:**
   - Compute Cronbach's Alpha for each variable dimension.
   - Map alpha scores to qualitative reliability categories.
   - Format summary table with variable name, indicator count, Cronbach's Alpha, and reliability status.
5. **Headless Execution & Evidence Capture:**
   - Update notebook source to make file paths resilient (check for target Excel filename first, fallback to `data.xlsx`).
   - Run `ExecutePreprocessor` to populate cell outputs within `.ipynb`.
   - Convert `.ipynb` to `.html` via `nbconvert`.
   - Run a headless Playwright script to screenshot rendered HTML tables at 2x DPI with clean CSS padding and borders.
6. **Delivery:**
   - Store screenshots under the course/project screenshot directory (`screenshots/`).
   - Send concise numerical summary and deliver screenshots using `MEDIA:/absolute/path/to/screenshot.png`.

## Pitfalls

- Hardcoded column index slicing (e.g. `df.columns[9:24]`) breaks whenever surveys add respondent metadata or include `Total_X` columns in the Excel file; always filter by variable prefixes.
- Omitting Likert text conversion causes correlation calculations to fail or return NaN silently when survey answers contain text descriptions.
- Exporting pandas Styler tables via `dataframe_image` with matplotlib backend frequently distorts cell alignments, truncates wide text, and drops table boundaries; use Playwright headless HTML element screenshots for pixel-perfect report tables.
