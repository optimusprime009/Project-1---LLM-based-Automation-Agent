# Use the official Python image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies (added `openai`)
RUN pip install --no-cache-dir fastapi uvicorn requests gitpython beautifulsoup4 numpy openai

# Expose the FastAPI port
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
