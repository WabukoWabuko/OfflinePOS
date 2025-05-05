# OfflinePOS Setup Guide

Hey there! This guide will get you started with OfflinePOS using Docker, perfect for any machine. It’s beginner-friendly, so let’s dive in!

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
1. Start the container (not yet implemented, will be added in Phase 2):
   ```bash
   docker-compose up --build
   ```
2. Stop the container:
   ```bash
   docker-compose down
   ```

## Troubleshooting
- **Docker not starting**: Ensure Docker is running (`sudo systemctl start docker`) and you’re in the `docker` group.
- **Git issues**: Verify Git is installed (`git --version`) and the repo URL is correct.

## Next Steps
- Phase 2: Set up backend, frontend, and database.
- Check `docs/` for updates after each phase.