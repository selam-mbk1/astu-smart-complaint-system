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
        with open('chatbot/data.json') as f:
            data = json.load(f)

        response = "Sorry, I don't understand."
        for item in data:
            if user_message in item['question'].lower():
                response = item['answer']
                break

        return JsonResponse({'response': response})