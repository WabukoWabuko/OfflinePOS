# OfflinePOS Setup Guide

Hey there! This guide will help you run the OfflinePOS system entirely in Docker containers, so you don’t need to worry about local machine issues. It’s super beginner-friendly, let’s go!

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
- **Terminal**: Use Terminal (macOS/Linux) or Command Prompt (Windows).

## Step 1: Clone the Repository
1. Open your terminal.
2. Navigate to your project directory:
   ```bash
   cd ~/Desktop
   ```
3. Clone the repo:
   ```bash
   git clone https://github.com/YourUsername/OfflinePOS.git
   cd OfflinePOS
   ```
   Replace `YourUsername` with your GitHub username.

## Step 2: Run with Docker
1. Start both backend and frontend:
   ```bash
   docker-compose up --build
   ```
2. Access the services:
   - **Backend API**: `http://localhost:5000`
   - **Frontend (web)**: `http://localhost:8000` (open in a browser)
3. To stop:
   ```bash
   docker-compose down
   ```

## Step 3: Test the System
1. **Frontend**:
   - Open `http://localhost:8000` in a browser.
   - Check the login screen with:
     - Username/password fields.
     - Online/offline status (green/red).
     - Dark mode toggle.
     - Language switch (English/Spanish).
2. **Backend API**:
   - Test with `curl` or Postman:
     ```bash
     # Register a user
     curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123","role":"admin"}' http://localhost:5000/api/register
     # Login
     curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}' http://localhost:5000/api/login
     ```
3. **Logs**:
   - View container logs:
     ```bash
     docker-compose logs offlinepos
     ```
   - Check backend logs in `logs/backend.log` (in the project root).

## Step 4: Test Offline Features
1. **Network Status**:
   - The login screen (`http://localhost:8000`) shows online/offline status.
   - Test standalone:
     ```bash
     docker exec -it offlinepos python app/utils/network.py
     ```
2. **Backup/Restore**:
   - Create a backup:
     ```bash
     docker exec -it offlinepos python app/utils/backup.py
     ```
   - Check `backups/` for the backup file.
3. **Cloud Sync (Placeholder)**:
   - Run:
     ```bash
     docker exec -it offlinepos python app/utils/sync.py
     ```

## Troubleshooting
- **Docker not starting**: Ensure Docker is running (`sudo systemctl start docker`) and you’re in the `docker` group.
- **Port conflict**: If ports 5000 or 8000 are in use, edit `docker-compose.yml` (e.g., `5001:5000`, `8001:8000`).
- **Database issues**: Check if `offline_pos.db` exists in the project root.
- **Frontend not loading**: Ensure `http://localhost:8000` is accessed, not `https`.

## Next Steps
- Connect the login screen to the backend API.
- Build the dashboard and other UI screens.
- Implement full cloud sync with PostgreSQL.
- Package the app for Windows/macOS/Linux.

If you get stuck, check the GitHub issues page or ask for help!