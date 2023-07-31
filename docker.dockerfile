# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python requirements file to the container
COPY requirements.txt .

# Install the required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the web scraping script to the container
COPY web_scraping.py .

# Copy the SQLite database file to the container (if needed)
# COPY currency_data.db .

# Run the Python script when the container starts
CMD ["python", "web_scraping.py"]
