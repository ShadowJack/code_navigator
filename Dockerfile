# Stage 1: Build the app
FROM python:3.10 AS builder

# Set the working directory in the builder stage
WORKDIR /build

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Copy the app files to the builder stage
COPY . .

# Stage 2: Create the final image
FROM python:3.10-slim

# Set the working directory in the final stage
WORKDIR /app

# Copy the built app from the builder stage to the final stage
COPY --from=builder /install /usr/local
COPY --from=builder /build .

# Set environment variables
ENV FLASK_APP=web_service.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port on which the app will run
EXPOSE 8000

# Run the app when the container starts
CMD ["flask", "run"]
