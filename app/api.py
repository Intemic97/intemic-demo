import fastapi
from fastapi import HTTPException
from http import HTTPStatus

from db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from model.data import TaskResponse, TaskBody



router = fastapi.APIRouter()

@router.get("/task", status_code=HTTPStatus.OK)
def get_task(db: Session = fastapi.Depends(get_db)):
    query = text("""
      SELECT * FROM "Kumar_anvil_test"
    """)
    result = db.execute(query)
    tasks = [
        TaskResponse(id=row[0], task=row[2], name=row[3])
        for row in result.fetchall()
    ]

    return tasks

@router.post("/task",status_code=HTTPStatus.CREATED)
def post_task(task :TaskBody,
              db: Session = fastapi.Depends(get_db),
              ):
    try:
        query = text("""
            INSERT INTO "Kumar_anvil_test" (task, name)
            VALUES (:task, :name)
            RETURNING id, task, name
        """)
        
        result = db.execute(query, {"task": task.name, "name": task.task})
        db.commit()

        new_task = result.fetchone()

        if not new_task:
            raise HTTPException(status_code=500, detail="Failed to create task")

        return TaskResponse(id=new_task[0], name=new_task[1], task=new_task[2])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/task/{task_id}",  status_code=HTTPStatus.OK)
def update_task(task_id: int, task_update: TaskBody, db: Session = fastapi.Depends(get_db)):
    try:
        query = text("""
            UPDATE "Kumar_anvil_test"
            SET task = :task, name = :name
            WHERE id = :task_id
            RETURNING id, task, name
        """)
        
        result = db.execute(query, {"task": task_update.name, "name": task_update.task, "task_id": task_id})
        db.commit()
        updated_task = result.fetchone()

        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")

        return TaskResponse(id=updated_task[0], name=updated_task[1], task=updated_task[2])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/task/{task_id}", status_code=HTTPStatus.OK)
def delete_task(task_id: int, db: Session = fastapi.Depends(get_db)):
    try:
        query = text("""
        SELECT * FROM "Kumar_anvil_test" where id =:task_id
        """)
        result = db.execute(query, {"task_id": task_id})
        task = result.fetchone()
        if task:
            query = text("""
                DELETE FROM "Kumar_anvil_test"
                WHERE id = :task_id
            """)
            
            db.execute(query, {"task_id": task_id})
            db.commit()

            return {"message":f"Deleted task with id {task_id}"}
        else:
            return {"message":"Task with this id not exist"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Task with this id not exist")