# Use official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies (including Playwright)
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browser binaries and OS dependencies
# This works here because Docker is running as root during the build phase!
RUN playwright install chromium --with-deps

# Copy the rest of the application code
COPY . .

# Expose the port (Render will dynamically inject $PORT)
EXPOSE 8000

# Command to run the application
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
