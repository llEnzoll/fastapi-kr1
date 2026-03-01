from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, validator
from typing import List
from models import User as UserModel

app = FastAPI()

# ==============================
# 1.1 Базовый JSON эндпоинт
# ==============================

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в моё приложение FastAPI!"}


# ==============================
# 1.2 Возврат HTML файла
# (если нужно вернуть HTML вместо JSON —
# просто закомментируй read_root и раскомментируй код ниже)
# ==============================

# @app.get("/")
# def read_html():
#     return FileResponse("index.html")


# ==============================
# 1.3 POST /calculate
# ==============================

class Numbers(BaseModel):
    num1: float
    num2: float

@app.post("/calculate")
def calculate(numbers: Numbers):
    return {"result": numbers.num1 + numbers.num2}


# ==============================
# 1.4 GET /users
# ==============================

user = UserModel(name="Eric", id=1)

@app.get("/users")
def get_user():
    return user


# ==============================
# 1.5 POST /user (взрослый или нет)
# ==============================

class UserAge(BaseModel):
    name: str
    age: int

@app.post("/user")
def check_user(user: UserAge):
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": user.age >= 18
    }


# ==============================
# 2.1 POST /feedback
# ==============================

feedback_storage: List = []

class Feedback(BaseModel):
    name: str
    message: str

@app.post("/feedback")
def add_feedback(feedback: Feedback):
    feedback_storage.append(feedback)
    return {
        "message": f"Feedback received. Thank you, {feedback.name}."
    }


# ==============================
# 2.2 Валидация + фильтр слов
# ==============================

class FeedbackValidated(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)

    @validator("message")
    def check_bad_words(cls, value):
        forbidden_words = ["кринж", "рофл", "вайб"]
        for word in forbidden_words:
            if word.lower() in value.lower():
                raise ValueError("Message contains inappropriate words.")
        return value

@app.post("/feedback-validated")
def add_validated_feedback(feedback: FeedbackValidated):
    feedback_storage.append(feedback)
    return {
        "message": f"Validated feedback received. Thank you, {feedback.name}."
    }