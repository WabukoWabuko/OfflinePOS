# OfflinePOS Setup Guide

Hey there! This guide will help you set up the OfflinePOS system on your computer. It’s written for beginners, so don’t worry if you’re new to coding. Let’s get started!

## Prerequisites
- **Python 3.11**: Download and install from [python.org](https://www.python.org).
- **Git**: Install from [git-scm.com](https://git-scm.com) to manage code.
- **Code Editor**: Use [VS Code](https://code.visualstudio.com) or any text editor.
- **Terminal**: Use Command Prompt (Windows), Terminal (macOS/Linux), or VS Code’s built-in terminal.

## Step 1: Clone the Repository
1. Open your terminal.
2. Navigate to where you want the project (e.g., `cd ~/Desktop`).
3. Clone the repository:
   ```bash
   git clone https://github.com//OfflinePOS.git/WabukoWabukod OfflinePOS
   ```
   Replace `YourUsername` with your GitHub username.

## Step 2: Set Up a Virtual Environment
A virtual environment keeps the project’s dependencies separate.
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate it:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   You’ll see `(venv)` in your terminal when it’s active.

## Step 3: Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

## Step 4: Run the Frontend (Flet)
The frontend is the user interface built with Flet.
1. Run the login screen:
   ```bash
   python app/frontend/main.py
   ```
2. A window will open showing the login screen. Try typing a username and password (it won’t log in yet since we need to connect it to the backend).

## Step 5: Run the Backend (Flask)
The backend handles login and other logic.
1. In a new terminal (keep the frontend running), activate the virtual environment again:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Run the Flask app:
   ```bash
   python app/backend/app.py
   ```
3. The API will be available at `http://localhost:5000`.

## Step 6: Test the API
You can test the backend using `curl` or a tool like Postman.
1. Register a user:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123","role":"admin"}' http://localhost:5000/api/register
   ```
2. Try logging in:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}' http://localhost:5000/api/login
   ```
   You should see a “Login successful” message.

## Troubleshooting
- **Error: Module not found**: Ensure the virtual environment is active and dependencies are installed (`pip install -r requirements.txt`).
- **Database not found**: The SQLite database (`offline_pos.db`) is created automatically when you run the backend.
- **Port conflict**: If `port 5000` is in use, stop other apps or change the port in `app/backend/app.py` (e.g., `app.run(debug=True, port=5001)`).

## Next Steps
- Connect the login screen to the backend API.
- Build the dashboard and other UI screens.
- Add more backend endpoints for products, sales, etc.

If you get stuck, check the GitHub issues page or ask for help!
