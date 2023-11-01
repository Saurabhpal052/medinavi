import json
from django.http import JsonResponse
import os
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
current_app_dir = os.path.dirname(os.path.abspath(__file__ ))
dbg=open('symptoms.txt','a')
api_url=[]
@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        bot_response = process_user_message(user_message)
        return JsonResponse({'message': bot_response})
    return render(request, 'chatbot_app/chatbot.html')

def process_user_message(user_message):
    with open(os.path.join(current_app_dir, 'medicalterms.json'), 'r') as json_file:
        data = json.load(json_file)
    search_query = user_message
    for item in data:
        if search_query.lower() in item['name'].lower() or search_query.lower() in item['text'].lower():
            return (item['text'])
    return "I don't know"
