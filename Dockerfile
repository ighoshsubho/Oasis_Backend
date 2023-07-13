# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code to the container
COPY . .

# Expose the port on which the FastAPI app will run
EXPOSE 8000

# Set the Redis connection details as environment variables
ENV REDIS_PORT=18297

# Start the FastAPI app using Uvicorn server with Redis caching
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]