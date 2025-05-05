# OfflinePOS Setup Guide

Hey there! This guide will help you set up the OfflinePOS system using Docker to avoid local machine issues. It’s beginner-friendly, so let’s dive in!

## Prerequisites
- **Docker**: Install Docker and Docker Compose:
  - Ubuntu:
    ```bash
    sudo apt update
    sudo apt install docker.io docker-compose
    sudo usermod -aG docker $USER
    ```
    Log out and back in.
  - Verify: `docker --version`, `docker-compose --version`.
- **Git**: Install from [git-scm.com](https://git-scm.com).
- **Code Editor**: Use [VS Code](https://code.visualstudio.com).
- **Terminal**: Use Terminal (macOS/Linux) or Command Prompt (Windows).

## Step 1: Clone the Repository
1. Open your terminal.
2. Navigate to your project directory (e.g., `cd ~/Desktop`).
3. Clone the repo:
   ```bash
   git clone https://github.com/YourUsername/OfflinePOS.git
   cd OfflinePOS
   ```
   Replace `YourUsername` with your GitHub username.

## Step 2: Run with Docker
1. Start the backend:
   ```bash
   docker-compose up --build
   ```
2. The Flask API will be at `http://localhost:5000`.
3. To stop, press `Ctrl+C` or run:
   ```bash
   docker-compose down
   ```

## Step 3: Run the Frontend (Local)
The frontend isn’t containerized yet, so run it locally:
1. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the login screen:
   ```bash
   python app/frontend/main.py
   ```
4. You’ll see the login screen with:
   - Online/offline status (green/red).
   - Dark mode toggle.
   - Language switch (English/Spanish).

## Step 4: Test the API
Test the backend with `curl` or Postman:
1. Register a user:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123","role":"admin"}' http://localhost:5000/api/register
   ```
2. Login:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}' http://localhost:5000/api/login
   ```

## Step 5: Test Offline Features
1. **Network Status**: The login screen shows online/offline status.
2. **Backup/Restore**:
   - Run:
     ```bash
     python app/utils/backup.py
     ```
   - Check `backups/` for the backup file.
3. **Cloud Sync (Placeholder)**:
   - Run:
     ```bash
     python app/utils/sync.py
     ```

## Step 6: Check Logs
- Backend logs are in `logs/backend.log` (inside the Docker container).
- To view:
  ```bash
  docker-compose logs backend
  ```

## Troubleshooting
- **Docker not starting**: Ensure Docker is running (`sudo systemctl start docker`) and you’re in the `docker` group.
- **ModuleNotFoundError**: Docker sets `PYTHONPATH`, so this should be resolved. If running locally, use `PYTHONPATH=. python app/backend/app.py`.
- **Port conflict**: If `port 5000` is in use, edit `docker-compose.yml` to change the port (e.g., `5001:5000`).
- **Database issues**: Check if `offline_pos.db` exists in the project root.

## Next Steps
- Containerize the frontend.
- Connect the login screen to the backend API.
- Implement full cloud sync with PostgreSQL.
- Build the dashboard and other features.

If you get stuck, check the GitHub issues page or ask for help!