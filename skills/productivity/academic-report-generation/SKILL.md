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

- Inspect reference documents before writing: page count, cover fields, chapter headings, paragraph density, embedded-image count, captions, tables, headers, and footers. For PDF examples, extract text and inspect rendered cover before reproducing its hierarchy, logo, spacing, and typography.
- Treat examples as layout and depth references only. Never copy their student identity, old data, old screenshots, old results, or source-specific claims. For interview or proposal documents, distinguish supplied facts from suggested responses; label unverified answers prominently as drafts, not actual partner testimony. Keep title, cover subtitle, body, and diagrams centered on the project's primary deliverable; present speculative integrations as optional future scope rather than making one proposed feature the thesis.
- Create one standalone report per meeting when examples are one report per meeting. Do not collapse seven meeting reports into one combined file.
- Put the user's exact identity in every document: `Hidayathul Fikri` (`2411083008`). Derive course, program, semester, institution, and instructor from the current request or source; do not copy a reference student's identity or assume every document is for Machine Learning.
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
5. Build DOCX with consistent page size, margins, typography, headings, cover, header/footer, captions, code/output blocks, and embedded images. Use short paragraphs and numbered/bulleted lists where examples do. For cover-only revisions, edit the existing document instead of rebuilding it: preserve the logo and body, adjust cover paragraphs in place, then compare the body paragraph text before/after and validate the DOCX package. Inspect actual rendered cover before delivery; paragraph counts and package validation cannot reveal a cover pushed off-page by cumulative spacing. For phone reading, provide a fixed-layout PDF alongside the editable DOCX and inspect its rendered first page.
6. Render or convert each DOCX to PDF using a real document renderer when available. If unavailable, use a separately implemented PDF builder only when its text and image content can be re-read and validated; do not claim layout parity without visual inspection. When the source is an example PDF, reuse its cover page only when permitted and replace sample-specific text without changing its logo or unrelated metadata; inspect the rendered result and re-extract its text.
7. Verify every report independently: expected identity, meeting title, chapter headings, nonzero readable text, embedded-image count, expected artifact references, and page depth comparable to its reference. Count outputs programmatically, never by memory.
8. Report separate file paths for every DOCX and PDF, plus verification totals and any renderer limitation.

### Project documentation (proposal, SRS, interview, ERD, use case)

1. Read the current proposal and all supplied examples first. Extract example structure and render its cover; distinguish reference layout from reference domain, person, and invented claims. Compare scope against the latest approved proposal before drafting diagrams, requirements, or presentation slides. If a design link is inaccessible, use only the supplied screenshot, caption it as a partial view, and do not claim to have reviewed the full prototype.
2. Mark facts provided by the user separately from unconfirmed interview details. Draft interview answers as examples, not testimony. In SRS, make each functional requirement testable with acceptance criteria; record optional modules outside the core scope instead of promising them in prose or diagrams.
3. Make use cases actor goals inside a system boundary; associate only roles that truly use each function. Use `«include»`/`«extend»` only with proper UML direction and semantics, not to show step order. Model ERD cardinalities from actual nullable/unique FK constraints: a nullable FK permits zero-or-one parent, a unique child FK permits zero-or-one child. Avoid storing customer measurements as mutable shared data when they are snapshots of individual orders.
4. Verify diagram geometry after rendering: lines must connect at correct card/oval edges without crossing labels, each constraint badge must fit, and legend must agree with dashed/optional relationships. On presentation slides, split a dense ERD into legible segments with explicit FK references rather than shrinking a full-page diagram until field names become unreadable; keep the complete ERD as a separate artifact. Render and inspect the cover and at least a content page of each document; Word package validity and text extraction alone cannot prove mobile legibility or prevent a cover from splitting.
5. Fit appendix diagrams and prototype screenshots to both available page width and height while preserving aspect ratio; use an A4 landscape page for wide evidence, add a caption/source, and render every appendix page to check clipping and print legibility. A screenshot of the opening viewport is evidence of that view only, not the full site. If a true DOCX-to-PDF renderer is unavailable, produce a separately laid out PDF from the same approved content and inspect it; do not imply pixel-identical conversion. A PDF is useful for fixed-layout viewing on phones while DOCX remains editable.

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
