# Feature: Progress persistence across reloads

## Problem
If the user accidentally refreshes the page or closes the browser tab,
all progress is lost — session state is ephemeral.

## Proposed solution
Persist the quiz state to the browser's `localStorage` via Streamlit's
`st.query_params` or a custom JavaScript component:

### Approach A — `st.query_params` (limited)
Encode the current state (index, score, answers) as URL parameters.
On reload, restore from query params. Limitations: URL length cap (~2 KB).

### Approach B — Local storage via a custom component
Write a small Streamlit component (or use `st.markdown` with an HTML/JS
bridge) to read/write `localStorage`. More robust for larger state.

### Approach C — Server-side file
Write a temporary JSON file to disk with the session state.
Simple but creates clutter and doesn't survive across machines.

## JSON impact
None.

## UI/UX impact
- **Sidebar:** small indicator: "Progress saved" / "Restored from last session".
- **On reload:** the app shows a toast or info box: "Found a saved quiz.
  Click 'Resume' to continue or 'Start new' to begin again."
- **After completion:** saved state is cleared.

## Acceptance criteria
1. Refreshing the page mid-quiz shows a resume prompt.
2. Resuming restores: current question index, score, answers so far.
3. Saved state is cleared after the quiz is completed or explicitly discarded.
4. Works across browser sessions (localStorage persists until cleared).

## Priority
**Won't** for v1 — adds complexity and fragility. Re-evaluate if users
frequently report lost progress.

## Dependencies
- Custom JavaScript component or `st.components.v1.html` bridge.
- Must handle serialisation/deserialisation of `st.session_state` safely.
- `st.query_params` approach is simpler but limited — test URL size first.
