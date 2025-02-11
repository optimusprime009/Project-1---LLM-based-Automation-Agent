from fastapi import FastAPI, HTTPException
import os
import subprocess
import json
import sqlite3
import requests
from datetime import datetime
from pathlib import Path
import git
from bs4 import BeautifulSoup
from pydantic import BaseModel
import openai
import numpy as np
from PIL import Image
from pydub import AudioSegment
import markdown
import pandas as pd

# Load OpenAI API Key
api_key = os.getenv("AIPROXY_TOKEN") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OpenAI API key. Set AIPROXY_TOKEN or OPENAI_API_KEY.")

openai_client = openai.Client(api_key=api_key)

app = FastAPI()

class TaskRequest(BaseModel):
    task: str

def execute_task(task: str):
    task = task.lower()
    if "install uv and run datagen" in task:
        return task_a1()
    elif "format" in task and "prettier" in task:
        return task_a2()
    elif "count wednesdays" in task:
        return task_a3()
    elif "sort contacts" in task:
        return task_a4()
    elif "extract first lines from recent logs" in task:
        return task_a5()
    elif "generate markdown index" in task:
        return task_a6()
    elif "extract sender email" in task:
        return task_a7()
    elif "extract credit card number" in task:
        return task_a8()
    elif "find similar comments" in task:
        return task_a9()
    elif "compute total sales" in task:
        return task_a10()
    elif "fetch data from api" in task:
        return task_b3()
    elif "clone git repo" in task:
        return task_b4()
    elif "run sql query" in task:
        return task_b5()
    elif "scrape website" in task:
        return task_b6()
    elif "compress image" in task:
        return task_b7()
    elif "transcribe mp3" in task:
        return task_b8()
    elif "convert markdown to html" in task:
        return task_b9()
    elif "filter csv" in task:
        return task_b10()
    else:
        raise HTTPException(status_code=400, detail="Unknown task.")

# ---------------- TASK IMPLEMENTATIONS ---------------- #

def task_a1():
    subprocess.run(["pip", "install", "uv"], check=True)
    subprocess.run(["python", "datagen.py", os.environ.get("USER_EMAIL", "test@example.com")], check=True)
    return "Datagen script executed."

def task_a2():
    subprocess.run(["npx", "prettier", "--write", "/data/format.md"], check=True)
    return "Formatted /data/format.md."

def task_a3():
    with open("/data/dates.txt", "r") as f:
        dates = [line.strip() for line in f.readlines()]
    wednesday_count = sum(1 for date in dates if datetime.strptime(date, "%Y-%m-%d").weekday() == 2)
    with open("/data/dates-wednesdays.txt", "w") as f:
        f.write(str(wednesday_count))
    return "Wednesdays counted and saved."

def task_a4():
    with open("/data/contacts.json", "r") as f:
        contacts = json.load(f)
    contacts.sort(key=lambda x: (x["last_name"], x["first_name"]))
    with open("/data/contacts-sorted.json", "w") as f:
        json.dump(contacts, f, indent=4)
    return "Contacts sorted and saved."

def task_a5():
    logs = sorted(Path("/data/logs").glob("*.log"), key=os.path.getmtime, reverse=True)[:10]
    with open("/data/logs-recent.txt", "w") as f:
        for log in logs:
            with open(log, "r") as lf:
                f.write(lf.readline())
    return "Recent log lines extracted."

def task_a6():
    index = {}
    for md_file in Path("/data/docs").rglob("*.md"):
        with open(md_file, "r") as f:
            for line in f:
                if line.startswith("# "):
                    index[md_file.name] = line[2:].strip()
                    break
    with open("/data/docs/index.json", "w") as f:
        json.dump(index, f, indent=4)
    return "Markdown index created."

def task_a7():
    return "LLM extraction of sender email not implemented yet."

def task_a8():
    return "LLM extraction of credit card number not implemented yet."

def task_a9():
    return "Embedding-based comment similarity detection not implemented yet."

def task_a10():
    conn = sqlite3.connect("/data/ticket-sales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type='Gold'")
    total_sales = cursor.fetchone()[0] or 0
    conn.close()
    with open("/data/ticket-sales-gold.txt", "w") as f:
        f.write(str(total_sales))
    return "Total sales calculated and saved."

def task_b3():
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    with open("/data/api-data.json", "w") as f:
        json.dump(response.json(), f, indent=4)
    return "Fetched data from API and saved."

def task_b4():
    repo_url = "https://github.com/example/repo.git"
    repo_path = "/data/repo"
    git.Repo.clone_from(repo_url, repo_path)
    return "Git repository cloned."

def task_b5():
    conn = sqlite3.connect("/data/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    result = cursor.fetchone()[0]
    conn.close()
    with open("/data/sql-query-result.txt", "w") as f:
        f.write(str(result))
    return "SQL query executed and result saved."

def task_b6():
    return "Website scraping not implemented yet."

def task_b7():
    return "Image compression not implemented yet."

def task_b8():
    return "Audio transcription not implemented yet."

def task_b9():
    return "Markdown conversion not implemented yet."

def task_b10():
    return "CSV filtering not implemented yet."

@app.post("/run")
def run_task(request: TaskRequest):
    result = execute_task(request.task)
    return {"message": result}

@app.get("/read")
def read_file(path: str):
    if not path.startswith("/data/"):
        raise HTTPException(status_code=400, detail="Access to this path is restricted.")
    try:
        with open(path, "r") as file:
            return {"content": file.read()}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")
