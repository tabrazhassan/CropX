from flask import Flask, request, jsonify
import numpy as np
import pickle

app = Flask(__name__)

# Load the crop recommendation model
crop_recommendation_model_path = 'models/RandomForest1.pkl'
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))

@app.route('/recommend_crop', methods=['POST'])
def recommend_crop():
    try:
        # Get input data from the request
        input_data = request.get_json()

        # Extract input values
        N = float(input_data['N'])
        P = float(input_data['P'])
        K = float(input_data['K'])
        temperature = float(input_data['temperature'])
        humidity = float(input_data['humidity'])
        ph = float(input_data['ph'])
        rainfall = float(input_data['rainfall'])

        data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

        # Predict probabilities for all crops
        crop_probabilities = crop_recommendation_model.predict_proba(data)

        # Get the class labels (crop names)
        crop_labels = crop_recommendation_model.classes_

        # Create a dictionary with crop names and their corresponding probabilities
        crop_prob_dict = {crop: prob for crop, prob in zip(crop_labels, crop_probabilities[0])}

        # Sort the crops by probability in descending order
        sorted_crops = sorted(crop_prob_dict.items(), key=lambda x: x[1], reverse=True)

        # Get the top 3 to 5 crops
        top_crops = sorted_crops[:3]  # You can adjust this number as needed

        # Prepare the response
        response_data = {
            "top_crops": [{"crop": crop, "probability": prob} for crop, prob in top_crops]
        }

        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
