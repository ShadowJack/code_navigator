FROM python:3.10

# Set the working directory in the builder stage
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files
COPY ./code_navigator /app/code_navigator
COPY ./__init__.py .
COPY ./web_service.py .
COPY .env .

# Expose the port on which the app will run
EXPOSE 8000

# Run the app when the container starts
CMD ["uvicorn", "web_service:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
