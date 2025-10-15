from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS", default="mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.skill_summarizer

task_collection = database.get_collection("tasks")
skill_collection = database.get_collection("skills")

def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "date": task["date"],
        "extracted_skills": task.get("extracted_skills", []),
        "confirmed_skills": task.get("confirmed_skills", []),
    }

def skill_helper(skill) -> dict:
    return {
        "id": str(skill["_id"]),
        "name": skill["name"],
        "category": skill.get("category"),
        "level": skill.get("level"),
    }