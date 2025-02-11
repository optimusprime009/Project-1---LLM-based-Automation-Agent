FROM python:3.12

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y ffmpeg \
    && pip install --no-cache-dir fastapi uvicorn requests gitpython beautifulsoup4 numpy openai pillow pydub markdown pandas

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
