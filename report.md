🐍 Backdoor Snake Game - Complete Documentation
📋 Table of Contents
Project Overview

System Requirements

Quick Start

Detailed Setup Guide

How to Play

Feature Verification

Troubleshooting

Grading Criteria

🎯 Project Overview
This educational project demonstrates cybersecurity concepts through a classic Snake game. It shows how applications can incorporate security mechanisms for learning purposes.

Learning Objectives:

How applications check for dependencies

How persistence mechanisms work

How reverse shells operate

The importance of security awareness

💻 System Requirements
Component	Requirement
Operating System	Windows 10/11
Python Version	3.8 or higher
RAM	4GB minimum
Disk Space	100MB free
Network	Localhost access (ports 8080, 4444)
🚀 Quick Start
Project Structure
text
D:\Backdoor\
│
├── 📁 server/                    # Dependency server
│   ├── server.py                  # HTTP server
│   └── 📁 dependencies/            # Wheel files
│       ├── pygame-2.6.1-cp312-cp312-win_amd64.whl
│       └── requests-2.32.5-py3-none-any.whl
│
├── 📁 game/                       # Main game
│   └── snake_game.py               # Snake game with backdoor
│
├── 📁 listener/                   # Attacker control
│   └── listener.py                  # Reverse shell listener
│
└── 📁 cleaner/                    # Cleanup application
    └── cleaner.py                   # Removes persistence
📦 Detailed Setup Guide
Step 1: Install Python
powershell
# Check Python version
python --version
# Must be 3.8 or higher
Step 2: Download Wheel Files
Download these files and place them in D:\Backdoor\server\dependencies\:

File	Download Link
pygame-2.6.1-cp312-cp312-win_amd64.whl	https://pypi.org/project/pygame/#files
requests-2.32.5-py3-none-any.whl	https://pypi.org/project/requests/#files
powershell
# Verify files are in place
dir D:\Backdoor\server\dependencies
Step 3: Open FOUR Terminals
Terminal 1 - Start Dependency Server
powershell
cd D:\Backdoor\server
python server.py
Expected Output:

text
============================================================
BACKDOOR SNAKE GAME - DEPENDENCY SERVER
============================================================
Server started at http://localhost:8080
Serving dependencies from: D:\Backdoor\server\dependencies

Available files:
  - pygame-2.6.1-cp312-cp312-win_amd64.whl (10.13 MB)
  - requests-2.32.5-py3-none-any.whl (0.06 MB)

Waiting for connections...
✅ Keep this terminal open

Terminal 2 - Start Listener
powershell
cd D:\Backdoor\listener
python listener.py
Expected Output:

text
[*] Listening on 0.0.0.0:4444
[*] Waiting for connections...
✅ Keep this terminal open

Terminal 3 - Run Game (First Time)
powershell
cd D:\Backdoor\game

# Uninstall existing modules to test fresh installation
pip uninstall pygame requests -y

# Run the game
python snake_game.py
Terminal 4 - Run Cleaner
powershell
cd D:\Backdoor\cleaner
python cleaner.py
🎮 How to Play
Game Controls
Key	Action
⬆️ Arrow Up	Move snake up
⬇️ Arrow Down	Move snake down
⬅️ Arrow Left	Move snake left
➡️ Arrow Right	Move snake right
P	Pause/Resume
R	Restart after game over
ESC	Exit game
Game Rules
Eat red apples to grow (+10 points)

Don't hit the walls

Don't collide with yourself

Try to achieve highest score

✅ Feature Verification
Feature 1: Dependency Installation
What should happen:

Game checks for pygame and requests

Dialog boxes ask for permission

Files download from local server

Installation completes

Game starts

Verification Commands:

powershell
# After game runs, check if modules installed
pip list | findstr pygame
pip list | findstr requests
Feature 2: Reverse Shell Access
Check Terminal 2 - Should see:

text
[*] Listening on 0.0.0.0:4444
[*] Waiting for connections...
[+] Connection from ('127.0.0.1', 54321)
[+] Interactive shell opened.

[+] Connection Established
    Hostname: DESKTOP-XXXXXX
    OS: Windows 10
    Python: 3.12.6
    Current User: username
    Working Directory: D:\Backdoor\game
Test Shell Commands:

powershell
shell> whoami
# Shows username

shell> dir
# Lists directory contents

shell> ipconfig
# Shows network config

shell> cd ..
# Changes directory

shell> echo test
# Prints: test

shell> exit
# Closes connection
Feature 3: Persistence
Check Registry:

powershell
# Open Registry Editor
regedit

# Navigate to:
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run

# Look for:
Name: WindowsUpdateService
Value: "C:\Python312\python.exe" "D:\Backdoor\game\snake_game.py"
Check Startup Folder:

powershell
# Open Explorer and paste:
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

# Look for:
SystemHelper.bat
Quick Command:

powershell
# Check both with one command
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
Feature 4: No Interruption
Test while playing:

Game runs at steady 10 FPS

Open other applications - no lag

Run shell commands - game continues

Download files - game smooth

Feature 5: Cleaner Application
Test Cleaner Functions:

Run cleaner:

powershell
cd D:\Backdoor\cleaner
python cleaner.py
Verify detection - Should show:

Registry: WindowsUpdateService

Startup File: SystemHelper.bat

Test buttons:

Click "Select All" - all items highlight

Click "Deselect All" - items unhighlight

Click "Refresh" - list reloads

Remove items:

Click "Remove Selected Items"

Click "Yes" on confirmation

Progress bar appears

Success message shows

Verify removal:

powershell
# Check registry - entry should be gone
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run

# Check startup folder - file should be gone
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
🔍 Quick Test Commands
Test Server
powershell
# Open browser and visit:
http://localhost:8080
http://localhost:8080/check-deps
http://localhost:8080/list-deps
http://localhost:8080/dependencies/requests-2.32.5-py3-none-any.whl
Test All Features at Once
powershell
# Create test script: test_all.bat
@echo off
echo TESTING BACKDOOR SNAKE GAME
echo ============================
echo.
echo 1. Testing Python version:
python --version
echo.
echo 2. Testing server connection:
curl -s http://localhost:8080/check-deps
echo.
echo 3. Checking dependencies folder:
dir D:\Backdoor\server\dependencies
echo.
echo 4. Checking persistence:
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
echo.
echo 5. Checking ports:
netstat -an | findstr 8080
netstat -an | findstr 4444
echo.
echo 6. Checking installed modules:
pip list | findstr pygame
pip list | findstr requests
🚨 Troubleshooting
Common Issues
Problem	Solution
"No module named 'requests'"	pip install requests
"Address already in use"	taskkill /F /IM python.exe
"404 Not Found"	Check filenames in dependencies folder
"Invalid wheel filename"	Download correct wheel for Python 3.12
No shell connection	New-NetFirewallRule -DisplayName "Allow 4444" -Direction Inbound -LocalPort 4444 -Protocol TCP -Action Allow
Persistence not working	Run game as administrator
Cleaner not detecting items	Click "Refresh" button
Reset Everything
powershell
# Kill all Python processes
taskkill /F /IM python.exe

# Remove persistence manually
reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v WindowsUpdateService /f
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\SystemHelper.bat"

# Uninstall modules
pip uninstall pygame requests -y

# Clear pip cache
pip cache purge
