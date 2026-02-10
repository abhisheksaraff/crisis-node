FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# 1. Copy and install requirements first (to leverage Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the rest of your backend folder content into /app
COPY . .

# 3. Ensure the /app directory is in the Python Path
ENV PYTHONPATH=/app

# 4. Start Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]