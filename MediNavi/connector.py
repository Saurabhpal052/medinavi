import requests

def get_prediction(request, input_data):
    api_url = "http://127.0.0.1:5001/predict_disease" 
    data = {"input": input_data}
    response = requests.get(api_url, json=data)

    if response.status_code == 200:
        prediction = response.json()
        return prediction
    else:
        return {"error": "API request failed"}
