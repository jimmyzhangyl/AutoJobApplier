# AutoJobApplier

Automate your next job application process

## How it works?

Step1: Collect user searching critals (user submit form in frontend application)
Step2: Seaching on job ads platforms (only support Seek at the moment)
Step3: Scrap job details and filted with user critals <-- Current stage
Step4: Ask ChatGPT model preparing cover letter
Step5: Submit application with Selenium

### Seek model: key parts

Critical css elements and workflows: Manually figure out from seek.com

## Developer manual

Python 3.8 or higher
Framework: python/flask

## Installation Instructions

1.Initialize Virtual Environment
Navigate to the backend directory and run:
`python -m venv venv`

2.Activate the virtual environment

- On Windows:
  `.\venv\Scripts\activate`
- On macOS/Linux:
  `source venv/bin/activate`

  3.Install the required dependencies
  It is recommended to install from setup.py in the backend folder:
  `pip install .`
  Alternatively, you can install from requirements.txt:
  `pip install -r requirements.txt`

  4.Start the Flask application.
  `python server/app.py`

Q: showing errors like `Import "flask" could not be resolved`
A: Means your python interpeter path is incorrect, it is not pointing to current venv that contains lib this project need.
known issue with mac: you may have an alias config to override python path. To check this run `alias` in your terminal
-Temporaty disable alias: `unalias python`
-Permanently Remove or Modify the Alias, comment out line with `#` or delete the line 
    --If you are using zsh (the default shell on macOS Catalina and later):`nano ~/.zshrc`
    --For bash (if you're using an older shell or have switched):`nano ~/.bashrc`
    --For bash on login shells:`nano ~/.bash_profile`
  remember to reload the shell configuration `source ~/.zshrc` (If you edited a different file, replace ~/.zshrc with the appropriate file path.)
(ref to this article https://www.reddit.com/r/learnpython/comments/1azfh5r/pythons_path_on_macos/)

## Helpful commands and tips

### Testing

`pytest`

### Updating Requirements File

Ensure your virtual environment is active.
Update requirements.txt
`pip freeze > requirements.txt`

### Uninstall All Packages

-On Windows
`pip freeze | ForEach-Object { pip uninstall -y $_ }`
-On Unix-based systems
`pip freeze | xargs pip uninstall -y`

### Debugging

In app.py, ensure you are loading the appropriate .env.development file for debugging purposes. This will enable logging.
-API results will be written to jobs.json.
-Logger traces can be found in app_debug.log.

## Future devolope TODO list

- integrate with firebase, allow user login with google account
- DB to store searched job ids & user related info(resume, specialized gpt prompts)
- job apply report & auto apply schedule
- Follow up email for unrecorded questions
- Enhance unrecorded questions with prefilled answer from GPT, but need comfirm from user
- secure payment mothods if deploy to public
- generatic model, utlizing ChatGpt(Or train other LLMs) to find workflow and key css tags to complete the submission task
