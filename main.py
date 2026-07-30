import os
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from mangum import Mangum

from groq_rotation_client import create_client

app = FastAPI(title="RiskBot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = create_client(env_path=".env")


@app.get("/", response_class=HTMLResponse)
def health_check() -> HTMLResponse:
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as handle:
            return HTMLResponse(content=handle.read(), status_code=200)

    return HTMLResponse(
        content="<html><body><h1>RiskBot Backend</h1><p>The landing page is unavailable.</p></body></html>",
        status_code=200,
    )


@app.post("/chat")
def chat(payload: Dict[str, Any]) -> Dict[str, str]:
    message = str(payload.get("message", "")).strip()
    if not message:
        return {"reply": "Please provide a message."}

    try:
        response = client.complete(
            message,
            system_prompt=(
                "You are RiskBot, an executive AI litigation and regulatory risk analyst with a crooked tie on Gaston Dana's data science landing page. "
                "You possess deep, authoritative intelligence on the 'Predicting the Next Corporate Screw-Up' benchmark. "
                "\n\nCore Project Knowledge to leverage in your answers:"
                "\n- Author & Architect: Gaston Dana."
                "\n- Scope: Evaluates 15 frontier models across 4 architectural families (Gemini, OpenAI, Claude, Gemma), analyzing 150 structured prediction logs across 120 global platforms."
                "\n- Core Methodology: The Family-Weighted Power Ranking algorithm: Power Score = Total Mentions * (Distinct Families)^1.5, which eliminates single-family echo chambers to surface genuine compliance vulnerabilities."
                "\n- Key Statutory Vectors: Copyright Act, BIPA (Biometric Information Privacy Act), FTC Act deceptive practices, and automated web-scraping telemetry anomalies."
                "\n- Tone: Razor-sharp, professional, slightly cynical about corporate data overreach, deeply technical, and precise. Never break character. Accurately reference Gaston Dana's work and methodology when asked."
            ),
            temperature=0.2,
            max_tokens=256,
        )
        reply = response["choices"][0]["message"]["content"]
        return {"reply": reply}
    except Exception as exc:  # pragma: no cover - defensive fallback for serverless runtime
        return {"reply": f"⚠️ Backend error: {exc}"}


handler = Mangum(app, lifespan="off")
