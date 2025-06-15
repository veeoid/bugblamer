import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from blame import analyze_failure

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("upload.html", {
        "request": request,
        "suggestion": None,  # explicitly clear old suggestion
        "log": "",
        "diff": ""
    })



@app.post("/analyze")
async def analyze(request: Request, log: UploadFile = File(...), diff: UploadFile = File(...)):
    log_text = (await log.read()).decode("utf-8")
    diff_text = (await diff.read()).decode("utf-8")
    suggestion = analyze_failure(log_text, diff_text)
    return templates.TemplateResponse("upload.html", {
        "request": request,
        "suggestion": suggestion,
        "log": log_text,
        "diff": diff_text
    })


@app.post("/analyze/gitlab")
async def analyze_gitlab(
    request: Request,
    project_id: str = Form(...),
    job_id: str = Form(...),
    token: str = Form(...)
):
    headers = {"PRIVATE-TOKEN": token}
    base_url = f"https://gitlab.com/api/v4/projects/{project_id}"

    try:
        # Get CI logs
        log_res = httpx.get(f"{base_url}/jobs/{job_id}/trace", headers=headers)
        if log_res.status_code != 200:
            raise Exception("Could not fetch CI logs.")
        log_text = log_res.text

        # Get job info for commit SHA
        job_info = httpx.get(f"{base_url}/jobs/{job_id}", headers=headers).json()
        commit_sha = job_info["commit"]["id"]

        # Get git diff for that commit
        diff_res = httpx.get(f"{base_url}/repository/commits/{commit_sha}/diff", headers=headers)
        diff_text = "\n".join([f"{d['new_path']}:\n{d['diff']}" for d in diff_res.json()])

        suggestion = analyze_failure(log_text, diff_text)

        return templates.TemplateResponse("upload.html", {
            "request": request,
            "suggestion": suggestion,
            "log": log_text,
            "diff": diff_text
        })

    except Exception as e:
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "suggestion": f"❌ Error: {str(e)}"
        })


@app.get("/debug-static")
def debug_static():
    import os
    if os.path.exists("static"):
        return {"exists": True, "files": os.listdir("static")}
    else:
        return {"exists": False, "message": "static directory not found"}

