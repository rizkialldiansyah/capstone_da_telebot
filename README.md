# Telegram Chatbot

This is developed as one of [Algoritma Academy](https://algorit.ma/) Data Analytics Specialization Capstone Projects. The deliverable of this project is a Python script to create a Telegram chatbot using `telebot` package. We will also deploy the chatbot to [Railway](https://railway.app/) and use `Flask` to set up the backend application.

## Rubrics

The maximum score you will obtain from this project is 16 points:  

- **Setup (3 points)**
    - [ ] **Prepare virtual environment**
      - Please provide `requirements.txt` on the project folder.
    - [ ] **Create Telegram bot API via BotFather**
      - Please provide your bot link when making a submission.
    - [ ] **Using `os.environ` to secure token**
      - Important: Make sure you do not push `.env` to your GitHub Repository.

- **Chatbot functionalities**
    - **Basic function (3 points)**
        - [ ] **Command `/start` or `/help`**: correctly respond to user trigger
        - [ ] **Command `/about`**: provide developer information
        - [ ] **Function `echo_all()`**: using `emoji`
    - **Summary text report: `/summary` (3 points)**
        - [ ] Perform necessary **data wrangling** steps to extract information
        - [ ] Perform the right **mathematical calculation**
        - [ ] Send **summary message** using `Template`
    - **Visualization report: `/plot` (4 points)**
        - [ ] Perform necessary **data wrangling** steps to extract information
        - [ ] Perform the right **mathematical calculation**
        - [ ] **Send plot** with caption
        - [ ] **Tidy** plot layout (title, label, color, size)
- **Application deployment (3 points)**
    - [ ] Using **`Flask`** to serve the chatbot as an application
    - [ ] **Deploy** to Railway
    - [ ] Deployed chatbot run smoothly **without error**

## Project File Structure

```
telebot
├── 📁 assets
├── 📁 cache
├── 📁 data_input
├── 📁 template_text
├── .gitignore
├── </> app.py
├── </> bot_local.py
├── 📝 Notebook Guide.ipynb
├── 🚀 Procfile
├── 📝 requirements.txt
└── 📝 runtime.txt
```

- Folders (**DO NOT CHANGE**):
    - `assets`: Images used in notebook
    - `cache`: Pickled Python object
    - `data_input`: Dataset for analysis
    - `template_text`: Text files for chat template

- Application-related Files (**TO BE COMPLETED BY STUDENT**):
    - `app.py`: Main `Flask` application
    - `bot_local.py`: Telegram bot to be run locally
    - `Notebook Guide.ipynb`: Main guide for the project workflow

- Deployment-related Files (**DO NOT CHANGE**):
    - `.gitignore`: List of file extensions to be ignored when `git push` from local
    - `Procfile`: Commands for app's dynos on Railway
    - `requirements.txt`: List of package dependencies to be installed on Railway
    - `runtime.txt`: Python version to be installed on Railway

## Requirements

- **Python 3.10**
- `emoji==2.2.0`
- `Flask==2.2.2`
- `gunicorn==20.1.0`
- `matplotlib==3.6.2`
- `pandas==1.5.2`
- `pyTelegramBotAPI==4.8.0`
- `python-dotenv==0.21.0`
- `gTTS==2.3.0`

For instructions on how to prepare the virtual environment and requirements, please read `Notebook Guide.ipynb`.

## Expected Output

### Telegram Bot Account

Create a bot that can provide report on Facebook daily ads for different marketing campaign. Here is an example: https://t.me/algo_capstone_telebot

<p align="center" width="100%">
    <img src="assets/readme/telegram-bot.png" width="350px"> 
</p>

Here are the chatbot functionalities:

1. Command `/start` or `/help`: send welcome message containing list of available commands.

<p align="center" width="100%">
    <img src="assets/readme/start.png" width="350px"> 
</p>

2. Command `/about`: send information about the bot developer.

<p align="center" width="100%">
    <img src="assets/readme/about.png" width="350px"> 
</p>

3. Command `/summary`: generate text report for selected campaign ID.

<p align="center" width="100%">
    <img src="assets/readme/summary-1.png" width="350px">
</p>

Reply from bot after campaign ID is selected:

<p align="center" width="100%">
    <img src="assets/readme/summary-2.png" width="350px">
</p>

4. Command `/plot`: generate visualization and voice message report per age group for selected campaign ID.

<p align="center" width="100%">
    <img src="assets/readme/plot-1.png" width="350px">
</p>

Reply from bot after campaign ID is selected:

<p align="center" width="100%">
    <img src="assets/readme/plot-2.png" width="350px">
</p>

**Voice message:** 
<a href="https://drive.google.com/file/d/16hVORo-heUOjWje_g62aV6380-toBwWp/view?usp=sharing" target="_blank">Sample audio for Campaign ID 916</a>

> This is your requested plot for Campaign ID 916.
> Age group with the highest total spent is 30-34, while the lowest is 40-44. 
> Age group with the highest total approved conversion is 30-34, while the lowest is 45-49.
> Age group with the highest average CPC is 45-49, while the lowest is 40-44.

5. Default message: handle messages other than the previous commands.

<p align="center" width="100%">
    <img src="assets/readme/default-message.png" width="350px">
</p>

### Deployed Application

<p align="center" width="100%">
    <img src="assets/readme/deployed-app-railway.png" width="350px"> 
</p>

This bot is expected to run **continuously** on a server. Therefore we create a `Flask` application which deployed to Railway. 