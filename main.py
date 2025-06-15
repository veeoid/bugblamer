# main.py
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from blame import analyze_failure
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

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


