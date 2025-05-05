# OfflinePOS Setup Guide

Hey there! This guide will get you running OfflinePOS in Docker, perfect for any machine. It’s beginner-friendly, so let’s go!

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
1. Navigate to your project directory:
   ```bash
   cd ~/Desktop
   ```
2. Clone the repo:
   ```bash
   git clone https://github.com/YourUsername/OfflinePOS.git
   cd OfflinePOS
   ```

## Step 2: Run with Docker
1. Start the backend and frontend:
   ```bash
   docker-compose up --build
   ```
2. Access:
   - **Frontend**: `http://localhost:8000` (browser)
   - **Backend API**: `http://localhost:5000` (via `curl` or Postman)
3. Stop:
   ```bash
   docker-compose down
   ```

## Step 3: Test the System
1. **Frontend**:
   - Open `http://localhost:8000` in a browser.
   - Verify the login screen with username/password fields and a login button.
2. **Backend API**:
   - Test with `curl`:
     ```bash
     # Register a user
     curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123","role":"admin"}' http://localhost:5000/api/register
     # Login
     curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}' http://localhost:5000/api/login
     ```
   - Expected login output:
     ```json
     {"message":"Login successful","role":"admin","user_id":1}
     ```
3. **Logs**:
   - Check backend logs:
     ```bash
     docker-compose logs offlinepos
     cat logs/backend.log
     ```

## Troubleshooting
- **Docker not starting**: Ensure Docker is running (`sudo systemctl start docker`) and you’re in the `docker` group.
- **Port conflict**: If ports 5000 or 8000 are in use, edit `docker-compose.yml` (e.g., `5001:5000`, `8001:8000`).
- **Database issues**: Check if `offline_pos.db` exists in the project root.
- **Frontend not loading**: Use `http://localhost:8000` (not `https`).

## Next Steps
- Phase 3: Add offline features and cloud sync.
- Phase 4: Implement dark mode, localization, and more.
- Check `docs/` for updates.