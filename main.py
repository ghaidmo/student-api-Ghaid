from os import major
from typing import Optional
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
app = FastAPI()


class NewStudents(BaseModel):
    name: Optional[str] = None
    major: Optional[str]
    gender: Optional[str]


IDs = ['1', '2', '3']
StudentInfo = [{'name': 'ghaid', 'major': 'CS', "gender": "female"},
               {'name': 'khalid', 'major': 'CiS', "gender": "male"},
               {'name': 'lina', 'major': 'CS', "gender": "female"}]
Students = dict(zip(IDs, StudentInfo))
Based_On_Gender = {}


@app.get("/students")
def index(id: Optional[str] = None, gender: Optional[str] = None):
    if id == None and gender == None:
        return Students
    elif gender != None and id == None:
        for i in Students:
            if Students[i]['gender'] == gender:
                Based_On_Gender[i] = Students[i]
                return Based_On_Gender
    else:
        return Students[id]


@app.get("/students/{id}")
def index(id):
    if id in Students:
        return Students[id]
    else:
        return "ID Does Not Exist"


@app.post("/students/")
async def Add_New(student: NewStudents):
    NextID = str(len(Students)+1)
    Students[NextID] = {"name": student.name,
                        "major": student.major,
                        "gender": student.gender}
    return student


@app.delete("/students/{id}")
def delete_student(id: int):
    if id in Students:
        Students.pop(id)
    else:
        return "No Matching Student ID"


@app.put("/students/{id}")
async def Put_Student(id, student: NewStudents):
    if id in Students:
        Students.pop(id)

    Students[id] = {"name": student.name,
                    "major": student.major,
                    "gender": student.gender}
    return student


@app.patch("/student/{id}", response_model=NewStudents)
async def update_student(id: str, student: NewStudents):
    stored_item_data = Students[id]
    stored_item_model = NewStudents(**stored_item_data)
    update_data = student.dict(exclude_unset=True)
    updated_student = stored_item_model.copy(update=update_data)
    Students[id] = jsonable_encoder(updated_student)
    return updated_student
