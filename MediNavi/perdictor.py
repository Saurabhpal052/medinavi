from flask import Flask, request, jsonify
from flask_restful import reqparse, Api, Resource
import pickle
from flask_restful import Resource
import pandas as pd
import numpy as np
from flashtext import KeywordProcessor
import regex as re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
from collections import Counter

# Data loading and preprocessing (These parts can be included in a function)
data = pd.read_csv("C:/Users/Adhiraj/Downloads/Original_Dataset.csv")
des_data = pd.read_csv("C:/Users/Adhiraj/Downloads/Disease_Description.csv")
doc = pd.read_csv("C:/Users/Adhiraj/Downloads/zocdoc.csv")
doc.drop(['Unnamed: 0'], axis=1, inplace=True)

data1 = pd.read_csv("C:/Users/Adhiraj/Downloads/data1.csv")
data1.columns = data1.columns.str.strip()

with open('disease.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Data preprocessing (Label encoding and keyword processing)
parser = reqparse.RequestParser()
parser.add_argument('query')

doc_data = pd.read_csv("C:/Users/Adhiraj/Downloads/Doctor_Versus_Disease.csv", encoding='latin1',
                     names=['Disease', 'Specialist'])
doc_data['Specialist'] = np.where((doc_data['Disease'] == 'Tuberculosis'), 'Pulmonologist', doc_data['Specialist'])
doc = doc.rename(columns={'speciality': 'Specialist'})
merged_df = doc.merge(doc_data, on='Specialist', how='left')
merged_df.drop(['Disease'], axis=1, inplace=True)

var_mod = ['Disease']
le = LabelEncoder()
for i in var_mod:
    data1[i] = le.fit_transform(data1[i])

sym = data1.columns
regex = re.compile('_')
sym = [i if regex.search(i) is None else i.replace('_', ' ') for i in sym]
keyword_processor = KeywordProcessor()
keyword_processor.add_keywords_from_list(sym)

test_col = []
for col in data1.columns:
    if col != 'Disease':
        test_col.append(col)

test_data = {}
symptoms = []
predicted = []
# Function for disease prediction
def predict_disease(user_input):
    symptoms.clear()
    predicted.clear()
    matched_keyword = keyword_processor.extract_keywords(user_input)
    if len(matched_keyword) == 0:
        print("No Matches")
    else:
        regex = re.compile(' ')
        processed_keywords = [i if regex.search(i) is None else i.replace(' ', '_') for i in matched_keyword]
        print("Symptoms you have:", processed_keywords)

    for column in test_col:
        test_data[column] = 1 if column in symptoms else 0
        test_df = pd.DataFrame(test_data, index=[0])
    predict_disease = model.predict(test_df)
    predict_disease = le.inverse_transform(predict_disease)
    predicted.extend(predict_disease)
    disease_counts = Counter(predicted)
    percentage_per_disease = {disease: (count) for disease, count in disease_counts.items()}
    result_df = pd.DataFrame({"Disease": list(percentage_per_disease.keys()),
                             "Chances": list(percentage_per_disease.values())})
    result_df = result_df.merge(doc_data, on='Disease', how='left')
    result_df = result_df.merge(des_data, on='Disease', how='left')
    result_df = result_df.merge(merged_df, on='Specialist', how='left')
    result_df = result_df.drop_duplicates()
    result_df = result_df.drop('Description', axis=1)
    result_df = result_df.drop('Chances', axis=1)
    return result_df

# Flask app initialization
app = Flask(__name__)
api = Api(app)



@app.route('/', methods=['GET', 'POST'])
# Flask Resource for your API
class Predict(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str)
        args = parser.parse_args()

        user_input = args['query']
        result_df = predict_disease(user_input)

        # Create a response JSON
        return jsonify({
            "input": user_input,
            "predictions": result_df.to_dict(orient="records")
        })

# Add a new route for disease prediction
api.add_resource(Predict, '/predict_disease')

if __name__ == '__main__':
    app.run(debug=True, port=5001)