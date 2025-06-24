# PrepMe: AI-Powered Job Analyzer and Interview Preparation Tool

PrepMe is a GUI-based Python application that helps users:
- Analyze job postings from URLs
- Match them with their skills and portfolio (CSV file)
- Generate custom interview questions and preparation tips using LLMs

It uses a large language model via Groq, with the ability to scrape static and JavaScript-rendered job listings using Selenium + Edge WebDriver.

---

## Setup Instructions

### 1. INSTALL DEPENDENCIES

Run the following command in terminal:
```
./install_dependencies.sh
```

This will:
- Create a Python virtual environment (`venv`)
- Install all required packages using pip

If you are on Windows, use:
```
bash install_dependencies.sh
```
or manually install packages using pip:
```
pip install -r requirements.txt
```

---

### 2. BROWSER DRIVER (Edge)

Make sure Microsoft Edge is installed.

The script will automatically download Edge WebDriver using `webdriver-manager`.
No manual setup required.

---

### 3. API KEY (Groq / OpenAI)

Set your Groq API Key in the script:
- Open `prepme.py`
- Locate the line: `groq_api_key=...`
- Replace it with your actual key

---

### 4. RUNNING THE APP

To launch the GUI:
```
python prepme.py
```

To test job extraction only:
- You can modify the `extract_job_data` function to run standalone.

---

### 5. TIPS

- Microsoft Edge must be installed.
- If the job site uses JavaScript (e.g., Google Careers), the Edge WebDriver is essential.
- Only static HTML pages can be scraped without a browser.

---

### 6. CLEANUP

To remove the virtual environment:
```
deactivate
rm -rf venv
```
