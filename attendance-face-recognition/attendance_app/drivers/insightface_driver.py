import insightface
import cv2

class InsightFaceEngine:
    def __init__(self):
        self.app = insightface.app.FaceAnalysis(name="buffalo_l")
        self.app.prepare(ctx_id=-1)   # CPU mode

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = self.app.get(rgb)

        out = []
        for f in faces:
            x1, y1, x2, y2 = f.bbox.astype(int)
            out.append({
                "box": [x1, y1, x2, y2],
                "embedding": f.normed_embedding.tolist() if hasattr(f, "normed_embedding") else None,
                "score": float(f.det_score)
            })
        return out
