# Feature: Domain breakdown in results

## Status
✅ Implemented (basic — shows question count per domain).

## Problem
The user finishes a quiz and sees only a total score — no insight into
which subject areas (domains) they are strong or weak in.

## Proposed solution
After the quiz ends, show a per-domain breakdown:

- Total questions per domain
- Correct answers per domain
- Percentage per domain
- Visual indicator (progress bar or pie chart)

## JSON impact
Each question must have a `domein` field with a string value
(e.g. `"Cloud Concepts"`, `"Azure Architecture and Services"`,
`"Azure Management and Governance"`).

## UI/UX impact
- **Results screen:** add a section "Domain breakdown" below the total score.
- For each domain: domain name + `X/Y correct (Z%)` + a small progress bar.
- Optionally: sort by weakest domain first.

## Acceptance criteria
1. Questions without a `domein` field are grouped under "Uncategorised".
2. Domains are sorted by performance (lowest % first).
3. Each domain row shows a coloured progress bar.

## Priority
**Must** for v1.1 — currently shows only counts, not per-domain correct scores.
Full implementation requires tracking per-domain score in session state.

## Dependencies
- `st.session_state` needs a `domein_score` dict: `{domein: {totaal: N, goed: M}}`.
- Updated in the feedback loop alongside `st.session_state.score`.
