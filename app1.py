from flask import Flask, request, jsonify, render_template, redirect, url_for
import pickle
import numpy as np
import pandas as pd
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)

# Load the trained model
with open('crop_yield_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the dataset for historical data and detailed analysis
data = pd.read_csv('crop_yield_data.csv')

def convert_to_numerical(data):
    mapping = {
        'region': {'north': 0, 'south': 1, 'east': 2, 'west': 3},
        'crop_type': {'wheat': 0, 'corn': 1, 'rice': 2, 'soybean': 3},
        'soil_type': {'clay': 0, 'sandy': 1, 'silty': 2, 'loamy': 3},
        'previous_crop': {'none': 0, 'corn': 1, 'wheat': 2, 'soybean': 3}
    }
    return [
        float(data['temperature']),
        float(data['rainfall']),
        float(data['soil_ph']),
        float(data['soil_moisture']),
        mapping['region'][data['region'].lower()],
        mapping['crop_type'][data['crop_type'].lower()],
        mapping['soil_type'][data['soil_type'].lower()],
        float(data['sunlight_hours']),
        float(data['fertilizer_used']),
        float(data['pesticides_used']),
        mapping['previous_crop'][data['previous_crop'].lower()]
    ]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array([convert_to_numerical(data)])
    prediction = model.predict(features)
    rounded_prediction = round(prediction[0], 2)
    return jsonify({'yield': f"{rounded_prediction} metric tons per hectare"})

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/historical')
def historical_page():
    return render_template('historical.html')

@app.route('/region')
def region_page():
    return render_template('region.html')

@app.route('/crop_type')
def crop_type_page():
    return render_template('crop_type.html')

@app.route('/historical_data')
def historical_data():
    # Convert DataFrame to list of dictionaries
    historical_data = data.to_dict(orient='records')
    return jsonify(historical_data)

@app.route('/detailed_analysis')
def detailed_analysis_page():
    return render_template('detailed_analysis.html')

@app.route('/detailed_analysis_data')
def detailed_analysis_data():
    analysis = {
        'average_yield': data['yield'].mean(),
        'max_yield': data['yield'].max(),
        'min_yield': data['yield'].min(),
        'yield_by_crop_type': data.groupby('crop_type')['yield'].mean().to_dict(),
    }
    return jsonify(analysis)

@app.route('/redirect_to_detailed_analysis')
def redirect_to_detailed_analysis():
    return redirect(url_for('detailed_analysis_page'))

if __name__ == '__main__':
    app.run(debug=True)
