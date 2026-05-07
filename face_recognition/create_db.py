# create_db.py
from deepface import DeepFace
import pickle
import os

db = {}
db_folder = "student_db"  # Folder where you put student images

print("Creating database... this might take a minute.")

# Loop through all images in student_db
if not os.path.exists(db_folder):
    os.makedirs(db_folder)
    print(f"Created folder '{db_folder}'. Please put student images inside it!")
    exit()

for file in os.listdir(db_folder):
    if file.endswith(('.jpg', '.jpeg', '.png')):
        name = os.path.splitext(file)[0]  # Use filename as student name
        img_path = os.path.join(db_folder, file)
        
        try:
            # Generate embedding
            embedding = DeepFace.represent(
                img_path=img_path, 
                model_name="Facenet", 
                enforce_detection=False
            )[0]["embedding"]
            
            # Save to dictionary (list allows multiple photos per student later)
            if name not in db:
                db[name] = []
            db[name].append(embedding)
            print(f"✅ Learned face for: {name}")
        except Exception as e:
            print(f"❌ Could not process {file}: {e}")

# Save the database to a file
with open("embeddings.pkl", "wb") as f:
    pickle.dump(db, f)

print("Database saved as 'embeddings.pkl'!")