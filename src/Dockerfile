# Use the official Python base image
FROM python:latest

# Set the working directory in the Docker container
WORKDIR /workspace

# Copy the requirements.txt file into the container
COPY requirements.txt /workspace/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code into the container
# COPY . /workspace/

# Command to run when the container starts
# CMD ["python", "your_script.py"]
