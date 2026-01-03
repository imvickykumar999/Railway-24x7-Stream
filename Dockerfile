# Use a lightweight Python image
FROM python:3.9-slim

# Install FFmpeg (required to run the ffmpeg command inside Python)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the script and the video file into the container
# Ensure your video file is named 'video.mp4' or update stream.py
COPY stream.py .
COPY video.mp4 .

# Run the python script
CMD ["python", "stream.py"]
