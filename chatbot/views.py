import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def chatbot_page(request):
    return render(request, 'chatbot/chat.html')

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').lower()

        with open('chatbot/responses.json') as f:
            data = json.load(f)

        response = "Sorry, I don't understand."

        for key, value in data.items():
            if key in user_message:
                response = value
                break

        return JsonResponse({'response': response})