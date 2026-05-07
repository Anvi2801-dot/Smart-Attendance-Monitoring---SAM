from deepface import DeepFace
import cv2
import os
import time
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
frames_folder = os.path.join(SCRIPT_DIR, "..", "face_recognition", "frames")
faces_folder = os.path.join(SCRIPT_DIR, "..", "face_recognition", "detected_faces")

print(f"Reading from: {frames_folder}")
print(f"Saving to: {faces_folder}")

if os.path.exists(faces_folder):
    print(f"🧹 Clearing existing detected faces in: {faces_folder}")
    shutil.rmtree(faces_folder)
os.makedirs(faces_folder, exist_ok=True)

if not os.listdir(frames_folder):
    print(f"⚠️ Warning: {frames_folder} is empty! Run extract_frames.py first.")

# Loop through each frame image
for img_name in os.listdir(frames_folder):
    if img_name.startswith('.'): continue # Skip hidden Mac files
    
    img_path = os.path.join(frames_folder, img_name)
    print(f"Processing: {img_name}...")

    try:
        faces = DeepFace.extract_faces(
            img_path=img_path,
            detector_backend="retinaface",
            enforce_detection=False
        )

        for i, face in enumerate(faces):
            face_img = face["face"] * 255
            # Fix: Convert RGB to BGR for OpenCV
            face_img = cv2.cvtColor(face_img.astype('uint8'), cv2.COLOR_RGB2BGR)

            face_file = os.path.join(faces_folder, f"{img_name}_face_{i}.jpg")
            cv2.imwrite(face_file, face_img)

    except Exception as e:
        print(f"❌ Error processing {img_name}: {e}")
    
    time.sleep(0.1)

print(f"✅ Faces detected and saved in {faces_folder}")