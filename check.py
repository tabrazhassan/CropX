from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load your pre-trained model from a pickle file
with open('models/RandomForest1.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse input features from the request JSON
        data = request.get_json()
        nitrogen = data['N']
        phosphorus = data['P']
        potassium = data['K']
        temperature = data['temperature']
        humidity = data['humidity']
        ph = data['ph']
        rainfall = data['rainfall']

        # Make predictions using your model
        prediction = model.predict([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])

        # Convert the prediction to a string
        prediction_str = str(prediction[0])

        return jsonify({'prediction': prediction_str})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
