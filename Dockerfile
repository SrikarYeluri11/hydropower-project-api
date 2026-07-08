# Use official Python image
FROM python:3.10

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the rest of the files into the container
COPY . .

# Hugging Face Spaces requires apps to run on port 7860
EXPOSE 7860

# Start the Flask API using Gunicorn on port 7860
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:7860"]
