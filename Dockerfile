FROM python:3.10.12-slim

# Set the working directory
WORKDIR /app

# Copy all files to the working directory
COPY . /app

# Install espeak-ng
RUN apt-get update && apt-get install -y espeak-ng
RUN apt-get update && apt-get install -y libportaudio2

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose port 8000
EXPOSE 8000
