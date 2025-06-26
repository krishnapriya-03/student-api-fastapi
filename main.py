from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# --- In-memory storage ---
students = []
classes = []
class_registrations = {}  # class_id: list of student_ids

# --- Models ---
class Student(BaseModel):
    id: int
    first_name: str
    middle_name: str
    last_name: str
    age: int
    city: str

class Class(BaseModel):
    id: int
    class_name: str
    description: str
    start_date: str  # Format: YYYY-MM-DD
    end_date: str
    number_of_hours: int

# --- Home route ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Student-Class Management API"}

# --- Student Routes ---
@app.post("/students/")
def create_student(student: Student):
    students.append(student)
    return {"message": "Student added successfully", "student": student}

@app.get("/students/", response_model=List[Student])
def get_students():
    return students

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for index, student in enumerate(students):
        if student.id == student_id:
            students[index] = updated_student
            return {"message": "Student updated successfully", "student": updated_student}
    return {"error": "Student not found"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, student in enumerate(students):
        if student.id == student_id:
            deleted = students.pop(index)
            return {"message": "Student deleted successfully", "student": deleted}
    return {"error": "Student not found"}

# --- Class Routes ---
@app.post("/classes/")
def create_class(class_: Class):
    classes.append(class_)
    return {"message": "Class created successfully", "class": class_}

@app.get("/classes/", response_model=List[Class])
def get_classes():
    return classes

@app.put("/classes/{class_id}")
def update_class(class_id: int, updated_class: Class):
    for index, class_ in enumerate(classes):
        if class_.id == class_id:
            classes[index] = updated_class
            return {"message": "Class updated successfully", "class": updated_class}
    return {"error": "Class not found"}

@app.delete("/classes/{class_id}")
def delete_class(class_id: int):
    for index, class_ in enumerate(classes):
        if class_.id == class_id:
            deleted = classes.pop(index)
            return {"message": "Class deleted successfully", "class": deleted}
    return {"error": "Class not found"}

# --- Register student to class ---
@app.post("/register/")
def register_student_to_class(student_id: int, class_id: int):
    if not any(s.id == student_id for s in students):
        return {"error": "Student not found"}
    if not any(c.id == class_id for c in classes):
        return {"error": "Class not found"}

    if class_id not in class_registrations:
        class_registrations[class_id] = []

    if student_id in class_registrations[class_id]:
        return {"message": "Student already registered for this class"}

    class_registrations[class_id].append(student_id)
    return {"message": f"Student {student_id} registered to class {class_id}"}

# --- Get students in a class ---
@app.get("/classes/{class_id}/students", response_model=List[Student])
def get_students_in_class(class_id: int):
    if class_id not in class_registrations:
        return []

    student_ids = class_registrations[class_id]
    registered_students = [s for s in students if s.id in student_ids]
    return registered_students
