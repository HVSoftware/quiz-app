# Feature: Mixed quiz (multiple JSON files)

## Problem
The user has multiple quiz JSONs (e.g. AZ-900, Networking, Security) and
wants to draw questions from several at once for a comprehensive practice
session.

## Proposed solution
Allow multi-select of quiz files in the sidebar:

1. Replace the single-select dropdown with a multi-select widget.
2. When multiple quizzes are selected, pool all questions together.
3. Apply shuffle + truncation over the combined pool.
4. Show a label: "Mixed quiz: AZ-900 + Networking" or similar.

## JSON impact
None.

## UI/UX impact
- **Sidebar:** dropdown becomes multi-select checkboxes or a multiselect widget.
- **Label:** "Mixed ({N} quizzes)" when >1 selected.
- **Results screen:** show per-quiz breakdown alongside per-domain.
- The distinction between questions from different source files is visible
  in the review (e.g. "AZ-900 — Q3").

## Acceptance criteria
1. Selecting 0 quizzes shows a warning.
2. Selecting 1 quiz behaves exactly like the current single-select.
3. Selecting 2+ pools all questions, domain tags are preserved.
4. Truncation and shuffle work over the combined set.
5. Results show per-source breakdown.

## Priority
**Could** for v1.3.

## Dependencies
- `toon_sidebar()` widgets need to change from `st.selectbox` to
  `st.multiselect` or a set of checkboxes.
- `_start_quiz()` needs to accept multiple paths and merge them.
- Results screen needs per-source breakdown.
