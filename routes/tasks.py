from fastapi import APIRouter, HTTPException, status
from models.tasks import Tasks
from typing import List
from beanie import PydanticObjectId, UpdateResponse

tasks_router = APIRouter()


@tasks_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_tasks() -> List[Tasks]:
    tasks = await Tasks.find_all().to_list()
    return tasks


@tasks_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_task(id: PydanticObjectId) -> Tasks:
    task = await Tasks.find_one(Tasks.id == id)
    if not task:
        raise HTTPException(404, "Task not found.")
    return task


@tasks_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tasks(task: Tasks):
    await task.create()

    return {"message": "successfully inserted"}


@tasks_router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_tasks(id: PydanticObjectId, task: Tasks):
    task = await Tasks.find_one(Tasks.id == id).update(
        {
            "$set": {
                Tasks.title: task.title,
                Tasks.content: task.content,
                Tasks.date_created: task.date_created,
                Tasks.is_done: task.is_done,
            }
        },
        response_type=UpdateResponse.UPDATE_RESULT,
    )

    if not task.raw_result["n"]:
        raise HTTPException(404, "Task not found.")

    return {"message": "Updated. ", "task": task.raw_result}


@tasks_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: PydanticObjectId):
    task = await Tasks.find_one(Tasks.id == id).delete()

    if not task.deleted_count:
        raise HTTPException(404, "Task not found.")

    return {"message": f"{id} Deleted successfully"}
