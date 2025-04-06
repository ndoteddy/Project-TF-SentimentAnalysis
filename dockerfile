# Use an official TensorFlow runtime as the base image
FROM tensorflow/tensorflow:2.10.0

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the app and model
COPY . .

EXPOSE 8080
# Run the app
CMD ["python", "app.py"]




