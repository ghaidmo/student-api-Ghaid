from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder

from modules import Gender, NewStudents, NewStudents_Patch
from session import JSONResponse

app = FastAPI()
###

Students = {"1": {'name': 'ghaid', 'major': 'CS', "gender": "female"},
            "2": {'name': 'khalid', 'major': 'CiS', "gender": "male"},
            "3": {'name': 'lina', 'major': 'CS', "gender": "female"},
            "4": {'name': 'ahmad', 'major': 'CS', "gender": "male"}}


def data_input(id: str, student: NewStudents) -> dict:
    Students[id] = {"name": student.name,
                    "major": student.major,
                    "gender": student.gender}
    return student

##


@app.get("/students")
def get(major: Optional[str] = None, gender: Optional[str] = None) -> JSONResponse:
    if major and gender:
        filtered_students = list(filter(
            lambda x: x['major'] == major and x['gender'] == gender, Students.values()))
    elif major and not gender:
        filtered_students = list(filter(
            lambda x: x['major'] == major, Students.values()))
    elif gender and not major:
        filtered_students = list(filter(
            lambda x: x['gender'] == gender, Students.values()))
    else:
        return Students
    return filtered_students


@app.get("/students/{id}")
def get_student_by_id(id: str) -> JSONResponse:
    if id not in Students.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Student with id: {id} dose not exist'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': Students.get(id)})


@app.post("/students/")
def add_new_student(student: NewStudents) -> JSONResponse:
    try:
        data_input(str(uuid4()), student)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Bad data')
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'data': student})


@app.delete("/students/{id}")
def delete_student(id: str):
    if id in Students.keys():
        Students.pop(id)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Student with id: {id} dose not exist'
    )


@app.put("/students/{id}")
def put_student(id: str, student: NewStudents) -> JSONResponse:
    if id in Students.keys():
        Students.pop(id)
    data_input(id, student)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': Students.get(id)})


@app.patch("/student/{id}")
def update_student(id: str, student: NewStudents_Patch):
    updated_student = NewStudents_Patch(
        **Students.get(id)).copy(update=student.dict(exclude_unset=True))
    data_input(id, NewStudents(**jsonable_encoder(updated_student)))
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data updated': updated_student})
