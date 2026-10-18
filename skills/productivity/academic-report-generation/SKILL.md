---
name: academic-report-generation
description: Use when creating academic practical reports from examples.
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [academic reports, DOCX, PDF, screenshots, reference matching]
    category: productivity
    related_skills: [docx, pdf]
---

# Academic Report Generation

Generate practical-course reports that match supplied examples in depth and structure while keeping student identity, data, results, and screenshots original.

## Always-On Rules

- Inspect reference documents before writing: page count, cover fields, chapter headings, paragraph density, embedded-image count, captions, tables, headers, and footers.
- Treat examples as layout and depth references only. Never copy their student identity, old data, old screenshots, old results, or source-specific claims.
- Create one standalone report per meeting when examples are one report per meeting. Do not collapse seven meeting reports into one combined file.
- Put exact user identity in every report. For this user: `Hidayathul Fikri`, `2411083008`, `D4 Teknologi Rekayasa Perangkat Lunak (TRPL)`, Semester 5, `Machine Learning`.
- Make each report meeting-specific: title, theory, methodology, code workflow, metrics, artifacts, discussion, conclusion, and screenshots must correspond to that meeting's actual program.
- Use executed program output for all numerical claims. Generate fresh screenshots from that execution; do not reuse screenshots from examples.
- Use a complete academic structure: cover, identity, BAB I Pendahuluan, BAB II Landasan Teori, BAB III Metodologi Praktikum, BAB IV Hasil dan Pembahasan, BAB V Kesimpulan, and figure captions.
- Match reference figure density. Split long terminal output into readable stage screenshots and place figures near the relevant discussion; one giant screenshot at the end is insufficient evidence.
- Keep DOCX as editable source. Generate PDF only after DOCX content is complete.

## Procedure

1. Inventory all reference DOCX/PDF files and group them by meeting. Extract text, page counts, heading outline, image counts, tables, cover identity fields, and caption patterns.
2. Inventory source programs and datasets. Map each meeting to its actual program, generated artifacts, outputs, metrics, and figures. Run programs in dependency order and capture exit status plus stderr.
3. Build fresh, readable evidence images from each program's output. Split output by logical stage or section, not arbitrary tiny fragments. Label every figure with meeting and stage.
4. Draft each meeting independently. Reuse global formatting, not body content. Include concrete output values and explain what they mean; omit unsupported claims.
5. Build DOCX with consistent page size, margins, typography, headings, cover, header/footer, captions, code/output blocks, and embedded images. Use short paragraphs and numbered/bulleted lists where examples do.
6. Render or convert each DOCX to PDF using a real document renderer when available. If unavailable, use a separately implemented PDF builder only when its text and image content can be re-read and validated; do not claim layout parity without visual inspection.
7. Verify every report independently: expected identity, meeting title, chapter headings, nonzero readable text, embedded-image count, expected artifact references, and page depth comparable to its reference. Count outputs programmatically, never by memory.
8. Report separate file paths for every DOCX and PDF, plus verification totals and any renderer limitation.

## Validation Checklist

- Seven requested meetings produce seven DOCX and seven PDF files.
- Each file contains `Hidayathul Fikri` and `2411083008`.
- Each report has its own meeting title and meeting-specific discussion.
- Each report embeds multiple relevant fresh screenshots where the reference uses figures.
- Old example identity, data, screenshots, and results are absent.
- DOCX reopens successfully; PDF text extraction finds identity and title.
- Page count and figure density are checked per report, not asserted from the combined set.

## Pitfalls

- Do not collapse multiple deliverables into one combined report; separate files are part of the format requirement.
- Do not use one generic paragraph set for every meeting; academic review detects copied or mismatched explanations.
- Do not infer visual similarity from text extraction alone; image density, captions, page breaks, and cover layout need structural and visual checks.
- Do not invent missing screenshots or results; rerun the source program or state the evidence gap.
- Do not silently substitute a short custom PDF for a reference-quality DOCX workflow; preserve an editable DOCX and disclose renderer limits.
