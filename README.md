# EquiVision

**Vision Beyond Bias. Seeking Equality. Shaping Fairness.**

EquiVision is a Streamlit-based AI attendance and event management system built around a single question: how do the small, often unexamined decisions in event logistics (who sits where, who ends up on which team, whether a headcount even accounts for non-binary participants) end up reinforcing gender bias instead of preventing it. The system uses real-time face and gender detection, algorithmic seat allocation, fairness-aware team formation, and analytics to make those decisions explicit, measurable, and adjustable, rather than left to default social patterns.

---

## Motivation

Most event and attendance software treats gender, if it considers it at all, as a static label on a form. In practice, gender bias at events shows up procedurally, not just in attitudes:

- Seating is often split by gender "for safety" or convention, which can produce unequal viewing angles, reinforce assumptions about who needs protection, and separate participants who paid identical fees for identical access.
- Teams often self-select along gender lines, which can skew participation and collaboration and quietly reinforce stereotypes about who is "naturally suited" to a given task.
- Non-binary participants are frequently left out of headcounts and seating logic entirely, because most systems are built around a strict binary.

EquiVision was designed to address these as concrete, solvable problems, not as a policy statement, but as constraints an allocation algorithm can actually take into account.

## Aim

To build a system that can, from a live camera feed or uploaded images:

1. Detect and count participants by gender (including a self-declared, non-binary-inclusive option), with confidence scoring and an "unknown" fallback.
2. Prevent duplicate attendance entries, both within a single event and across related sub-events.
3. Allocate seats and teams in a way that is gender-balanced by default, but configurable, including a same-gender clustering setting, so that gender balance doesn't come at the cost of participants' comfort.
4. Surface all of this through a live analytics dashboard and exportable reports, so organizers can see the actual gender composition of their event as it happens, not just estimate it afterward.
5. Do all of the above while giving organizers a genuine privacy-first mode that discards face data and personal identifiers entirely.

## Design Approach

The system was planned around a few deliberate decisions before implementation:

- **Two attendance modes (Normal and Privacy)**: Normal mode retains name, ID, branch, and age alongside gender and seat data for full event records; Privacy mode retains only gender and seat assignment, discarding face images and identity entirely. This was a conscious tradeoff between usability for the host and data minimization for the participant.
- **Confidence-scored gender detection with manual override**: since automated gender classification from images is inherently imperfect and binary-biased, the system reports a confidence score and always allows a self-declared category, including non-binary, rather than forcing a binary AI verdict as final.
- **Duplicate handling via face encoding, not just name matching**: to catch re-registration attempts even when a participant re-enters through a different camera angle, lighting condition, or image upload, and to flag (rather than silently block) duplicates across sub-events within the same main event.
- **Configurable seating algorithm rather than a fixed rule**: a strict alternating boy-girl-boy seating pattern is the "ideal" case, but real headcounts are rarely evenly split. The seating logic instead targets row-level balance across the whole hall and exposes a same-gender cluster size setting, so hosts can decide how strictly to enforce alternation versus participant comfort.
- **A weighted skill-scoring and fairness-swap algorithm for team/role allocation**: rather than assigning roles purely by self-selection (which tends to reproduce gendered team splits) or purely by gender quota (which ignores actual skill fit), the system scores each candidate against a role's weighted skill requirements, then checks whether swapping two candidates across roles would improve gender balance within an organizer-defined tolerance threshold (e.g., 20 percent). A swap is only made if it stays within that threshold, so fairness adjustments never come at the cost of assigning someone to a role they're clearly unsuited for.
- **Local, JSON-backed persistence**: since this was built for single-event and small-institution use rather than as a hosted multi-tenant product, all data is stored locally rather than requiring a backend service or cloud database.

---

## Features

- **User Authentication**: Local username/password login with multi-user support
- **AI Attendance (Live / Upload)**: Detects faces from camera or uploaded images using DeepFace, identifies gender, and registers participants
- **Smart Seat Allocation**: Automatically assigns seats in a configurable hall layout (rows x columns) with gender-aware clustering
- **Duplicate Detection**: Uses face encodings to prevent double-registration within an event, and flags re-registration across sub-events
- **Privacy Mode**: Anonymous attendance mode that discards personal data and face images
- **Database View**: Password-protected, editable participant records
- **Analytics Dashboard**: Gender distribution pie charts, age vs. gender histograms, and an interactive seating heatmap
- **Export Reports**: Download attendance as CSV or an auto-generated PDF (with charts)
- **Batch Upload**: Process multiple photos at once for bulk registration
- **Team Analysis**: Analyze and generate balanced gender teams from registered participants
- **Team Role Allocation**: Define roles with weighted skill requirements and allocate members using a fairness-aware scoring and swap algorithm, with configurable gender-balancing thresholds
- **Folder Management**: Organize related events under shared main-event folders, with aggregated cross-event statistics

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App | Streamlit |
| Face Detection & Gender AI | DeepFace (TF-Keras backend) |
| Image Processing | OpenCV, Pillow |
| Data | Pandas, NumPy |
| Charts | Plotly |
| PDF Reports | FPDF + Kaleido |
| Persistence | Local JSON (via `local_store.py`) |

---

## Project Structure

```
Coding/
├── glasstry.py          # Main Streamlit app (all pages & routing)
├── face_engine.py       # FaceEngine class (DeepFace wrapper, encoding, detection)
├── utils.py             # SeatingManager, TeamManager, TeamBalancer logic
├── local_store.py       # Local JSON persistence (users, events, sessions)
├── fix_files.py         # Utility script for fixing/migrating data files
├── requirements.txt     # Python dependencies
├── data/                # Local JSON data storage
├── ui/
│   ├── __init__.py      # UI exports
│   ├── theme.py         # Premium CSS theme injection & UI components
│   ├── components.py    # Reusable Streamlit UI components
│   └── animations.js    # Frontend animations (particles, stars)
└── .streamlit/
    └── secrets.toml      # Streamlit secrets (if applicable)
```

---

## Installation

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd Coding
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run glasstry.py
   ```

---

## Dependencies

```
streamlit
pandas
numpy
opencv-python-headless
deepface
Pillow
fpdf
tf-keras
kaleido
plotly
```

---

## Notes

- Face detection uses DeepFace with the SSD backend by default for speed.
- All data is stored locally in JSON files under the `data/` directory, with no cloud dependency.
- AI models are lazy-loaded on first use to avoid slow startup times.
- PDF chart generation requires the `kaleido` package.