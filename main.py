from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from logic import sanitize_input, calculate_actual

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend domain
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class SkillItem(BaseModel):
    skill: str
    claimed: int
    answer: str

class AnalyzeRequest(BaseModel):
    skills: List[SkillItem]

@app.get("/")
def home():
    return {"status": "Backend running securely", "message": "Skill Gap Analyzer API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Skill Gap Analyzer"}

@app.post("/analyze")
def analyze(data: AnalyzeRequest):
    """
    Analyze skill gap for each submitted skill
    Returns claimed level, actual level, and gap
    """
    results = []
    
    for item in data.skills:
        # Sanitize user input for security
        clean_answer = sanitize_input(item.answer)
        
        # Calculate actual skill level based on response
        actual = calculate_actual(clean_answer)
        
        # Calculate gap
        gap = item.claimed - actual
        
        results.append({
            "skill": item.skill,
            "claimed": item.claimed,
            "actual": actual,
            "gap": gap,
            "feedback": get_feedback(gap)
        })
    
    return {
        "analysis": results,
        "total_skills_analyzed": len(results)
    }

def get_feedback(gap: int) -> str:
    """Generate helpful feedback based on gap size"""
    if gap <= 0:
        return "Excellent! Your skills match your claims."
    elif gap == 1:
        return "Good! A small gap - minor improvement needed."
    elif gap == 2:
        return "Moderate gap - focused practice recommended."
    else:
        return "Significant gap - substantial learning required."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)