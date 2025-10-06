from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import csv

from vaultsync import update_buffer
from digest import generate_digest
from storage import log_transaction
from daily_summary import get_daily_summary

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    digest = generate_digest("data.csv")
    return templates.TemplateResponse("dashboard.html", {"request": request, "digest": digest})

@app.post("/log")
async def log(request: Request, tx_type: str = Form(...), source: str = Form(...), amount: float = Form(...), status: str = Form(...), notes: str = Form(...)):
    entry = {
        "Type": tx_type,
        "Source/Vendor": source,
        "Amount": amount,
        "Status": status,
        "Notes": notes
    }
    log_transaction("data.csv", entry)
    return await dashboard(request)

@app.post("/update")
async def update(request: Request):
    update_buffer("data.csv")
    return await dashboard(request)

@app.get("/daily-summary", response_class=HTMLResponse)
async def daily_summary(request: Request):
    summary = get_daily_summary("data.csv")
    return templates.TemplateResponse("daily_summary.html", {
        "request": request,
        "summary": summary
    })
