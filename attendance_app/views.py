from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.video_processor import process_video_file
import json

@csrf_exempt
def upload_video(request):
    file = request.FILES.get("video")
    if not file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    file_path = "media/" + file.name
    with open(file_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)

    return JsonResponse({"message": "Uploaded", "file_path": file_path})


@csrf_exempt
def process_video(request):
    data = json.loads(request.body)
    path = data.get("file_path")

    if not path:
        return JsonResponse({"error": "file_path missing"}, status=400)

    results = process_video_file(path)
    return JsonResponse({"status": "done", "results": results})
