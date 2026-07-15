#!/usr/bin/env python3
"""Streamlit quiz app — load JSON quizzes and play them interactively.

Usage:
    streamlit run app.py
"""

import json
import random
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

QUIZ_DIRS = [
    Path(__file__).resolve().parent / "quizzes",
]

REQUIRED_FIELDS = {"vraag", "opties", "antwoord"}
OPTIONAL_FIELDS = {"toelichting", "domein"}


# ---------------------------------------------------------------------------
# Quiz loading
# ---------------------------------------------------------------------------


def scan_quiz_files() -> dict[str, Path]:
    """Scan QUIZ_DIRS for * .json files and return {label: path}."""
    files: dict[str, Path] = {}
    label_counts: dict[str, int] = {}
    for d in QUIZ_DIRS:
        if not d.exists():
            continue
        for fp in sorted(d.rglob("*.json")):
            label_base = fp.stem.removeprefix("quiz-")
            count = label_counts.get(label_base, 0) + 1
            label_counts[label_base] = count
            label = label_base if count == 1 else f"{label_base} ({count})"
            i = count + 1
            while label in files:
                label = f"{label_base} ({i})"
                i += 1
            files[label] = fp
    return files


def load_quiz(path: Path) -> list[dict]:
    """Load and validate a quiz JSON file.

    Returns a list of question dicts.
    Each question must have: vraag (str), opties (list[str]), antwoord (int).
    May have: toelichting (str), domein (str).

    Raises ValueError on structural errors.
    """
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("JSON root must be an array of questions.")
    if not raw:
        raise ValueError("Quiz is empty.")

    for i, q in enumerate(raw, 1):
        missing = REQUIRED_FIELDS - q.keys()
        if missing:
            raise ValueError(f"Question {i} is missing fields: {missing}")
        if not isinstance(q["vraag"], str) or not q["vraag"].strip():
            raise ValueError(f"Question {i}: 'vraag' must be a non-empty string.")
        if not isinstance(q["opties"], list) or len(q["opties"]) < 2:
            raise ValueError(f"Question {i}: 'opties' must be a list with ≥2 items.")
        if not isinstance(q["antwoord"], int) or not (0 <= q["antwoord"] < len(q["opties"])):
            raise ValueError(f"Question {i}: 'antwoord' must be a valid 0-based index.")
    return raw


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------


def init_state(vragen: list[dict]) -> None:
    """Initialise or reset session state for a new quiz."""
    st.session_state.vragen = vragen
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.beantwoord = False
    st.session_state.keuze = None
    st.session_state.voltooid = False
    st.session_state.start_tijd = datetime.now()
    st.session_state.quiz_gestart = True


def _get(key: str, default=None):
    """Safely get a session_state value (handles missing keys)."""
    return st.session_state.get(key, default)


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------


def toon_sidebar(quiz_files: dict[str, Path]) -> None:
    """Render the sidebar with quiz selection and settings."""
    with st.sidebar:
        st.header("Quiz App")
        st.caption("AZ-900 & Networking practice exams")
        st.divider()

        if not quiz_files:
            st.error("No quiz files found.")
            return

        labels = list(quiz_files.keys())
        idx = labels.index(st.session_state.get("quiz_label", labels[0])) if st.session_state.get("quiz_label") in labels else 0  # fmt: skip
        gekozen = st.selectbox("Choose a quiz", labels, index=idx, key="quiz_label")

        st.session_state.aantal = st.slider(
            "Number of questions",
            min_value=5,
            max_value=100,
            value=min(20, 100),
            step=5,
        )

        st.session_state.shuffle = st.checkbox("Shuffle questions", value=True)

        if st.button("Start quiz", type="primary", use_container_width=True):
            _start_quiz(quiz_files[gekozen])

        st.divider()
        if _get("quiz_gestart", False):
            toon_score_overzicht()
            if st.button("Stop & restart", use_container_width=True):
                _reset_quiz()


def _start_quiz(path: Path) -> None:
    """Load questions, apply settings, and initialise state."""
    try:
        vragen = load_quiz(path)
    except (json.JSONDecodeError, ValueError, OSError) as exc:
        st.error(f"Failed to load quiz: {exc}")
        return

    if st.session_state.shuffle:
        random.shuffle(vragen)

    aantal = st.session_state.aantal
    if 0 < aantal < len(vragen):
        vragen = vragen[:aantal]

    init_state(vragen)


def _reset_quiz() -> None:
    """Clear session state to return to the start screen."""
    for key in ("vragen", "index", "score", "beantwoord", "keuze", "voltooid", "start_tijd", "quiz_gestart"):
        st.session_state.pop(key, None)


def toon_score_overzicht() -> None:
    """Show a live score summary in the sidebar."""
    vragen = _get("vragen", [])
    totaal = len(vragen)
    score = _get("score", 0)
    index = _get("index", 0)

    st.metric("Score", f"{score}/{totaal}")
    pct = (score / totaal * 100) if totaal else 0
    st.progress(pct / 100, text=f"{pct:.0f}%")

    if st.session_state.get("voltooid", False):
        st.success(f"**Completed!**")
        from datetime import datetime
        duur = datetime.now() - st.session_state.start_tijd
        st.caption(f"Time: {int(duur.total_seconds() // 60)}m {int(duur.total_seconds() % 60)}s")
    else:
        st.caption(f"Question {min(index + 1, totaal)}/{totaal}")


def toon_vraag() -> None:
    """Display the current question and handle answer selection + feedback."""
    vragen = st.session_state.vragen
    totaal = len(vragen)
    i = st.session_state.index

    if i >= totaal:
        toon_eindscherm()
        return

    q = vragen[i]
    beantwoord = st.session_state.beantwoord

    # Progress
    st.progress((i + 1) / totaal, text=f"Question {i + 1} of {totaal}")
    st.divider()

    # Domain badge
    if q.get("domein"):
        st.caption(f"**{q['domein']}**")

    # Question text
    st.markdown(f"### {q['vraag']}")

    # Options
    opties = q["opties"]
    disabled = beantwoord
    keuze = st.radio(
        "Select your answer:",
        range(len(opties)),
        format_func=lambda x: opties[x],
        index=None,
        key=f"radio_{i}",
        disabled=disabled,
        label_visibility="collapsed",
    )

    # Submit button
    col1, col2 = st.columns([1, 5])
    with col1:
        verstuurd = st.button(
            "Submit",
            type="primary",
            disabled=beantwoord or keuze is None,
            use_container_width=True,
        )

    if verstuurd and keuze is not None:
        st.session_state.keuze = keuze
        st.session_state.beantwoord = True
        st.rerun()

    # --- Feedback (shown after submission) ---
    if beantwoord:
        keuze_gemaakt = st.session_state.keuze
        juist = keuze_gemaakt == q["antwoord"]

        if juist:
            st.success("**Correct!**")
        else:
            st.error(f"**Wrong.** Correct answer: **{opties[q['antwoord']]}**")

        # Update score
        if juist and not st.session_state.get("score_bijgewerkt", False):
            st.session_state.score += 1
            st.session_state.score_bijgewerkt = True

        # Next button (placed here so the user doesn't have to scroll past the answers)
        st.divider()
        if st.button("Next →", type="secondary", use_container_width=False):
            st.session_state.score_bijgewerkt = False
            st.session_state.index += 1
            st.session_state.beantwoord = False
            st.session_state.keuze = None
            if st.session_state.index >= totaal:
                st.session_state.voltooid = True
            st.rerun()

        # Highlight options with colour
        for idx, optie in enumerate(opties):
            if idx == q["antwoord"]:
                st.markdown(f":green-background[**{optie}**]  *(correct)*")
            elif idx == keuze_gemaakt and not juist:
                st.markdown(f":red-background[~~{optie}~~]  *(your choice)*")
            else:
                st.markdown(optie)

        # Explanation
        if q.get("toelichting"):
            with st.expander("Explanation", expanded=True):
                st.info(q["toelichting"])


def toon_eindscherm() -> None:
    """Show the final results screen after all questions are answered."""
    st.balloons()
    totaal = len(st.session_state.vragen)
    score = st.session_state.score
    pct = (score / totaal * 100) if totaal else 0

    st.markdown("## Quiz Complete!")
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Correct", score)
    col2.metric("Total", totaal)
    col3.metric("Score", f"{pct:.0f}%")

    duur = datetime.now() - st.session_state.start_tijd
    st.caption(f"Time taken: {int(duur.total_seconds() // 60)}m {int(duur.total_seconds() % 60)}s")

    st.progress(pct / 100)

    if pct >= 80:
        st.success("Excellent! You're well prepared.")
    elif pct >= 60:
        st.warning("Good, but review the topics you missed.")
    else:
        st.error("More study needed. Focus on your weak domains.")

    # Per-domain breakdown
    domeinen = {}
    for q in st.session_state.vragen:
        d = q.get("domein", "Uncategorised")
        domeinen.setdefault(d, {"totaal": 0, "goed": 0})
    # We need to track per-domain score — we only have total score in state.
    # For now, show per-domain distribution.
    from collections import Counter
    domein_telling = Counter(q.get("domein", "Uncategorised") for q in st.session_state.vragen)
    if len(domein_telling) > 1:
        st.divider()
        st.markdown("### Domain breakdown")
        for d, count in domein_telling.most_common():
            st.caption(f"{d}: {count} questions")

    st.divider()
    if st.button("Start new quiz", type="primary"):
        _reset_quiz()
        st.rerun()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Entry point: render sidebar and question or end screen."""
    st.set_page_config(
        page_title="Quiz App",
        page_icon="",
        layout="centered",
    )

    quiz_files = scan_quiz_files()
    toon_sidebar(quiz_files)

    if _get("quiz_gestart", False):
        if _get("voltooid", False):
            toon_eindscherm()
        else:
            toon_vraag()
    else:
        # Welcome screen
        st.markdown("## Welcome to the Quiz App")
        st.markdown(
            """
            Load practice exams from JSON files and test your knowledge.

            **How to use:**
            1. Select a quiz from the sidebar.
            2. Choose the number of questions and toggle shuffle.
            3. Click **Start quiz**.
            4. Answer each question and review the explanation.
            5. See your final score at the end.
            """
        )
        if not quiz_files:
            st.warning("No quiz files found. Add JSON files to the `Exams/` or `Modules/` directory.")


if __name__ == "__main__":
    main()
