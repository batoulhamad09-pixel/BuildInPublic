import openai
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------
# CLI: original script
# -------------------
def main(): 
    print("💪 Welcome to your AI Personal Trainer!")
    goal = input("What's your fitness goal? ")
    experience = input("What's your experience level (beginner/intermediate/advanced)? ")
    days = input("How many days per week can you train? ")
    equipment = input("What equipment do you have? ")

    prompt = f"""
    You are a personal trainer. Create a 1-week gym plan for someone with:
    Goal: {goal}
    Experience: {experience}
    Days per week: {days}
    Equipment: {equipment}
    Return it as a structured text plan (Day 1, Day 2...).
    """

    # UPDATED TO NEW API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    print("\n🏋️ Your Gym Plan:\n")
    print(response.choices[0].message.content)

# -------------------
# Web API: FastAPI
# -------------------
app = FastAPI(title="AI Personal Trainer API")

# Home route so you don't get 404
@app.get("/")
def home():
    return {"message": "API is running — go to /docs"}

class UserData(BaseModel):
    goal: str
    experience: str
    days_per_week: int
    equipment: List[str] = []

@app.post("/generate_plan")
def generate_plan(user: UserData):
    prompt = f"""
    You are a personal trainer. Create a 1-week gym plan for someone with:
    Goal: {user.goal}
    Experience: {user.experience}
    Days per week: {user.days_per_week}
    Equipment: {', '.join(user.equipment)}
    Return it as a structured text plan (Day 1, Day 2...).
    """

    # CORRECT NEW API CALL
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return {"plan": response.choices[0].message.content}

# -------------------
# Run CLI if script is executed directly
# -------------------
if __name__ == "__main__":
    main()

