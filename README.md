# Sentiment Analysis API

This project provides a basic sentiment analysis API built using TensorFlow, Flask, and Google Cloud services. It allows you to send text data via POST requests and receive sentiment predictions (positive, neutral, or negative) in response.

## Table of Contents

-   [Author](#author)
-   [Prerequisites](#prerequisites)
-   [Setup Instructions](#setup-instructions)
-   [Running the Project Locally](#running-the-project-locally)
-   [Deploying to Cloud Run](#deploying-to-cloud-run)
-   [API Usage](#api-usage)
-   [Important Notes](#important-notes)
-   [Additional Notes](#additional-notes)
-   [License](#license)

## Author

Hernando Ivan Teddy

## Prerequisites

Before getting started, make sure you have the following:

-   **Google Cloud Project**: A Google Cloud project with billing enabled.
-   **Google Cloud SDK**: Install and configure [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
-   **Docker**: Install [Docker](https://docs.docker.com/get-docker/).
-   **Python Dependencies**: Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Setup Instructions

1.  **Clone the Repository:**

    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```

2.  **Download Model and Tokenizer from Google Cloud Storage (GCS):**

    -   Ensure your GCS bucket contains the model and tokenizer files (`sentiment_analysis_model.h5` and `tokenizer.pickle`).
    -   The application will automatically download these files from GCS when it starts.

## Import in collab


In order to run the project in Colab, you'll need to install some dependencies.

Go to the folder  /collab/my_model inside this repository

This collab file will run the sentiment training and produce our machine learning model

## Running the Project Locally

1.  **Set up Google Cloud credentials:**

    -   If running locally, set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your Google Cloud credentials file.

        ```bash
        export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
        ```

2.  **Run the Flask app:**

    ```bash
    python app.py
    ```

    This will start the Flask server locally, and you can access it at `http://localhost:8080`.

## Deploying to Cloud Run

1.  **Step 1: Build the Docker Image**

    To deploy the application to Google Cloud Run, you first need to build the Docker image. Replace `<project-id>` with your actual Google Cloud project ID.

    ```bash
    docker build -t gcr.io/<project-id>/sentiment-analysis .
    ```

2.  **Step 2: Push the Docker Image to Google Container Registry**

    After building the image, push it to Google Container Registry (GCR):

    ```bash
    docker push gcr.io/<project-id>/sentiment-analysis
    ```

3.  **Step 3: Deploy the Image to Cloud Run**

    Now, deploy the image to Google Cloud Run:

    ```bash
    gcloud run deploy sentiment-analysis \
      --image gcr.io/<project-id>/sentiment-analysis \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --memory 1Gi
    ```

## API Usage

-   **Endpoint**: `/predict`
-   **Method**: `POST`
-   **Body**: The request body should be in JSON format with a `text` field containing the sentence to be analyzed.

**Example request:**

```json
{
  "text": "I love this product!"
}

**Response:**

The API will return a JSON object with the sentiment prediction (0 for negative, 1 for neutral, 2 for positive) and the probability score.

Example response:

JSON

{
  "sentiment": 2,
  "probability": 0.95
}
```

## Important Notes
Permissions: Make sure your Cloud Run service account has permission to read from the GCS bucket (roles/storage.objectViewer).

Credentials: If running locally or in a custom environment, set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your service account credentials. On Cloud Run, it uses the default service account.
Additional Notes

The application uses a pre-trained sentiment analysis model saved in Google Cloud Storage (GCS). The model is loaded when the application starts.

The application also uses a tokenizer (saved as a .pickle file) to preprocess the input text before making predictions.

## License
This project is licensed under the MIT License.