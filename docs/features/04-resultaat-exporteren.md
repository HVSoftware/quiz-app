# Feature: Export results (CSV / PDF)

## Problem
The user wants to keep a record of their quiz attempts — score, date, which
questions were wrong — to track improvement over time.

## Proposed solution
Add export buttons on the results screen:

### CSV export
- One row per attempt: `date, quiz_name, score, total, percentage, duration`.
- Optional detail rows: per question — `question, correct_answer, user_answer, result`.
- Downloaded automatically via Streamlit's `st.download_button`.

### PDF export (stretch goal)
- A formatted report with logo, score summary, and question review.
- Generated with `reportlab` or `fpdf2` (additional dependency).

## JSON impact
None.

## UI/UX impact
- **Results screen:** two buttons: "Download results (CSV)" and optionally
  "Download report (PDF)".
- CSV is generated on-the-fly from session state.

## Acceptance criteria
1. CSV includes at minimum: date, quiz name, score, total, percentage.
2. Optional detail CSV includes per-question rows.
3. File is named `quiz-{naam}-{date}.csv`.
4. No external services — everything is generated client-side.

## Priority
**Could** for v1.3.

## Dependencies
- Python `csv` module (stdlib) for CSV export.
- `fpdf2` or `reportlab` for PDF (optional).
- Accumulated answer data in session state.
