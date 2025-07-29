# Use full Python image instead of slim
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the app
CMD ["gunicorn", "news.wsgi:application", "--bind", "0.0.0.0:8000"]
