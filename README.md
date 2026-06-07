# EquiVision 👁️‍🗨️
**Vision Beyond Bias. Seeking Equality. Shaping Fairness.**

EquiVision is a Streamlit-based AI attendance and event management system with real-time gender detection, smart seat allocation, analytics, and team management features.

---

## 🚀 Features

- **🔐 User Authentication** — Local username/password login with multi-user support
- **📸 AI Attendance (Live / Upload)** — Detects faces from camera or uploaded images using DeepFace, identifies gender, and registers participants
- **🪑 Smart Seat Allocation** — Automatically assigns seats in a configurable hall layout (rows × columns) with gender-aware clustering
- **🔁 Duplicate Detection** — Uses face encodings to prevent double-registration within the same event
- **🔒 Privacy Mode** — Anonymous attendance mode that hides personal data
- **📋 Database View** — Password-protected editable participant records
- **📊 Analytics Dashboard** — Gender distribution pie charts, age vs gender histograms, and an interactive seating heatmap
- **📥 Export Reports** — Download attendance as CSV or auto-generated PDF (with charts)
- **📂 Batch Upload** — Process multiple photos at once for bulk registration
- **👥 Team Analysis** — Analyze and create balanced gender teams from registered participants
- **🏅 Team Role Allocation** — Define roles with skill requirements and allocate members with optional gender-balancing threshold
- **📁 Folder Management** — Organize events into main folders

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / App** | Streamlit |
| **Face Detection & Gender AI** | DeepFace (TF-Keras backend) |
| **Image Processing** | OpenCV, Pillow |
| **Data** | Pandas, NumPy |
| **Charts** | Plotly |
| **PDF Reports** | FPDF + Kaleido |
| **Persistence** | Local JSON (via `local_store.py`) |

---

## 📁 Project Structure

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
    └── secrets.toml     # Streamlit secrets (if applicable)
```

---

## ⚙️ Installation

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

## 📦 Dependencies

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

## 📝 Notes

- Face detection uses DeepFace with the **SSD backend** by default for speed.
- All data is stored **locally** in JSON files under the `data/` directory — no cloud required.
- AI models are **lazy-loaded** on first use to avoid slow startup times.
- PDF chart generation requires the `kaleido` package.
