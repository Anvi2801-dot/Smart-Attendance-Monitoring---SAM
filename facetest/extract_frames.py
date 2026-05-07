import cv2
import os

import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
output_folder = os.path.join(SCRIPT_DIR, "..", "face_recognition", "frames")
video_path = "/Users/anvisinghparihar/Downloads/1F-Classroom vy-102_VYAS 1st Floor_VYAS 1st Floor_20251006104001_20251006104501_24458379 (1).mp4"

if os.path.exists(output_folder):
    print(f"🧹 Clearing existing frames in: {output_folder}")
    shutil.rmtree(output_folder)
os.makedirs(output_folder, exist_ok=True)


cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"❌ Error: Could not open video file at {video_path}")
    exit()

fps = int(cap.get(cv2.CAP_PROP_FPS))

frame_count = 0
saved_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % (fps * 5) == 0:
        filename = f"{output_folder}/frame_{saved_count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"  💾 Saved: {filename}")
        saved_count += 1

    frame_count += 1

cap.release()
print(f"✅ Extraction complete. Saved {saved_count} frames to '{output_folder}'")