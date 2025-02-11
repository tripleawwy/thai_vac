FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy the project files
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expose the port the app runs on
EXPOSE 8050

# Run the Dash app
CMD ["python", "app.py"]
