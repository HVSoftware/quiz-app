# User Guide — Quiz App

## Installation

### Prerequisites

- Python 3.10+
- pip (Python package manager)

### Setup

```bash
cd QuizApp
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### Start the app

```bash
.venv/bin/streamlit run app.py
```

Or use the helper script:

```bash
./run.sh
```

Open your browser at **http://localhost:8501**.

---

## How to use

### 1. Select a quiz

In the **sidebar** on the left, choose a quiz from the dropdown menu.
Available quizzes are auto-discovered from the `Exams/` and `Modules/` directories.

### 2. Configure settings

- **Number of questions** — use the slider to limit how many questions you want (min 5, max 100).
- **Shuffle questions** — tick the box to randomise the order.

### 3. Start

Click **Start quiz** to begin.

### 4. Answer a question

- Read the question text.
- Click one of the radio buttons to select your answer.
- Click **Submit**.

### 5. See feedback

After submission:

- **Correct** — the answer is highlighted in green.
- **Wrong** — your choice is struck through in red; the correct answer is shown in green.
- **Explanation** — expand the *Explanation* section to read why the answer is correct.

Click **Next →** to move to the next question.

### 6. Track your progress

The sidebar shows:

- Live score: `X/Y`
- Progress bar with percentage
- Current question number

### 7. Finish

After the last question, the **results screen** shows:

- Total correct / total questions
- Percentage score
- Time taken
- A summary message based on your score
- Domain breakdown (if questions have domain categories)

Click **Start new quiz** to begin again.

### 8. Stop mid-quiz

Click **Stop & restart** in the sidebar at any time to abandon the current quiz
and return to the welcome screen.

---

## Adding a new quiz

1. Create a JSON file following the format below.
2. Place it in the `Exams/` directory (or a subdirectory).
3. Restart the app — it will appear in the dropdown automatically.

### JSON format

```json
[
  {
    "vraag": "What is cloud computing?",
    "opties": [
      "Storing files on remote servers only",
      "Delivering computing services over the internet on a pay-as-you-go basis",
      "Running software applications on a local machine"
    ],
    "antwoord": 1,
    "domein": "Cloud Concepts",
    "toelichting": "Cloud computing is the delivery of computing services over the internet with pay-as-you-go pricing."
  }
]
```

| Field        | Required | Description                            |
|-------------|----------|----------------------------------------|
| `vraag`      | yes      | Question text                          |
| `opties`     | yes      | Array of answer choices (≥2)           |
| `antwoord`   | yes      | Index of the correct answer (0-based)  |
| `domein`     | no       | Category name (shown as a badge)       |
| `toelichting` | no      | Explanation shown after answering      |

---

## Troubleshooting

| Problem                        | Solution                                        |
|-------------------------------|--------------------------------------------------|
| "No quiz files found"          | Place `.json` files in the `quizzes/` directory  |
| "Failed to load quiz"          | Check JSON syntax and required fields             |
| Port 8501 already in use       | `streamlit run app.py --server.port 8502`         |
| Quiz freezes after page reload | Session is lost — click Start quiz again           |

---

## Deployment: Streamlit Community Cloud

### 1. Push to GitHub

```bash
cd QuizApp
git init
git add -A
git commit -m "Initial commit"
```

Create a repository on GitHub (e.g. `az900-quiz-app`), then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/az900-quiz-app.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Sign in with your GitHub account.
3. Click **"New app"**.
4. Select your GitHub repository (`az900-quiz-app`).
5. Set:
   - **Branch:** `main`
   - **Main file:** `app.py`
6. Click **Deploy**.

### 3. App is live

Your app will be available at:  
`https://YOUR_USERNAME-az900-quiz-app.streamlit.app`

Every push to `main` triggers an automatic redeploy.
