from flask import Flask, request, jsonify
from google.cloud import storage
import tensorflow as tf
import os
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import logging

# Initialize the Flask app
app = Flask(__name__)

# === CONFIGURATION ===
GCS_BUCKET_NAME = 'my_machine_learning_model'
GCS_MODEL_PATH = 'models/sentiment_analysis_model.h5'
LOCAL_MODEL_PATH = 'sentiment_analysis_model.h5'
TOKENIZER_LOCAL_PATH = 'tokenizer.pickle'
TOKENIZER_GCS_PATH = 'models/tokenizer.pickle'

# Setup logging for better debugging and monitoring
logging.basicConfig(level=logging.INFO)

# === DOWNLOAD TOKENIZER FROM GCS ===
def download_tokenizer_from_gcs():
    if not os.path.exists(TOKENIZER_LOCAL_PATH):  # Check if the file exists locally
        try:
            logging.info("Downloading tokenizer from GCS...")
            # Initialize the GCS client
            client = storage.Client()
            bucket = client.bucket(GCS_BUCKET_NAME)  # Access the bucket
            blob = bucket.blob(TOKENIZER_GCS_PATH)  # Reference the file in the bucket
            
            # Download the file to the local path in Cloud Run's environment or Colab
            blob.download_to_filename(TOKENIZER_LOCAL_PATH)
            logging.info("Tokenizer downloaded successfully from GCS.")
        except Exception as e:
            logging.error(f"Error downloading tokenizer: {e}")
            raise

# Download tokenizer if not already available locally
download_tokenizer_from_gcs()

# === DOWNLOAD MODEL FROM GCS ===
def download_model_from_gcs():
    if not os.path.exists(LOCAL_MODEL_PATH):
        logging.info("Downloading model from GCS...")
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(GCS_MODEL_PATH)
        blob.download_to_filename(LOCAL_MODEL_PATH)
        logging.info("Model downloaded successfully from GCS.")

# Download model if not already available locally
download_model_from_gcs()

# === LOAD MODEL ===
logging.info("Loading model...")
model = tf.keras.models.load_model(LOCAL_MODEL_PATH)
logging.info("Model loaded successfully.")

# === LOAD TOKENIZER ===
logging.info("Loading tokenizer...")
with open(TOKENIZER_LOCAL_PATH, 'rb') as handle:
    tokenizer = pickle.load(handle)
logging.info("Tokenizer loaded successfully.")

# === PREDICTION FUNCTION ===
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the POST request
        data = request.get_json()

        # Validate input
        if 'text' not in data:
            return jsonify({'error': 'No text provided for prediction'}), 400
        
        text = data['text']

        # Preprocess the input text: Convert to sequences and pad
        seq = tokenizer.texts_to_sequences([text])
        padded = pad_sequences(seq, padding='post', maxlen=20)

        # Predict sentiment using the loaded model
        prediction = model.predict(padded)

        # Convert the prediction to a sentiment label
        sentiment_score = float(prediction[0][0])  # The probability of being positive
        sentiment_label = 'positive' if sentiment_score > 0.5 else 'negative'

        # Prepare a detailed response with sentiment and probability
        response = {
            'sentiment': sentiment_label,
            'probability': sentiment_score
        }

        return jsonify(response)

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({'error': 'Prediction failed', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
