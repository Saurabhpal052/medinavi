from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse
import json

from .form import DiseaseInfoForm 


restructured_data={}
response_data={}
# Create your views here.
@csrf_exempt
def yourMayHave(request:HttpResponse):
    api_url = 'http://localhost:5001/predict_disease'
    a=request.POST['Symptoms']
    data = {'query': a}
    response = requests.post(api_url, json=data)

    if response.status_code != 200:
        # Handle API request error
        return JsonResponse({'error': 'Failed to call Flask API'}, status=500)
    # else:
    # Parse the JSON response from the Flask API
    global restructured_data,response_data
    response_data = response.json()
    restructured_data = {
"user_input": response_data["input"],
"disease_recommendations": []
}   
    process()
    # restructured_json = json.dumps(restructured_data, indent=2)
    
    disease_forms = []
    for data in restructured_data:
        disease_form = DiseaseInfoForm(doctors_data=data["doctors"], initial=data)
        disease_forms.append(disease_form)

    # Render the template with the forms
    return render(request, 'youMay.html', {'disease_forms': disease_forms})
    # return JsonResponse(restructured_data)

def process():

    global restructured_data
    # Loop through the predictions and restructure the data
    for prediction in response_data["predictions"]:
        disease_name = prediction["Disease"]
        chances = prediction["Chances"]
        doctor_name = prediction["Doctor's Name"]
        specialist = prediction["Specialist"]

        # Check if doctor_name is NaN and handle it
        if doctor_name == "NaN":
            doctor_name = None

        # Find the recommendation for this disease
        disease_recommendation = next(
            (recommendation for recommendation in restructured_data["disease_recommendations"] if recommendation["disease"] == disease_name),
            None
        )

        if disease_recommendation is None:
            disease_recommendation = {
                "disease": disease_name,
                "chances": chances,
                "doctors": []
            }
            restructured_data["disease_recommendations"].append(disease_recommendation)

        if doctor_name:
            doctor_data = {
                "name": doctor_name,
                "specialist": specialist
            }
            disease_recommendation["doctors"].append(doctor_data)
