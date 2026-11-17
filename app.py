import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv, set_key

ENV_FILE = ".env"
if not os.path.exists(ENV_FILE): open(ENV_FILE, 'w').close()
load_dotenv(ENV_FILE)

app = FastAPI()

class SettingsModel(BaseModel):
    gemini_key: str
    openrouter_key: str
    tg_bot_token: str
    tg_chat_id: str
    ai_model: str  # يېڭىدىن قوشۇلغان مودېل تاللاش ئۆزگەرگۈچىسى

@app.post("/api/settings")
def save_settings(settings: SettingsModel):
    set_key(ENV_FILE, "GEMINI_API_KEY", settings.gemini_key)
    set_key(ENV_FILE, "OPENROUTER_API_KEY", settings.openrouter_key)
    set_key(ENV_FILE, "TG_BOT_TOKEN", settings.tg_bot_token)
    set_key(ENV_FILE, "TG_CHAT_ID", settings.tg_chat_id)
    set_key(ENV_FILE, "AI_MODEL", settings.ai_model)
    return {"status": "success", "message": "تەڭشەكلەر مۇۋەپپەقىيەتلىك ساقلاندى!"}

@app.get("/api/settings")
def get_settings():
    return {
        "gemini_key": os.getenv("GEMINI_API_KEY", ""),
        "openrouter_key": os.getenv("OPENROUTER_API_KEY", ""),
        "tg_bot_token": os.getenv("TG_BOT_TOKEN", ""),
        "tg_chat_id": os.getenv("TG_CHAT_ID", ""),
        "ai_model": os.getenv("AI_MODEL", "gemini-1.5-pro")
    }

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)