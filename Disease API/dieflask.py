from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('EfficientNetB3-wheat-98.67.h5')

# Load the class information from the csv file
class_info = pd.read_csv('class_dict (1).csv')

# Function to preprocess the input image
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(class_info['height'][0], class_info['width'][0]))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

# Function to classify the input image
def classify_image(img_path):
    img_array = preprocess_image(img_path)
    predictions = model.predict(img_array)
    
    # Get the class index with the highest probability
    predicted_class_index = np.argmax(predictions)
    
    # Map the class index to the corresponding class label using your csv data
    class_label = class_info['class'].iloc[predicted_class_index]
    probability = predictions[0, predicted_class_index]
    
    return class_label, probability

# API endpoint for image classification
@app.route('/classify', methods=['POST'])
def classify():
    try:
        # Get the image file from the request
        img_file = request.files['image']
        img_path = 'temp_image.jpg'
        img_file.save(img_path)
        
        # Perform image classification
        top_class, top_probability = classify_image(img_path)
        
        # Check if the classified class is in the wheat classes
        wheat_classes = class_info['class'].tolist()
        if top_class in wheat_classes:
            result = {"class": top_class}
        else:
            result = {"error": "Invalid: The provided image is not related to wheat diseases."}
        
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)
