# BOT Background Tasks

## Prerequisites
- Python 3.x installed
- Pip installed
- Virtualenv installed (Optional but recommended for isolated environment)
  
# HOW to INSTALL - Steps to Set Up and Run the Bot
### 1. Update Pip
```bash
# On Windows
python -m pip install --upgrade pip
# On Linux
pip install --upgrade pip
```
### 2. Create and Activate Virtual Environment
- On Windows
```bash
# Navigate to the bot directory
cd path/to/bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```
- On Linux
```bash
# Navigate to the bot directory
cd path/to/bot

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```
### 3. Install Requirements
```bash
# Upgrade pip within the virtual environment
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```
### 4. Set Up Environment Variables
- Copy and rename the .env.example file to .env
- Open the .env file and edit it with your bot/application information

### 5. Run the Bot
```bash
# Run the bot from the 'bot' folder
python bot/main.py
```

# Some useful commands[Windows]

## Install DotEnv
pip install python-dotenv

## Discord Install
pip install discord.py

## Install - Upgrade PIP
pip install --upgrade pip

## Discord[VOICE] Install
python -m pip install -U discord.py[voice]

## To install the libraries within requirements.txt, run the code below in the terminal:
pip install -r requirements.txt

## To create requirements.txt, run the code below in the terminal
pip freeze > requirements.txt
