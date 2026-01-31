import importlib
from django.conf import settings

DRIVER_MAP = {
    "yolo": "attendance_app.drivers.yolo_driver.YOLOFaceDetector",
    "insight": "attendance_app.drivers.insightface_driver.InsightFaceEngine",
}

def load_driver():
    choice = getattr(settings, "RECOGNITION_DRIVER", "insight")
    path, cls = DRIVER_MAP[choice].rsplit(".", 1)
    module = importlib.import_module(path)
    Driver = getattr(module, cls)
    return Driver()

detector = load_driver()
