# how to INSTALL
- 0. Update your Pip: pip install --upgrade pip
- 1. Create a venv: (On Windows OS open cmd, navigate to the bot path and use this command: virtualenv venv)
- 1.1 Them use this command: .\venv\Scripts\activate
- 1.2 You need Install the requirements and DotEnv
- 1.2.1 update your pip in your virtual venv: pip install --upgrade pip
- 1.2.2 Install: pip install -r requirements.txt
- 2. Change the file name ".env.example" to ".env"
- 2.1 Open .env and edit it with notepad
- 3. Run the bot: main.py (this main.py is inside the folder bot: bot/main.py)


# Install - Upgrade PIP
pip install --upgrade pip

# Install the requirements
pip install -r requirements.txt

# Install DotEnv
pip install python-dotenv

# Some useful commands
# Discord Install
pip install discord.py

# Discord[VOICE] Install
python -m pip install -U discord.py[voice]

# To install the libraries within requirements.txt, run the code below in the terminal:
pip install -r requirements.txt

# To create requirements.txt, run the code below in the terminal
pip freeze > requirements.txt
