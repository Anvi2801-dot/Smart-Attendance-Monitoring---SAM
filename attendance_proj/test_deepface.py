from deepface import DeepFace

result = DeepFace.analyze(
    img_path="test.jpg",
    actions=['emotion', 'age', 'gender'],
    detector_backend='retinaface'
)

print(result)
