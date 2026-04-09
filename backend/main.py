from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid

from safety_filter import SafetyFilter
from emotion_detector import EmotionDetector
from llm_service import MockLLMService

app = FastAPI(title="MINDFUL AI API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
safety_filter = SafetyFilter()
emotion_detector = EmotionDetector()
llm_service = MockLLMService()

# In-memory session store for POC
# Maps session_id to {"state": "LISTENING"}
sessions = {}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    mode: Optional[str] = "THERAPIST" # New: THERAPIST or REFLECTOR

class ChatResponse(BaseModel):
    text: str
    session_id: str
    is_crisis: bool = False
    detected_emotion: str = "Neutral"
    gravity_score: float = 0.0 # New
    orbits: list = [] # New
    distortions: list = [] # New
    mode: str = "THERAPIST" # New

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    # 1. Session Management
    session_id = req.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = {
            "state": "LISTENING",
            "gravity": 0.3, # Initial stable gravity
            "mode": req.mode or "THERAPIST",
            "orbits": {} # Map of topic -> weight
        }
        
    session = sessions[session_id]
    current_state = session["state"]
    # Update mode if requested
    if req.mode:
        session["mode"] = req.mode

    user_message = req.message

    # 2. Immediate Safety Check
    risk_level = safety_filter.analyze(user_message)
    if risk_level == "CRISIS":
        # Bypass LLM and return strict crisis protocol
        crisis_text = llm_service.get_crisis_response()
        # Reset state on crisis
        session["state"] = "LISTENING"
        session["gravity"] = 0.9 # High gravity on crisis
        return ChatResponse(
            text=crisis_text, 
            session_id=session_id, 
            is_crisis=True,
            detected_emotion="Despair",
            gravity_score=0.9,
            mode=session["mode"]
        )
        
    # 3. Emotion Detection
    emotion = emotion_detector.analyze(user_message)
    
    # Update gravity based on emotion
    gravity_impact = emotion_detector.get_gravity_impact(emotion)
    session["gravity"] = max(0.1, min(1.0, session["gravity"] + gravity_impact))
    
    # 4. Generate Response & Update State
    # Passing gravity and mode to LLM service
    response_data = llm_service.generate_response(
        user_message, 
        current_state, 
        emotion, 
        mode=session["mode"],
        current_gravity=session["gravity"]
    )
    
    # Update session context
    session["state"] = response_data["state"]
    
    # Update orbits (topics)
    if "topics" in response_data:
        for topic, weight in response_data["topics"].items():
            session["orbits"][topic] = max(0.2, min(1.0, session["orbits"].get(topic, 0) + weight))

    return ChatResponse(
        text=response_data["text"],
        session_id=session_id,
        is_crisis=False,
        detected_emotion=response_data["detected_emotion"],
        gravity_score=session["gravity"],
        orbits=[{"topic": k, "weight": v} for k, v in session["orbits"].items()],
        distortions=response_data.get("distortions", []),
        mode=session["mode"]
    )

# Mount static files at the end to not override APIs
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
