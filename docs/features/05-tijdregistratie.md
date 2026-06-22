# Feature: Time tracking

## Problem
The user wants to know how long they spent on a quiz — total time and,
ideally, time per question — to gauge their pacing for the real exam.

## Proposed solution

### Phase 1: Total time (✅ partially implemented)
Show total elapsed time on the results screen.

### Phase 2: Per-question timing
Track how long the user spends on each individual question and show it
in the review.

### Phase 3: Countdown timer (exam mode)
Show a countdown timer during exam mode (e.g. 85 minutes for AZ-900).

## JSON impact
None.

## UI/UX impact
- **Sidebar:** show elapsed time during the quiz: "Elapsed: 12m 34s".
- **Results screen:** "Time taken: 12m 34s".
- **Per-question (Phase 2):** "Question 5 — 45s" in a review list.
- **Countdown (Phase 3):** visible timer in the sidebar, warning colour
  when <10 minutes remain, auto-submit when time runs out.

## Acceptance criteria
1. Total time is accurate to the second.
2. Timer survives Streamlit reruns (stored in session_state).
3. Per-question timing shows reasonable values (not including idle time).
4. Countdown mode triggers a warning at 10 minutes.

## Priority
**Could** for v1.3.

## Dependencies
- Phase 1: already uses `datetime.now()` in `st.session_state.start_tijd`.
- Phase 2: needs `start_tijd_per_vraag` in session state.
- Phase 3: requires `st.empty()` + `time.sleep()` or `st.rerun()` loop for
  real-time countdown. Streamlit's rerun model makes real-time clocks tricky.
