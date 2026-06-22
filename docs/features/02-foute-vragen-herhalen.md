# Feature: Wrong-answers review mode

## Problem
After completing a quiz, the user wants to retry only the questions they
answered incorrectly — without going through the entire set again.

## Proposed solution
Add a "Review wrong answers" button on the results screen:

1. Collect all incorrectly answered questions into a filtered list.
2. Start a new mini-quiz with just those questions.
3. Track if the user gets them right on the second attempt.
4. Optionally: continue until all questions are answered correctly (persistent mode).

## JSON impact
None — the data already exists.

## UI/UX impact
- **Results screen:** new button "Review X wrong answers" (X = number of errors).
- Works exactly like a normal quiz but with a subset of questions.
- The end screen of the review mode shows improvement: "Now X/Y correct."

## Acceptance criteria
1. Button only appears when there are wrong answers.
2. Questions are re-shuffled.
3. After review, show comparison: "First attempt: Z% / Review: W%".
4. User can return to the main results screen after review.

## Priority
**Should** for v1.2.

## Dependencies
- `st.session_state` needs a `fouten` list — populated during feedback.
- Could reuse the existing question loop with a filtered `vragen` list.
