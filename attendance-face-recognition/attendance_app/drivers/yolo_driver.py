from ultralytics import YOLO
import numpy as np

class YOLOFaceDetector:
    def __init__(self, model_name="yolov8n"):
        self.model = YOLO(model_name)

    def detect(self, frame):
        results = self.model(frame)[0]
        if not hasattr(results, "boxes"):
            return []

        boxes = results.boxes.xyxy.cpu().numpy()
        confs = results.boxes.conf.cpu().numpy()

        out = []
        for box, conf in zip(boxes, confs):
            x1, y1, x2, y2 = box
            out.append({
                "box": [int(x1), int(y1), int(x2), int(y2)],
                "conf": float(conf)
            })
        return out
