from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="KitchenLedger Core Integration Platform")

# Configure broad execution permissions for client connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reference relative templates folder maps
base_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

@app.get("/", response_class=HTMLResponse)
async def serve_root_dashboard(request: Request):
    return """
    <html>
        <head><title>Kitchen Ledger Engine</title></head>
        <body style='font-family:sans-serif; background:#0b1326; color:#dae2fd; padding:3rem; text-align:center;'>
            <h1>Kitchen Ledger Engine Active</h1>
            <p>Select Operational Extension Module Interface:</p>
            <a href='/load-test' style='color:#4edea3; margin:10px; display:inline-block;'>Open Live Load Test Simulator</a><br>
            <a href='/manifest' style='color:#ffb95f; margin:10px; display:inline-block;'>Open Daily Export Manifest Console</a>
        </body>
    </html>
    """

@app.get("/load-test", response_class=HTMLResponse)
async def serve_load_test(request: Request):
    return templates.TemplateResponse("load-test.html", {"request": request})

@app.get("/manifest", response_class=HTMLResponse)
async def serve_manifest(request: Request):
    return templates.TemplateResponse("manifest.html", {"request": request})

@app.get("/api/metrics")
async def fetch_telemetry():
    return {
        "throughput_tx_min": 850,
        "latency_ms": 42,
        "cpu_usage_pct": 78.4,
        "active_websockets": 4800
    }
