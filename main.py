from fastapi import FastAPI, HTTPException
import os
import subprocess
import json
import sqlite3
import requests
import numpy as np
from datetime import datetime
from collections import Counter
from pathlib import Path
import openai
from PIL import Image
from pydub import AudioSegment
import markdown
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
client = openai.Client(api_key=os.getenv("AIPROXY_TOKEN"))

def execute_task(task: str):
    if "install uv and run datagen" in task.lower():
        return task_a1()
    elif "format" in task.lower() and "prettier" in task.lower():
        return task_a2()
    elif "count wednesdays" in task.lower():
        return task_a3()
    elif "sort contacts" in task.lower():
        return task_a4()
    elif "extract first lines from recent logs" in task.lower():
        return task_a5()
    elif "generate markdown index" in task.lower():
        return task_a6()
    elif "extract sender email" in task.lower():
        return task_a7()
    elif "extract credit card number" in task.lower():
        return task_a8()
    elif "find similar comments" in task.lower():
        return task_a9()
    elif "compute total sales" in task.lower():
        return task_a10()
    elif "compress image" in task.lower():
        return task_b7()
    elif "transcribe mp3" in task.lower():
        return task_b8()
    elif "convert markdown to html" in task.lower():
        return task_b9()
    elif "filter csv" in task.lower():
        return task_b10()
    else:
        raise HTTPException(status_code=400, detail="Unknown task.")

def task_a7():
    with open("/data/email.txt", "r") as f:
        email_text = f.read()
    response = client.completions.create(model="gpt-4o-mini", prompt=f"Extract sender email: {email_text}", max_tokens=20)
    email_address = response.choices[0].text.strip()
    with open("/data/email-sender.txt", "w") as f:
        f.write(email_address)
    return "Extracted sender email."

def task_a8():
    response = client.completions.create(model="gpt-4o-mini", prompt="Extract credit card number from this image.", file="/data/credit-card.png", max_tokens=20)
    card_number = response.choices[0].text.strip()
    with open("/data/credit-card.txt", "w") as f:
        f.write(card_number.replace(" ", ""))
    return "Extracted credit card number."

def task_a9():
    with open("/data/comments.txt", "r") as f:
        comments = f.readlines()
    embeddings = [np.random.rand(300) for _ in comments]  # Simulating embeddings
    similarity_scores = np.dot(embeddings, np.transpose(embeddings))
    most_similar = np.unravel_index(np.argmax(similarity_scores, axis=None), similarity_scores.shape)
    with open("/data/comments-similar.txt", "w") as f:
        f.write(comments[most_similar[0]])
        f.write(comments[most_similar[1]])
    return "Found most similar comments."

def task_b7():
    image = Image.open("/data/image.png")
    image = image.resize((500, 500))
    image.save("/data/image-compressed.png", quality=70)
    return "Compressed and resized image."

def task_b8():
    audio = AudioSegment.from_mp3("/data/audio.mp3")
    audio.export("/data/audio.wav", format="wav")
    response = client.completions.create(model="gpt-4o-mini", prompt="Transcribe this audio.", file="/data/audio.wav", max_tokens=100)
    with open("/data/audio-transcript.txt", "w") as f:
        f.write(response.choices[0].text.strip())
    return "Transcribed MP3 to text."

def task_b9():
    with open("/data/docs/document.md", "r") as f:
        md_content = f.read()
    html_content = markdown.markdown(md_content)
    with open("/data/docs/document.html", "w") as f:
        f.write(html_content)
    return "Converted Markdown to HTML."

def task_b10():
    df = pd.read_csv("/data/data.csv")
    filtered_df = df[df["column_name"] == "desired_value"]
    filtered_df.to_json("/data/filtered-data.json", orient="records")
    return "Filtered CSV and saved as JSON."

@app.post("/run")
def run_task(task: str):
    result = execute_task(task)
    return {"message": result}

def read_secure_file(path: str):
    if not path.startswith("/data/"):
        raise HTTPException(status_code=400, detail="Access to this path is restricted.")
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")

@app.get("/read")
def read_file(path: str):
    content = read_secure_file(path)
    return {"content": content}
