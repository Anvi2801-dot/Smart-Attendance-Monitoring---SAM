from deepface import DeepFace
import os
import pickle

KNOWN_DIR = "known_faces"
embeddings = {}

for person in os.listdir(KNOWN_DIR):
    person_path = os.path.join(KNOWN_DIR, person)
    embeddings[person] = []

    for img in os.listdir(person_path):
        img_path = os.path.join(person_path, img)

        rep = DeepFace.represent(
            img_path=img_path,
            model_name="Facenet",
            enforce_detection=False
        )

        embeddings[person].append(rep[0]["embedding"])

with open("embeddings.pkl", "wb") as f:
    pickle.dump(embeddings, f)

print("✅ Face embeddings stored")