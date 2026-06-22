# Feature: Exam mode (feedback at the end)

## Problem
In study mode, seeing the correct answer immediately makes it too easy —
the user wants a realistic exam simulation where results are only shown
after all questions are answered.

## Proposed solution
Add an **Exam mode** toggle in the sidebar (next to Shuffle):

- **Study mode** (default): instant feedback per question — current behaviour.
- **Exam mode**: no feedback during the quiz. The user answers all questions,
  then sees the full results + per-question review on the results page.

## JSON impact
None.

## UI/UX impact
- **Sidebar:** checkbox "Exam mode (show results at the end)".
- **During quiz (exam mode):**
  - Submit button changes to "Save answer".
  - No green/red feedback, no explanation expander.
  - After submit, the next question appears immediately.
  - A small counter shows "Answered: X/Y".
- **Results page (exam mode):**
  - Show total score.
  - Show a collapsible review list: each question with submitted answer,
    correct answer, and explanation.
  - Allow filtering: all / correct / wrong.

## Acceptance criteria
1. Toggling exam mode mid-quiz resets the quiz (to prevent confusion).
2. Exam mode disables shuffle by default (optional, can be overridden).
3. On results page, every question is reviewable with correct/incorrect marking.
4. Timer (if implemented) should be visible during exam mode.

## Priority
**Should** for v1.2.

## Dependencies
- `st.session_state` needs an `antwoorden` list storing `{index, keuze, juist}` for review.
- The UI flow in `toon_vraag()` needs a branch for exam mode.
