# 🐞 BugBlamer

## **BugBlamer** is a simple AI powered tool that helps you figure out which commit most likely caused your CI pipeline to fail. You can upload your CI logs and Git diffs or connect it to your GitLab project. It analyzes the failure using a language model and suggests the most likely cause so you can debug faster without the guesswork.

---

## 🚀 Features

- **Intuitive Web Interface:** Upload your CI log and git diff files with ease.
- **AI-Powered Analysis:** Uses Groq API to analyze failures and suggest the most probable culprit commit, with reasoning.
- **GitLab Integration:** Fetch logs and diffs directly from your GitLab CI jobs (just provide project and job IDs).
- **Instant Feedback:** Get results in seconds, right in your browser.
- **Secure:** API keys and secrets are managed via environment variables.

---

## 🗂️ Project Structure

```
bugblamer/
│
├── main.py               # FastAPI app entry point & API routes
├── blame.py              # Core logic for AI-based analysis
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not committed)
├── templates/
│   └── upload.html       # Jinja2 template for the web UI
├── static/               # (Optional) Static files (CSS, JS, etc.)
├── test_data/            # Example log and diff files
└── .gitignore
```

---

## ⚡ Quick Start

1. **Clone the repository**

   ```
   git clone https://github.com/yourusername/bugblamer.git
   cd bugblamer
   ```

2. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

3. **Configure your environment**

   Create a `.env` file in the project root:

   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the app locally**

   ```
   uvicorn main:app --reload
   ```

   Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🛠️ Usage

- **Manual Upload:**  
  On the homepage, upload your CI log and git diff files, then click **Analyze**.  
  The AI will review your files and suggest which commit is most likely responsible for the failure, along with an explanation.

- **GitLab Integration:**  
  Use the GitLab form to fetch logs and diffs directly from your project by entering your Project ID, Job ID, and a GitLab access token.

---

## 🐳 Docker Support

Build and run BugBlamer in a container:

```
docker build -t bugblamer .
docker run -p 8080:8080 --env-file .env bugblamer
```

---

## 📦 Requirements

- Python 3.11+
- See `requirements.txt` for all dependencies

---

## 🙋 FAQ

**Q: Is my code or log data sent to third parties?**  
A: Only the log and diff content you upload is sent to the Groq API for analysis. No data is stored on the server.

**Q: Can I use this with other CI systems?**  
A: Yes! As long as you can provide the CI log and git diff, BugBlamer can analyze it.

---

## 📄 License

MIT License

---

\*\*Happy debugging!
