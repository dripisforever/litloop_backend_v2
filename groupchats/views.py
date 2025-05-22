import os
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from google import genai

# Configure Gemini API
client = genai.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

@csrf_exempt
@require_GET
def chat_with_gemini(request):
    user_message = request.GET.get("q", "").strip()

    if not user_message:
        return HttpResponseBadRequest("Missing 'q' query parameter.")

    try:

        response = client.models.generate_content(contents=user_message, model='gemini-2.0-flash-001')

        # Message.objects.create(content=response)
        # response = model.generate_content(user_message)

        return JsonResponse({
            "response": response.text
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
