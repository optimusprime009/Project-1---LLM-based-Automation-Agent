from fastapi import FastAPI, HTTPException
import os
import subprocess
import json
import sqlite3
import requests
from datetime import datetime
from collections import Counter
from pathlib import Path
import git
from bs4 import BeautifulSoup
from pydantic import BaseModel

app = FastAPI()

class TaskRequest(BaseModel):
    task: str

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
    elif "fetch data from api" in task.lower():
        return task_b3()
    elif "clone git repo" in task.lower():
        return task_b4()
    elif "run sql query" in task.lower():
        return task_b5()
    elif "scrape website" in task.lower():
        return task_b6()
    else:
        raise HTTPException(status_code=400, detail="Unknown task.")


def task_b3():
    try:
        print("Fetching data from API...")  # Debugging line
        response = requests.get("https://jsonplaceholder.typicode.com/todos/1")

        if response.status_code == 200:
            print("API request successful.")  # Debugging line
            
            # ✅ Create /data/ folder if it does not exist
            os.makedirs("data", exist_ok=True)

            # ✅ Write to data/api-data.json (without leading "/")
            with open("data/api-data.json", "w") as f:
                json.dump(response.json(), f, indent=4)
            return "Fetched data from API and saved."

        print(f"API request failed with status code: {response.status_code}")
        return f"Failed to fetch data. Status code: {response.status_code}"

    except Exception as e:
        print(f"Error in task_b3: {e}")  # Print error to FastAPI logs
        raise HTTPException(status_code=500, detail=str(e))  # Return error message


def task_b4():
    repo_url = "https://github.com/example/repo.git"
    repo_path = "/data/repo"
    if not os.path.exists(repo_path):
        git.Repo.clone_from(repo_url, repo_path)
    repo = git.Repo(repo_path)
    with open(os.path.join(repo_path, "new_file.txt"), "w") as f:
        f.write("This is a new commit.")
    repo.index.add(["new_file.txt"])
    repo.index.commit("Added new file")
    return "Git repository cloned and committed."

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
    url = "https://example.com"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "No Title"
        with open("/data/scraped-data.txt", "w") as f:
            f.write(title)
        return "Website scraped and data saved."
    return "Failed to scrape website."

@app.post("/run")
def run_task(request: TaskRequest):
    result = execute_task(request.task)
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
