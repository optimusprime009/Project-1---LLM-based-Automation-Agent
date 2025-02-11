# LLM-Based Automation Agent

## 📌 Overview
The **LLM-Based Automation Agent** is a FastAPI-based automation tool designed to process plain-English tasks, execute various operations, and generate verifiable outputs. The agent uses **GPT-4o-Mini** to interpret tasks and automate routine operations such as file processing, data extraction, API calls, and more.

## 🚀 Features
- **Task Execution**: Runs tasks based on natural language commands.
- **File Processing**: Reads and modifies files securely.
- **LLM Integration**: Uses GPT-4o-Mini for processing ambiguous instructions.
- **Docker Support**: Easily deployable as a containerized service.
- **Security Constraints**: Prevents access to unauthorized files and deletion operations.

## 🛠️ Installation
### **1. Clone the Repository**
```sh
git clone https://github.com/your-username/automation-agent.git
cd automation-agent
```

### **2. Install Dependencies**
Ensure Python 3.12+ is installed, then run:
```sh
pip install -r requirements.txt
```

### **3. Set Up API Key**
Obtain an AI Proxy token and export it:
```sh
export AIPROXY_TOKEN=your_api_key  # Linux/macOS
set AIPROXY_TOKEN=your_api_key  # Windows
```

### **4. Run the Application**
```sh
uvicorn main:app --reload
```

## 🐳 Docker Deployment
### **1. Build the Docker Image**
```sh
docker build -t automation-agent .
```

### **2. Run the Container**
```sh
docker run -p 8000:8000 -e AIPROXY_TOKEN=your_api_key automation-agent
```

## 📡 API Usage
### **1. Execute a Task**
**Endpoint:** `POST /run`
```sh
curl -X POST "http://127.0.0.1:8000/run" -H "Content-Type: application/json" -d '{"task": "Fetch data from an API and save it"}'
```

**Response:**
```json
{"message": "Fetched data from API and saved."}
```

### **2. Read a File**
**Endpoint:** `GET /read?path=/data/api-data.json`
```sh
curl -X GET "http://127.0.0.1:8000/read?path=/data/api-data.json"
```

## 📂 Project Structure
```
├── main.py            # FastAPI application
├── Dockerfile         # Docker container setup
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
├── LICENSE            # MIT License
├── tests/             # Unit tests directory
├── data/              # Storage directory for processed files
├── .gitignore         # Git ignore file
├── .gitattributes     # Git attributes file
└── .dockerignore      # Docker ignore file
```

## 🤝 Contribution
Contributions are welcome! To contribute:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

## 📜 License
This project is licensed under the **MIT License**.

## 📧 Contact
For any queries, contact: `your.email@example.com`


 
