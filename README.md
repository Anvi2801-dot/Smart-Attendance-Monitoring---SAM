# 🎓 Smart Attendance Monitoring — SAM

A real-time face detection and recognition system for automated attendance tracking. SAM extracts frames from a classroom video feed, detects faces using **RetinaFace**, and matches them against a pre-registered dataset using **FaceNet** embeddings — logging attendance automatically.

---

## ✨ Features

- 🎥 **Video frame extraction** — samples one frame every 5 seconds from classroom footage
- 🧹 **Image enhancement** — applies CLAHE (Contrast Limited Adaptive Histogram Equalization) for better recognition in low-light conditions
- 🔍 **Face detection** — extracts individual face crops from frames using RetinaFace
- 🧠 **Face recognition** — matches faces via cosine similarity on FaceNet embeddings
- 📊 **Hybrid attendance logic** — requires a minimum tick count *and* confidence threshold to mark a student present, reducing false positives
- 📁 **Modular pipeline** — each stage (extract → detect → recognise → report) is an independent, runnable script

---

## 🗂️ Project Structure

```
Smart-Attendance-Monitoring---SAM/
├── attendance_app/           # Django app (views, models, URLs)
├── attendance_proj/          # Django project settings
├── face_recognition/
│   ├── frames/               # Extracted video frames (auto-generated)
│   ├── detected_faces/       # Cropped face images (auto-generated)
│   ├── known_faces/          # Pre-registered faces, one folder per person
│   ├── embeddings.pkl        # Serialised FaceNet embeddings (auto-generated)
│   ├── build_embeddings.py  
│   └── recognize.py
├── facetest/                 # Experimentation scripts
│   ├── detect_faces.py
│   ├── enhance_frame.py
│   └── extract_frames.py
├── frontend/                 # Web UI (HTML / CSS / JS)
├── public/                   # Static assets
├── manage.py
├── requirements.txt
├── package.json
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| Face Detection | RetinaFace (via DeepFace) |
| Face Recognition | FaceNet (via DeepFace) |
| Similarity Metric | Cosine similarity |
| Image Processing | OpenCV, CLAHE |
| Frontend | HTML, CSS, JavaScript |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js & npm
- A classroom video file (`.mp4`)

### Installation

```bash
# Clone the repository
git clone https://github.com/Anvi2801-dot/Smart-Attendance-Monitoring---SAM.git
cd Smart-Attendance-Monitoring---SAM

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install
```

### Running the Django App

```bash
python manage.py migrate
python manage.py runserver
```

Then open your browser at `http://localhost:8000`.

---

## 📸 Recognition Pipeline

SAM runs as a 4-stage pipeline. Each script can be run independently.

### Stage 1 — Register Known Faces

Place images for each student in `face_recognition/known_faces/<Name>/`, then run:

```bash
python face_recognition/generate_embeddings.py
```

This generates FaceNet embeddings for every registered face and saves them to `embeddings.pkl`.

### Stage 2 — Extract Frames from Video

```bash
python face_recognition/extract_frames.py
```

Samples one frame every **5 seconds** from the classroom video and saves them to `face_recognition/frames/`. Update the `video_path` variable in the script to point to your footage.

### Stage 3 — Detect & Crop Faces

```bash
python face_recognition/detect_faces.py
```

Runs RetinaFace on each frame, crops individual faces, and saves them to `face_recognition/detected_faces/`. Optionally pre-process frames with CLAHE enhancement (`enhance.py`) for better results in poor lighting.

### Stage 4 — Recognise & Generate Report

```bash
python face_recognition/recognize.py
```

Compares each detected face against `embeddings.pkl` using cosine similarity and prints a final attendance report.

---

## 📊 Attendance Logic

SAM uses a **hybrid tick-based approach** to avoid false positives from a single frame match:

| Parameter | Default | Description |
|---|---|---|
| `THRESHOLD` | `0.70` | Minimum cosine similarity score to count a tick |
| `MIN_TICKS_REQUIRED` | `10` | Minimum ticks needed to mark a student **Present** |

**Decision rules:**

- `ticks >= MIN_TICKS_REQUIRED` → ✅ **Present** (with average confidence score)
- `0 < ticks < MIN_TICKS_REQUIRED` → ❌ **Absent** (weak match, not enough frames)
- `ticks == 0` → ❌ **Absent** (no match found)

**Sample output:**

```
==================================================
             FINAL ATTENDANCE REPORT
==================================================
Person_2       : PRESENT ✅ (Avg Conf: 0.84, Ticks: 14)
==================================================
```

---

## 🖼️ Image Enhancement

For low-quality or dim classroom footage, the `enhance.py` module applies **CLAHE** to the L channel of the LAB colour space before face detection, improving contrast without overexposing bright areas.

```python
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
```

---

## 📦 Key Dependencies

```
deepface
retina-face
opencv-python
numpy
django
```

See `requirements.txt` for the full list.

---
