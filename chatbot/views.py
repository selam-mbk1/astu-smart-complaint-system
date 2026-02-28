import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatbotFAQ
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .forms import ChatbotFAQForm
from django.contrib import messages

# Load static responses once
with open('chatbot/responses.json') as f:
    static_responses = json.load(f)

# ----------------------
# Chatbot Page
# ----------------------
def chatbot_page(request):
    return render(request, 'chatbot/chat.html')


# ----------------------
# Chatbot API (real-time)
# ----------------------
@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').lower().strip()
        response = "Sorry, I don't understand. Can you try rephrasing?"

        # 1️⃣ Dynamic FAQs from DB
        faqs = ChatbotFAQ.objects.all()
        for faq in faqs:
            if faq.keywords:
                keywords = [k.strip().lower() for k in faq.keywords.split(',')]
                if any(word in user_message for word in keywords):
                    response = faq.answer
                    break
            elif faq.question.lower() in user_message:
                response = faq.answer
                break

        # 2️⃣ Static JSON responses fallback
        if response.startswith("Sorry"):
            for key, value in static_responses.items():
                if key in user_message:
                    response = value
                    break

        # 3️⃣ Hardcoded common intents (submit/check complaints)
        submit_keywords = ["submit", "complaint", "form", "file", "report"]
        if any(word in user_message for word in submit_keywords):
            response = (
                "To submit a complaint, please follow these steps:\n"
                "• Select the appropriate category.\n"
                "• Add a descriptive title.\n"
                "• Explain your issue in detail.\n"
                "• Upload any files if needed.\n"
                "• Click 'Submit' to send your complaint."
            )

        check_status_keywords = ["check status", "my complaints", "complaint status"]
        if any(word in user_message for word in check_status_keywords):
            response = (
                "To check your complaint status, go to 'My Complaints' on your dashboard. "
                "You will see all complaints you submitted and their current status."
            )

        return JsonResponse({'response': response})


@login_required
@role_required('admin')
def faq_list(request):
    faqs = ChatbotFAQ.objects.all().order_by('-id')
    return render(request, 'chatbot/faq_list.html', {'faqs': faqs})

@login_required
@role_required('admin')
def faq_add(request):
    form = ChatbotFAQForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "FAQ added successfully.")
        return redirect('faq_list')
    return render(request, 'chatbot/manage_faq.html', {'form': form, 'title': 'Add FAQ'})

@login_required
@role_required('admin')
def faq_edit(request, pk):
    faq = get_object_or_404(ChatbotFAQ, pk=pk)
    form = ChatbotFAQForm(request.POST or None, instance=faq)
    if form.is_valid():
        form.save()
        messages.success(request, "FAQ updated successfully.")
        return redirect('faq_list')
    return render(request, 'chatbot/manage_faq.html', {'form': form, 'title': 'Edit FAQ'})

@login_required
@role_required('admin')
def faq_delete(request, pk):
    faq = get_object_or_404(ChatbotFAQ, pk=pk)
    if request.method == 'POST':
        faq.delete()
        messages.success(request, "FAQ deleted successfully.")
        return redirect('faq_list')
    return render(request, 'chatbot/confirm_delete.html', {'object': faq})