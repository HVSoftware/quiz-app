# Design Decisions — Quiz App

## Overview

A lightweight, interactive quiz application built with [Streamlit](https://streamlit.io).
Loads question banks from local JSON files and presents them as a multiple-choice quiz
with instant feedback, scoring, and per-domain results.

---

## Why Streamlit?

| Approach     | Pros                                          | Cons                                          |
| ------------ | --------------------------------------------- | --------------------------------------------- |
| **Streamlit** | Single Python file, no build step, hot-reload | Limited layout control                        |
| Flask+HTML   | Full control over UI                          | Requires HTML/CSS/JS, more boilerplate        |
| React         | Rich interactivity, component ecosystem       | npm build step, JSX, state management overhead |
| Static HTML/JS | Zero server deps, works offline               | No server-side persistence, more JS code      |

**Chosen:** Streamlit — fastest path from JSON to interactive quiz with zero front-end
experience needed.

---

## Data model

### Question schema

```json
{
  "vraag": "Question text",
  "opties": ["Option A", "Option B", "Option C", "Option D"],
  "antwoord": 2,
  "domein": "Cloud Concepts",
  "toelichting": "Explanation shown after answering"
}
```

| Field        | Type            | Required | Description                          |
|-------------|-----------------|----------|--------------------------------------|
| `vraag`      | `string`        | yes      | Question text (Markdown supported)   |
| `opties`     | `array[string]` | yes      | At least 2 answer choices            |
| `antwoord`   | `integer`       | yes      | 0-based index into `opties`          |
| `domein`     | `string`        | no       | Domain category for result breakdown |
| `toelichting` | `string`       | no       | Explanation shown after answering    |

### File format

- Each file is a JSON **array** of question objects (`[]`).
- Files are auto-discovered in `../Exams/` and `../Modules/` via `scan_quiz_files()`.
- File name becomes the quiz label without `quiz-` prefix (e.g. `quizzes/quiz-az900-practice-v2.json` → `az900-practice-v2`), and duplicates are auto-numbered (`name`, `name (2)`, ...).

### Validation rules (`load_quiz`)

- Root must be a non-empty array.
- Every question must contain `vraag`, `opties`, `antwoord`.
- `vraag` must be a non-empty string.
- `opties` must be a list with ≥2 items.
- `antwoord` must be a valid 0-based index within `opties`.
- On failure: `ValueError` is raised and shown to the user in the sidebar.

---

## Session state architecture

All state lives in `st.session_state`. No database, no files — data is ephemeral.

| Key                | Type      | Description                             |
|--------------------|-----------|------------------------------------------|
| `vragen`            | `list`    | Loaded question objects                  |
| `index`             | `int`     | Current question index (0-based)         |
| `score`             | `int`     | Number of correct answers                |
| `beantwoord`        | `bool`    | Has the current question been submitted? |
| `keuze`             | `int`     | The option index the user selected       |
| `voltooid`          | `bool`    | All questions answered                   |
| `start_tijd`        | `datetime` | When the quiz was started               |
| `score_bijgewerkt`  | `bool`    | Prevents double-counting on rerun        |
| `quiz_gestart`      | `bool`    | Is a quiz in progress?                   |
| `quiz_label`        | `str`     | Currently selected quiz label            |
| `aantal`            | `int`     | Number of questions to ask               |
| `shuffle`           | `bool`    | Shuffle toggle                           |

### State flow

```
Start screen ──[Start quiz]──> init_state() ──> Question loop
                                                    │
                                          ┌─────────┴─────────┐
                                          │                   │
                                     Submit answer      Last question
                                          │                   │
                                     Show feedback      toon_eindscherm()
                                          │                   │
                                      [Next →]          [Start new quiz]
                                          │                   │
                                     index++               _reset_quiz()
                                          │                   │
                                          └───────────────────┘
```

---

## Component architecture

```
main()
├── scan_quiz_files()       — discover JSON files in watch dirs
├── toon_sidebar()          — sidebar: quiz selection + settings
│   ├── Start button ── _start_quiz()
│   │   ├── load_quiz()    — load & validate JSON
│   │   └── init_state()   — reset session state
│   └── Score overzicht    — live score (during quiz)
├── toon_vraag()           — progress + question + radio + feedback
│   ├── Answer → feedback
│   └── Next → index++
└── toon_eindscherm()      — final score + restart
```

### Function responsibilities

| Function            | Responsibility                            | SOLID principle |
|---------------------|-------------------------------------------|-----------------|
| `scan_quiz_files`    | Discovers JSON files in configured dirs   | Single responsibility |
| `load_quiz`          | Reads & validates JSON structure          | Single responsibility, Open/closed |
| `init_state`         | (Re)sets all session state keys           | — |
| `toon_sidebar`       | Renders sidebar with selection & settings | Single responsibility |
| `toon_vraag`         | Renders current question + handles answer | Single responsibility |
| `toon_eindscherm`    | Renders results + restart button          | Single responsibility |
| `main`               | Orchestrates the flow based on state      | Dependency inversion (calls abstractions) |

---

## Edge cases & error handling

| Scenario                      | Handling                                   |
|------------------------------|--------------------------------------------|
| No quiz files found           | Warning message on welcome screen          |
| Malformed JSON                | `try/except` in `_start_quiz`, error shown |
| Missing required fields       | `ValueError` during `load_quiz` validation |
| Empty question list           | `ValueError`: "Quiz is empty."             |
| Single-option question        | Validation rejects <2 options              |
| Invalid `antwoord` index      | Validation rejects out-of-range index      |
| Page reload during quiz       | Session state resets → start screen        |
| All questions answered        | `toon_eindscherm()` triggered automatically |

---

## Security

- The app runs **locally only** (`localhost:8501` by default).
- No data is sent to external servers.
- Quiz files are read-only; the app never writes to them.
- No authentication required — this is a single-user local tool.

---

## Performance

- JSON files are typically <500 KB — load time is negligible.
- No external API calls or database queries.
- Streamlit reruns the entire script on each interaction — use `st.session_state`
  to avoid redundant work. This is acceptable for <200 questions.

---

## Future extensions (see `docs/features/`)

1. Domain breakdown in results (partial — pie chart, per-domain score)
2. Wrong-answers-only review mode (spaced repetition)
3. Exam mode (feedback only at the end)
4. Export results (CSV / PDF download)
5. Time tracking per question
6. Mixed quiz from multiple JSON files
7. Session persistence across reloads
