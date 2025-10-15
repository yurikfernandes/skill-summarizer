from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from .database import (
    task_collection, skill_collection, task_helper, skill_helper
)
from .models import Task, Skill, PyObjectId


app = FastAPI()


@app.post("/tasks", response_description="Add new task", response_model=Task)
async def create_task(task: Task = Body(...)):
    task = jsonable_encoder(task)
    new_task = await task_collection.insert_one(task)
    created_task = await task_collection.find_one({"_id": new_task.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=task_helper(created_task))


@app.get("/tasks", response_description="List all tasks", response_model=List[Task])
async def list_tasks():
    tasks = []
    for task in await task_collection.find().to_list(1000):
        tasks.append(task_helper(task))

    return tasks


@app.get("/tasks/{id}", response_description="Get a single task", response_model=Task)
async def get_task(id: str):
    if (task := await task_collection.find_one({"_id": PyObjectId(id)})) is not None:
        return task_helper(task)
    
    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@app.put("/tasks/{id}", response_description="Update a task", response_model=Task)
async def update_task(id: str, task: dict = Body(...)):
    task = {k: v for k, v in task.items() if v is not None}
    if len(task) >= 1:
        update_result = await task_collection.update_one(
            {"_id": PyObjectId(id)}, {"$set": task}
        )
        if update_result.modified_count == 1:
            if (
                updated_task := await task_collection.find_one({"_id": PyObjectId(id)})
            ) is not None:
                return task_helper(updated_task)

    if (existing_task := await task_collection.find_one({"_id": PyObjectId(id)})) is not None:
        return task_helper(existing_task)

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@app.delete("/tasks/{id}", response_description="Delete a task")
async def delete_task(id: str):
    delete_result = await task_collection.delete_one({"_id": PyObjectId(id)})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@app.post("/skills", response_description="Add new skill", response_model=Skill)
async def create_skill(skill: Skill = Body(...)):
    skill = jsonable_encoder(skill)
    new_skill = await skill_collection.insert_one(skill)
    created_skill = await skill_collection.find_one({"_id": new_skill.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=skill_helper(created_skill))


@app.get("/skills", response_description="List all skills", response_model=List[Skill])
async def list_skills():
    skills = []
    for skill in await skill_collection.find().to_list(1000):
        skills.append(skill_helper(skill))

    return skills


@app.get("/skills/{id}", response_description="Get a single skill", response_model=Skill)
async def get_skill(id: str):
    if (skill := await skill_collection.find_one({"_id": PyObjectId(id)})) is not None:
        return skill_helper(skill)
    
    raise HTTPException(status_code=404, detail=f"Skill {id} not found")


@app.put("/skills/{id}", response_description="Update a skill", response_model=Skill)
async def update_skill(id: str, skill: dict = Body(...)):
    skill = {k: v for k, v in skill.items() if v is not None}
    if len(skill) >= 1:
        update_result = await skill_collection.update_one(
            {"_id": PyObjectId(id)}, {"$set": skill}
        )
        if update_result.modified_count == 1:
            if (
                updated_skill := await skill_collection.find_one({"_id": PyObjectId(id)})
            ) is not None:
                return skill_helper(updated_skill)

    if (existing_skill := await skill_collection.find_one({"_id": PyObjectId(id)})) is not None:
        return skill_helper(existing_skill)

    raise HTTPException(status_code=404, detail=f"Skill {id} not found")


@app.delete("/skills/{id}", response_description="Delete a skill")
async def delete_skill(id: str):
    delete_result = await skill_collection.delete_one({"_id": PyObjectId(id)})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    raise HTTPException(status_code=404, detail=f"Skill {id} not found")