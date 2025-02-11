from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/run")
def run_task(task: str):
    # Placeholder for task execution logic
    return {"message": f"Task '{task}' received and will be processed."}

@app.get("/read")
def read_file(path: str):
    try:
        # Security check: Ensure path is within /data
        if not path.startswith("/data/"):
            raise HTTPException(status_code=400, detail="Access to this path is restricted.")
        
        with open(path, "r") as file:
            content = file.read()
        return {"content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")
