from flask import Flask, request
from keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
from flask import Flask, request, jsonify
from keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import tempfile

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the 'image' file is included in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    try:
        image_file = request.files['image']

        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
            image_file.save(temp_image)
            image_path = temp_image.name

        # Load the image, preprocess, and make predictions
        image = load_img(image_path, target_size=(128, 128))
        image = img_to_array(image)
        image = image / 255.0
        image = image.reshape(1, image.shape[0], image.shape[1], image.shape[2])

        # Make predictions using your model
        model_path = 'wheatDiseaseModel (1).h5'  # Change this to your model path
        model = load_model(model_path)

        predictions = model.predict(image)

        class_labels = ['Crown and Root Rot', 'Healthy Wheat', 'Leaf Rust', 'Wheat Loose']  # Change labels accordingly
        predicted_class_index = np.argmax(predictions)
        predicted_class_label = class_labels[predicted_class_index]

        return jsonify({
            'predicted_class': predicted_class_label
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
