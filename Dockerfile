# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    ffmpeg \
    libespeak1 \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    opencv-python \
    pytesseract \
    pyttsx3 \
    numpy

# Install additional Tesseract language packs (optional)
RUN apt-get update && apt-get install -y \
    tesseract-ocr-eng \
    tesseract-ocr-fra \
    tesseract-ocr-deu

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Make port 80 available to the world outside this container
EXPOSE 80

# Define volume for image input/output
VOLUME ["/app/images", "/app/ocr_outputs"]

# Run script when the container launches
CMD ["python", "img-to-text.py"]

