import cv2
import os
import pickle
import numpy as np
from deepface import DeepFace
import shutil

def process_video_file(path):
    SERVICES_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_DIR = os.path.dirname(SERVICES_DIR)
    PROJ_DIR = os.path.dirname(APP_DIR)  
    ROOT_DIR = os.path.dirname(PROJ_DIR) 

    pkl_path = os.path.join(PROJ_DIR, "face_recognition", "embeddings.pkl")
    
    faces_dir = os.path.join(ROOT_DIR, "face_recognition", "detected_faces")
    
    video_path = os.path.join(ROOT_DIR, "media", "video.mp4")

    print(f"--- Step 1: Cleaning: {faces_dir} ---")
    if os.path.exists(faces_dir):
        shutil.rmtree(faces_dir)
    os.makedirs(faces_dir, exist_ok=True)

    print(f"--- Step 2: Starting Extraction from {video_path} ---")
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ CRITICAL ERROR: Could not find video at {video_path}")
        return []

    video_fps = cap.get(cv2.CAP_PROP_FPS) or 30 
    interval = max(1, int(video_fps / 5)) # 5 FPS
    
    count = 0
    saved_count = 0
    
    while cap.isOpened() and saved_count < 300: 
        ret, frame = cap.read()
        if not ret: break
        
        if count % interval == 0:
            try:
                face_objs = DeepFace.extract_faces(
                    img_path=frame, 
                    detector_backend="retinaface", 
                    enforce_detection=True 
                )
                
                for i, face_obj in enumerate(face_objs):
        
                    print(f"Processing Frame {count} | Face: {i}") 
                    face_img = (face_obj["face"] * 255).astype(np.uint8)
                    face_img = cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR)
                    
                    face_filename = f"frame_{count}_face_{i}.jpg"
                    cv2.imwrite(os.path.join(faces_dir, face_filename), face_img)
                    saved_count += 1
                    
            except Exception:
                pass
        count += 1
        
    cap.release()
    print(f"Successfully extracted {saved_count} faces.")

    if not os.path.exists(pkl_path):
        print(f"❌ ERROR: Pickle file missing at {pkl_path}")
        return []

    with open(pkl_path, "rb") as f:
        db = pickle.load(f)

    attendance_counts = {}
    print("--- Step 3: Running AI Recognition ---")
    
    for img in sorted(os.listdir(faces_dir)):
        if img.startswith('.'): continue
        img_path = os.path.join(faces_dir, img)
        
        try:
            results = DeepFace.represent(img_path=img_path, model_name="Facenet", enforce_detection=False)
            if not results: continue
            
            test_emb = results[0]["embedding"]
            best_name, best_score = "Unknown", 0

            for name, embs in db.items():
                for e in embs:
                    score = np.dot(test_emb, e) / (np.linalg.norm(test_emb) * np.linalg.norm(e))
                    if score > best_score:
                        best_score, best_name = score, name

            status_icon = "✅" if best_score > 0.70 else "❌"
            print(f"File: {img} | Best Match: {best_name} | Score: {best_score:.4f} {status_icon}")

            if best_score > 0.70:
                attendance_counts[best_name] = attendance_counts.get(best_name, 0) + 1
                
        except Exception as e:
            print(f"Recognition Error processing {img}: {e}")
            continue


    student_metadata = {
        "person1": {"id": 1, "image": "/photo/student_1.png", "display_name": "Person_1"},
        "person2": {"id": 2, "image": "/photo/student_2.png", "display_name": "Person_2"},
        "person3": {"id": 3, "image": "/photo/student_3.png", "display_name": "Person_3"},
        "person4": {"id": 4, "image": "https://robohash.org/student_4?set=set5", "display_name": "Person_4"},
    }

    final_attendance = []

    for key, meta in student_metadata.items():
        is_present = attendance_counts.get(key, 0) >= 1
        
        final_attendance.append({
            "id": meta["id"],
            "name": meta["display_name"],
            "image": meta["image"],
            "status": "Present" if is_present else "Absent"
        })
    
    print(f"--- Final Summary for React: {final_attendance} ---")
    return final_attendance