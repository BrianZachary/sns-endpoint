FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY sns_listener.py .

# Expose the port the app runs on
EXPOSE 8080

# Run the application
ENTRYPOINT ["python", "sns_listener.py"]
