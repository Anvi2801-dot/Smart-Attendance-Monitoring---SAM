from deepface import DeepFace
import pickle
import os
import numpy as np

with open("embeddings.pkl", "rb") as f:
    db = pickle.load(f)

all_students = ["Person_2"] 

attendance_counts = {} 
all_scores = {}

THRESHOLD = 0.70           
MIN_TICKS_REQUIRED = 10    

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


detected_folder = "detected_faces"

print(f"Starting recognition on {len(os.listdir(detected_folder))} images...")

for img in os.listdir(detected_folder):
    if img.startswith('.'): continue 
    
    path = os.path.join(detected_folder, img)
    
    try:
        results = DeepFace.represent(
            img_path=path,
            model_name="Facenet",
            enforce_detection=False
        )
        
        if not results: continue
        test_emb = results[0]["embedding"]

        best_name = "Unknown"
        best_score = 0

        for name, embs in db.items():
            for e in embs:
                score = cosine(test_emb, e)
                if score > best_score:
                    best_score = score
                    best_name = name

        if best_score > THRESHOLD:
            print(f"✅ {img} → {best_name} ({best_score:.2f})")
            attendance_counts[best_name] = attendance_counts.get(best_name, 0) + 1
            
            if best_name not in all_scores:
                all_scores[best_name] = []
            all_scores[best_name].append(best_score)
        else:
            # Uncomment below if you want to see every 'Unknown'
            print(f"❌ {img} → Unknown ({best_score:.2f})")
            pass

    except Exception as e:
        print(f"⚠️ Error processing {img}: {e}")

# 4. FINAL ATTENDANCE SUMMARY (The Hybrid Approach)
print("\n" + "="*50)
print("             FINAL ATTENDANCE REPORT")
print("="*50)

for student in all_students:
    count = attendance_counts.get(student, 0)
    scores = all_scores.get(student, [0])
    avg_conf = np.mean(scores)

    # Final Decision Logic
    if count >= MIN_TICKS_REQUIRED:
        status = f"PRESENT ✅ (Avg Conf: {avg_conf:.2f}, Ticks: {count})"
    elif count > 0:
        status = f"ABSENT ❌ (Weak Match: only {count} ticks)"
    else:
        status = "ABSENT ❌ (No match found)"
    
    print(f"{student:<15}: {status}")

print("="*50)