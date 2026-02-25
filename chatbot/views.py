import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

with open('chatbot/responses.json') as f:
    data = json.load(f)


@csrf_exempt
def chatbot_response(request):

    message = request.POST.get("message", "").lower()

    for key in data:
        if key in message:
            return JsonResponse({"response": data[key]})

    return JsonResponse({
        "response": "Please submit your complaint through the system."
    })
